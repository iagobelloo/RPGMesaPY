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
            "last_checkpoint_beat": 1,
            "last_checkpoint_bg": "tavern_bg.jpg",
            "current_day": 1,
            "suprimentos_acampamento": 1,
            "suprimentos_maximos": 1,
            "inventory": {"i_potion_healing": 1, "i_rations": 2},
            "discovered_monsters": [],
            "discovered_rumors": [],
            "meta": {"loop_count": 0, "segredo_tirano": False}
        }
        self.current_save_slot: int = 1

    def save_game(self, slot: int = None, save_path: str = None) -> bool:
        """
        Salva o estado atual do jogo em disco com fidelidade absoluta de metadados nos 3 slots.
        Garante a gravação estruturada em 'saves/save_slot_{slot}.json' e compatibilidade com 'saves/slot{slot}.json'.
        """
        import datetime
        import re
        if save_path:
            target_path = save_path
            slot_paths = [save_path]
            m = re.search(r'(?:slot_?)([1-3])', save_path)
            target_slot = int(m.group(1)) if m else getattr(self, "current_save_slot", 1)
        elif slot is not None and isinstance(slot, str) and (".json" in slot or "/" in slot or "\\" in slot):
            target_path = slot
            slot_paths = [slot]
            m = re.search(r'(?:slot_?)([1-3])', slot)
            target_slot = int(m.group(1)) if m else getattr(self, "current_save_slot", 1)
        else:
            try:
                target_slot = int(slot) if slot is not None else getattr(self, "current_save_slot", 1)
            except (ValueError, TypeError):
                target_slot = getattr(self, "current_save_slot", 1)
            if target_slot not in [1, 2, 3]:
                target_slot = getattr(self, "current_save_slot", 1) if getattr(self, "current_save_slot", 1) in [1, 2, 3] else 1
            self.current_save_slot = target_slot
            slot_paths = [
                f"saves/save_slot_{target_slot}.json",
                f"saves/slot{target_slot}.json"
            ]
            target_path = slot_paths[0]

        try:
            pc = self.game_state.get("player_character") or {}
            now_iso = datetime.datetime.now().isoformat()
            
            beat_num = int(self.story.current_beat) if str(self.story.current_beat).isdigit() else 1
            act_title = "Ato I" if beat_num <= 5 else ("Ato II" if beat_num <= 10 else "Ato III")
            beat_name = "Taverna do Dragão Acordado"
            try:
                with open("data/campaign.json", "r", encoding="utf-8") as cf:
                    camp_data = json.load(cf)
                    if str(beat_num) in camp_data:
                        beat_name = camp_data[str(beat_num)].get("name", beat_name)
            except Exception:
                pass
            location_str = f"{act_title} • {beat_name}"

            char_gender = pc.get("gender") or pc.get("genero")
            if not char_gender:
                from core.dnd_rules import PROTAGONIST_GENDER_MAP
                char_race = pc.get("race", "Humano")
                char_class = pc.get("class", "Guerreiro")
                char_gender = PROTAGONIST_GENDER_MAP.get(char_race, {}).get(char_class, "male")

            quests = self.game_state.get("quest_log", [])
            quests_done = sum(1 for q in quests if isinstance(q, dict) and q.get("status") == "concluida")

            self.game_state["slot"] = target_slot
            self.game_state["timestamp"] = now_iso
            self.game_state["saved_at"] = now_iso
            self.game_state["name"] = pc.get("name", "Aventureiro")
            self.game_state["race"] = pc.get("race", "Humano")
            self.game_state["class"] = pc.get("class", "Guerreiro")
            self.game_state["gender"] = char_gender
            self.game_state["level"] = pc.get("level", 1)
            self.game_state["hp_current"] = pc.get("hp_current", 10)
            self.game_state["hp_max"] = pc.get("hp_max", 10)
            self.game_state["gold"] = pc.get("gold", self.game_state.get("gold", 15))
            self.game_state["current_day"] = self.game_state.get("current_day", 1)
            self.game_state["location"] = location_str
            self.game_state["quests_completed"] = quests_done
            self.game_state["discovered_rumors"] = list(self.game_state.get("discovered_rumors", []))
            self.game_state["discovered_monsters"] = list(self.game_state.get("discovered_monsters", []))
            self.game_mode = getattr(self, "game_mode", "EXPLORACAO")
            self.game_state["game_mode"] = self.game_mode
            self.game_state["story_beat"] = beat_num
            self.game_state["story_flags"] = dict(self.story.flags)

            save_payload = copy.deepcopy(self.game_state)
            for p in slot_paths:
                os.makedirs(os.path.dirname(p) or "saves", exist_ok=True)
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(save_payload, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"[Sistema] Erro ao salvar o jogo em {target_path}: {e}")
            return False

    def load_game(self, slot: int = None, save_path: str = None) -> bool:
        """Carrega o estado do jogo do disco para o Core Engine com isolamento estrito entre slots."""
        import re
        if save_path:
            target_path = save_path
            m = re.search(r'(?:slot_?)([1-3])', save_path)
            target_slot = int(m.group(1)) if m else getattr(self, "current_save_slot", 1)
        elif slot is not None and isinstance(slot, str) and (".json" in slot or "/" in slot or "\\" in slot):
            target_path = slot
            m = re.search(r'(?:slot_?)([1-3])', slot)
            target_slot = int(m.group(1)) if m else getattr(self, "current_save_slot", 1)
        else:
            try:
                target_slot = int(slot) if slot is not None else getattr(self, "current_save_slot", 1)
            except (ValueError, TypeError):
                target_slot = getattr(self, "current_save_slot", 1)
            if target_slot not in [1, 2, 3]:
                target_slot = getattr(self, "current_save_slot", 1) if getattr(self, "current_save_slot", 1) in [1, 2, 3] else 1
            self.current_save_slot = target_slot
            p1 = f"saves/save_slot_{target_slot}.json"
            p2 = f"saves/slot{target_slot}.json"
            if os.path.exists(p1) and os.path.exists(p2):
                target_path = p1 if os.path.getmtime(p1) >= os.path.getmtime(p2) else p2
            elif os.path.exists(p1):
                target_path = p1
            elif os.path.exists(p2):
                target_path = p2
            else:
                target_path = p1

        if not os.path.exists(target_path):
            print(f"[Sistema] Nenhum save encontrado em {target_path}.")
            return False
            
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if "player_character" not in data or not data["player_character"]:
                raise ValueError("O save não contém dados válidos de personagem (player_character nulo ou ausente).")
                
            # Limpa e restaura o estado da sessão (evitando vazamento de dados de outros slots)
            default_state = {
                "player_character": None,
                "recent_history": [],
                "known_npcs": {},
                "quest_log": [],
                "story_beat": 1,
                "active_side_quest": None,
                "side_quest_origin": None,
                "last_checkpoint_type": "TAVERNA",
                "last_checkpoint_beat": 1,
                "last_checkpoint_bg": "tavern_bg.jpg",
                "current_day": 1,
                "suprimentos_acampamento": 1,
                "suprimentos_maximos": 1,
                "inventory": {"i_potion_healing": 1, "i_rations": 2},
                "discovered_monsters": [],
                "discovered_rumors": [],
                "meta": {"loop_count": 0, "segredo_tirano": False}
            }
            self.game_state.clear()
            self.game_state.update(default_state)
            self.game_state.update(copy.deepcopy(data))

            pc = self.game_state["player_character"]
            if isinstance(pc, dict) and isinstance(pc.get("attributes"), dict):
                from core.dnd_rules import sync_attributes_dict
                sync_attributes_dict(pc["attributes"])

            disc_m = data.get("discovered_monsters")
            self.game_state["discovered_monsters"] = list(disc_m) if isinstance(disc_m, list) else []
            disc_r = data.get("discovered_rumors")
            self.game_state["discovered_rumors"] = list(disc_r) if isinstance(disc_r, list) else []
            if not isinstance(self.game_state.get("quest_log"), list):
                self.game_state["quest_log"] = []
            if not isinstance(self.game_state.get("inventory"), dict):
                self.game_state["inventory"] = {}
            if not isinstance(self.game_state.get("meta"), dict):
                self.game_state["meta"] = {"loop_count": 0, "segredo_tirano": False}

            self.game_state["slot"] = target_slot
            self.current_save_slot = target_slot
            self.story.current_beat = data.get("story_beat", getattr(self.story, "current_beat", 1))
            self.game_state["story_beat"] = self.story.current_beat

            # Restaura cenário e chave de background
            cur_bg = data.get("current_background", "tavern_bg.jpg")
            self.game_state["current_background"] = cur_bg
            self.current_background_key = str(cur_bg).replace(".jpg", "").replace(".png", "")

            # Reset e mescla flags da campanha para evitar contaminação entre slots
            for k in list(self.story.flags.keys()):
                if k.startswith("ally_") or k == "final_boss_retried":
                    self.story.flags[k] = False
                else:
                    self.story.flags.pop(k, None)
            if "story_flags" in data and isinstance(data["story_flags"], dict):
                self.story.flags.update(data["story_flags"])

            self.game_mode = data.get("game_mode", "EXPLORACAO")
            self.active_combat_targets.clear()
            self.active_visual_npcs.clear()

            self.sync_inventory()
            
            print(f"[Sistema] Jogo carregado com sucesso de {target_path} (Slot {target_slot}). Atributos do personagem restaurados.")
            return True
        except Exception as e:
            raise RuntimeError(f"Falha crítica ao desserializar save de {target_path}: {e}")

    @staticmethod
    def get_slot_metadata(slot_num: int) -> dict:
        """Coleta resumo estruturado de um slot para a tela visual de saves."""
        try:
            slot_int = int(slot_num)
        except (ValueError, TypeError):
            slot_int = 1

        p1 = f"saves/save_slot_{slot_int}.json"
        p2 = f"saves/slot{slot_int}.json"
        if os.path.exists(p1) and os.path.exists(p2):
            save_path = p1 if os.path.getmtime(p1) >= os.path.getmtime(p2) else p2
        elif os.path.exists(p1):
            save_path = p1
        elif os.path.exists(p2):
            save_path = p2
        else:
            return {"slot": slot_int, "is_empty": True}

        try:
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            pc = data.get("player_character")
            if not pc or not isinstance(pc, dict):
                return {"slot": slot_int, "is_empty": True}
            
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

            char_gender = data.get("gender") or pc.get("gender") or pc.get("genero")
            if not char_gender:
                from core.dnd_rules import PROTAGONIST_GENDER_MAP
                char_race = data.get("race") or pc.get("race", "Humano")
                char_class = data.get("class") or pc.get("class", "Guerreiro")
                char_gender = PROTAGONIST_GENDER_MAP.get(char_race, {}).get(char_class, "male")

            time_val = data.get("timestamp") or data.get("saved_at", "")

            return {
                "slot": slot_int,
                "is_empty": False,
                "name": data.get("name") or pc.get("name", "Aventureiro"),
                "race": data.get("race") or pc.get("race", "Humano"),
                "class": data.get("class") or pc.get("class", "Guerreiro"),
                "gender": char_gender,
                "level": data.get("level", pc.get("level", 1)),
                "hp_current": data.get("hp_current", pc.get("hp_current", 10)),
                "hp_max": data.get("hp_max", pc.get("hp_max", 10)),
                "gold": data.get("gold", pc.get("gold", 15)),
                "story_beat": beat_num,
                "act_title": act_title,
                "beat_name": beat_name,
                "location": data.get("location") or f"{act_title} • {beat_name}",
                "current_day": data.get("current_day", 1),
                "quests_completed": data.get("quests_completed", quests_done),
                "discovered_rumors": list(data.get("discovered_rumors", [])),
                "discovered_monsters": list(data.get("discovered_monsters", [])),
                "game_mode": data.get("game_mode", "EXPLORACAO"),
                "timestamp": time_val,
                "saved_at": time_val
            }
        except Exception as e:
            print(f"[Sistema] Aviso ao ler metadata do slot {slot_int}: {e}")
            return {"slot": slot_int, "is_empty": True}

    @classmethod
    def get_all_slots_summary(cls) -> list:
        """Retorna os metadados dos 3 slots de salvamento."""
        return [cls.get_slot_metadata(i) for i in range(1, 4)]

    @staticmethod
    def delete_save_slot(slot_num: int) -> bool:
        """Exclui os arquivos de salvamento do slot especificado."""
        paths = [f"saves/save_slot_{slot_num}.json", f"saves/slot{slot_num}.json"]
        success = True
        for p in paths:
            if os.path.exists(p):
                try:
                    os.remove(p)
                    print(f"[Sistema] Slot {slot_num} ({p}) excluído com sucesso.")
                except Exception as e:
                    print(f"[Sistema] Erro ao excluir {p}: {e}")
                    success = False
        return success

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

    def discover_rumor(self, quest_id: str) -> bool:
        """
        Adiciona a quest_id aos rumores descobertos (discovered_rumors) caso exista em side_quests.json.
        Evita duplicação caso já tenha sido descoberto.
        Retorna True se for uma nova descoberta, False caso contrário.
        """
        if not quest_id:
            return False
        q_id = str(quest_id).strip()
        if not q_id:
            return False

        quest_data = self.story.get_side_quest(q_id)
        if not quest_data:
            return False

        rumors = self.game_state.setdefault("discovered_rumors", [])
        if not isinstance(rumors, list):
            self.game_state["discovered_rumors"] = []
            rumors = self.game_state["discovered_rumors"]

        if q_id not in rumors:
            rumors.append(q_id)
            title = quest_data.get("title", q_id)
            sys_log = f"[SISTEMA] Novo Rumor Descoberto: '{title}'. Consulte seu Grimório/Diário."
            self.ui_queue.put({"type": "system_message", "content": sys_log})
            return True
        return False

    def get_discovered_rumors(self) -> List[str]:
        """Retorna a lista de IDs de rumores e missões secundárias descobertos pelo jogador."""
        rumors = self.game_state.get("discovered_rumors", [])
        if not isinstance(rumors, list):
            self.game_state["discovered_rumors"] = []
            return []
        return list(rumors)


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

    def is_overencumbered(self, pc: dict = None) -> bool:
        """Verifica se o personagem está sobrecarregado (itens acima do limite de slots de inventário)."""
        target_pc = pc if pc is not None else self.game_state.get("player_character")
        used, max_slots = self.get_inventory_capacity(target_pc)
        return used > max_slots

    def get_character_speed(self, pc: dict = None) -> float:
        """
        Retorna o deslocamento em metros do personagem, aplicando penalidade de -1.5m em caso de sobrecarga.
        Elfo da Floresta: 10.5m, Humano/Draconato/Meio-Orc/Tiefling: 9.0m, Anão/Halfling: 7.5m.
        """
        target_pc = pc if pc is not None else self.game_state.get("player_character")
        from core.dnd_rules import get_racial_speed
        base_speed = 9.0
        if isinstance(target_pc, dict):
            if "speed_m" in target_pc:
                try:
                    base_speed = float(target_pc["speed_m"])
                except (ValueError, TypeError):
                    base_speed = 9.0
            elif "speed" in target_pc:
                try:
                    base_speed = float(str(target_pc["speed"]).replace("m", "").strip())
                except (ValueError, TypeError):
                    base_speed = 9.0
            else:
                base_speed = get_racial_speed(target_pc.get("race", "Humano"))

        if self.is_overencumbered(target_pc):
            return max(1.5, base_speed - 1.5)
        return base_speed

    def calculate_travel_cost(self, pc: dict = None) -> tuple:
        """
        Calcula os custos de viagem (dias_de_viagem, suprimentos_consumidos, deslocamento_efetivo, is_overencumbered):
        - Deslocamento 10.5m: 1 suprimento, 1 dia
        - Deslocamento 9.0m: 2 suprimentos, 2 dias
        - Deslocamento 7.5m: 3 suprimentos, 3 dias
        - Sobrecarga de inventário: penalidade de -1.5m de deslocamento e +1 suprimento consumido (+1 dia).
        """
        target_pc = pc if pc is not None else self.game_state.get("player_character")
        from core.dnd_rules import get_racial_speed
        base_speed = 9.0
        if isinstance(target_pc, dict):
            if "speed_m" in target_pc:
                try:
                    base_speed = float(target_pc["speed_m"])
                except (ValueError, TypeError):
                    base_speed = 9.0
            elif "speed" in target_pc:
                try:
                    base_speed = float(str(target_pc["speed"]).replace("m", "").strip())
                except (ValueError, TypeError):
                    base_speed = 9.0
            else:
                base_speed = get_racial_speed(target_pc.get("race", "Humano"))

        is_encumbered = self.is_overencumbered(target_pc)
        effective_speed = max(1.5, base_speed - 1.5) if is_encumbered else base_speed

        if base_speed >= 10.0:
            base_days = 1
            base_supplies = 1
        elif base_speed >= 8.5:
            base_days = 2
            base_supplies = 2
        else:
            base_days = 3
            base_supplies = 3

        if is_encumbered:
            travel_days = base_days + 1
            supplies_needed = base_supplies + 1
        else:
            travel_days = base_days
            supplies_needed = base_supplies

        return (travel_days, supplies_needed, effective_speed, is_encumbered)

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

    def _recalculate_ac(self, pc: dict = None) -> int:
        """Recalcula deterministicamente a CA (Classe de Armadura / ac) do personagem conforme regras do D&D 5e."""
        if pc is None:
            pc = self.game_state.get("player_character")
        if not pc or not isinstance(pc, dict):
            return 10
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

    def get_available_skills(self) -> list[dict]:
        """
        Retorna a lista de habilidades ativas e passivas disponíveis para o personagem do jogador,
        baseado na sua classe, nível e habilidades desbloqueadas.
        Formato: {"id": str, "name": str, "desc": str, "cost": str, "tier": int, "acquired": bool}
        """
        pc = self.game_state.get("player_character", {})
        c_name = pc.get("class", "Guerreiro")
        level = max(1, int(pc.get("level", 1)))
        
        from core.combat_system import expand_unlocked_skills, normalize_skill_id
        unlocked_set = expand_unlocked_skills(pc.get("unlocked_skills", []))
        
        skills_db = {}
        try:
            with open("data/class_skills.json", "r", encoding="utf-8") as f:
                skills_db = json.load(f)
        except Exception as e:
            print(f"[SessionManager] Erro ao ler class_skills.json: {e}")

        available = []
        seen_ids = set()
        
        # 1. Habilidades da árvore da classe
        for sk in skills_db.get(c_name, []):
            s_id = sk.get("id", "")
            s_tier = int(sk.get("tier", 1))
            s_req = int(sk.get("level_req", s_tier))
            
            # Disponível se o nível for suficiente ou se estiver em unlocked_skills
            if s_req <= level or s_id in unlocked_set:
                if s_id in ["second_wind", "hunters_mark", "sneak_attack", "cunning_action"]:
                    cost = "Ação Bônus"
                else:
                    cost = sk.get("cost")
                    if not cost:
                        if sk.get("type") == "passiva":
                            cost = "Passiva"
                        else:
                            cost = "Ação"
                
                available.append({
                    "id": s_id,
                    "name": sk.get("name", s_id.title()),
                    "desc": sk.get("description", ""),
                    "cost": cost,
                    "tier": s_tier,
                    "acquired": True
                })
                seen_ids.add(s_id)
        
        # 2. Habilidades inatas / fundamentais de classe 5e
        if c_name == "Patrulheiro" and "hunters_mark" not in seen_ids:
            available.append({
                "id": "hunters_mark",
                "name": "Marca do Caçador",
                "desc": "Foca sua atenção em uma criatura como presa. Seus ataques contra o alvo causam +1d6 de dano adicional.",
                "cost": "Ação Bônus",
                "tier": 1,
                "acquired": True
            })
            seen_ids.add("hunters_mark")

        if c_name == "Ladino" and "sneak_attack" not in seen_ids:
            available.append({
                "id": "sneak_attack",
                "name": "Ataque Furtivo",
                "desc": "Aproveita a distração do inimigo para causar +1d6 de dano de precisão no próximo ataque.",
                "cost": "Ação Bônus",
                "tier": 1,
                "acquired": True
            })
            seen_ids.add("sneak_attack")

        if c_name == "Guerreiro" and "second_wind" not in seen_ids:
            available.append({
                "id": "second_wind",
                "name": "Retomar o Fôlego",
                "desc": "Usa sua ação bônus para recuperar 1d10 + Nível de Guerreiro em Pontos de Vida.",
                "cost": "Ação Bônus",
                "tier": 1,
                "acquired": True
            })
            seen_ids.add("second_wind")

        return available

    def get_available_spells(self) -> list[dict]:
        """
        Retorna a lista de magias disponíveis para conjuradores (Mago e Clérigo).
        Retorna lista vazia para classes puramente marciais no nível 1 (Guerreiro, Ladino, Patrulheiro Nv 1).
        Formato: {"id": str, "name": str, "desc": str, "level": int, "cost": str, "slots": int | None}
        """
        pc = self.game_state.get("player_character", {})
        c_name = pc.get("class", "Guerreiro")
        level = max(1, int(pc.get("level", 1)))
        
        # Classes puramente marciais no nível 1 não possuem magias
        if c_name in ["Guerreiro", "Ladino"] or (c_name == "Patrulheiro" and level == 1):
            return []
        if c_name not in ["Mago", "Clérigo", "Paladino"]:
            return []
        if c_name == "Paladino" and level < 2:
            return []
            
        slots_dict = pc.setdefault("spell_slots", {"1": 2})
        slots_nv1 = int(slots_dict.get("1", 2))
        
        spells = []
        if c_name == "Mago":
            spells = [
                {
                    "id": "fire_bolt",
                    "name": "Raio de Fogo",
                    "desc": "Você arremessa um feixe ardente contra um alvo ao alcance, causando 1d10 de dano ígneo.",
                    "level": 0,
                    "cost": "Ação",
                    "slots": None
                },
                {
                    "id": "magic_missile",
                    "name": "Mísseis Mágicos",
                    "desc": "Cria dardos mágicos brilhantes causando dano de força infalível (3d4+3).",
                    "level": 1,
                    "cost": "Ação",
                    "slots": slots_nv1
                },
                {
                    "id": "shield",
                    "name": "Escudo Arcano",
                    "desc": "Ergue uma barreira mágica instantânea, ganhando +5 na sua CA.",
                    "level": 1,
                    "cost": "Reação",
                    "slots": slots_nv1
                },
                {
                    "id": "mage_armor",
                    "name": "Armadura Arcana",
                    "desc": "Envolve o corpo com energia protetora, fixando a CA base em 13 + Modificador de Destreza.",
                    "level": 1,
                    "cost": "Ação",
                    "slots": slots_nv1
                }
            ]
        elif c_name == "Clérigo":
            spells = [
                {
                    "id": "sacred_flame",
                    "name": "Chama Sagrada",
                    "desc": "Radiação divina desce sobre o alvo, causando 1d8 de dano radiante.",
                    "level": 0,
                    "cost": "Ação",
                    "slots": None
                },
                {
                    "id": "cure_wounds",
                    "name": "Curar Ferimentos",
                    "desc": "Uma criatura tocada recupera 1d8 + modificador de conjuração em Pontos de Vida.",
                    "level": 1,
                    "cost": "Ação",
                    "slots": slots_nv1
                },
                {
                    "id": "guiding_bolt",
                    "name": "Raio Guiador",
                    "desc": "Um raio de luz ofuscante atinge o inimigo causando 4d6 de dano radiante.",
                    "level": 1,
                    "cost": "Ação",
                    "slots": slots_nv1
                },
                {
                    "id": "shield_of_faith",
                    "name": "Escudo da Fé",
                    "desc": "Um campo cintilante envolve o alvo, concedendo um bônus de +2 na CA.",
                    "level": 1,
                    "cost": "Ação Bônus",
                    "slots": slots_nv1
                }
            ]
        elif c_name == "Paladino" and level >= 2:
            spells = [
                {
                    "id": "cure_wounds",
                    "name": "Curar Ferimentos",
                    "desc": "Uma criatura tocada recupera 1d8 + modificador de conjuração em Pontos de Vida.",
                    "level": 1,
                    "cost": "Ação",
                    "slots": slots_nv1
                },
                {
                    "id": "shield_of_faith",
                    "name": "Escudo da Fé",
                    "desc": "Um campo cintilante envolve o alvo, concedendo um bônus de +2 na CA.",
                    "level": 1,
                    "cost": "Ação Bônus",
                    "slots": slots_nv1
                }
            ]

        return spells

    def use_skill(self, skill_id_or_name: str, target: str = None) -> dict:
        """
        Execução mecânica real de uma habilidade de classe (D&D 5e).
        Aplica os efeitos reais (cura, marca, buff) no PC ou nos alvos ativos,
        e despacha os logs de sistema e narrativa na ui_queue.
        """
        pc = self.game_state.get("player_character", {})
        from core.combat_system import resolve_skill_effect, normalize_skill_id
        from core.dice_engine import DiceEngine
        
        canon_id = normalize_skill_id(skill_id_or_name)
        s_low = str(skill_id_or_name).lower().strip()
        level = max(1, int(pc.get("level", 1)))
        hp_max = max(1, int(pc.get("hp_max", 10)))
        
        log_msg = ""
        success = True
        
        if canon_id in ["hunters_mark", "sk_ranger_2"] or "marca" in s_low:
            alvo_obj = None
            if target and target in self.active_combat_targets:
                alvo_obj = self.active_combat_targets[target]
            elif self.active_combat_targets:
                enemies = [t for t in self.active_combat_targets.values() if t.get("faction") == "enemy" and t.get("status") != "morto" and t.get("pv_atual", 0) > 0]
                if enemies:
                    alvo_obj = enemies[0]
            
            if alvo_obj:
                alvo_obj["_marked_by_hunters_mark"] = True
                alvo_nome = alvo_obj.get("name", "Inimigo")
                pc["_active_hunters_mark_target"] = alvo_nome
            else:
                alvo_nome = target or "o alvo"
                pc["_active_hunters_mark_target"] = alvo_nome
            log_msg = f"🏹 [HABILIDADE] Marca do Caçador fixada em {alvo_nome}! (+1d6 de dano em ataques contra este alvo)\n"
            
        elif canon_id == "second_wind" or "retomar" in s_low or "folego" in s_low or "fôlego" in s_low:
            cura = DiceEngine.parse_and_roll_dice("1d10") + level
            pc["hp_current"] = min(hp_max, pc.get("hp_current", hp_max) + cura)
            log_msg = f"🎲 [HABILIDADE - CURA] Retomar o Fôlego: recuperou +{cura} PV (1d10 + Nv {level}) ➔ PV: {pc['hp_current']}/{hp_max}!\n"

        elif canon_id == "lay_on_hands" or "cura pelas m" in s_low:
            cura = level * 5
            pc["hp_current"] = min(hp_max, pc.get("hp_current", hp_max) + cura)
            log_msg = f"🎲 [HABILIDADE - CURA] Cura pelas Mãos: restaurou +{cura} PV (5x Nv {level}) ➔ PV: {pc['hp_current']}/{hp_max}!\n"

        elif canon_id in ["sneak_attack", "sk_rogue_1"] or "furtivo" in s_low:
            pc["_sneak_attack_active"] = True
            log_msg = "🗡️ [HABILIDADE] Ataque Furtivo preparado! (+1d6 de dano de precisão no próximo ataque)\n"

        elif canon_id in ["arcane_recovery", "sk_mage_1"] or "recupera" in s_low:
            slots = pc.setdefault("spell_slots", {"1": 2})
            slots["1"] = int(slots.get("1", 0)) + 1
            log_msg = f"✨ [HABILIDADE - ARCANO] Recuperação Arcana: +1 Espaço de Magia de Nível 1 restaurado (Total Nv 1: {slots['1']})!\n"

        else:
            target_list = [self.active_combat_targets[target]] if (target and target in self.active_combat_targets) else []
            log_msg = resolve_skill_effect(skill_id_or_name, pc, target_list, self.active_combat_targets, self.game_state)
            if not log_msg:
                log_msg = f"⚡ [HABILIDADE] {skill_id_or_name.title()} ativada com sucesso!\n"

        self.ui_queue.put({"type": "system_message", "content": log_msg})
        self.ui_queue.put({"type": "narrative", "content": log_msg, "npc_falando": "Mestre"})
        return {"success": success, "log": log_msg, "skill": skill_id_or_name}

    def cast_spell(self, spell_id_or_name: str, target: str = None) -> dict:
        """
        Execução mecânica real de conjuração de magia (D&D 5e).
        Consome spell slots caso o nível da magia seja > 0.
        Aplica dano, cura ou buff e despacha os logs de sistema e narrativa na ui_queue.
        """
        pc = self.game_state.get("player_character", {})
        from core.dice_engine import DiceEngine
        from core.dnd_rules import get_modifier
        
        s_norm = str(spell_id_or_name).lower().strip().replace(" ", "_")
        
        spell_db = {
            "magic_missile": {"name": "Mísseis Mágicos", "level": 1, "type": "damage", "dice": "3d4+3", "element": "força"},
            "misseis_magicos": {"name": "Mísseis Mágicos", "level": 1, "type": "damage", "dice": "3d4+3", "element": "força"},
            "mísseis_mágicos": {"name": "Mísseis Mágicos", "level": 1, "type": "damage", "dice": "3d4+3", "element": "força"},
            "fire_bolt": {"name": "Raio de Fogo", "level": 0, "type": "damage", "dice": "1d10", "element": "fogo"},
            "raio_de_fogo": {"name": "Raio de Fogo", "level": 0, "type": "damage", "dice": "1d10", "element": "fogo"},
            "sacred_flame": {"name": "Chama Sagrada", "level": 0, "type": "damage", "dice": "1d8", "element": "radiante"},
            "chama_sagrada": {"name": "Chama Sagrada", "level": 0, "type": "damage", "dice": "1d8", "element": "radiante"},
            "guiding_bolt": {"name": "Raio Guiador", "level": 1, "type": "damage", "dice": "4d6", "element": "radiante"},
            "raio_guiador": {"name": "Raio Guiador", "level": 1, "type": "damage", "dice": "4d6", "element": "radiante"},
            "cure_wounds": {"name": "Curar Ferimentos", "level": 1, "type": "heal", "dice": "1d8"},
            "curar_ferimentos": {"name": "Curar Ferimentos", "level": 1, "type": "heal", "dice": "1d8"},
            "shield": {"name": "Escudo Arcano", "level": 1, "type": "buff", "ac_bonus": 5},
            "escudo_arcano": {"name": "Escudo Arcano", "level": 1, "type": "buff", "ac_bonus": 5},
            "shield_of_faith": {"name": "Escudo da Fé", "level": 1, "type": "buff", "ac_bonus": 2},
            "escudo_da_fe": {"name": "Escudo da Fé", "level": 1, "type": "buff", "ac_bonus": 2},
            "escudo_da_fé": {"name": "Escudo da Fé", "level": 1, "type": "buff", "ac_bonus": 2},
            "mage_armor": {"name": "Armadura Arcana", "level": 1, "type": "buff", "base_ac": 13},
            "armadura_arcana": {"name": "Armadura Arcana", "level": 1, "type": "buff", "base_ac": 13}
        }
        
        spell_info = spell_db.get(s_norm)
        if not spell_info:
            for k, data in spell_db.items():
                if k in s_norm or s_norm in k:
                    spell_info = data
                    break
                    
        if not spell_info:
            spell_info = {"name": spell_id_or_name.title(), "level": 1, "type": "damage", "dice": "1d8", "element": "mágico"}

        spell_level = spell_info.get("level", 1)
        spell_name = spell_info.get("name", spell_id_or_name.title())

        # Consome slots se level > 0
        if spell_level > 0:
            slots = pc.setdefault("spell_slots", {"1": 2})
            disponiveis = int(slots.get(str(spell_level), 0))
            if disponiveis <= 0:
                err_msg = f"[SISTEMA] Você não possui espaços de magia de nível {spell_level} restantes!"
                self.ui_queue.put({"type": "system_message", "content": err_msg})
                return {"success": False, "message": err_msg, "log": err_msg}
            slots[str(spell_level)] = disponiveis - 1

        log_msg = ""
        m_type = spell_info.get("type", "damage")

        if m_type == "heal":
            mod_conjuracao = get_modifier(pc.get("attributes", {}).get("SAB", pc.get("attributes", {}).get("WIS", 10)))
            if pc.get("class") == "Paladino":
                mod_conjuracao = get_modifier(pc.get("attributes", {}).get("CAR", pc.get("attributes", {}).get("CHA", 10)))
            cura = DiceEngine.parse_and_roll_dice(spell_info.get("dice", "1d8")) + max(0, mod_conjuracao)
            hp_max = max(1, int(pc.get("hp_max", 10)))
            pc["hp_current"] = min(hp_max, pc.get("hp_current", hp_max) + cura)
            log_msg = f"🎲 [MAGIA - CURA] {spell_name}: restaurou +{cura} PV ➔ PV: {pc['hp_current']}/{hp_max}!\n"

        elif m_type == "buff":
            if "ac_bonus" in spell_info:
                bonus = spell_info["ac_bonus"]
                pc["ca"] = pc.get("ca", 10) + bonus
                pc["ac"] = pc["ca"]
                log_msg = f"🛡️ [MAGIA] {spell_name} ativada! Concede +{bonus} na CA (CA atual: {pc['ca']})!\n"
            elif "base_ac" in spell_info:
                mod_des = get_modifier(pc.get("attributes", {}).get("DES", pc.get("attributes", {}).get("DEX", 10)))
                nova_ca = spell_info["base_ac"] + mod_des
                pc["ca"] = max(pc.get("ca", 10), nova_ca)
                pc["ac"] = pc["ca"]
                log_msg = f"🛡️ [MAGIA] {spell_name} ativada! Sua CA foi fixada em {pc['ca']}!\n"

        else:
            alvo_obj = None
            if target and target in self.active_combat_targets:
                alvo_obj = self.active_combat_targets[target]
            elif self.active_combat_targets:
                enemies = [t for t in self.active_combat_targets.values() if t.get("faction") == "enemy" and t.get("status") != "morto" and t.get("pv_atual", 0) > 0]
                if enemies:
                    alvo_obj = enemies[0]

            dano = DiceEngine.parse_and_roll_dice(spell_info.get("dice", "1d8"))
            if alvo_obj:
                alvo_obj["pv_atual"] = max(0, alvo_obj.get("pv_atual", 10) - dano)
                if alvo_obj["pv_atual"] == 0:
                    alvo_obj["status"] = "morto"
                alvo_nome = alvo_obj.get("name", "o inimigo")
                pv_rest = alvo_obj.get("pv_atual", 0)
                pv_max_t = alvo_obj.get("pv_max", 10)
                log_msg = f"✨ [MAGIA] {spell_name} atinge {alvo_nome} causando {dano} de dano! (PV: {pv_rest}/{pv_max_t})\n"
            else:
                alvo_nome = target or "o vazio"
                log_msg = f"✨ [MAGIA] {spell_name} conjurada contra {alvo_nome} causando {dano} de dano de dispersão!\n"

        self.ui_queue.put({"type": "system_message", "content": log_msg})
        self.ui_queue.put({"type": "narrative", "content": log_msg, "npc_falando": "Mestre"})
        return {"success": True, "log": log_msg, "spell": spell_name}

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
        Consome dias de marcha e suprimentos com base no deslocamento racial e sobrecarga.
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

        # Mecânica de Deslocamento e Viagem
        travel_days, supplies_needed, effective_speed, is_encumbered = self.calculate_travel_cost()
        self.game_state["current_day"] = self.game_state.get("current_day", 1) + travel_days
        self.game_state["suprimentos_acampamento"] = max(0, self.game_state.get("suprimentos_acampamento", 0) - supplies_needed)
        if self.get_inventory_item_count("i_rations") > 0:
            self.consume_inventory_item("i_rations", min(self.get_inventory_item_count("i_rations"), supplies_needed))

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

        # Dispara eventos de transição e narrativa com beat inteiro
        q_title = quest_data.get("title", quest_id)
        current_beat_int = int(self.story.current_beat) if str(self.story.current_beat).isdigit() else 1
        self.ui_queue.put({
            "type": "beat_transition",
            "beat": current_beat_int,
            "name": f"Missão: {q_title}",
            "bg": quest_bg,
            "bg_image": quest_bg,
            "description": quest_data.get("description", "")
        })

        encumber_note = " A sobrecarga da mochila (-1.5m) desacelerou o passo (+1 suprimento consumido)." if is_encumbered else ""
        sys_msg = (
            f"[SISTEMA] Viagem para '{q_title}' concluída! "
            f"Marcha de {travel_days} {'dia' if travel_days == 1 else 'dias'} (Deslocamento: {effective_speed}m). "
            f"Consumidos {supplies_needed} suprimentos/rações.{encumber_note} O combate tem início!"
        )
        self.ui_queue.put({"type": "system_message", "content": sys_msg})

        travel_narrative = (
            f"Após marchar por {travel_days} {'dia' if travel_days == 1 else 'dias'} pelas trilhas perigosas e consumir "
            f"{supplies_needed} {'ração' if supplies_needed == 1 else 'rações'} de suprimentos,{encumber_note} "
            f"você alcança o covil do perigo."
        )
        dialogue = quest_data.get("dialogue_intro", f"Você adentra a área de '{q_title}'. O perigo se manifesta!")
        full_narrative = f"{travel_narrative} {dialogue}"
        self.ui_queue.put({"type": "narrative", "content": full_narrative, "npc_falando": "Maelor"})
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
        origin_beat_int = int(origin_beat) if str(origin_beat).isdigit() else int(self.story.current_beat)

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
                "beat": origin_beat_int,
                "name": f"Retorno ao Hub: {origin_name}",
                "bg": origin_bg,
                "bg_image": origin_bg
            })
            ret_text = (
                f"Vitorioso, você deixa o cenário de '{q_title}' com os despojos recolhidos "
                f"e retorna para {origin_name} com sua missão cumprida com louvor."
            )
            self.ui_queue.put({"type": "narrative", "content": ret_text, "npc_falando": "Maelor"})
        else:
            self.ui_queue.put({
                "type": "beat_transition",
                "beat": origin_beat_int,
                "name": f"Recuo Tático: {origin_name}",
                "bg": origin_bg,
                "bg_image": origin_bg
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
        pc = self.game_state.get("player_character") or {}
        
        # Bloco 7 / Bloco 37: O Clímax do Tirano das Cinzas - Déjà Vu
        meta = self.game_state.setdefault("meta", {"loop_count": 0, "segredo_tirano": False})
        if self.story.is_climax() and meta.get("loop_count", 0) == 0:
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
            self.current_background_key = "deja_vu_bg"
            
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

        # Condição A: Ressurreição Automática por Item (Pergaminho de Ressurreição)
        elif self.get_inventory_item_count("i_scroll_revive") > 0 and not meta.get("revive_used", False):
            self.consume_inventory_item("i_scroll_revive", 1)
            meta["revive_used"] = True
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
            
        # Condição B: Morte Verdadeira e Retorno ao Checkpoint Seguro
        else:
            try:
                raw_beat = self.game_state.get("last_checkpoint_beat", 1)
                beat_destino = int(raw_beat) if raw_beat is not None else 1
            except (ValueError, TypeError):
                beat_destino = 1
            if beat_destino < 1:
                beat_destino = 1

            self.story.current_beat = beat_destino
            self.game_state["story_beat"] = beat_destino

            bg_destino = "tavern_bg.jpg" if beat_destino <= 1 else self.game_state.get("last_checkpoint_bg", "tavern_bg.jpg")
            self.game_state["current_background"] = bg_destino
            self.current_background_key = str(bg_destino).replace(".jpg", "").replace(".png", "")

            pc["hp_current"] = pc.get("hp_max", 10)
            pc["status"] = "vivo"
            self.game_mode = "EXPLORACAO"
            self.active_combat_targets.clear()
            self.active_visual_npcs.clear()
            self.game_state["active_side_quest"] = None
            self.game_state["side_quest_origin"] = None

            # Emitir evento de transição de cena para a UI via self.ui_queue.put
            self.ui_queue.put({
                "type": "beat_transition",
                "beat": beat_destino,
                "name": "Taverna do Dragão Acordado" if beat_destino <= 1 else "Acampamento Seguro",
                "description": "Você acorda com a respiração ofegante junto às chamas crepitantes da lareira...",
                "bg_image": self.game_state["current_background"]
            })

            # Emitir a narrativa poética e imersiva do Menestrel Maelor via self.ui_queue.put
            narrativa_morte = (
                "O mundo escureceu e o golpe parecia ter selado seu destino... Contudo, você abre os olhos com um sobressalto "
                "junto às brasas crepitantes da Taverna do Dragão Acordado. O Menestrel Maelor dedilha seu alaúde "
                "em uma melodia serena e observa: 'Nem toda derrota é o fim da canção, bravo aventureiro. O fogo das cinzas "
                "ainda queima em seu peito. Descanse, recupere o fôlego e erga-se novamente, pois o Tirano ainda aguarda.'"
            )
            self.ui_queue.put({"type": "narrative", "content": narrativa_morte, "npc_falando": "Maelor"})

            # Salvar o estado do jogo atualizado no slot atual chamando self.save_game(self.current_save_slot)
            self.save_game(self.current_save_slot)

    def _push_event(self, event_type: str, data: Dict[str, Any]):
        event = {"type": event_type}
        event.update(data)
        self.ui_event_queue.append(event)

    def find_combat_target(self, target_ref: str) -> Optional[Dict[str, Any]]:
        """
        Localiza um participante de combate com base em referência flexível (D&D 5e targeting):
        - 'self', 'eu', 'heroi', 'player' -> player_character
        - Chave exata em active_combat_targets
        - Campo 'id' ou 'narrative_id' dentro dos dados do monstro
        - Índice numérico (ex: '1' -> 1º inimigo vivo, '2' -> 2º)
        - Sufixo UUID (ex: 'a1b2' para 'Lobo Terrível a1b2')
        - tipo_bestiario (ex: 'm_bandit', 'bandit', 'goblin')
        - Substring no nome ou na chave
        - Fallback: primeiro inimigo vivo
        """
        pc = self.game_state.get("player_character") or {}
        hero_name = str(pc.get("name", "Herói")).lower()
        if not target_ref:
            living_enemies = [
                v for v in self.active_combat_targets.values()
                if v.get("faction", "enemy") == "enemy" and v.get("status") != "morto" and v.get("pv_atual", 0) > 0
            ]
            return living_enemies[0] if living_enemies else None

        ref_str = str(target_ref).strip()
        ref_low = ref_str.lower()

        if ref_low in ["self", "eu", "heroi", "herói", "proprio", "próprio", "si mesmo", "player", hero_name]:
            return pc

        living_enemies = [
            (k, v) for k, v in self.active_combat_targets.items()
            if v.get("faction", "enemy") == "enemy" and v.get("status") != "morto" and v.get("pv_atual", 0) > 0
        ]

        # 1. Chave exata
        for k, v in self.active_combat_targets.items():
            if k.lower() == ref_low:
                return v

        # 2. Índice numérico (1-indexed entre inimigos vivos)
        if ref_str.isdigit():
            idx = int(ref_str) - 1
            if 0 <= idx < len(living_enemies):
                return living_enemies[idx][1]

        # 3. Campo 'id' ou 'narrative_id'
        for k, v in self.active_combat_targets.items():
            v_id = str(v.get("id", "")).lower()
            if v_id and (v_id == ref_low or v_id == ref_low.replace("m_", "")):
                return v

        # 4. Sufixo UUID / 4-char suffix (ex: 'Lobo Terrível a1b2')
        for k, v in self.active_combat_targets.items():
            parts = k.split()
            if len(parts) > 1 and parts[-1].lower() == ref_low:
                return v

        # 5. tipo_bestiario
        for k, v in self.active_combat_targets.items():
            t_best = str(v.get("tipo_bestiario", "")).lower()
            if t_best and (t_best == ref_low or t_best.replace("m_", "") == ref_low.replace("m_", "")):
                return v

        # 6. Substring de nome ou chave
        clean_ref = ref_low.replace("m_", "").replace("_", " ")
        for k, v in self.active_combat_targets.items():
            k_clean = k.lower().replace("m_", "").replace("_", " ")
            v_name = str(v.get("name", "")).lower().replace("m_", "").replace("_", " ")
            if clean_ref in k_clean or k_clean in clean_ref or clean_ref in v_name or v_name in clean_ref:
                return v

        # 7. Fallback para o primeiro inimigo vivo em combate
        if living_enemies:
            return living_enemies[0][1]

        return None

    def process_action_async(self, player_input: str, bgs_list: list, lista_bestiario: list):
        """Inicia o Worker Daemon da IA."""
        self.is_ai_thinking = True
        import threading
        t = threading.Thread(target=self._async_turn_processor, args=(player_input, bgs_list, lista_bestiario), daemon=True)
        t.start()
        
    def _async_turn_processor(self, player_input: str, bgs_list: list, lista_bestiario: list):
        """Pipeline do Motor Triplo rodando em Background."""
        try:
            pc = self.game_state.get("player_character")
            if not pc or not isinstance(pc, dict):
                self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Nenhum personagem ativo encontrado. Crie ou carregue seu herói para iniciar a aventura."})
                return
            
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
            travel_prefixes = [
                "travel_side_quest:", "travel_side_quest ", "travel_quest:", "travel_quest ",
                "btn_travel_quest:", "btn_travel_quest "
            ]
            if any(player_input.startswith(p) for p in travel_prefixes) or player_input in ["btn_travel_quest", "travel_quest", "travel_side_quest"]:
                prefix = next((p for p in travel_prefixes if player_input.startswith(p)), "")
                quest_id = player_input[len(prefix):].strip() if prefix else ""
                if not quest_id:
                    active_q = self.get_active_quests()
                    if active_q:
                        quest_id = active_q[0].get("id", "")
                    else:
                        avail = self.story.get_available_quests_for_current_act()
                        if avail:
                            quest_id = avail[0].get("id", "")
                if quest_id:
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
            elif any(player_input.lower().startswith(p) for p in ["dodge", "esquivar", "esquivo", "acao_esquiva", "action_dodge"]):
                json_data = {
                    "tipo_acao": "ESQUIVAR",
                    "recurso_utilizado": "nenhum",
                    "alvo": [],
                    "intencao_cena": "O herói assume a postura tática de Esquivar (Dodge)."
                }
            elif any(player_input.lower().startswith(p) for p in ["disengage", "desengajar", "desengajo", "recuar_seguro"]):
                json_data = {
                    "tipo_acao": "DESENGAJAR",
                    "recurso_utilizado": "nenhum",
                    "alvo": [],
                    "intencao_cena": "O herói executa a ação de Desengajar (Disengage)."
                }
            elif any(player_input.lower().startswith(p) for p in ["move:", "mover:", "deslocar:", "movimento:"]):
                prefix = next(p for p in ["move:", "mover:", "deslocar:", "movimento:"] if player_input.lower().startswith(p))
                sub_move = player_input[len(prefix):].strip()
                json_data = {
                    "tipo_acao": "MOVER",
                    "recurso_utilizado": sub_move or "fechar_distancia",
                    "alvo": [],
                    "intencao_cena": f"Movimento tático: {sub_move or 'fechar distância'}."
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

                import re
                # 1. Comando direto de salvamento de jogo (Chat / Interface)
                is_save_cmd = False
                if p_low in ["salvar", "save", "salvar jogo", "salvar o jogo", "save game"]:
                    is_save_cmd = True
                elif p_low.startswith("save_slot:") or p_low.startswith("salvar_slot:"):
                    is_save_cmd = True
                elif re.match(r'^(?:salvar|save)(?:\s+o\s+jogo|\s+jogo)?(?:\s+no)?\s+slot\s*[:=]?\s*[1-3]', p_low):
                    is_save_cmd = True
                elif re.match(r'^(?:salvar|save)\s+[1-3]$', p_low):
                    is_save_cmd = True

                if is_save_cmd:
                    target_slot = getattr(self, "current_save_slot", 1)
                    m = re.search(r'(?:slot\s*[:=]?\s*|slot_)?([1-3])\b', p_low)
                    if m:
                        try:
                            target_slot = int(m.group(1))
                        except (ValueError, TypeError):
                            target_slot = getattr(self, "current_save_slot", 1)
                    if target_slot not in [1, 2, 3]:
                        target_slot = 1

                    success = self.save_game(slot=target_slot)
                    if success:
                        sys_msg = f"[SISTEMA] Jogo salvo com sucesso no Slot {target_slot}!"
                        self.ui_queue.put({"type": "system_message", "content": sys_msg})
                        self.ui_queue.put({
                            "type": "narrative",
                            "content": f"O tempo se curva à sua vontade e o destino da sua jornada foi registrado no Slot {target_slot}.",
                            "npc_falando": "Mestre"
                        })
                        self._push_event("system_event", {"text": f"Jogo salvo com sucesso no Slot {target_slot}!"})
                    else:
                        sys_msg = f"[SISTEMA] Erro ao tentar salvar no Slot {target_slot}."
                        self.ui_queue.put({"type": "system_message", "content": sys_msg})
                        self.ui_queue.put({
                            "type": "narrative",
                            "content": "Uma força invisível impede a gravação dos seus feitos no momento.",
                            "npc_falando": "Mestre"
                        })
                    return

                # 2. Ação Rápida: Observação do Cenário (Percepção CD 12)
                if (
                    "observo atentamente" in p_low
                    or "procurando detalhes" in p_low
                    or p_low == "observar"
                    or p_low == "olhar ao redor"
                    or p_low.startswith("observar ")
                ):
                    import random
                    from core.dnd_rules import get_modifier
                    attrs = pc.get("attributes", {})
                    wis_val = attrs.get("SAB", attrs.get("WIS", 10))
                    wis_mod = get_modifier(wis_val)
                    profs = pc.get("proficiencies", [])
                    is_prof = any("percep" in str(p).lower() for p in profs)
                    prof_bonus = pc.get("proficiency_bonus", 2) if is_prof else 0

                    d20_roll = random.randint(1, 20)
                    total = d20_roll + wis_mod + prof_bonus
                    dc = 12
                    is_success = (d20_roll == 20) or (d20_roll != 1 and total >= dc)

                    falante = "Taverneiro" if self.story.current_beat <= 1 else "Mestre"

                    if self.game_mode == "COMBATE":
                        if is_success:
                            enemies_info = [
                                f"{t.get('tipo_bestiario', k)} ({t.get('pv_atual', 0)}/{t.get('pv_max', 0)} PV)"
                                for k, t in self.active_combat_targets.items()
                                if t.get('faction') == 'enemy' and t.get('status') != 'morto'
                            ]
                            targets_desc = ", ".join(enemies_info) if enemies_info else "nenhuma ameaça direta"
                            sys_msg = f"[TESTE] Percepção CD {dc} | d20: {d20_roll} + {wis_mod} (mod) + {prof_bonus} (prof) = {total} (SUCESSO!). Você avalia taticamente o combate: {targets_desc}."
                            narrative = "Seus olhos experientes escaneiam o campo de batalha. Você nota os padrões de ataque e as vulnerabilidades na guarda dos inimigos."
                        else:
                            sys_msg = f"[TESTE] Percepção CD {dc} | d20: {d20_roll} + {wis_mod} (mod) + {prof_bonus} (prof) = {total} (FALHA). O turbilhão do combate dispersa sua atenção."
                            narrative = "O reflexo das lâminas e a adrenalina do momento impedem que você estude minuciosamente o terreno ou as aberturas inimigas."
                    else:
                        if is_success:
                            if self.story.current_beat <= 1:
                                self.discover_rumor("sq_goblin_clearing")
                                sys_msg = f"[TESTE] Percepção CD {dc} | d20: {d20_roll} + {wis_mod} (mod) + {prof_bonus} (prof) = {total} (SUCESSO!). Você nota os detalhes e rumores do ambiente."
                                narrative = "Você percorre os olhos pela Taverna do Dragão Acordado. Próximo à lareira crepitante, aventureiros cochicham sobre caravanas emboscadas na Clareira dos Goblins. No mural de avisos, um cartaz oficial promete recompensas para quem investigar a floresta."
                            else:
                                sys_msg = f"[TESTE] Percepção CD {dc} | d20: {d20_roll} + {wis_mod} (mod) + {prof_bonus} (prof) = {total} (SUCESSO!). Você examina detalhadamente os arredores."
                                env_prompt = self.story.get_environment_prompt()
                                try:
                                    narrative = self.ai.generate_narrative_from_math(f"Percepção bem-sucedida ({total} vs CD {dc})", env_prompt)
                                except Exception:
                                    narrative = "Você observa com atenção cada detalhe do ambiente: pegadas no solo, a direção dos ventos e sinais sutis que revelam os perigos da região."
                        else:
                            sys_msg = f"[TESTE] Percepção CD {dc} | d20: {d20_roll} + {wis_mod} (mod) + {prof_bonus} (prof) = {total} (FALHA). Você não nota nada de incomum."
                            if self.story.current_beat <= 1:
                                narrative = "A taverna segue em seu burburinho costumeiro; canecas batem nas mesas e fumaça de cachimbo paira no ar, sem nada além da rotina habitual."
                            else:
                                narrative = "A penumbra e o cansaço da marcha turvam sua visão; você não consegue identificar pistas ou detalhes além do óbvio."

                    self.ui_queue.put({"type": "system_message", "content": sys_msg})
                    self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": falante})
                    return

                # 3. Ação Rápida: Diálogo com quem estiver por perto (Persuasão CD 11)
                if (
                    "aproximo-me e tento conversar" in p_low
                    or "conversar com quem estiver por perto" in p_low
                    or p_low == "conversar"
                    or p_low == "dialogar"
                ):
                    import random
                    from core.dnd_rules import get_modifier
                    attrs = pc.get("attributes", {})
                    cha_val = attrs.get("CAR", attrs.get("CHA", 10))
                    cha_mod = get_modifier(cha_val)
                    profs = pc.get("proficiencies", [])
                    is_prof = any("persua" in str(p).lower() for p in profs)
                    prof_bonus = pc.get("proficiency_bonus", 2) if is_prof else 0

                    d20_roll = random.randint(1, 20)
                    total = d20_roll + cha_mod + prof_bonus
                    dc = 11
                    is_success = (d20_roll == 20) or (d20_roll != 1 and total >= dc)

                    falante = "Taverneiro" if self.story.current_beat <= 1 else "Mestre"

                    if self.game_mode == "COMBATE":
                        if is_success:
                            sys_msg = f"[TESTE] Persuasão CD {dc} | d20: {d20_roll} + {cha_mod} (mod) + {prof_bonus} (prof) = {total} (SUCESSO!). Você tenta intimidar ou exigir rendição."
                            narrative = "Você brada com firmeza através do caos do combate. Seus inimigos hesitam por um instante, intimidados pela autoridade de sua presença."
                        else:
                            sys_msg = f"[TESTE] Persuasão CD {dc} | d20: {d20_roll} + {cha_mod} (mod) + {prof_bonus} (prof) = {total} (FALHA). As ameaças são ignoradas."
                            narrative = "Seus adversários respondem com zombaria e rosnados ferozes. No campo de batalha, suas palavras são engolidas pelo ferro e pelo sangue."
                    else:
                        if is_success:
                            if self.story.current_beat <= 1:
                                self.discover_rumor("sq_goblin_clearing")
                                sys_msg = f"[TESTE] Persuasão CD {dc} | d20: {d20_roll} + {cha_mod} (mod) + {prof_bonus} (prof) = {total} (SUCESSO!). O taverneiro compartilha informações valiosas."
                                narrative = "Maelor, o taverneiro, enxuga uma caneca de estanho e inclina-se sobre o balcão: 'Se procura trabalho e ouro fácil, forasteiro, comerciantes relatam que goblins estão emboscando carroças na Clareira da Mata Leste. Os guardas nada fazem. Talvez alguém com sua têmpera consiga limpar o caminho.'"
                            else:
                                sys_msg = f"[TESTE] Persuasão CD {dc} | d20: {d20_roll} + {cha_mod} (mod) + {prof_bonus} (prof) = {total} (SUCESSO!). Seu interlocutor se mostra receptivo."
                                env_prompt = self.story.get_environment_prompt()
                                try:
                                    narrative = self.ai.generate_narrative_from_math(f"Persuasão bem-sucedida ({total} vs CD {dc})", env_prompt)
                                except Exception:
                                    narrative = "A pessoa mais próxima baixa a guarda diante de sua cortesia e compartilha boatos sobre os acontecimentos recentes da região."
                        else:
                            sys_msg = f"[TESTE] Persuasão CD {dc} | d20: {d20_roll} + {cha_mod} (mod) + {prof_bonus} (prof) = {total} (FALHA). O interlocutor é reticente."
                            if self.story.current_beat <= 1:
                                narrative = "Maelor mal ergue a cabeça do balcão: 'Perguntas demais dão sede, novato. Se quiser prosear, peça um hidromel e pague a conta primeiro.'"
                            else:
                                narrative = "Aqueles ao redor evitam seu olhar, murmurando entre dentes e ignorando qualquer tentativa de aproximação."

                    self.ui_queue.put({"type": "system_message", "content": sys_msg})
                    self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": falante})
                    return

                json_data = self.ai.parse_player_intent(player_input, temp_state)
            
            tipo_acao = json_data.get("tipo_acao", "INTERAGIR_AMBIENTE")
            intencao = json_data.get("intencao_cena", "manter")
            p_low = player_input.lower().strip()

            # Detecção de diálogos e interações com o ambiente na Taverna (Beat <= 1)
            dialogue_interaction_keywords = [
                "falar", "falo", "conversar", "converso", "perguntar", "pergunto", "dialogar", "dialogo",
                "taverneiro", "estalajadeiro", "balcao", "balcão", "mesa", "cadeira", "pedir", "peço",
                "ouvir", "ouço", "olhar", "olho", "observar", "observo", "examinar", "investigar",
                "rumor", "rumores", "cerveja", "caneca", "bebida", "beber", "bebo", "comer", "como",
                "comida", "garçom", "garcom", "garconete", "bardo", "menestrel"
            ]
            is_dialogue_or_interaction = any(kw in p_low for kw in dialogue_interaction_keywords)

            # Detecção e Destravamento de Avanço Natural da Taverna (Beat 1 -> Beat 2)
            has_table_exit = any(k in p_low for k in ["sair da mesa", "sair da cadeira", "levantar da mesa", "levantar da cadeira"])
            strong_exit_keywords = [
                "sair da taverna", "saio da taverna", "deixar a taverna", "deixo a taverna",
                "abro a porta", "abrir a porta", "abro a porta da taverna", "abrir a porta da taverna",
                "vou para a estrada", "pegar a estrada", "pego a estrada", "ir para a estrada",
                "seguir viagem", "sigo viagem", "partir", "parto", "ir embora", "vou embora",
                "vou lá fora", "vou la fora", "sair para a estrada", "saio para a estrada",
                "seguir em frente", "sigo em frente", "estrada", "viajar", "viajo",
                "prosseguir", "prossigo", "avancar", "avançar", "avanço", "avanco",
                "proximo beat", "próximo beat"
            ]
            import re
            has_strong_exit = any(
                re.search(rf"\b{re.escape(kw)}\b", p_low) if len(kw.split()) == 1 else (kw in p_low)
                for kw in strong_exit_keywords
            )
            has_standalone_exit = any(re.search(rf"\b{re.escape(kw)}\b", p_low) for kw in ["sair", "saio"]) and not has_table_exit
            is_explicit_advance = (has_strong_exit or has_standalone_exit) and (not is_dialogue_or_interaction)

            tavern_false_advances = [
                "sair da mesa", "sair da cadeira", "levantar da mesa", "levantar da cadeira",
                "levantar", "ir ao balcao", "ir ao balcão",
                "balcao", "balcão", "mesa", "cadeira", "procurar missao", "procurar missão",
                "ouvir rumor", "ouvir rumores", "conversar", "falar", "perguntar", "beber",
                "cerveja", "caneca", "taverneiro", "pedir bebida", "olhar taverna"
            ]
            has_false_advance_kw = (not is_explicit_advance) and any(kw in p_low for kw in tavern_false_advances)

            if self.story.current_beat <= 1:
                # Se o jogador expressou claramente a intenção de sair da taverna sem diálogo ativo
                if is_explicit_advance:
                    tipo_acao = "AVANCAR_HISTORIA"
                    intencao = "avancar"
                    json_data["tipo_acao"] = "AVANCAR_HISTORIA"
                    json_data["intencao_cena"] = "avancar"
                elif is_dialogue_or_interaction and tipo_acao == "AVANCAR_HISTORIA":
                    tipo_acao = "DIALOGAR" if any(w in p_low for w in ["falar", "falo", "convers", "dialog", "pergunt", "propost", "taverneiro", "estalajadeiro"]) else "INTERAGIR_CENARIO"
                    intencao = f"Interagir no cenário: {player_input}"
                    json_data["tipo_acao"] = tipo_acao
                    json_data["intencao_cena"] = intencao

            # TRAVA ANTI-AVANÇO INVOLUNTÁRIO DE BEAT (Tarefa 2)
            if tipo_acao == "AVANCAR_HISTORIA":
                is_false_advance = False
                if self.story.current_beat <= 1:
                    if not is_explicit_advance or is_dialogue_or_interaction:
                        is_false_advance = True
                elif has_false_advance_kw:
                    is_false_advance = True

                if is_false_advance:
                    tipo_acao = "DIALOGAR" if any(w in p_low for w in ["falar", "convers", "dialog", "pergunt", "propost"]) else "INTERAGIR_CENARIO"
                    intencao = f"Interagir no cenário: {player_input}"
                    json_data["tipo_acao"] = tipo_acao
                    json_data["intencao_cena"] = intencao

            # Tratamento Civil/Social de Zona Segura na Taverna (Beat 1)
            if self.story.current_beat <= 1 and tipo_acao == "ATACAR" and (self.game_mode == "EXPLORACAO" or not self.active_combat_targets):
                self.game_mode = "EXPLORACAO"
                self.active_combat_targets.clear()
                self.active_visual_npcs.clear()
                sys_msg = "[ZONA SEGURA] A Taverna do Dragão Acordado é um refúgio de paz. Conflitos armados são proibidos pelas regras da casa e pela guarda."
                narrative = "Maelor desvia a lâmina com um toque firme de sua acha de lenha e bate no balcão de carvalho com olhar severo: 'Guarde o aço, forasteiro. Aqui bebe-se em paz; sangue derrama-se lá fora.' O bater metálico de alabardas do lado de fora ecoa o aviso silencioso da patrulha local."
                self.ui_queue.put({"type": "system_message", "content": sys_msg})
                self.ui_queue.put({"type": "narrative", "content": narrative, "npc_falando": "Taverneiro"})
                return

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

                raw_target = str(alvos[0]).strip() if alvos else ""
                target_obj = self.find_combat_target(raw_target)
                alvo_principal = None
                if target_obj:
                    for k, v in self.active_combat_targets.items():
                        if v is target_obj:
                            alvo_principal = k
                            break
                    if not alvo_principal:
                        alvo_principal = target_obj.get("name", raw_target or "Inimigo")
                else:
                    alvo_principal = raw_target or "Inimigo"

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
                    
                is_heal_or_support = (
                    spell_data.get("mechanical_action") in ["heal", "buff", "support", "revive"]
                    or spell_data.get("target_type") in ["single_ally", "touch", "self"]
                    or "curar" in spell_data.get("name", "").lower()
                    or "cura" in spell_data.get("name", "").lower()
                )

                if spell_data.get("mechanical_action") == "damage" and self.game_mode == "EXPLORACAO":
                    if self.story.current_beat <= 1 and not [v for v in self.active_combat_targets.values() if v.get("faction") == "enemy" and v.get("pv_atual", 0) > 0]:
                        self.ui_queue.put({"type": "system_message", "content": "[ZONA SEGURA] Magias ofensivas são estritamente proibidas dentro da Taverna!"})
                        self.ui_queue.put({
                            "type": "narrative",
                            "content": "Maelor bate com a caneca pesada no balcão e ergue a mão aberta, dissipando a centelha arcana: 'Guarde a magia, conjurador. Aqui bebe-se em paz; sangue derrama-se lá fora.' Os olhares austeros da guarda advertem contra qualquer motim.",
                            "npc_falando": "Taverneiro"
                        })
                        return
                    self.game_mode = "COMBATE"
                    
                parsed["tipo_acao"] = "magia"
                parsed["recurso_utilizado"] = recurso
                parsed["spell_data"] = spell_data
                parsed["intencao_cena"] = "conjuracao_magia" if is_heal_or_support else "iniciar_combate"
                
                if spell_data.get("target_type") == "aoe":
                    # Define alvo dummy só para passar pelo validador do Phase 1 (já que AoE ignora o loop de alvos mas requer a lista)
                    if not self.active_combat_targets:
                        self.ui_queue.put({"type": "system_message", "content": "[SISTEMA] Não há inimigos na área de efeito."})
                        return
                    parsed["alvo"] = [list(self.active_combat_targets.keys())[0]]
                else:
                    hero_name = pc.get("name", "Herói")
                    raw_target = str(alvos[0]).strip() if (alvos and alvos[0] not in ["", "nenhum", None]) else ""
                    if is_heal_or_support and (not raw_target or raw_target.lower() in ["self", "eu", "heroi", "herói", "proprio", "próprio", "si mesmo", hero_name.lower()]):
                        alvo_principal = hero_name
                    elif is_heal_or_support and not self.active_combat_targets:
                        alvo_principal = hero_name
                    else:
                        target_obj = self.find_combat_target(raw_target)
                        if target_obj:
                            alvo_principal = None
                            for k, v in self.active_combat_targets.items():
                                if v is target_obj:
                                    alvo_principal = k
                                    break
                            if not alvo_principal:
                                alvo_principal = hero_name if target_obj is pc else target_obj.get("name", raw_target or "Inimigo")
                        elif is_heal_or_support:
                            alvo_principal = hero_name
                        elif self.game_mode == "COMBATE":
                            self.ui_queue.put({"type": "system_message", "content": f"[SISTEMA] Alvo '{raw_target}' não encontrado no combate. Ação cancelada."})
                            return
                        else:
                            alvo_principal = hero_name

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
                    self.game_state["last_checkpoint_bg"] = "tavern_bg.jpg"
                    self.save_game()
                    
                    sys_log = f"[SISTEMA] Descanso seguro na Taverna (Dia {self.game_state.get('current_day', 1)}). HP 100%. Suprimentos restaurados. Jogo Salvo."
                    narrative_descanso = ""
                    try:
                        narrative_descanso = self.ai.generate_narrative_from_math(sys_log, "Descanso na taverna com fogo e guisado")
                    except Exception:
                        narrative_descanso = sys_log

                    # Reatividade de Aliados no Hub da Taverna (Item 4.1)
                    rumor = self.get_tavern_allies_rumors()
                    extra_allies_text = ""
                    if rumor:
                        self.ui_queue.put({"type": "system_message", "content": rumor})
                        unlocked = self.story.get_unlocked_allies()
                        nomes = ", ".join([ally.get("name", k) for k, ally in unlocked.items()])
                        extra_allies_text = f"\n\nMaelor observa os rostos na penumbra e assente com solenidade: 'Seus companheiros {nomes} estão atentos nas sombras. Quando a hora chegar, não lutará sozinho.'"

                    combined_narrative = f"{narrative_descanso}{extra_allies_text}" if extra_allies_text else narrative_descanso
                    self.ui_queue.put({"type": "narrative", "content": combined_narrative, "npc_falando": "Mestre"})
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
                        self.game_state["last_checkpoint_bg"] = self.game_state.get("current_background", "tavern_bg.jpg")
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
                        self.discover_monster(tipo_best)
                        
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

                # Reatividade de Aliados e Rumores no Hub da Taverna (Beat 1)
                extra_rumor_text = ""
                if self.story.current_beat <= 1:
                    rumor = self.get_tavern_allies_rumors()
                    if rumor:
                        self.ui_queue.put({"type": "system_message", "content": rumor})
                        unlocked = self.story.get_unlocked_allies()
                        nomes = ", ".join([ally.get("name", k) for k, ally in unlocked.items()])
                        extra_rumor_text = f"\n\nMaelor se inclina sobre o balcão da taverna e sussurra: 'Fique atento. {nomes} estão acampados nas proximidades e prontos para a batalha final.'"

                    # Desbloqueio orgânico de rumores da Taverna no Beat 1 via interação/diálogo/balcão/mural
                    rumor_keywords = ["rumor", "missao", "missão", "trabalho", "mural", "quadro", "lenhador", "balcao", "balcão", "ouvir", "noticia", "notícia", "servico", "serviço"]
                    if any(kw in p_low for kw in rumor_keywords):
                        self.discover_rumor("sq_goblin_clearing")

                env_prompt = self.story.get_environment_prompt()
                falante = "Taverneiro" if self.story.current_beat <= 1 else "Mestre"
                try:
                    narrative = self.ai.generate_narrative_from_math(env_prompt, player_input)
                except Exception as e:
                    narrative = f"[SISTEMA] Falha ao interagir com cenário: {e}"
                if extra_rumor_text:
                    narrative = f"{narrative}{extra_rumor_text}"
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

            elif str(tipo_acao).upper() in ["ESQUIVAR", "DODGE", "ESQUIVA"]:
                parsed["tipo_acao"] = "esquivar"
                parsed["intencao_cena"] = intencao

            elif str(tipo_acao).upper() in ["DESENGAJAR", "DISENGAGE", "RECUAR_SEGURO"]:
                parsed["tipo_acao"] = "desengajar"
                parsed["intencao_cena"] = intencao

            elif str(tipo_acao).upper() in ["MOVER", "MOVIMENTO", "DESLOCAR"]:
                parsed["tipo_acao"] = "movimento"
                parsed["recurso_utilizado"] = json_data.get("recurso_utilizado") or intencao
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
                    
            # FASE 1: Matemática
            from core.combat_system import resolve_action
            alvos_raw = parsed.get("alvo", ["nenhum"])
            if isinstance(alvos_raw, str):
                alvos_raw = [alvos_raw]
                
            target_entities = []
            hero_name = pc.get("name", "Herói")
            for alvo in alvos_raw:
                if alvo != "nenhum":
                    achou_ent = self.find_combat_target(alvo)
                    if achou_ent:
                        target_entities.append(achou_ent)
                    elif self.game_mode == "COMBATE" and self.story.current_beat > 1:
                        # Auto-instanciação de Segurança se nenhum inimigo existia fora de hub
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
                init_order = result.get("initiative_order", [])
                if init_order:
                    self.game_state["initiative_order"] = init_order
                    self.ui_queue.put({"type": "initiative_order", "order": init_order})
                
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
                elif parsed.get("tipo_acao") in ["teste_pericia", "uso_item", "habilidade", "magia", "esquivar", "desengajar"]:
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
                    sys_log = f"🎲 [DADO - TESTE] Percepção: {tot} vs CD {cd} ➔ {res_str}!"
                elif any(w in (intencao or "").lower() for w in ["convers", "fal", "dialog", "pergunt", "propost"]):
                    from core.dice_engine import DiceEngine
                    from core.dnd_rules import get_modifier
                    dado = DiceEngine.roll_d20()
                    mod = get_modifier(pc.get("attributes", {}).get("CHA", 10))
                    tot = dado + mod + 2
                    cd = 11
                    res_str = "SUCESSO" if tot >= cd else "FALHA"
                    sys_log = f"🎲 [DADO - TESTE] Persuasão: {tot} vs CD {cd} ➔ {res_str}!"
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
                return
            else:
                enemies_left = [t for t in self.active_combat_targets.values() if t.get("faction", "enemy") == "enemy" and t.get("status") != "morto" and t.get("pv_atual", 0) > 0]
                if len(enemies_left) == 0 and self.game_mode == "COMBATE":
                    self.check_combat_resolution()
                    return
            # Enviar para UI (após o turno completo): UMA ÚNICA mensagem narrativa estruturada por turno
            self.ui_queue.put({"type": "narrative", "content": player_bubble, "npc_falando": "Mestre"})
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.ui_queue.put({"type": "system_message", "content": f"[ERRO INTERNO] {str(e)}"})
        finally:
            self.is_ai_thinking = False

# Alias de interoperabilidade
GameEngine = SessionManager


# Alias de interoperabilidade
GameEngine = SessionManager
