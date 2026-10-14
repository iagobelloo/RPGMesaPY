"""MÃ³dulo de OrquestraÃ§Ã£o Principal (Controller/Facade) do Jogo."""

import json
import os
import copy
from typing import Dict, Any, List

from core.dice_engine import DiceEngine
from core.combat_system import TurnManager, ConditionManager, DeathSaveTracker
from core.time_manager import RestSystem
from ai_master.ai_client import AIGameMaster

class CharacterBuilder:
    """Gerencia a criaÃ§Ã£o passo a passo de um personagem de D&D 5e (Regras Oficiais)."""
    
    @staticmethod
    def roll_stats_4d6_drop_lowest() -> int:
        rolls = [DiceEngine.roll_d6() for _ in range(4)]
        rolls.remove(min(rolls))
        return sum(rolls)

class SessionManager:
    """O Maestro (Facade) que orquestra todas as mecÃ¢nicas."""
    def __init__(self, ai_master: AIGameMaster = None):
        self.ai = ai_master
        self.turn_manager = TurnManager()
        self.condition_manager = ConditionManager()
        self.death_tracker = DeathSaveTracker()
        self.ui_event_queue: List[Dict[str, Any]] = []
        
        # Fila AssÃ­ncrona para comunicaÃ§Ã£o Thread-Safe
        import queue
        self.ui_queue = queue.Queue()
        
        from core.story_engine import StoryManager
        self.story = StoryManager()
        
        # Caches na RAM para cortar I/O bloqueante
        self.spells_db = {}
        try:
            with open("data/spells.json", "r", encoding="utf-8") as f:
                self.spells_db = json.load(f)
        except Exception as e:
            print(f"[Sistema] Erro ao carregar spells.json: {e}")

        self.items_db = {}
        try:
            with open("data/items.json", "r", encoding="utf-8") as f:
                self.items_db = json.load(f)
        except Exception as e:
            print(f"[Sistema] Erro ao carregar items.json: {e}")

        self.class_skills_db = {}
        try:
            with open("data/class_skills.json", "r", encoding="utf-8") as f:
                self.class_skills_db = json.load(f)
        except Exception as e:
            print(f"[Sistema] Erro ao carregar class_skills.json: {e}")

        # Estados Persistentes Globais
        self.is_ai_thinking = False
        self.game_mode = "EXPLORACAO"
        self.current_background_key = "tavern"
        self.active_visual_npcs = {}
        self.active_combat_targets = {}
        
        self.game_state: Dict[str, Any] = {
            "player_character": None,
            "recent_history": [],
            "known_npcs": {},
            "quest_log": [],
            "story_beat": self.story.current_beat,
            "active_side_quest": None,
            "side_quest_origin": None,
            "last_checkpoint_type": "TAVERNA",
            "last_checkpoint_beat": 0,
            "current_day": 1,
            "suprimentos_acampamento": 1,
            "suprimentos_maximos": 1,
            "inventory": {"i_potion_healing": 1, "i_rations": 2},
            "discovered_monsters": [],
            "meta": {"loop_count": 0, "segredo_tirano": False}
        }
        self.current_save_slot: int = 1

    def save_game(self, slot: int = None, save_path: str = None) -> bool:
        """Salva o estado atual do jogo em disco."""
        import datetime
        if save_path:
            target_path = save_path
        elif slot is not None and isinstance(slot, str) and (".json" in slot or "/" in slot or "\\" in slot):
            target_path = slot
        else:
            target_slot = int(slot) if slot is not None else getattr(self, "current_save_slot", 1)
            self.current_save_slot = target_slot
            target_path = f"saves/slot{target_slot}.json"

        try:
            os.makedirs(os.path.dirname(target_path) or "saves", exist_ok=True)
            self.game_state["story_beat"] = self.story.current_beat
            self.game_state["story_flags"] = self.story.flags
            self.game_state["saved_at"] = datetime.datetime.now().isoformat()
            self.game_state["slot"] = getattr(self, "current_save_slot", 1)
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(self.game_state, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"[Sistema] Erro ao salvar o jogo em {target_path}: {e}")
            return False

    def load_game(self, slot: int = None, save_path: str = None) -> bool:
        """Carrega o estado do jogo do disco para o Core Engine."""
        if save_path:
            target_path = save_path
        elif slot is not None and isinstance(slot, str) and (".json" in slot or "/" in slot or "\\" in slot):
            target_path = slot
        else:
            target_slot = int(slot) if slot is not None else getattr(self, "current_save_slot", 1)
            self.current_save_slot = target_slot
            target_path = f"saves/slot{target_slot}.json"

        if not os.path.exists(target_path):
            print(f"[Sistema] Nenhum save encontrado em {target_path}.")
            return False
            
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if "player_character" not in data or not data["player_character"]:
                raise ValueError("O save não contém dados válidos de personagem (player_character nulo ou ausente).")
                
            # Atualiza o estado da sessão (Desserialização)
            self.game_state["player_character"] = data["player_character"]
            self.game_state["recent_history"] = data.get("recent_history", [])
            self.game_state["known_npcs"] = data.get("known_npcs", {})
            self.game_state["quest_log"] = data.get("quest_log", [])
            self.game_state["active_side_quest"] = data.get("active_side_quest", None)
            self.game_state["side_quest_origin"] = data.get("side_quest_origin", None)
            self.game_state["last_checkpoint_type"] = data.get("last_checkpoint_type", "TAVERNA")
            self.game_state["last_checkpoint_beat"] = data.get("last_checkpoint_beat", 0)
            self.game_state["current_day"] = data.get("current_day", 1)
            self.game_state["suprimentos_acampamento"] = data.get("suprimentos_acampamento", 1)
            self.game_state["suprimentos_maximos"] = data.get("suprimentos_maximos", 1)
            self.game_state["inventory"] = data.get("inventory", {})
            self.game_state["discovered_monsters"] = data.get("discovered_monsters", [])
            self.game_state["meta"] = data.get("meta", {"loop_count": 0, "segredo_tirano": False})
            self.game_state["saved_at"] = data.get("saved_at", "")
            self.game_state["slot"] = data.get("slot", getattr(self, "current_save_slot", 1))
            
            self.story.current_beat = data.get("story_beat", 0)
            self.game_state["story_beat"] = self.story.current_beat
            self.story.flags = data.get("story_flags", self.story.flags)
            self.sync_inventory()
            
            print(f"[Sistema] Jogo carregado com sucesso de {target_path}. Atributos do personagem restaurados.")
            return True
        except Exception as e:
            raise RuntimeError(f"Falha crítica ao desserializar save de {target_path}: {e}")

    @staticmethod
    def get_slot_metadata(slot_num: int) -> dict:
        """Coleta resumo estruturado de um slot para a tela visual de saves."""
        save_path = f"saves/slot{slot_num}.json"
        if not os.path.exists(save_path):
            return {"slot": slot_num, "is_empty": True}
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            pc = data.get("player_character")
            if not pc or not isinstance(pc, dict):
                return {"slot": slot_num, "is_empty": True}
            
            beat_num = data.get("story_beat", 1)
            # Resolve nome do Beat e Ato
            act_title = "Ato I" if beat_num <= 5 else ("Ato II" if beat_num <= 10 else "Ato III")
            beat_name = "Taverna do Dragão Acordado"
            try:
                with open("data/campaign.json", "r", encoding="utf-8") as cf:
                    camp_data = json.load(cf)
                    if str(beat_num) in camp_data:
                        beat_name = camp_data[str(beat_num)].get("name", beat_name)
            except Exception:
                pass

            # Conta missões concluídas
            quests = data.get("quest_log", [])
            quests_done = sum(1 for q in quests if isinstance(q, dict) and q.get("status") == "concluida")

            return {
                "slot": slot_num,
                "is_empty": False,
                "name": pc.get("name", "Aventureiro"),
                "race": pc.get("race", "Humano"),
                "class": pc.get("class", "Guerreiro"),
                "gender": pc.get("gender") or pc.get("genero") or "male",
                "level": pc.get("level", 1),
                "hp_current": pc.get("hp_current", 10),
                "hp_max": pc.get("hp_max", 10),
                "gold": pc.get("gold", data.get("gold", 15)),
                "story_beat": beat_num,
                "act_title": act_title,
                "beat_name": beat_name,
                "location": f"{act_title} • {beat_name}",
                "current_day": data.get("current_day", 1),
                "quests_completed": quests_done,
                "saved_at": data.get("saved_at", "")
            }
        except Exception as e:
            print(f"[Sistema] Aviso ao ler metadata do slot {slot_num}: {e}")
            return {"slot": slot_num, "is_empty": True}

    @classmethod
    def get_all_slots_summary(cls) -> list:
        """Retorna os metadados dos 3 slots de salvamento."""
        return [cls.get_slot_metadata(i) for i in range(1, 4)]

    @staticmethod
    def delete_save_slot(slot_num: int) -> bool:
        """Exclui o arquivo de salvamento do slot especificado."""
        save_path = f"saves/slot{slot_num}.json"
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
                print(f"[Sistema] Slot {slot_num} excluído com sucesso.")
                return True
            except Exception as e:
                print(f"[Sistema] Erro ao excluir slot {slot_num}: {e}")
                return False
        return True

    def discover_monster(self, monster_id: str) -> bool:
        """
        Registra uma nova criatura descoberta no bestiário do diário/grimório do jogador.
        Evita duplicatas e mantém o registro persistente no game_state.
        """
        if not monster_id:
            return False
        m_id = str(monster_id).strip()
        if not m_id:
            return False
        discovered = self.game_state.setdefault("discovered_monsters", [])
        if m_id not in discovered:
            discovered.append(m_id)
            return True
        return False

    def get_discovered_monsters(self) -> List[str]:
        """Retorna a lista de criaturas e monstros já descobertos pelo jogador na campanha."""
        discovered = self.game_state.get("discovered_monsters", [])
        if not isinstance(discovered, list):
            self.game_state["discovered_monsters"] = []
            return []
        return list(discovered)

    def sync_inventory(self) -> None:
        """Sincroniza game_state['inventory'] e pc['inventory'] para evitar AttributeError."""
        pc = self.game_state.get("player_character")
        if not pc or not isinstance(pc, dict):
            return
            
        gs_inv = self.game_state.setdefault("inventory", {})
        if not isinstance(gs_inv, dict):
            self.game_state["inventory"] = {}
            gs_inv = self.game_state["inventory"]
            
        pc_inv = pc.get("inventory")
        if pc_inv is None:
            pc["inventory"] = gs_inv
        elif isinstance(pc_inv, dict):
            for k, v in pc_inv.items():
                if k not in gs_inv or gs_inv[k] < v:
                    gs_inv[k] = v
            for k, v in gs_inv.items():
                if k not in pc_inv or pc_inv[k] < v:
                    pc_inv[k] = v

    def get_inventory_item_count(self, item_id: str) -> int:
        """Retorna a quantidade de um item de forma agnóstica a formato (dict ou list)."""
        count = 0
        gs_inv = self.game_state.get("inventory")
        if isinstance(gs_inv, dict):
            count = max(count, gs_inv.get(item_id, 0))
            
        pc = self.game_state.get("player_character")
        if isinstance(pc, dict):
            pc_inv = pc.get("inventory")
            if isinstance(pc_inv, dict):
                count = max(count, pc_inv.get(item_id, 0))
            elif isinstance(pc_inv, list):
                item_name = ""
                for cat in self.items_db.values():
                    if isinstance(cat, dict):
                        for k, v in cat.items():
                            if v.get("id") == item_id:
                                item_name = v.get("name", "")
                                break
                    if item_name: break
                
                list_count = 0
                for it in pc_inv:
                    it_str = str(it).lower()
                    if it_str == item_id.lower() or (item_name and item_name.lower() in it_str):
                        list_count += 1
                count = max(count, list_count)
        return count

    def consume_inventory_item(self, item_id: str, amount: int = 1) -> bool:
        """Consome o item com segurança de game_state e pc sem gerar AttributeError."""
        if self.get_inventory_item_count(item_id) < amount:
            return False
            
        gs_inv = self.game_state.setdefault("inventory", {})
        if isinstance(gs_inv, dict) and item_id in gs_inv:
            gs_inv[item_id] = max(0, gs_inv[item_id] - amount)
            
        pc = self.game_state.get("player_character")
        if isinstance(pc, dict):
            pc_inv = pc.get("inventory")
            if isinstance(pc_inv, dict) and item_id in pc_inv:
                pc_inv[item_id] = max(0, pc_inv[item_id] - amount)
            elif isinstance(pc_inv, list):
                item_name = ""
                for cat in self.items_db.values():
                    if isinstance(cat, dict):
                        for k, v in cat.items():
                            if v.get("id") == item_id:
                                item_name = v.get("name", "")
                                break
                    if item_name: break
                removidos = 0
                i = 0
                while i < len(pc_inv) and removidos < amount:
                    it_str = str(pc_inv[i]).lower()
                    if it_str == item_id.lower() or (item_name and item_name.lower() in it_str):
                        pc_inv.pop(i)
                        removidos += 1
                    else:
                        i += 1
        return True

    def add_inventory_item(self, item_id: str, amount: int = 1) -> None:
        """Adiciona item ao inventário sincronizado."""
        gs_inv = self.game_state.setdefault("inventory", {})
        if isinstance(gs_inv, dict):
            gs_inv[item_id] = gs_inv.get(item_id, 0) + amount
            
        pc = self.game_state.get("player_character")
        if isinstance(pc, dict):
            pc_inv = pc.get("inventory")
            if isinstance(pc_inv, dict):
                pc_inv[item_id] = pc_inv.get(item_id, 0) + amount
            elif isinstance(pc_inv, list):
                item_name = item_id
                for cat in self.items_db.values():
                    if isinstance(cat, dict):
                        for k, v in cat.items():
                            if v.get("id") == item_id:
                                item_name = v.get("name", item_id)
                                break
                    if item_name != item_id: break
                for _ in range(amount):
                    pc_inv.append(item_name)

    def get_inventory_capacity(self, pc: dict = None) -> tuple:
        """
        Calcula o limite de carga e ocupação da mochila do personagem conforme regras do D&D 5e:
        - slots_maximos = 10 + max(0, mod_FOR) (mínimo 10, máximo 14).
        - Armas, armaduras e escudos: 1 slot cada.
        - Poções / antídotos / elixires: empilham até 3 por slot.
        - Rações: empilham até 5 por slot.
        - Acessórios: empilham até 2 por slot.
        Retorna (slots_usados, slots_maximos).
        """
        import math
        target_pc = pc if pc is not None else (self.game_state.get("player_character") or {})
        
        attrs = target_pc.get("attributes") or target_pc.get("atributos") or {}
        for_val = 10
        if isinstance(attrs, dict):
            for_val = attrs.get("FOR", attrs.get("Força", attrs.get("STR", 10)))
        mod_for = (for_val - 10) // 2
        slots_max = min(14, max(10, 10 + max(0, mod_for)))

        inv_dict = {}
        if pc is not None and isinstance(pc, dict) and isinstance(pc.get("inventory"), dict):
            inv_dict = pc["inventory"]
        else:
            gs_inv = self.game_state.get("inventory", {})
            if isinstance(gs_inv, dict):
                inv_dict = gs_inv

        slots_used = 0
        for item_id, count in inv_dict.items():
            if not count or count <= 0:
                continue
            it_low = str(item_id).lower()

            # 1. Rações: até 5 por slot
            if "ration" in it_low or item_id in ["i_rations", "i_hearty_rations"]:
                slots_used += math.ceil(count / 5)
            # 2. Poções / Antídotos / Elixires / Pergaminhos: até 3 por slot
            elif any(pk in it_low for pk in ["potion", "antidote", "elixir", "scroll", "poção", "pocao"]):
                slots_used += math.ceil(count / 3)
            # 3. Acessórios: 2 por slot
            elif any(ak in it_low for ak in ["ring", "amulet", "cloak", "boots", "anel", "amuleto", "manto", "bota"]):
                slots_used += math.ceil(count / 2)
            else:
                matched_cat = None
                for cat_name, cat_items in self.items_db.items():
                    if isinstance(cat_items, dict):
                        for k, v in cat_items.items():
                            if v.get("id") == item_id or k == item_id:
                                matched_cat = cat_name
                                break
                    if matched_cat:
                        break
                
                if matched_cat in ["weapons", "armor"]:
                    slots_used += count * 1
                elif matched_cat == "accessories":
                    slots_used += math.ceil(count / 2)
                elif matched_cat == "consumables":
                    slots_used += math.ceil(count / 3)
                else:
                    if any(w in it_low for w in ["sword", "axe", "bow", "hammer", "mace", "shield", "armor", "dagger", "staff", "espada", "escudo", "machado", "arco"]):
                        slots_used += count * 1
                    else:
                        slots_used += math.ceil(count / 3)

        return (slots_used, slots_max)

    def can_add_item(self, item_id: str, count: int = 1, pc: dict = None) -> bool:
        """Verifica se a adição do item respeitará o limite máximo de slots da mochila."""
        import copy
        if pc is not None and isinstance(pc, dict) and isinstance(pc.get("inventory"), dict):
            sim_pc = copy.deepcopy(pc)
            sim_pc["inventory"][item_id] = sim_pc["inventory"].get(item_id, 0) + count
            used, max_slots = self.get_inventory_capacity(sim_pc)
            return used <= max_slots
        else:
            target_pc = pc if pc is not None else (self.game_state.get("player_character") or {})
            orig_gs_inv = self.game_state.get("inventory", {})
            sim_gs_inv = copy.deepcopy(orig_gs_inv) if isinstance(orig_gs_inv, dict) else {}
            sim_gs_inv[item_id] = sim_gs_inv.get(item_id, 0) + count
            
            old_inv = self.game_state.get("inventory")
            self.game_state["inventory"] = sim_gs_inv
            try:
                used, max_slots = self.get_inventory_capacity(target_pc)
                return used <= max_slots
            finally:
                self.game_state["inventory"] = old_inv

    def apply_level_up(self, attr_bonuses: dict = None, chosen_skill_id: str = None, pc: dict = None) -> dict:
        """
        Aplica a progressão de Nível oficial do D&D 5e:
        - Incremento de Nível
        - Recálculo de PV máximo (dado_vida // 2 + 1 + mod_CON, mínimo 1)
        - Aplicação de Aumento de Atributos (+1 em 2 ou +2 em 1)
        - Desbloqueio e registro da Habilidade escolhida na Árvore de Classes
        - Atualização do patamar de XP e bônus de proficiência
        """
        from core.dnd_rules import CLASSES, get_modifier
        target_pc = pc if pc is not None else self.game_state.get("player_character")
        if not target_pc or not isinstance(target_pc, dict):
            return {"success": False, "error": "Nenhum personagem ativo para subir de nível."}

        cur_level = target_pc.get("level", 1)
        next_level = cur_level + 1
        target_pc["level"] = next_level

        # 1. Atributos
        from core.dnd_rules import sync_attributes_dict, normalize_skill_id, SKILL_CANONICAL_TO_UI
        attrs = target_pc.setdefault("attributes", {})
        if not isinstance(attrs, dict):
            target_pc["attributes"] = {"FOR": 10, "DES": 10, "CON": 10, "INT": 10, "SAB": 10, "CAR": 10}
            attrs = target_pc["attributes"]

        if attr_bonuses and isinstance(attr_bonuses, dict):
            map_pt = {
                "Força": "FOR", "Destreza": "DES", "Constituição": "CON",
                "Inteligência": "INT", "Sabedoria": "SAB", "Carisma": "CAR",
                "STR": "FOR", "DEX": "DES", "CON": "CON",
                "INT": "INT", "WIS": "SAB", "CHA": "CAR"
            }
            for k, v in attr_bonuses.items():
                k_norm = map_pt.get(k, map_pt.get(k.upper().strip(), k.upper().strip()))
                if k_norm in ["FOR", "DES", "CON", "INT", "SAB", "CAR"]:
                    en_equiv = {"FOR": "STR", "DES": "DEX", "CON": "CON", "INT": "INT", "SAB": "WIS", "CAR": "CHA"}[k_norm]
                    base_val = attrs.get(k_norm, attrs.get(en_equiv, 10))
                    attrs[k_norm] = base_val + int(v)
                    attrs[en_equiv] = attrs[k_norm]
            sync_attributes_dict(attrs)
            if "atributos" in target_pc and isinstance(target_pc["atributos"], dict):
                map_en_pt = {"FOR": "Força", "DES": "Destreza", "CON": "Constituição", "INT": "Inteligência", "SAB": "Sabedoria", "CAR": "Carisma"}
                for en, pt in map_en_pt.items():
                    if en in attrs:
                        target_pc["atributos"][pt] = attrs[en]
        else:
            sync_attributes_dict(attrs)

        # 2. PV Máximo
        class_name = target_pc.get("class", "Guerreiro")
        class_data = CLASSES.get(class_name, {})
        dado_vida = class_data.get("dado_vida", 8)
        con_val = attrs.get("CON", attrs.get("Constituição", 10))
        con_mod = get_modifier(con_val)
        pv_gain = max(1, (dado_vida // 2) + 1 + con_mod)

        target_pc["hp_max"] = target_pc.get("hp_max", 10) + pv_gain
        target_pc["hp_current"] = min(target_pc["hp_max"], target_pc.get("hp_current", 10) + pv_gain)

        # Recalcula CA se Destreza mudou
        self._recalculate_ac(target_pc)

        # 3. Proficiência
        target_pc["proficiency_bonus"] = 3 if next_level >= 5 else 2

        # 4. Habilidade Escolhida da Árvore
        added_skill_data = None
        if chosen_skill_id:
            unlocked = target_pc.setdefault("unlocked_skills", [])
            canonical_skill_id = normalize_skill_id(chosen_skill_id)
            ui_skill_id = SKILL_CANONICAL_TO_UI.get(canonical_skill_id)
            for sid in [chosen_skill_id, canonical_skill_id, ui_skill_id]:
                if sid and sid not in unlocked:
                    unlocked.append(sid)
            
            c_skills = self.class_skills_db.get(class_name, [])
            for sk in c_skills:
                if sk.get("id") in [chosen_skill_id, canonical_skill_id]:
                    added_skill_data = sk
                    abilities = target_pc.setdefault("abilities", [])
                    if sk.get("name") not in abilities:
                        abilities.append(sk.get("name"))
                    # Aplica efeitos passivos diretos na ficha se houver
                    eff = sk.get("effect", {})
                    if eff.get("ac_bonus"):
                        target_pc["ac"] = target_pc.get("ac", 10) + eff["ac_bonus"]
                        target_pc["ca"] = target_pc["ac"]
                    if eff.get("spell_dc_bonus"):
                        target_pc["spell_save_dc"] = target_pc.get("spell_save_dc", 13) + eff["spell_dc_bonus"]
                    break

        # 5. Tabela de XP para o próximo nível
        XP_TABLE = {1: 300, 2: 900, 3: 2700, 4: 6500, 5: 14000, 6: 23000, 7: 34000}
        target_pc["xp_to_next_level"] = XP_TABLE.get(next_level, next_level * 5000)

        # 6. Spell slots se conjurador
        if class_name in ["Mago", "Clérigo"]:
            slots = target_pc.setdefault("spell_slots", {"1": 2, "2": 0, "3": 0})
            if next_level >= 3:
                slots["2"] = max(slots.get("2", 0), 2)
            if next_level >= 5:
                slots["3"] = max(slots.get("3", 0), 2)
        elif class_name in ["Paladino", "Patrulheiro"]:
            slots = target_pc.setdefault("spell_slots", {"1": 0, "2": 0})
            if next_level >= 2:
                slots["1"] = max(slots.get("1", 0), 2)
            if next_level >= 5:
                slots["2"] = max(slots.get("2", 0), 2)

        lvl_msg = f"[SISTEMA] LEVEL UP! {target_pc.get('name', 'O herói')} atingiu o Nível {next_level}! +{pv_gain} PV Máximos (Total: {target_pc['hp_max']})."
        if added_skill_data:
            lvl_msg += f" Nova habilidade: '{added_skill_data['name']}' ({added_skill_data['type']})."
        self.ui_queue.put({"type": "system_message", "content": lvl_msg})

        return {
            "success": True,
            "level": next_level,
            "hp_max": target_pc["hp_max"],
            "hp_current": target_pc["hp_current"],
            "pv_gain": pv_gain,
            "attributes": attrs,
            "unlocked_skills": target_pc.get("unlocked_skills", []),
            "new_skill": added_skill_data
        }

    def _recalculate_ac(self, pc: dict) -> int:
        """Recalcula deterministicamente a CA (Classe de Armadura / ac) do personagem conforme regras do D&D 5e."""
        from core.dnd_rules import get_modifier, ARMADURAS_5E
        dex_val = 10
        attrs = pc.get("attributes") or pc.get("atributos") or {}
        if isinstance(attrs, dict):
            dex_val = attrs.get("DES", attrs.get("Destreza", 10))
        dex_mod = get_modifier(dex_val)

        # Identifica armadura equipada
        equipped_armor = pc.get("equipped_armor")
        if not equipped_armor and isinstance(pc.get("equipment"), dict):
            equipped_armor = pc["equipment"].get("armor")

        ac = 10 + dex_mod
        if equipped_armor:
            arm_str = str(equipped_armor).lower().strip()
            # 1. Procura em items_db["armor"]
            found_item = None
            for k, v in self.items_db.get("armor", {}).items():
                if v.get("id", "").lower() == arm_str or v.get("name", "").lower() == arm_str or k.lower() == arm_str:
                    found_item = v
                    break
            if found_item:
                itype = found_item.get("type", "")
                base_ac = found_item.get("ac_bonus", 10)
                if itype == "armor_light":
                    ac = base_ac + dex_mod
                elif itype == "armor_medium":
                    ac = base_ac + min(2, dex_mod)
                elif itype == "armor_heavy":
                    ac = base_ac
                else:
                    ac = base_ac
            else:
                # 2. Procura em ARMADURAS_5E
                matched_arm = None
                for k, v in ARMADURAS_5E.items():
                    if k in arm_str or arm_str in k:
                        matched_arm = v
                        break
                if matched_arm:
                    if matched_arm.get("soma_des"):
                        lim = matched_arm.get("limite_des")
                        ac = matched_arm.get("ca_base", 10) + (min(lim, dex_mod) if lim is not None else dex_mod)
                    else:
                        ac = matched_arm.get("ca_base", 10)

        # Bônus de Escudo (+2 padrão D&D 5e)
        has_shield = pc.get("has_shield", False)
        if not has_shield and isinstance(pc.get("equipment"), dict):
            has_shield = bool(pc["equipment"].get("shield"))

        if has_shield:
            shield_bonus = 2
            shield_name = ""
            if isinstance(pc.get("equipment"), dict):
                shield_name = str(pc["equipment"].get("shield", "")).lower()
            for k, v in self.items_db.get("armor", {}).items():
                if v.get("type") == "shield" and (v.get("id", "").lower() in shield_name or v.get("name", "").lower() in shield_name):
                    shield_bonus = v.get("ac_bonus", 2)
                    break
            ac += shield_bonus

        pc["ac"] = ac
        pc["ca"] = ac
        return ac

    def equip_item(self, item_name_or_id: str) -> bool:
        """Equipa uma arma, armadura ou escudo, atualizando a ficha do herói e recalculando a CA se necessário."""
        pc = self.game_state.get("player_character")
        if not pc or not isinstance(pc, dict):
            self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Nenhum personagem ativo para equipar item."})
            return False

        req_clean = item_name_or_id.strip()
        req_low = req_clean.lower()

        # Procura correspondência no items_db
        matched_item_data = None
        matched_category = None  # 'weapon', 'armor', 'shield'

        for cat_name, cat_items in self.items_db.items():
            if isinstance(cat_items, dict):
                for k, v in cat_items.items():
                    v_id = v.get("id", "").lower()
                    v_name = v.get("name", "").lower()
                    if req_low == v_id or req_low == v_name or req_low == k.lower():
                        matched_item_data = v
                        if cat_name == "weapons":
                            matched_category = "weapon"
                        elif cat_name == "armor":
                            matched_category = "shield" if v.get("type") == "shield" else "armor"
                        break
            if matched_item_data:
                break

        from core.dnd_rules import ARMAS_5E, ARMADURAS_5E
        if not matched_category:
            for w_name in ARMAS_5E.keys():
                if req_low == w_name or w_name in req_low:
                    matched_category = "weapon"
                    matched_item_data = {"name": w_name.title(), "id": f"i_{w_name.replace(' ', '_')}"}
                    break

        if not matched_category:
            for a_name in ARMADURAS_5E.keys():
                if req_low == a_name or a_name in req_low:
                    matched_category = "shield" if a_name == "escudo" else "armor"
                    matched_item_data = {"name": a_name.title(), "id": f"i_{a_name.replace(' ', '_')}"}
                    break

        if not matched_category:
            if "escudo" in req_low or "shield" in req_low:
                matched_category = "shield"
                matched_item_data = {"name": req_clean.title(), "id": req_clean}
            elif "armadura" in req_low or "armor" in req_low or "cota" in req_low or "couro" in req_low:
                matched_category = "armor"
                matched_item_data = {"name": req_clean.title(), "id": req_clean}
            else:
                matched_category = "weapon"
                matched_item_data = {"name": req_clean.title(), "id": req_clean}

        item_display_name = matched_item_data.get("name", req_clean)
        item_id = matched_item_data.get("id", req_clean)

        # 1. Validar Posse no inventário ou equipamento
        has_item = False
        if (self.get_inventory_item_count(item_id) > 0 or 
            self.get_inventory_item_count(item_display_name) > 0 or 
            self.get_inventory_item_count(req_clean) > 0):
            has_item = True
        else:
            gs_inv = self.game_state.get("inventory", {})
            pc_inv = pc.get("inventory", {})
            if isinstance(gs_inv, dict) and any(req_low in str(k).lower() for k in gs_inv.keys()):
                has_item = True
            elif isinstance(pc_inv, dict) and any(req_low in str(k).lower() for k in pc_inv.keys()):
                has_item = True
            elif isinstance(pc_inv, list) and any(req_low in str(it).lower() for it in pc_inv):
                has_item = True
            else:
                eq = pc.get("equipment")
                if isinstance(eq, list) and any(req_low in str(it).lower() for it in eq):
                    has_item = True
                elif isinstance(eq, dict) and any(req_low in str(v).lower() for v in eq.values()):
                    has_item = True

        if not has_item:
            msg_err = f"[SISTEMA] Você não possui o item '{req_clean}' em seu inventário."
            self.ui_queue.put({"type": "system_message", "content": msg_err})
            return False

        # Garante equipamento estruturado no PC
        if not isinstance(pc.get("equipment"), dict):
            old_list = pc.get("equipment", [])
            pc["equipment"] = {"items": old_list if isinstance(old_list, list) else []}

        pc_name = pc.get("name", "O herói")

        if matched_category == "shield":
            pc["has_shield"] = True
            pc["equipment"]["shield"] = item_display_name
            nova_ca = self._recalculate_ac(pc)
            log_msg = f"[SISTEMA] {pc_name} empunha {item_display_name}. Ataques e reflexos agora utilizam este equipamento. Classe de Armadura atualizada para {nova_ca}."
        elif matched_category == "armor":
            pc["equipped_armor"] = item_display_name
            pc["equipment"]["armor"] = item_display_name
            nova_ca = self._recalculate_ac(pc)
            log_msg = f"[SISTEMA] {pc_name} veste {item_display_name}. Ataques e reflexos agora utilizam este equipamento. Classe de Armadura atualizada para {nova_ca}."
        else:
            pc["equipped_weapon"] = item_display_name
            pc["equipment"]["weapon"] = item_display_name
            log_msg = f"[SISTEMA] {pc_name} empunha {item_display_name}. Ataques e reflexos agora utilizam este equipamento."

        self.ui_queue.put({"type": "system_message", "content": log_msg})
        self.ui_queue.put({"type": "narrative", "content": log_msg, "npc_falando": "Mestre"})
        return True

    def get_tavern_allies_rumors(self) -> str | None:
        """Gera rumor solene citando nomes dos heróis juramentados reunidos no Hub da Taverna."""
        unlocked = self.story.get_unlocked_allies()
        if not unlocked:
            return None
        nomes = ", ".join([ally.get("name", k) for k, ally in unlocked.items()])
        rumor = f"[RUMORES DA TAVERNA] Sussurros entre os lenhadores confirmam: {nomes} afiam suas armas e vigiam as rotas da montanha aguardando o chamado para o clímax."
        return rumor

    def accept_side_quest(self, quest_id: str) -> bool:
        """
        Registra uma side quest no quest_log do jogador com status 'ativa'.
        Evita duplicação caso a quest já esteja ativa ou concluída.
        """
        quest_data = self.story.get_side_quest(quest_id)
        if not quest_data:
            print(f"[GameEngine] Side quest '{quest_id}' não encontrada no compêndio.")
            return False

        log = self.game_state.setdefault("quest_log", [])
        if not isinstance(log, list):
            self.game_state["quest_log"] = []
            log = self.game_state["quest_log"]

        # Evita duplicação
        for entry in log:
            if isinstance(entry, dict) and entry.get("id") == quest_id:
                if entry.get("status") in ["ativa", "concluida"]:
                    print(f"[GameEngine] Side quest '{quest_id}' já está {entry.get('status')}.")
                    return False

        objectives_raw = quest_data.get("objectives", [])
        if isinstance(objectives_raw, str):
            objectives_raw = [objectives_raw]
        elif not isinstance(objectives_raw, list):
            objectives_raw = []

        formatted_objectives = []
        for obj in objectives_raw:
            if isinstance(obj, dict):
                formatted_objectives.append(obj)
            else:
                formatted_objectives.append({"text": str(obj), "done": False})

        new_entry = {
            "id": quest_id,
            "title": quest_data.get("title", quest_id),
            "description": quest_data.get("description", ""),
            "objective": formatted_objectives[0]["text"] if formatted_objectives else quest_data.get("objective", ""),
            "objectives": formatted_objectives,
            "location": quest_data.get("location", quest_data.get("source", "")),
            "act": quest_data.get("act", 1),
            "recommended_level": quest_data.get("recommended_level", 1),
            "bg_image": quest_data.get("bg_image", ""),
            "source": quest_data.get("source", ""),
            "associated_hero_id": quest_data.get("associated_hero_id", ""),
            "status": "ativa",
            "progress": 0,
            "target_progress": quest_data.get("target_progress", len(formatted_objectives) if formatted_objectives else 1),
            "rewards": copy.deepcopy(quest_data.get("rewards", {}))
        }
        log.append(new_entry)

        sys_log = f"[SISTEMA] Nova Missão Aceita: '{new_entry['title']}'."
        self.ui_queue.put({"type": "system_message", "content": sys_log})
        return True

    def complete_side_quest(self, quest_id: str) -> Dict[str, Any]:
        """
        Marca a side quest como 'concluida' e distribui as recompensas matemáticas:
        XP, Ouro, Suprimentos e Itens (adicionados ao inventário sincronizado).
        """
        log = self.game_state.get("quest_log", [])
        if not isinstance(log, list):
            return {"success": False, "error": "quest_log inválido"}

        target_quest = None
        for entry in log:
            if isinstance(entry, dict) and entry.get("id") == quest_id:
                target_quest = entry
                break

        if not target_quest or target_quest.get("status") != "ativa":
            return {"success": False, "error": f"Quest '{quest_id}' não encontrada ou não está ativa."}

        # Atualiza status e marca todos os objetivos como concluídos
        target_quest["status"] = "concluida"
        target_quest["progress"] = target_quest.get("target_progress", 1)
        if "objectives" in target_quest and isinstance(target_quest["objectives"], list):
            for obj in target_quest["objectives"]:
                if isinstance(obj, dict):
                    obj["done"] = True

        rewards = target_quest.get("rewards", {})
        xp_reward = rewards.get("xp", 0)
        gold_reward = rewards.get("gold", 0)
        items_reward = rewards.get("items", [])
        supplies_reward = rewards.get("supplies", rewards.get("suprimentos_acampamento", 0))

        # 1. Entrega de XP e Ouro
        pc = self.game_state.get("player_character")
        if isinstance(pc, dict):
            if xp_reward > 0:
                pc["xp"] = pc.get("xp", 0) + xp_reward
            if gold_reward > 0:
                pc["gold"] = pc.get("gold", 0) + gold_reward
                self.game_state["gold"] = self.game_state.get("gold", 0) + gold_reward

        # 2. Suprimentos
        if supplies_reward > 0:
            sup_max = self.game_state.get("suprimentos_maximos", 5)
            self.game_state["suprimentos_acampamento"] = min(
                self.game_state.get("suprimentos_acampamento", 0) + supplies_reward,
                sup_max
            )

        # 3. Itens
        delivered_items = []
        if isinstance(items_reward, list):
            for it in items_reward:
                self.add_inventory_item(it, 1)
                delivered_items.append(it)
        elif isinstance(items_reward, dict):
            for it, qty in items_reward.items():
                self.add_inventory_item(it, qty)
                delivered_items.append(f"{it} (x{qty})")

        self.sync_inventory()

        # 4. Juramento do herói resgatado (se a missão possuir associated_hero_id)
        hero_id = target_quest.get("associated_hero_id")
        rescued_hero = None
        if hero_id:
            unlocked = self.story.unlock_ally(hero_id)
            if unlocked:
                hero_data = self.story.allies_pool.get(hero_id, {})
                rescued_hero = hero_data.get("name", hero_id)
                juramento_msg = (
                    f"[JURAMENTO DE ALIADO] {hero_data.get('name', hero_id)} ({hero_data.get('race', '')} {hero_data.get('class', '')}) "
                    f"foi libertado e jura sua lâmina à causa! O herói aguardará a marcha para a batalha final contra o Tirano."
                )
                self.ui_queue.put({"type": "system_message", "content": juramento_msg})
                narrativa_juramento = (
                    f"Diante das cinzas da batalha, {hero_data.get('name', hero_id)} inclina a cabeça em respeito e presta seu juramento solene: "
                    f"ele marchará ao seu lado no clímax final contra o Dragão Supremo."
                )
                self.ui_queue.put({"type": "narrative", "content": narrativa_juramento, "npc_falando": "Maelor"})

        sys_log = (
            f"[SISTEMA] Missão Concluída: '{target_quest.get('title', quest_id)}'! "
            f"Recompensas: +{xp_reward} XP, +{gold_reward} PO, "
            f"Itens: {delivered_items}, +{supplies_reward} Suprimentos."
        )
        if rescued_hero:
            sys_log += f" Aliado Juramentado: {rescued_hero}."
        self.ui_queue.put({"type": "system_message", "content": sys_log})

        return {
            "success": True,
            "quest_id": quest_id,
            "title": target_quest.get("title", quest_id),
            "rewards_given": {
                "xp": xp_reward,
                "gold": gold_reward,
                "items": delivered_items,
                "supplies": supplies_reward,
                "rescued_hero": rescued_hero
            }
        }

    def update_quest_objective(self, quest_id: str, objective_index: int = 0, done: bool = True) -> bool:
        """Marca um objetivo específico da quest como concluído ou pendente."""
        log = self.game_state.get("quest_log", [])
        if not isinstance(log, list):
            return False
        for entry in log:
            if isinstance(entry, dict) and entry.get("id") == quest_id:
                objs = entry.get("objectives", [])
                if 0 <= objective_index < len(objs):
                    if isinstance(objs[objective_index], dict):
                        objs[objective_index]["done"] = done
                    done_count = sum(1 for o in objs if isinstance(o, dict) and o.get("done"))
                    entry["progress"] = done_count
                    return True
        return False

    def get_active_quests(self) -> List[Dict[str, Any]]:
        """Retorna lista de quests ativas no quest_log."""
        log = self.game_state.get("quest_log", [])
        if not isinstance(log, list):
            return []
        return [copy.deepcopy(q) for q in log if isinstance(q, dict) and q.get("status") == "ativa"]

    def get_completed_quests(self) -> List[Dict[str, Any]]:
        """Retorna lista de quests concluídas no quest_log."""
        log = self.game_state.get("quest_log", [])
        if not isinstance(log, list):
            return []
        return [copy.deepcopy(q) for q in log if isinstance(q, dict) and q.get("status") == "concluida"]

    def is_safe_hub(self) -> bool:
        """Verifica se o jogador está em um local seguro (hub/acampamento em modo exploração sem combate)."""
        if self.game_mode != "EXPLORACAO":
            return False
        if self.story.is_climax():
            return False
        if self.game_state.get("active_side_quest"):
            return False
        enemies = [t for t in self.active_combat_targets.values() if t.get("faction", "enemy") == "enemy"]
        if len(enemies) > 0:
            return False

        # Verifica se o beat atual é um hub seguro ou acampamento (onde o jogador pode repousar e viajar)
        beat_str = str(self.story.current_beat)
        beat_data = self.story.campaign_data.get(beat_str, {})
        b_type = beat_data.get("type", "")
        b_name = beat_data.get("name", "").lower()
        has_recruits = beat_data.get("recruitable_allies", False)

        return b_type == "hub" or has_recruits or "acampamento" in b_name or "taverna" in b_name

    def travel_to_side_quest(self, quest_id: str) -> bool:
        """
        Inicia a viagem para o cenário de uma side quest (Bifurcação de exploração).
        Salva a origem do hub, troca o cenário, spawna os inimigos da quest e inicia combate.
        """
        if self.game_mode == "COMBATE":
            sys_log = "[SISTEMA] Impossível viajar para uma missão secundária durante combate ativo!"
            self.ui_queue.put({"type": "system_message", "content": sys_log})
            return False

        if self.game_state.get("active_side_quest"):
            sys_log = "[SISTEMA] Você já está em uma missão secundária ativa. Conclua-a ou fuja antes de partir para outra."
            self.ui_queue.put({"type": "system_message", "content": sys_log})
            return False

        quest_data = self.story.get_side_quest(quest_id)
        if not quest_data:
            sys_log = f"[SISTEMA] Missão '{quest_id}' não encontrada no compêndio."
            self.ui_queue.put({"type": "system_message", "content": sys_log})
            return False

        # Se ainda não estiver aceita no quest_log, aceita automaticamente
        log = self.game_state.setdefault("quest_log", [])
        is_in_log = any(isinstance(q, dict) and q.get("id") == quest_id for q in log)
        if not is_in_log:
            self.accept_side_quest(quest_id)

        # Salva o ponto de origem no Hub da campanha principal
        beat_str = str(self.story.current_beat)
        beat_data = self.story.campaign_data.get(beat_str, {})
        origin_bg = self.game_state.get("current_background", beat_data.get("bg_image", "tavern_bg.jpg"))
        self.game_state["side_quest_origin"] = {
            "beat": self.story.current_beat,
            "background": origin_bg,
            "location_name": beat_data.get("name", "Hub Seguro")
        }
        self.game_state["active_side_quest"] = quest_id

        # Atualiza cenário
        quest_bg = quest_data.get("bg_image", "goblin_camp_bg.jpg")
        self.game_state["current_background"] = quest_bg
        self.current_background_key = quest_bg.replace(".jpg", "").replace(".png", "")

        # Mantém aliados e remove inimigos anteriores
        self.active_combat_targets = {k: v for k, v in self.active_combat_targets.items() if v.get("faction") == "ally"}
        self.active_visual_npcs = {k: v for k, v in self.active_visual_npcs.items() if k in self.active_combat_targets}

        # Spawna inimigos da quest
        enemies_list = quest_data.get("enemies", [])
        self.story.spawn_enemies_from_list(enemies_list, self.active_combat_targets, self.active_visual_npcs)
        for e in enemies_list:
            self.discover_monster(e)
        self.game_mode = "COMBATE"

        # Dispara eventos de transição e narrativa
        q_title = quest_data.get("title", quest_id)
        self.ui_queue.put({
            "type": "beat_transition",
            "beat": f"Missão: {q_title}",
            "name": q_title,
            "bg": quest_bg
        })

        dialogue = quest_data.get("dialogue_intro", f"Você adentra a área de '{q_title}'. O perigo se manifesta!")
        sys_msg = f"[SISTEMA] Viagem para '{q_title}' concluída! O combate tem início!"
        self.ui_queue.put({"type": "system_message", "content": sys_msg})
        self.ui_queue.put({"type": "narrative", "content": dialogue, "npc_falando": "Maelor"})
        return True

    def return_from_side_quest(self, victory: bool = True) -> None:
        """
        Retorna da side quest para o ponto de origem no Hub da campanha.
        Se vitória: entrega recompensas oficiais e marca como concluída.
        Se fuga/derrota: mantém a quest ativa e recua com segurança.
        """
        quest_id = self.game_state.get("active_side_quest")
        if not quest_id:
            return

        origin = self.game_state.get("side_quest_origin") or {}
        origin_bg = origin.get("background", "tavern_bg.jpg")
        origin_name = origin.get("location_name", "Hub Seguro")
        origin_beat = origin.get("beat", self.story.current_beat)

        quest_data = self.story.get_side_quest(quest_id) or {}
        q_title = quest_data.get("title", quest_id)

        # Restaura cenário de origem
        self.game_state["current_background"] = origin_bg
        self.current_background_key = origin_bg.replace(".jpg", "").replace(".png", "")
        self.game_state["active_side_quest"] = None
        self.game_state["side_quest_origin"] = None
        self.game_mode = "EXPLORACAO"

        # Limpa inimigos de combate (preserva aliados)
        self.active_combat_targets = {k: v for k, v in self.active_combat_targets.items() if v.get("faction") == "ally"}
        self.active_visual_npcs = {k: v for k, v in self.active_visual_npcs.items() if k in self.active_combat_targets}

        if victory:
            # Entrega recompensas oficiais (XP, ouro, itens, suprimentos)
            res = self.complete_side_quest(quest_id)
            self.ui_queue.put({
                "type": "beat_transition",
                "beat": f"Retorno ao Hub: Beat {origin_beat}",
                "name": origin_name,
                "bg": origin_bg
            })
            ret_text = (
                f"Vitorioso, você deixa o cenário de '{q_title}' com os despojos recolhidos "
                f"e retorna para {origin_name} com sua missão cumprida com louvor."
            )
            self.ui_queue.put({"type": "narrative", "content": ret_text, "npc_falando": "Maelor"})
        else:
            self.ui_queue.put({
                "type": "beat_transition",
                "beat": f"Recuo Tático: Beat {origin_beat}",
                "name": origin_name,
                "bg": origin_bg
            })
            ret_text = (
                f"Percebendo o perigo iminente, você recua taticamente de '{q_title}' "
                f"e retorna para {origin_name}. A missão continua registrada para quando estiver mais forte."
            )
            self.ui_queue.put({"type": "system_message", "content": ret_text})
            self.ui_queue.put({"type": "narrative", "content": ret_text, "npc_falando": "Maelor"})

    def check_combat_resolution(self):
        pc = self.game_state.get("player_character", {})
        if pc.get("hp_current", 0) <= 0 or pc.get("status") == "morto":
            self.resolve_player_death()
            return
        """Bloco 40: Verifica e processa a vitória do combate."""
        enemies = [t for t in self.active_combat_targets.values() if t.get("faction", "enemy") == "enemy"]
        all_enemies_dead = len(enemies) == 0 or all(t.get("status") == "morto" or t.get("pv_atual", 0) <= 0 or t.get("hp_current", 0) <= 0 for t in enemies)
        if len(self.active_combat_targets) == 0 or all_enemies_dead:
            if "meta" in self.game_state:
                self.game_state["meta"]["revive_used"] = False

            # Tratamento de Vitória em Side Quest
            if self.game_state.get("active_side_quest"):
                self.return_from_side_quest(victory=True)
                return

            if not self.story.is_climax():
                self.game_mode = "EXPLORACAO"
                
                # Bônus de Vitória de Encontro
                pc = self.game_state.get("player_character", {})
                xp_bonus = 100
                import random
                gold_bonus = random.randint(15, 40)
                pc["xp"] = pc.get("xp", 0) + xp_bonus
                pc["gold"] = pc.get("gold", 0) + gold_bonus
                
                # Remove apenas os inimigos abatidos, mantendo aliados na party
                dead_enemy_keys = [k for k, v in self.active_combat_targets.items() if v.get("faction", "enemy") == "enemy"]
                for k in dead_enemy_keys:
                    self.active_combat_targets.pop(k, None)
                    self.active_visual_npcs.pop(k, None)
                    
                xp_to_next = pc.get("xp_to_next_level", 300)
                if pc.get("xp", 0) >= xp_to_next:
                    pc["has_pending_level_up"] = True
                    sys_lvl = f"\n🌟 [EVOLUÇÃO] XP suficiente para SUBIR DE NÍVEL ({pc['xp']}/{xp_to_next})!"
                else:
                    sys_lvl = ""
                    
                sys_log = f"[SISTEMA] Combate vencido no Beat {self.story.current_beat}! (+{xp_bonus} XP, +{gold_bonus} PO).{sys_lvl}"
                self.ui_queue.put({"type": "system_message", "content": sys_log})
                try:
                    prompt_vitoria = f"[SISTEMA] Combate vencido no Beat {self.story.current_beat}. Narre o silêncio que se segue, o sangue no chão, os despojos recolhidos, e convide o jogador a avançar na história."
                    narrative = self.ai.generate_narrative_from_math(sys_log, prompt_vitoria)
                except Exception:
                    narrative = sys_log
                self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
            else:
                self.game_mode = "EPILOGO"
                self.active_combat_targets.clear()
                self.active_visual_npcs.clear()
                sys_log = "[SISTEMA] O Tirano das Cinzas caiu. O ciclo de morte foi quebrado para sempre! FIM DA DEMO."
                self.ui_queue.put({"type": "system_message", "content": sys_log})
                try:
                    prompt_epilogo = "[SISTEMA] O Tirano das Cinzas caiu. O ciclo de morte foi quebrado. Narre de forma épica e cinematográfica a morte do dragão, a ruína do covil e o herói e seus aliados caminhando vitoriosos para a luz. Finalize o texto com 'FIM DA DEMO - OBRIGADO POR JOGAR'."
                    narrative = self.ai.generate_narrative_from_math(sys_log, prompt_epilogo)
                except Exception:
                    narrative = sys_log
                self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})

    def resolve_combat_victory(self):
        self.check_combat_resolution()

    def resolve_player_death(self):
        """Resolve a Morte do Jogador ou Wipe da Party."""
        pc = self.game_state.get("player_character", {})
        
        # Bloco 7 / Bloco 37: O Clímax do Tirano das Cinzas - Déjà Vu
        if self.story.is_climax():
            meta = self.game_state.setdefault("meta", {"loop_count": 0, "segredo_tirano": False})
            loop_count = meta.get("loop_count", 0)
            
            if loop_count == 0:
                # O wipe mortal do sopro do Dragão no Beat 15 (Loop 0)
                # Aciona o Déjà Vu!
                meta["loop_count"] = 1
                meta["segredo_tirano"] = True
                
                # Restaura snapshot exato (mesmo HP, XP, itens, habilidades e equipe de aliados completa intacta)
                snap = self.story.load_snapshot()
                if snap:
                    pc_snap, targets_snap, visual_snap = snap
                    self.game_state["player_character"] = pc_snap
                    self.active_combat_targets = targets_snap
                    self.active_visual_npcs = visual_snap
                    extra = self.story.get_snapshot_extra()
                    if "inventory" in extra:
                        self.game_state["inventory"] = copy.deepcopy(extra["inventory"])
                else:
                    pc["hp_current"] = pc.get("hp_max", 10)
                    pc["status"] = "vivo"
                
                pc_atual = self.game_state.get("player_character", {})
                pc_atual["status"] = "vivo"
                if pc_atual.get("hp_current", 0) <= 0:
                    pc_atual["hp_current"] = pc_atual.get("hp_max", 10)
                    
                for t_id, t_data in self.active_combat_targets.items():
                    if t_data.get("faction") == "ally":
                        t_data["status"] = "vivo"
                        if t_data.get("pv_atual", 0) <= 0:
                            t_data["pv_atual"] = t_data.get("pv_max", 10)
                    elif t_data.get("faction") == "enemy":
                        # Armadura do dragão quebrada!
                        t_data["status"] = "vivo"
                        t_data["pv_max"] = 100
                        t_data["pv_atual"] = 100
                        t_data["ca"] = 14
                        t_data["charge_turn"] = 0
                
                self.game_mode = "COMBATE"
                self.game_state["current_background"] = "deja_vu_bg.jpg"
                
                # Carrega o texto da cutscene do Déjà Vu (beat_15_loop_0_death)
                cutscene_text = ""
                try:
                    with open("data/game_cutscenes.json", "r", encoding="utf-8") as f:
                        cutscenes_db = json.load(f)
                        lines = cutscenes_db.get("beat_15_loop_0_death", [])
                        if lines:
                            cutscene_text = "\n\n".join(lines)
                except Exception:
                    pass
                
                sys_log = "[SISTEMA DÉJÀ VU] O fogo aniquila o seu corpo, mas o tempo se estilhaça e retrocede! O Déjà Vu é acionado. Você e todos os seus aliados retornam intactos ao momento exato em que pisaram no covil. O segredo do dragão foi ativado e sua carapaça está quebrada (CA 14, 100 PV)! A vitória é possível!"
                self.ui_queue.put({"type": "system_message", "content": sys_log})
                full_deja_vu_narrative = f"{cutscene_text}\n\n{sys_log}" if cutscene_text else sys_log
                self.ui_queue.put({"type": "narrative", "content": full_deja_vu_narrative, "npc_falando": "Mestre"})
                return
            else:
                self.game_mode = "GAME_OVER"
                self.active_combat_targets.clear()
                self.active_visual_npcs.clear()
                sys_log = "[SISTEMA] VOCÊ MORREU NO CONFRONTO FINAL. Retornando ao último ponto de descanso..."
                self.ui_queue.put({"type": "system_message", "content": sys_log})
                self.load_game()
                return

        # Condição A: Ressurreição Automática por Item (Pergaminho de Ressurreição)
        elif self.get_inventory_item_count("i_scroll_revive") > 0 and not self.game_state.setdefault("meta", {}).get("revive_used", False):
            self.consume_inventory_item("i_scroll_revive", 1)
            self.game_state["meta"]["revive_used"] = True
            pc["hp_current"] = max(1, pc.get("hp_max", 10) // 2)
            pc["status"] = "vivo"
            sys_log = "[SISTEMA] O Pergaminho de Ressurreição brilha intensamente! Você engana a morte e revive no meio do combate."
            self.ui_queue.put({"type": "system_message", "content": sys_log})
            try:
                narrative = self.ai.generate_narrative_from_math(sys_log, "Milagre de ressurreição no campo de batalha.")
            except Exception:
                narrative = sys_log
            self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
            return
            
        # Condição B: Morte Verdadeira
        else:
            self.game_mode = "GAME_OVER"
            self.active_combat_targets.clear()
            self.active_visual_npcs.clear()
            
            sys_log = "[SISTEMA] VOCÊ MORREU. O mundo escurece. Retornando ao último ponto de descanso..."
            self.ui_queue.put({"type": "system_message", "content": sys_log})
            try:
                narrative = self.ai.generate_narrative_from_math(sys_log, "Morte visceral e definitiva.")
            except Exception:
                narrative = sys_log
            self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                
            print("[Sistema] Executando load_game() devido a Morte Verdadeira...")
            self.load_game()

    def _push_event(self, event_type: str, data: Dict[str, Any]):
        event = {"type": event_type}
        event.update(data)
        self.ui_event_queue.append(event)

    def process_action_async(self, player_input: str, bgs_list: list, lista_bestiario: list):
        """Inicia o Worker Daemon da IA."""
        self.is_ai_thinking = True
        import threading
        t = threading.Thread(target=self._async_turn_processor, args=(player_input, bgs_list, lista_bestiario), daemon=True)
        t.start()
        
    def _async_turn_processor(self, player_input: str, bgs_list: list, lista_bestiario: list):
        """Pipeline do Motor Triplo rodando em Background."""
        try:
            pc = self.game_state.get("player_character", {})
            
            if self.story.current_beat == 0 and pc:
                self.story.inject_prologue_data(pc.get("race", ""), pc.get("class", ""), pc.get("background", ""))
                self.story.advance_beat() # Avança para Beat 1
                self.game_state["story_beat"] = self.story.current_beat
            
            # FASE 0: Parser LÃ³gico (NLP Extrator)
            from core.dnd_rules import BESTIARIO_5E
            
            # Monta estado simplificado para o NLP
            temp_state = self.game_state.copy()
            temp_state["game_mode"] = self.game_mode
            temp_state["active_combat_targets"] = {k: v for k, v in self.active_combat_targets.items() if v.get("status") != "morto"}
            
            # Atalho direto para comandos vindos do Grimório ou UI
            if player_input.startswith("travel_side_quest:"):
                quest_id = player_input.split("travel_side_quest:", 1)[1].strip()
                self.travel_to_side_quest(quest_id)
                return
            elif player_input.startswith("accept_side_quest:"):
                quest_id = player_input.split("accept_side_quest:", 1)[1].strip()
                self.accept_side_quest(quest_id)
                return
            elif any(player_input.lower().startswith(p) for p in ["equip_weapon:", "equip_item:", "equipar:", "equip:"]):
                for p in ["equip_weapon:", "equip_item:", "equipar:", "equip:"]:
                    if player_input.lower().startswith(p):
                        item_arg = player_input[len(p):].strip()
                        self.equip_item(item_arg)
                        return
            elif player_input.startswith("use_item:"):
                item_target = player_input.split("use_item:", 1)[1].strip()
                parts = item_target.split(":", 1)
                item_id = parts[0].strip()
                alvo = [parts[1].strip()] if len(parts) > 1 and parts[1].strip() else []
                json_data = {
                    "tipo_acao": "USAR_ITEM",
                    "recurso_utilizado": item_id,
                    "alvo": alvo,
                    "intencao_cena": f"O herói usa o item {item_id} da sua mochila."
                }
            elif player_input.startswith("cast_spell:"):
                spell_target = player_input.split("cast_spell:", 1)[1].strip()
                parts = spell_target.split(":", 1)
                spell_id = parts[0].strip()
                alvo = [parts[1].strip()] if len(parts) > 1 and parts[1].strip() else []
                if not alvo and self.active_combat_targets:
                    for k, v in self.active_combat_targets.items():
                        if v.get("faction") != "ally" and v.get("status") != "morto":
                            alvo = [k]
                            break
                    if not alvo:
                        alvo = [list(self.active_combat_targets.keys())[0]]
                json_data = {
                    "tipo_acao": "CONJURAR_MAGIA",
                    "recurso_utilizado": spell_id,
                    "alvo": alvo,
                    "intencao_cena": f"O herói conjura a magia {spell_id}."
                }
            elif player_input.lower().startswith("use_skill:") or player_input.lower().startswith("usar_habilidade:"):
                raw_payload = player_input.split(":", 1)[1].strip()
                parts = raw_payload.split("|")
                skill_id = parts[0].strip()
                alvo = [parts[1].strip()] if len(parts) > 1 and parts[1].strip() else []
                if not alvo and self.active_combat_targets:
                    for k, v in self.active_combat_targets.items():
                        if v.get("faction") != "ally" and v.get("status") != "morto":
                            alvo = [k]
                            break
                json_data = {
                    "tipo_acao": "USAR_HABILIDADE",
                    "recurso_utilizado": skill_id,
                    "alvo": alvo,
                    "intencao_cena": f"O herói utiliza a habilidade {skill_id}."
                }
            elif (
                player_input.lower().startswith("atacar")
                or player_input.lower().startswith("attack")
                or player_input.lower().startswith("atacar:")
                or player_input.lower().startswith("attack:")
            ):
                target_str = ""
                if ":" in player_input:
                    target_str = player_input.split(":", 1)[1].strip()
                elif " " in player_input.strip():
                    target_str = player_input.strip().split(" ", 1)[1].strip()

                alvo = [target_str] if target_str else []
                eq_w = pc.get("equipped_weapon") or (pc.get("equipment", {}).get("weapon") if isinstance(pc.get("equipment"), dict) else "ataque desarmado")
                json_data = {
                    "tipo_acao": "ATACAR",
                    "recurso_utilizado": eq_w,
                    "alvo": alvo,
                    "intencao_cena": f"O herói desfere um ataque contra {target_str or 'o inimigo'}."
                }
            else:
                p_low = player_input.lower().strip()
                # Detecção rápida de viagem ou aceitação em linguagem natural
                if any(w in p_low for w in ["viajar para", "partir para", "ir para"]) and any(w in p_low for w in ["missao", "missão", "covil", "altar", "bazar", "masmorra", "montanha", "cripta", "quest"]):
                    matched_qid = None
                    for sq in self.story.get_available_side_quests():
                        sq_id = sq.get("id", "")
                        sq_title = sq.get("title", "").lower()
                        if sq_id.lower() in p_low or any(wd in p_low for wd in sq_title.split() if len(wd) > 4):
                            matched_qid = sq_id
                            break
                    if matched_qid:
                        self.travel_to_side_quest(matched_qid)
                        return
                elif any(w in p_low for w in ["aceitar missao", "aceitar missão", "aceitar contrato", "aceitar rumor"]):
                    matched_qid = None
                    for sq in self.story.get_available_side_quests():
                        sq_id = sq.get("id", "")
                        sq_title = sq.get("title", "").lower()
                        if sq_id.lower() in p_low or any(wd in p_low for wd in sq_title.split() if len(wd) > 4):
                            matched_qid = sq_id
                            break
                    if not matched_qid:
                        act_quests = self.story.get_available_quests_for_current_act()
                        if act_quests:
                            matched_qid = act_quests[0].get("id")
                    if matched_qid:
                        self.accept_side_quest(matched_qid)
                        return

                json_data = self.ai.parse_player_intent(player_input, temp_state)
            
            tipo_acao = json_data.get("tipo_acao", "INTERAGIR_AMBIENTE")
            intencao = json_data.get("intencao_cena", "manter")
            p_low = player_input.lower().strip()

            # TRAVA ANTI-AVANÇO INVOLUNTÁRIO DE BEAT (Tarefa 2)
            # Palavras como "sair", "sair da mesa", conversas ou buscas por missão na Taverna NÃO podem avançar beat.
            if tipo_acao == "AVANCAR_HISTORIA":
                tavern_false_advances = [
                    "sair da mesa", "sair da cadeira", "levantar", "ir ao balcao", "ir ao balcão",
                    "balcao", "balcão", "mesa", "cadeira", "procurar missao", "procurar missão",
                    "ouvir rumor", "ouvir rumores", "conversar", "falar", "perguntar", "beber",
                    "cerveja", "caneca", "taverneiro", "pedir bebida", "olhar taverna"
                ]
                is_false_advance = any(kw in p_low for kw in tavern_false_advances)
                if not is_false_advance and self.story.current_beat <= 1:
                    explicit_advance_keywords = [
                        "viajar", "estrada", "partir", "prosseguir", "avancar", "avançar",
                        "seguir viagem", "sair para a estrada", "deixar a taverna", "ir para a estrada",
                        "proximo beat", "próximo beat", "seguir em frente"
                    ]
                    if not any(kw in p_low for kw in explicit_advance_keywords):
                        is_false_advance = True

                if is_false_advance:
                    tipo_acao = "DIALOGAR" if any(w in p_low for w in ["falar", "convers", "dialog", "pergunt", "propost"]) else "INTERAGIR_CENARIO"
                    intencao = f"Interagir no cenário: {player_input}"
                    json_data["tipo_acao"] = tipo_acao
                    json_data["intencao_cena"] = intencao
            
            # Filtro de Contexto (Modo de Jogo)
            if self.game_mode == "EXPLORACAO" and tipo_acao == "ATACAR":
                self.game_mode = "COMBATE"
            elif intencao == "fugir":
                if self.game_state.get("active_side_quest"):
                    self.return_from_side_quest(victory=False)
                    return
                self.game_mode = "EXPLORACAO"
                self.active_combat_targets.clear()
                self.active_visual_npcs.clear()
                
            # Compatibilidade com a Fase 1
            parsed = {
                "tipo_acao": "exploracao",
                "recurso_utilizado": "nenhum",
                "alvo": ["nenhum"],
                "intencao_cena": intencao,
                "npc_falando": "nenhum"
            }
            
            # O Roteador Principal
            if tipo_acao == "ATACAR":
                alvos = json_data.get("alvo", [])
                if isinstance(alvos, str):
                    alvos = [alvos] if alvos.strip() else []

                living_enemies = [
                    (k, v) for k, v in self.active_combat_targets.items()
                    if v.get("faction", "enemy") == "enemy" and v.get("status") != "morto" and v.get("pv_atual", 0) > 0
                ]

                alvo_principal = None
                if not alvos or alvos[0] in ["", "nenhum", None]:
                    if living_enemies:
                        alvo_principal = living_enemies[0][0]
                    elif self.active_combat_targets:
                        alvo_principal = list(self.active_combat_targets.keys())[0]
                    else:
                        alvo_principal = "Inimigo"
                else:
                    raw_target = str(alvos[0]).strip()
                    # 1. Busca exata por chave
                    for k, v in self.active_combat_targets.items():
                        if k.lower() == raw_target.lower():
                            alvo_principal = k
                            break
                    # 2. Busca por tipo_bestiario (ex: m_dire_wolf, m_bandit, goblin)
                    if not alvo_principal:
                        for k, v in self.active_combat_targets.items():
                            t_best = str(v.get("tipo_bestiario", "")).lower()
                            if t_best and (t_best == raw_target.lower() or t_best.replace("m_", "") == raw_target.lower().replace("m_", "")):
                                alvo_principal = k
                                break
                    # 3. Busca por substring no nome ou na chave
                    if not alvo_principal:
                        r_clean = raw_target.lower().replace("m_", "").replace("_", " ")
                        for k, v in self.active_combat_targets.items():
                            k_clean = k.lower().replace("m_", "").replace("_", " ")
                            v_name = str(v.get("name", "")).lower().replace("m_", "").replace("_", " ")
                            if r_clean in k_clean or k_clean in r_clean or r_clean in v_name or v_name in r_clean:
                                alvo_principal = k
                                break
                    # 4. Fallback em combate ativo com inimigos vivos
                    if not alvo_principal and living_enemies:
                        alvo_principal = living_enemies[0][0]
                    elif not alvo_principal:
                        alvo_principal = raw_target

                parsed["tipo_acao"] = "ataque"
                parsed["recurso_utilizado"] = json_data.get("recurso_utilizado") or pc.get("equipped_weapon") or "ataque desarmado"
                parsed["arma_usada"] = parsed["recurso_utilizado"]
                parsed["alvo"] = [alvo_principal]
                parsed["intencao_cena"] = "iniciar_combate"
                
            elif tipo_acao == "CONJURAR_MAGIA":
                recurso = json_data.get("recurso_utilizado", "")
                alvos = json_data.get("alvo", [])
                
                # Setup arcano
                if "spell_save_dc" not in pc:
                    pc["spell_save_dc"] = 14
                if "spell_slots" not in pc:
                    pc["spell_slots"] = {"1": 3, "2": 0, "3": 1}
                
                import json
                try:
                    spells_db = self.spells_db
                except Exception:
                    spells_db = {}
                    
                spell_id = None
                spell_data = None
                for escola, magias in spells_db.items():
                    for key, s_data in magias.items():
                        s_name = s_data.get("name", "").lower()
                        s_id = s_data.get("id", "").lower()
                        r_low = recurso.lower()
                        if s_name in r_low or r_low in s_name or s_id == r_low or key.lower() == r_low:
                            spell_id = key
                            spell_data = s_data
                            break
                    if spell_id: break
                
                if not spell_data:
                    self.ui_queue.put({"type": "system_message", "content": f"[SISTEMA] A magia '{recurso}' não é conhecida ou não existe no compêndio."})
                    return
                
                spell_level = spell_data.get("level", 1)
                
                # Deduct slot
                if spell_level > 0:
                    slots_avail = pc.get("spell_slots", {}).get(str(spell_level), 0)
                    if slots_avail <= 0:
                        self.ui_queue.put({"type": "system_message", "content": f"[SISTEMA] Você não tem Spell Slots de nível {spell_level} disponíveis para conjurar {spell_data.get('name')}!"})
                        return
                    pc["spell_slots"][str(spell_level)] -= 1
                    
                if spell_data.get("mechanical_action") == "damage" and self.game_mode == "EXPLORACAO":
                    self.game_mode = "COMBATE"
                    
                parsed["tipo_acao"] = "magia"
                parsed["recurso_utilizado"] = recurso
                parsed["spell_data"] = spell_data
                parsed["intencao_cena"] = "iniciar_combate"
                
                if spell_data.get("target_type") == "aoe":
                    # Define alvo dummy só para passar pelo validador do Phase 1 (já que AoE ignora o loop de alvos mas requer a lista)
                    if not self.active_combat_targets:
                        self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Não há inimigos na área de efeito."})
                        return
                    parsed["alvo"] = [list(self.active_combat_targets.keys())[0]]
                else:
                    if not alvos:
                        self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Você precisa de um alvo para esta magia direta."})
                        return
                        
                    alvo_principal = alvos[0]
                    achou_alvo = False
                    
                    for k in self.active_combat_targets.keys():
                        if alvo_principal.lower() in k.lower() or k.lower() in alvo_principal.lower():
                            achou_alvo = True
                            alvo_principal = k
                            break
                            
                    if not achou_alvo and self.game_mode == "COMBATE":
                        self.ui_queue.put({"type": "system_message", "content": f"[SISTEMA] Alvo '{alvos[0]}' não encontrado no combate. Ação cancelada."})
                        return
                    elif not achou_alvo:
                        alvo_principal = alvos[0]
                        
                    parsed["alvo"] = [alvo_principal]
                
            elif tipo_acao == "DESCANSAR":
                from core.time_manager import RestSystem
                if self.game_mode == "COMBATE":
                    self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Impossível descansar com ameaças por perto!"})
                    return
                
                beat_atual = self.story.current_beat
                if beat_atual <= 1:
                    # Hub (Taverna)
                    RestSystem.long_rest(pc, self.game_state)
                    self.game_state["suprimentos_acampamento"] = self.game_state.get("suprimentos_maximos", 1)
                    self.game_state["last_checkpoint_beat"] = beat_atual
                    self.game_state["last_checkpoint_type"] = "TAVERNA"
                    self.save_game()
                    
                    sys_log = f"[SISTEMA] Descanso seguro na Taverna (Dia {self.game_state.get('current_day', 1)}). HP 100%. Suprimentos restaurados. Jogo Salvo."
                    self.ui_queue.put({"type": "system_message", "content": sys_log})
                    try:
                        narrative = self.ai.generate_narrative_from_math(sys_log, "Descanso na taverna com fogo e guisado")
                        self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                    except:
                        pass

                    # Reatividade de Aliados no Hub da Taverna (Item 4.1)
                    rumor = self.get_tavern_allies_rumors()
                    if rumor:
                        self.ui_queue.put({"type": "system_message", "content": rumor})
                        unlocked = self.story.get_unlocked_allies()
                        nomes = ", ".join([ally.get("name", k) for k, ally in unlocked.items()])
                        maelor_msg = f"Maelor observa os rostos na penumbra e assente com solenidade: 'Seus companheiros {nomes} estão atentos nas sombras. Quando a hora chegar, não lutará sozinho.'"
                        self.ui_queue.put({"type": "narrative", "content": maelor_msg, "npc_falando": "Maelor"})
                    return
                else:
                    # Ermo (Acampamento)
                    if self.game_state.get("suprimentos_acampamento", 0) <= 0:
                        self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Sem suprimentos para acampar."})
                        return
                    
                    self.game_state["suprimentos_acampamento"] -= 1
                    import random
                    rolagem = random.randint(1, 20)
                    
                    if rolagem >= 11:
                        # Sucesso
                        RestSystem.long_rest(pc, self.game_state)
                        self.game_state["last_checkpoint_beat"] = beat_atual
                        self.game_state["last_checkpoint_type"] = "ACAMPAMENTO"
                        self.save_game()
                        sys_log = f"[SISTEMA] Acampamento seguro (Dia {self.game_state.get('current_day', 1)}). HP Restaurado. Suprimentos: {self.game_state['suprimentos_acampamento']}/{self.game_state.get('suprimentos_maximos', 1)}. Jogo Salvo."
                        self.ui_queue.put({"type": "system_message", "content": sys_log})
                        try:
                            narrative = self.ai.generate_narrative_from_math(sys_log, "Acampamento seguro com sono tenso mas reparador")
                            self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                        except:
                            pass
                        return
                    else:
                        # Emboscada
                        hp_max = pc.get("hp_max", 10)
                        pc["hp_current"] = int(hp_max * 0.8)
                        self.game_mode = "COMBATE"
                        
                        # Injeta monstro aleatório
                        from core.dnd_rules import BESTIARIO_5E
                        best_keys = list(BESTIARIO_5E.keys())
                        if not best_keys:
                            tipo_best = "goblin"
                        else:
                            tipo_best = random.choice(best_keys)
                            
                        best_data = BESTIARIO_5E.get(tipo_best, {"ca": 10, "pv_max": 10})
                        nome_inimigo = f"{tipo_best.title()} (Emboscada)"
                        self.active_combat_targets[nome_inimigo] = {
                            "name": nome_inimigo,
                            "pv_atual": best_data.get("pv_max", 10),
                            "pv_max": best_data.get("pv_max", 10),
                            "ca": best_data.get("ca", 10),
                            "tipo_bestiario": tipo_best,
                            "faction": "enemy"
                        }
                        self.active_visual_npcs[nome_inimigo] = tipo_best
                        
                        sys_log = f"[SISTEMA] EMBOSCADA! O descanso foi interrompido. HP restaurado em 80%. Iniciativa rolada!"
                        self.ui_queue.put({"type": "system_message", "content": sys_log})
                        try:
                            narrative = self.ai.generate_narrative_from_math(sys_log, "Acordar em sobressalto com um som na escuridão, empunhando a arma no susto")
                            self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                        except:
                            pass
                        return

            elif tipo_acao == "USAR_ITEM":
                recurso = json_data.get("recurso_utilizado")
                if not recurso:
                    self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Você precisa especificar qual item deseja usar."})
                    return
                
                all_items = self.items_db
                item_id = None
                item_data = None
                for cat in all_items.values():
                    if isinstance(cat, dict):
                        for key, data in cat.items():
                            if data.get("name", "").lower() in recurso.lower() or recurso.lower() in data.get("name", "").lower() or data.get("id", "").lower() == recurso.lower():
                                item_id = data.get("id")
                                item_data = data
                                break
                    if item_id: break
                
                if not item_id:
                    self.ui_queue.put({"type": "system_message", "content": f"[SISTEMA] O item '{recurso}' não foi reconhecido no compêndio de itens."})
                    return
                
                qtd_inventario = self.get_inventory_item_count(item_id)
                if qtd_inventario <= 0:
                    self.ui_queue.put({"type": "system_message", "content": f"[SISTEMA] Você não possui o item '{item_data.get('name', recurso)}'."})
                    return
                    
                mech_action = item_data.get("mechanical_action")
                
                if mech_action == "heal":
                    from core.dice_engine import DiceEngine
                    dice_val = item_data.get("dice_value", "2d4+2")
                    cura = DiceEngine.parse_and_roll_dice(dice_val)
                    hp_max = pc.get("hp_max", 10)
                    pc["hp_current"] = min(pc.get("hp_current", 10) + cura, hp_max)
                    
                    self.consume_inventory_item(item_id, 1)
                    restam = self.get_inventory_item_count(item_id)
                    sys_log_item = f"🎲 [DADO - CURA] {item_data.get('name')}: rolou {dice_val} = +{cura} PV (PV Atual: {pc['hp_current']}/{hp_max}). Restam: {restam}."
                    
                elif mech_action == "revive":
                    alvos = json_data.get("alvo", [])
                    if not alvos:
                        self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Você precisa de um alvo aliado para reviver."})
                        return
                    alvo_id = alvos[0]
                    achou = None
                    for k, v in self.active_combat_targets.items():
                        if alvo_id.lower() in k.lower() and v.get("faction") == "ally":
                            achou = k
                            break
                    if not achou:
                        self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Alvo aliado não encontrado para reviver."})
                        return
                        
                    if self.game_state.setdefault("meta", {}).get("revive_used", False):
                        self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] O item de ressurreição só pode ser usado UMA vez por batalha!"})
                        return
                        
                    alvo_data = self.active_combat_targets[achou]
                    if alvo_data.get("status") != "morto" and alvo_data.get("pv_atual", 1) > 0:
                        self.ui_queue.put({"type": "system_message", "content": f"[SISTEMA] {achou.title()} já está vivo."})
                        return
                        
                    self.game_state["meta"]["revive_used"] = True
                    hp_max = alvo_data.get("pv_max", 10)
                    alvo_data["pv_atual"] = max(1, hp_max // 2)
                    alvo_data["status"] = "vivo"
                    
                    self.consume_inventory_item(item_id, 1)
                    restam = self.get_inventory_item_count(item_id)
                    sys_log_item = f"[SISTEMA] Usou {item_data.get('name')}. {achou.title()} foi REVIVIDO com {alvo_data['pv_atual']} PV! Restam: {restam}."

                elif mech_action == "cure_condition":
                    cond = item_data.get("condition_target", "poisoned")
                    self.condition_manager.remove_condition(cond)
                    self.consume_inventory_item(item_id, 1)
                    restam = self.get_inventory_item_count(item_id)
                    sys_log_item = f"[SISTEMA] Usou {item_data.get('name')}. Condição '{cond}' purificada! Restam: {restam}."

                elif mech_action == "cure_all_conditions":
                    self.condition_manager.active_conditions.clear()
                    self.consume_inventory_item(item_id, 1)
                    restam = self.get_inventory_item_count(item_id)
                    sys_log_item = f"[SISTEMA] Usou {item_data.get('name')}. Todas as condições purificadas! Restam: {restam}."

                elif mech_action == "supply":
                    sup_gain = item_data.get("supply_amount", 1)
                    sup_max = self.game_state.get("suprimentos_maximos", 5)
                    self.game_state["suprimentos_acampamento"] = min(self.game_state.get("suprimentos_acampamento", 0) + sup_gain, sup_max)
                    self.consume_inventory_item(item_id, 1)
                    restam = self.get_inventory_item_count(item_id)
                    sys_log_item = f"[SISTEMA] Usou {item_data.get('name')}. +{sup_gain} suprimentos ({self.game_state['suprimentos_acampamento']}/{sup_max}). Restam: {restam}."

                else:
                    self.consume_inventory_item(item_id, 1)
                    restam = self.get_inventory_item_count(item_id)
                    sys_log_item = f"[SISTEMA] Usou {item_data.get('name')}. Restam: {restam}."
                    
                if self.game_mode == "EXPLORACAO":
                    self.ui_queue.put({"type": "system_message", "content": sys_log_item})
                    try:
                        narrative = self.ai.generate_narrative_from_math(sys_log_item, f"Usando {item_data.get('name')}")
                    except Exception:
                        narrative = sys_log_item
                    self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                    return
                else:
                    parsed["tipo_acao"] = "uso_item"
                    parsed["log_precalculado"] = sys_log_item

            elif str(tipo_acao).upper() in ["EQUIPAR", "EQUIPAR_ITEM", "EQUIP"]:
                recurso = json_data.get("recurso_utilizado") or json_data.get("item")
                if not recurso and json_data.get("alvo"):
                    recurso = json_data.get("alvo")[0]
                if recurso:
                    self.equip_item(recurso)
                else:
                    self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Especifique qual arma ou equipamento deseja equipar."})
                return

            elif str(tipo_acao).upper() in [
                "INTERAGIR_CENARIO", "DIALOGAR", "INTERAGIR_AMBIENTE", 
                "OBSERVAR", "CONVERSAR", "INVESTIGAR", "FALAR", "PERGUNTAR", "EXPLORAR", "OLHAR"
            ]:
                if self.story.current_beat == 12 and self.game_state.get('meta', {}).get('loop_count', 0) > 0 and not self.game_state.get('meta', {}).get('segredo_tirano', False):
                    self.game_state['meta']['segredo_tirano'] = True
                    sys_log = "[SISTEMA] Guiado por premonições de chamas, você vasculha o altar e encontra o 'Orbe Quebra-Chamas' (Artefato). A invulnerabilidade do Dragão foi anulada!"
                    self.ui_queue.put({"type": "system_message", "content": sys_log})
                    try:
                        narrative = self.ai.generate_narrative_from_math(sys_log, "Encontrar o orbe sagrado escondido no altar empoeirado")
                    except Exception:
                        narrative = sys_log
                    self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                    return

                # Reatividade de Aliados no Hub da Taverna (Item 4.1)
                if self.story.current_beat <= 1:
                    rumor = self.get_tavern_allies_rumors()
                    if rumor:
                        self.ui_queue.put({"type": "system_message", "content": rumor})
                        unlocked = self.story.get_unlocked_allies()
                        nomes = ", ".join([ally.get("name", k) for k, ally in unlocked.items()])
                        maelor_msg = f"Maelor se inclina sobre o balcão da taverna e sussurra: 'Fique atento. {nomes} estão acampados nas proximidades e prontos para a batalha final.'"
                        self.ui_queue.put({"type": "narrative", "content": maelor_msg, "npc_falando": "Maelor"})
                
                env_prompt = self.story.get_environment_prompt()
                falante = "Taverneiro" if self.story.current_beat <= 1 else "Mestre"
                try:
                    narrative = self.ai.generate_narrative_from_math(env_prompt, player_input)
                except Exception as e:
                    narrative = f"[SISTEMA] Falha ao interagir com cenário: {e}"
                self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": falante})
                return
                
            elif tipo_acao == "AVANCAR_HISTORIA":
                if self.game_mode == "COMBATE":
                    self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Impossível avançar com inimigos vivos."})
                    return
                    
                old_beat = self.story.current_beat
                self.story.advance_beat()
                new_beat = self.story.current_beat
                self.game_state["story_beat"] = new_beat
                
                # Recrutamento Orgânico de Aliados no novo Beat (reunidos para o Clímax)
                novo_aliado = self.story.recruit_ally_for_beat(new_beat, pc)
                if novo_aliado:
                    sys_log_ally = f"[SISTEMA] Um novo aliado juntou-se à sua causa: {novo_aliado['name']} ({novo_aliado['race']} {novo_aliado['class']})! Ele marchará com você rumo ao clímax."
                    self.ui_queue.put({"type": "system_message", "content": sys_log_ally})
                
                beat_str = str(new_beat)
                beat_data = self.story.campaign_data.get(beat_str, {})
                beat_name = beat_data.get("name", f"Beat {new_beat}")
                beat_prompt = beat_data.get("environment_prompt", "")
                bg_image = beat_data.get("bg_image", "tavern_bg.jpg")
                self.game_state["current_background"] = bg_image
                
                # Despacha evento estruturado de transição de beat para a UI
                self.ui_queue.put({
                    "type": "beat_transition",
                    "beat": new_beat,
                    "old_beat": old_beat,
                    "name": beat_name,
                    "description": beat_prompt,
                    "bg_image": bg_image
                })
                
                enemies = beat_data.get("enemies", [])
                
                if enemies:
                    self.game_mode = "COMBATE"
                    self.story.spawn_enemies_for_current_beat(self.active_combat_targets, self.active_visual_npcs)
                    for e in enemies:
                        self.discover_monster(e)
                    for t_id, t_data in self.active_combat_targets.items():
                        if t_data.get("faction", "enemy") == "enemy":
                            tipo_m = t_data.get("tipo_bestiario")
                            if tipo_m:
                                self.discover_monster(tipo_m)
                    
                    sys_log = f"[SISTEMA] AVANÇANDO PARA O BEAT {new_beat}. ENCONTRO INICIADO!"
                    
                    if self.story.is_climax():
                        meta = self.game_state.setdefault('meta', {'loop_count': 0, 'segredo_tirano': False})
                        loop_count = meta.get('loop_count', 0)
                        segredo = meta.get('segredo_tirano', False)
                        
                        # No Beat 15 (Clímax), todos os aliados recrutados entram em campo com ele contra o Dragão Supremo!
                        unlocked_allies = self.story.get_unlocked_allies()
                        for ally_id, ally_data in unlocked_allies.items():
                            nome_aliado = ally_data["name"]
                            self.active_combat_targets[nome_aliado] = copy.deepcopy(ally_data)
                            self.active_combat_targets[nome_aliado]["faction"] = "ally"
                            self.active_visual_npcs[nome_aliado] = ally_data.get("tipo_bestiario", "guerreiro")
                            
                        # Tira snapshot completo na entrada da batalha do Clímax
                        self.story.create_snapshot(
                            pc, 
                            self.active_combat_targets, 
                            self.active_visual_npcs, 
                            {"inventory": self.game_state.get("inventory", {})}
                        )
                        
                        # Apply stats to the boss
                        for k, v in self.active_combat_targets.items():
                            if v.get('faction') == 'enemy':
                                if loop_count == 0:
                                    v['pv_max'] = 999
                                    v['pv_atual'] = 999
                                    v['ca'] = 99
                                    sys_log = "[SISTEMA] O Tirano das Cinzas emerge do vulcão! Sua escama é inquebrável. Corra ou morra!"
                                elif loop_count >= 1 and not segredo:
                                    v['pv_max'] = 300
                                    v['pv_atual'] = 300
                                    v['ca'] = 22
                                    sys_log = "[SISTEMA] O Tirano das Cinzas emerge! O loop foi reiniciado. A batalha é real e excruciante!"
                                elif loop_count >= 1 and segredo:
                                    v['pv_max'] = 100
                                    v['pv_atual'] = 100
                                    v['ca'] = 14
                                    sys_log = "[SISTEMA] O Tirano das Cinzas emerge! O Orbe ressoa, rachando a armadura impenetrável do dragão. É a hora da vingança!"

                    self.ui_queue.put({"type": "system_message", "content": sys_log})
                    
                    try:
                        narrative = self.ai.generate_narrative_from_math(sys_log, "Uma emboscada selvagem e impiedosa ao entrar na nova área.")
                    except Exception:
                        narrative = sys_log
                    self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                else:
                    sys_log = f"[SISTEMA] Você deixa a área. Avançando para o Beat {self.story.current_beat}..."
                    self.ui_queue.put({"type": "system_message", "content": sys_log})
                    
                    try:
                        narrative = self.ai.generate_narrative_from_math(sys_log, "Transição de cenário, a jornada continua em um local seguro.")
                    except Exception:
                        narrative = sys_log
                    self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                return
                
            elif str(tipo_acao).upper() in ["SUBIR_NIVEL", "LEVEL_UP", "EVOLUIR"]:
                from core.dnd_rules import CharacterCalculator
                if pc.get("has_pending_level_up") or pc.get("xp", 0) >= pc.get("xp_to_next_level", 300):
                    res_lvl = CharacterCalculator.apply_level_up(pc)
                    sys_log_lvl = (
                        f"🌟 [EVOLUÇÃO D&D 5E] {pc.get('name', 'Herói')} subiu para o NÍVEL {res_lvl['new_level']}!\n"
                        f"  -> PV Máximo: +{res_lvl['hp_gained']} (Total: {res_lvl['hp_max']})\n"
                        f"  -> Bônus de Proficiência: +{res_lvl['proficiency_bonus']}\n"
                    )
                    if res_lvl.get("slots_unlocked"):
                        sys_log_lvl += f"  -> Novos Spell Slots desbloqueados: {res_lvl['slots_unlocked']}\n"
                    sys_log_lvl += f"  -> Próximo nível aos {pc.get('xp_to_next_level', 900)} XP."
                    
                    self.ui_queue.put({"type": "system_message", "content": sys_log_lvl})
                    try:
                        narrative = self.ai.generate_narrative_from_math(
                            sys_log_lvl, 
                            f"O herói canaliza sua experiência de batalha e atinge o nível {res_lvl['new_level']}."
                        )
                    except Exception:
                        narrative = sys_log_lvl
                    self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Mestre"})
                    return
                else:
                    sys_msg = f"[SISTEMA] XP insuficiente para subir de nível ({pc.get('xp', 0)}/{pc.get('xp_to_next_level', 300)} XP)."
                    self.ui_queue.put({"type": "system_message", "content": sys_msg})
                    return

            elif str(tipo_acao).upper() == "MOVER":
                parsed["tipo_acao"] = "movimento"
                parsed["intencao_cena"] = intencao

            elif str(tipo_acao).upper() in ["USAR_HABILIDADE", "ACAO_TATICA_5E"]:
                parsed["tipo_acao"] = "habilidade"
                parsed["recurso_utilizado"] = json_data.get("recurso_utilizado") or json_data.get("skill_id") or json_data.get("id", "")
                parsed["alvo"] = json_data.get("alvo", ["nenhum"])
                parsed["intencao_cena"] = intencao
                
            else:
                parsed["tipo_acao"] = "exploracao"
                parsed["intencao_cena"] = intencao
                    
            # Hook de Aliados e Snapshot no Clímax (Beat 15)
            if self.game_mode == "COMBATE" and self.story.is_climax():
                if self.story.snapshot is None:
                    unlocked_allies = self.story.get_unlocked_allies()
                    for ally_id, ally_data in unlocked_allies.items():
                        nome_aliado = ally_data["name"]
                        if nome_aliado not in self.active_combat_targets:
                            self.active_combat_targets[nome_aliado] = copy.deepcopy(ally_data)
                            self.active_combat_targets[nome_aliado]["faction"] = "ally"
                            self.active_visual_npcs[nome_aliado] = ally_data.get("tipo_bestiario", "guerreiro")
                    self.story.create_snapshot(
                        pc, 
                        self.active_combat_targets, 
                        self.active_visual_npcs, 
                        {"inventory": self.game_state.get("inventory", {})}
                    )
                    
            # FASE 1: MatemÃ¡tica
            from core.combat_system import resolve_action
            alvos_raw = parsed.get("alvo", ["nenhum"])
            if isinstance(alvos_raw, str):
                alvos_raw = [alvos_raw]
                
            target_entities = []
            for alvo in alvos_raw:
                if alvo != "nenhum":
                    achou_ent = None
                    if alvo in self.active_combat_targets:
                        achou_ent = self.active_combat_targets[alvo]
                    if not achou_ent:
                        for k, v in self.active_combat_targets.items():
                            t_best = str(v.get("tipo_bestiario", "")).lower()
                            if t_best and (t_best == alvo.lower() or t_best.replace("m_", "") == alvo.lower().replace("m_", "")):
                                achou_ent = v
                                break
                    if not achou_ent:
                        a_clean = alvo.lower().replace("m_", "").replace("_", " ")
                        for k, v in self.active_combat_targets.items():
                            k_clean = k.lower().replace("m_", "").replace("_", " ")
                            v_name = str(v.get("name", "")).lower().replace("m_", "").replace("_", " ")
                            if a_clean in k_clean or k_clean in a_clean or a_clean in v_name or v_name in a_clean:
                                achou_ent = v
                                break
                    if not achou_ent and self.game_mode == "COMBATE":
                        living_enemies = [
                            v for v in self.active_combat_targets.values()
                            if v.get("faction", "enemy") == "enemy" and v.get("status") != "morto" and v.get("pv_atual", 0) > 0
                        ]
                        if living_enemies:
                            achou_ent = living_enemies[0]
                    
                    if achou_ent:
                        target_entities.append(achou_ent)
                    elif self.game_mode == "COMBATE":
                        # Auto-instanciação de Segurança se nenhum inimigo existia
                        tipo_bestiario_match = "goblin"
                        for k in BESTIARIO_5E.keys():
                            if k.lower() in alvo.lower() or alvo.lower() in k.lower():
                                tipo_bestiario_match = k
                                break
                        
                        status = BESTIARIO_5E.get(tipo_bestiario_match, {"ca": 10, "pv_max": 10})
                        new_target = {
                            "name": alvo,
                            "pv_atual": status.get("pv_max", 10),
                            "pv_max": status.get("pv_max", 10),
                            "ca": status.get("ca", 10),
                            "tipo_bestiario": tipo_bestiario_match,
                            "faction": "enemy"
                        }
                        self.active_combat_targets[alvo] = new_target
                        self.active_visual_npcs[alvo] = tipo_bestiario_match
                        target_entities.append(new_target)
                        print(f"[Sistema] Auto-instanciando alvo ausente '{alvo}' como '{tipo_bestiario_match}' para o combate.")

            if self.game_mode == "COMBATE" and str(parsed.get("tipo_acao", "")).lower() in ["ataque", "atacar"] and not target_entities:
                living_enemies = [
                    v for v in self.active_combat_targets.values()
                    if v.get("faction", "enemy") == "enemy" and v.get("status") != "morto" and v.get("pv_atual", 0) > 0
                ]
                if living_enemies:
                    target_entities.append(living_enemies[0])
                                
            sys_log = ""
            status = "alive"
            if self.game_mode == "COMBATE":
                result = resolve_action(parsed, pc, target_entities, self.active_combat_targets, self.game_state)
                sys_log = result["sys_log"]
                status = result["status"]
                
                # O Lixeiro de CadÃ¡veres (Limpa quem morreu)
                mortos = []
                for t_id, t_data in self.active_combat_targets.items():
                    if t_data.get("pv_atual", 0) <= 0:
                        mortos.append(t_id)
                for morto in mortos:
                    if morto in self.active_combat_targets:
                        t_data = self.active_combat_targets[morto]
                        fac = t_data.get("faction", "enemy")
                        if fac == "enemy" and not t_data.get("_xp_awarded", False):
                            t_data["_xp_awarded"] = True
                            tipo_best = t_data.get("tipo_bestiario", "").lower().strip()
                            from core.dnd_rules import BESTIARIO_5E, CharacterCalculator
                            best_data = BESTIARIO_5E.get(tipo_best, {})
                            if not best_data:
                                for bk, bv in BESTIARIO_5E.items():
                                    if bk.lower().strip() == tipo_best:
                                        best_data = bv
                                        break
                            xp_ganha = best_data.get("xp", 50)
                            loot = CharacterCalculator.calculate_monster_loot(tipo_best, best_data)
                            gold_ganho = loot.get("gold", 5)
                            drop_item = loot.get("drop_item")
                            
                            pc["xp"] = pc.get("xp", 0) + xp_ganha
                            pc["gold"] = pc.get("gold", 0) + gold_ganho
                            
                            drop_str = ""
                            if drop_item:
                                self.add_inventory_item(drop_item, 1)
                                item_nome = drop_item
                                if drop_item in self.items_db.get("consumables", {}):
                                    item_nome = self.items_db["consumables"][drop_item].get("name", drop_item)
                                drop_str = f" e deixou {item_nome}!"
                                
                            sys_log += f"\n[SISTEMA] O inimigo '{morto}' foi abatido! (+{xp_ganha} XP, +{gold_ganho} PO){drop_str}"
                            
                            xp_next = pc.get("xp_to_next_level", 300)
                            if pc.get("xp", 0) >= xp_next:
                                pc["has_pending_level_up"] = True
                                sys_log += f"\n🌟 [EVOLUÇÃO] XP suficiente para SUBIR DE NÍVEL ({pc['xp']}/{xp_next})!"
                            
                            self.active_combat_targets.pop(morto, None)
                            self.active_visual_npcs.pop(morto, None)
                        elif fac == "ally":
                            sys_log += f"\n[SISTEMA] O aliado '{morto}' tombou em batalha!"
                    
                    
            else:
                # MODO EXPLORACAO
                if intencao == "fugir":
                    sys_log = "[SISTEMA] O jogador conseguiu escapar com sucesso! Combate encerrado."
                elif parsed.get("tipo_acao") in ["teste_pericia", "uso_item", "habilidade"]:
                    result = resolve_action(parsed, pc, target_entities, {}, self.game_state)
                    sys_log = result["sys_log"]
                    status = result["status"]
                elif any(w in (intencao or "").lower() for w in ["observ", "procur", "olh", "investig", "perceb"]):
                    from core.dice_engine import DiceEngine
                    from core.dnd_rules import get_modifier
                    dado = DiceEngine.roll_d20()
                    mod = get_modifier(pc.get("attributes", {}).get("WIS", 10))
                    tot = dado + mod + 2
                    cd = 12
                    res_str = "SUCESSO" if tot >= cd else "FALHA"
                    sys_log = f"🎲 [DADO - TESTE] Percepção: d20 ({dado}) + Mod/Prof (+{mod+2}) = {tot} vs CD {cd} ➔ {res_str}!"
                elif any(w in (intencao or "").lower() for w in ["convers", "fal", "dialog", "pergunt", "propost"]):
                    from core.dice_engine import DiceEngine
                    from core.dnd_rules import get_modifier
                    dado = DiceEngine.roll_d20()
                    mod = get_modifier(pc.get("attributes", {}).get("CHA", 10))
                    tot = dado + mod + 2
                    cd = 11
                    res_str = "SUCESSO" if tot >= cd else "FALHA"
                    sys_log = f"🎲 [DADO - TESTE] Persuasão: d20 ({dado}) + Mod/Prof (+{mod+2}) = {tot} vs CD {cd} ➔ {res_str}!"
                elif parsed.get("tipo_acao") == "movimento":
                    sys_log = f"[SISTEMA] Deslocamento: O aventureiro avança explorando o caminho adiante."
                else:
                    sys_log = f"[SISTEMA] Ação de '{parsed.get('tipo_acao', 'exploracao')}' processada no modo {self.game_mode}."
            
            # Atualiza o PC caso tenha recebido dano/cura
            self.game_state["player_character"] = pc
            
            # FASE 2: The Visceral Narrator (SaÃ­da em Duas Vias)
            
            # PASSO A (Dados)
            self.ui_queue.put({"type": "system_message", "content": sys_log})
            
            # PASSO B (Narrativa Segura)
            try:
                intencao = json_data.get("intencao_cena", "")
                narrative = self.ai.generate_narrative_from_math(sys_log, intencao)
                player_bubble = narrative
            except Exception as e:
                err_msg = "[SISTEMA] Falha na tradução narrativa. A matemática foi computada."
                self.ui_queue.put({"type": "system_message", "content": err_msg})
                player_bubble = err_msg
                
            # BLOCO 31: O Turno dos Inimigos (Batch Processing)
            enemies_alive_after_player = [t for t in self.active_combat_targets.values() if t.get("faction", "enemy") == "enemy" and t.get("pv_atual", 0) > 0 and t.get("status") != "morto"]
            
            if len(enemies_alive_after_player) > 0 and self.game_mode == "COMBATE" and pc.get("hp_current", 10) > 0:
                from core.combat_system import process_enemies_turn_batch
                batch_log = process_enemies_turn_batch(self.active_combat_targets, pc, self.game_state)
                if batch_log.strip():
                    self.ui_queue.put({"type": "system_message", "content": batch_log})
                    try:
                        enemy_narrative = self.ai.generate_narrative_from_math(batch_log, "Inimigos contra-atacam focando nos mais fracos")
                        player_bubble = f"{player_bubble}\n\n{enemy_narrative}"
                    except Exception:
                        self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Falha na tradução narrativa dos inimigos."})
                        player_bubble = f"{player_bubble}\n\n[SISTEMA] Falha na tradução narrativa dos inimigos."

            # BLOCO 32 / 40: Verificação de Ciclo e Limpeza de Cadáveres
            # O Lixeiro Pós-Narrativa
            self.active_combat_targets = {k: v for k, v in self.active_combat_targets.items() if v.get("status") != "morto" and v.get("pv_atual", 0) > 0}
            self.active_visual_npcs = {k: v for k, v in self.active_visual_npcs.items() if k in self.active_combat_targets}

            if pc.get("hp_current", 0) <= 0:
                self.resolve_player_death()
            else:
                enemies_left = [t for t in self.active_combat_targets.values() if t.get("faction", "enemy") == "enemy" and t.get("status") != "morto" and t.get("pv_atual", 0) > 0]
                if len(enemies_left) == 0 and self.game_mode == "COMBATE":
                    self.check_combat_resolution()
            # Enviar para UI (após o turno completo): UMA ÚNICA mensagem narrativa estruturada por turno
            self.ui_queue.put({"type": "narrative", "content": player_bubble, "npc_falando": "Mestre"})
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.ui_queue.put({"type": "system_message", "content": f"[ERRO INTERNO] {str(e)}"})

# Alias de interoperabilidade
GameEngine = SessionManager
