from typing import Dict, Any, Tuple, Optional, List
import copy
import unicodedata

def _normalize(text: str) -> str:
    """Normaliza texto para comparações sem acento e em caixa baixa."""
    if not text:
        return ""
    nfkd = unicodedata.normalize('NFKD', str(text))
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).strip().lower()

class StoryManager:
    """
    Motor Narrativo Sistêmico (Model Layer).
    Gerencia a progressão da história por Beats, recrutamento adaptativo de aliados
    e snapshots mecânicos para combate e Déjà Vu.
    """
    def __init__(self) -> None:
        self.current_beat: int = 1
        
        import json
        import os
        self.campaign_data = {}
        try:
            with open("data/campaign.json", "r", encoding="utf-8") as f:
                self.campaign_data = json.load(f)
        except Exception as e:
            print(f"[StoryEngine] Erro ao carregar campaign.json: {e}")

        # Cache de Side Quests e Heroes Lore com fallback resiliente
        self.side_quests_data: Dict[str, Any] = {}
        try:
            with open("data/side_quests.json", "r", encoding="utf-8") as f:
                self.side_quests_data = json.load(f)
        except Exception as e:
            self.side_quests_data = {}

        self.heroes_lore_data: Dict[str, Any] = {}
        try:
            with open("data/heroes_lore.json", "r", encoding="utf-8") as f:
                self.heroes_lore_data = json.load(f)
        except Exception as e:
            self.heroes_lore_data = {}

        # Pool Completo de Aliados D&D 5e carregado dinamicamente de heroes_lore.json (HERO-01 a HERO-42)
        # Mais aliases legados para 100% de retrocompatibilidade com testes e saves anteriores
        self.allies_pool: Dict[str, Dict[str, Any]] = {}
        for h_id, h_data in self.heroes_lore_data.items():
            if isinstance(h_data, dict):
                self.allies_pool[h_id] = copy.deepcopy(h_data)

        # Aliases legados retrocompatíveis com testes e campanhas
        legacy_allies = {
            "fighter": {
                "id": "fighter",
                "canonical_id": "HERO-31",
                "name": "Thorgar, o Implacável",
                "race": "Meio-Orc",
                "class": "Guerreiro",
                "pv_atual": 28,
                "pv_max": 28,
                "hp_current": 28,
                "hp_max": 28,
                "ca": 17,
                "ac": 17,
                "hit_dice": "1d10",
                "speed": "9m",
                "tipo_bestiario": "guerreiro",
                "attributes": {"STR": 16, "DEX": 13, "CON": 16, "INT": 8, "WIS": 12, "CHA": 10, "LUCK": 10},
                "actions": [
                    {"name": "Machado de Batalha", "hit_bonus": 5, "damage_dice": "1d8+3"}
                ],
                "abilities": ["Ataque Poderoso", "Resistência Implacável"],
                "faction": "ally",
                "sprite_key": "Thorgar Quebrador-de-Ossos",
                "portrait_key": "Thorgar Quebrador-de-Ossos",
                "level": 1,
                "proficiency_bonus": 2
            },
            "cleric": {
                "id": "cleric",
                "canonical_id": "HERO-08",
                "name": "Karg, o Devoto",
                "race": "Anão da Colina",
                "class": "Clérigo",
                "pv_atual": 24,
                "pv_max": 24,
                "hp_current": 24,
                "hp_max": 24,
                "ca": 18,
                "ac": 18,
                "hit_dice": "1d8",
                "speed": "7.5m",
                "tipo_bestiario": "clerigo",
                "attributes": {"STR": 14, "DEX": 10, "CON": 16, "INT": 8, "WIS": 16, "CHA": 12, "LUCK": 10},
                "actions": [
                    {"name": "Maça Sagrada", "hit_bonus": 4, "damage_dice": "1d6+2"},
                    {"name": "Chama Sagrada", "hit_bonus": 5, "damage_dice": "1d8"}
                ],
                "abilities": ["Cura Divina", "Resiliência Anã"],
                "spell_slots": {"1": 2},
                "faction": "ally",
                "sprite_key": "Kargan Forja-Divina",
                "portrait_key": "Kargan Forja-Divina",
                "level": 1,
                "proficiency_bonus": 2
            },
            "paladin": {
                "id": "paladin",
                "canonical_id": "HERO-15",
                "name": "Balthazar, Escama-Dourada",
                "race": "Draconato",
                "class": "Paladino",
                "pv_atual": 26,
                "pv_max": 26,
                "hp_current": 26,
                "hp_max": 26,
                "ca": 16,
                "ac": 16,
                "hit_dice": "1d10",
                "speed": "9m",
                "tipo_bestiario": "paladino",
                "attributes": {"STR": 16, "DEX": 10, "CON": 14, "INT": 8, "WIS": 12, "CHA": 15, "LUCK": 10},
                "actions": [
                    {"name": "Espada Longa Justa", "hit_bonus": 5, "damage_dice": "1d8+3"},
                    {"name": "Sopro de Fogo", "hit_bonus": 5, "damage_dice": "2d6"}
                ],
                "abilities": ["Destruição Divina", "Resistência Dracônica"],
                "spell_slots": {"1": 2},
                "faction": "ally",
                "sprite_key": "Balthazar Escama-Dourada",
                "portrait_key": "Balthazar Escama-Dourada",
                "level": 1,
                "proficiency_bonus": 2
            },
            "mage": {
                "id": "mage",
                "canonical_id": "HERO-40",
                "name": "Azaroth, o Arcanista",
                "race": "Tiefling",
                "class": "Mago",
                "pv_atual": 18,
                "pv_max": 18,
                "hp_current": 18,
                "hp_max": 18,
                "ca": 13,
                "ac": 13,
                "hit_dice": "1d6",
                "speed": "9m",
                "tipo_bestiario": "mago",
                "attributes": {"STR": 8, "DEX": 14, "CON": 14, "INT": 16, "WIS": 12, "CHA": 12, "LUCK": 10},
                "actions": [
                    {"name": "Raio de Fogo", "hit_bonus": 5, "damage_dice": "1d10"},
                    {"name": "Mísseis Mágicos", "hit_bonus": 99, "damage_dice": "3d4+3"}
                ],
                "abilities": ["Conjuração Arcana", "Resistência Infernal"],
                "spell_slots": {"1": 2},
                "faction": "ally",
                "sprite_key": "Azaroth o Necro-Arcanista",
                "portrait_key": "Azaroth o Necro-Arcanista",
                "level": 1,
                "proficiency_bonus": 2
            },
            "ranger": {
                "id": "ranger",
                "canonical_id": "HERO-23",
                "name": "Sylas, o Rastreador",
                "race": "Elfo da Floresta",
                "class": "Patrulheiro",
                "pv_atual": 22,
                "pv_max": 22,
                "hp_current": 22,
                "hp_max": 22,
                "ca": 15,
                "ac": 15,
                "hit_dice": "1d10",
                "speed": "10.5m",
                "tipo_bestiario": "patrulheiro",
                "attributes": {"STR": 12, "DEX": 16, "CON": 13, "INT": 10, "WIS": 15, "CHA": 8, "LUCK": 10},
                "actions": [
                    {"name": "Arco Longo Élfico", "hit_bonus": 6, "damage_dice": "1d8+3"}
                ],
                "abilities": ["Inimigo Favorito", "Passo Leve"],
                "spell_slots": {"1": 2},
                "faction": "ally",
                "sprite_key": "Sylas Rastreadora-da-Lua",
                "portrait_key": "Sylas Rastreadora-da-Lua",
                "level": 1,
                "proficiency_bonus": 2
            },
            "rogue": {
                "id": "rogue",
                "canonical_id": "HERO-30",
                "name": "Finn, Pés-Leves",
                "race": "Halfling",
                "class": "Ladino",
                "pv_atual": 20,
                "pv_max": 20,
                "hp_current": 20,
                "hp_max": 20,
                "ca": 15,
                "ac": 15,
                "hit_dice": "1d8",
                "speed": "7.5m",
                "tipo_bestiario": "ladino",
                "attributes": {"STR": 8, "DEX": 16, "CON": 14, "INT": 13, "WIS": 10, "CHA": 13, "LUCK": 12},
                "actions": [
                    {"name": "Ataque Furtivo com Rapieira", "hit_bonus": 6, "damage_dice": "1d8+1d6+4"}
                ],
                "abilities": ["Ataque Furtivo", "Sorte de Halfling"],
                "faction": "ally",
                "sprite_key": "Finn Pés-Leves",
                "portrait_key": "Finn Pés-Leves",
                "level": 1,
                "proficiency_bonus": 2
            },
            "guardian_human": {
                "id": "guardian_human",
                "canonical_id": "HERO-01",
                "name": "Valeria, a Protetora",
                "race": "Humano",
                "class": "Guerreiro",
                "pv_atual": 26,
                "pv_max": 26,
                "hp_current": 26,
                "hp_max": 26,
                "ca": 16,
                "ac": 16,
                "hit_dice": "1d10",
                "speed": "9m",
                "tipo_bestiario": "guerreiro",
                "attributes": {"STR": 16, "DEX": 13, "CON": 15, "INT": 9, "WIS": 13, "CHA": 11, "LUCK": 10},
                "actions": [
                    {"name": "Lança e Escudo", "hit_bonus": 5, "damage_dice": "1d8+3"}
                ],
                "abilities": ["Retomar o Fôlego", "Vontade Indomável"],
                "faction": "ally",
                "sprite_key": "Sir Alistair Valerius",
                "portrait_key": "Sir Alistair Valerius",
                "level": 1,
                "proficiency_bonus": 2
            }
        }
        for k, v in legacy_allies.items():
            self.allies_pool[k] = copy.deepcopy(v)

        # Alias extra para wizard
        if "mage" in self.allies_pool:
            wiz = copy.deepcopy(self.allies_pool["mage"])
            wiz["id"] = "wizard"
            self.allies_pool["wizard"] = wiz

        # Inicializa flags dinâmicas para todos os aliados (42 heróis + legados)
        self.flags: Dict[str, bool] = {
            "final_boss_retried": False
        }
        for ally_id in self.allies_pool:
            self.flags[f"ally_{ally_id}_unlocked"] = False
        self.flags["ally_warlock_unlocked"] = False

        self.campaign_log: Dict[int, str] = {}
        for beat_str, data in self.campaign_data.items():
            if beat_str.isdigit():
                beat_int = int(beat_str)
                self.campaign_log[beat_int] = f"{data.get('name', 'Beat')} - {data.get('type', 'Narrative')}"
        if 0 not in self.campaign_log:
            self.campaign_log[0] = "Prólogo: Origem do herói."
        self.snapshot: Optional[Dict[str, Any]] = None

    def get_available_side_quests(self, act: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retorna lista de side quests disponíveis, filtradas opcionalmente pelo Ato."""
        quests_list: List[Dict[str, Any]] = []
        raw_list: List[Dict[str, Any]] = []

        if isinstance(self.side_quests_data, dict):
            if "quests" in self.side_quests_data and isinstance(self.side_quests_data["quests"], list):
                raw_list = self.side_quests_data["quests"]
            elif "side_quests" in self.side_quests_data and isinstance(self.side_quests_data["side_quests"], list):
                raw_list = self.side_quests_data["side_quests"]
            else:
                for q_id, q_val in self.side_quests_data.items():
                    if isinstance(q_val, dict):
                        item = copy.deepcopy(q_val)
                        if "id" not in item:
                            item["id"] = q_id
                        raw_list.append(item)
        elif isinstance(self.side_quests_data, list):
            raw_list = self.side_quests_data

        for q in raw_list:
            if not isinstance(q, dict):
                continue
            q_copy = copy.deepcopy(q)
            if act is None:
                quests_list.append(q_copy)
            else:
                q_act = q_copy.get("act")
                if q_act is not None and int(q_act) == int(act):
                    quests_list.append(q_copy)

        return quests_list

    def get_side_quest(self, quest_id: str) -> Optional[Dict[str, Any]]:
        """Retorna os dados de uma side quest específica por ID."""
        if not quest_id:
            return None
        all_quests = self.get_available_side_quests()
        for q in all_quests:
            if q.get("id") == quest_id:
                return copy.deepcopy(q)
        return None

    def get_hero_lore(self, hero_id: str) -> Optional[Dict[str, Any]]:
        """Busca a lore completa do herói por ID, nome ou classe."""
        if not hero_id or not self.heroes_lore_data:
            return None
        norm_query = _normalize(hero_id)
        if hero_id in self.heroes_lore_data:
            return copy.deepcopy(self.heroes_lore_data[hero_id])

        class_mapping = {
            "fighter": "guerreiro",
            "cleric": "clerigo",
            "paladin": "paladino",
            "wizard": "mago",
            "mage": "mago",
            "ranger": "patrulheiro",
            "rogue": "ladino"
        }
        target_class_norm = class_mapping.get(norm_query, norm_query)

        for k, v in self.heroes_lore_data.items():
            if _normalize(k) == norm_query:
                return copy.deepcopy(v)
            if isinstance(v, dict):
                if _normalize(v.get("id", "")) == norm_query:
                    return copy.deepcopy(v)
                v_name = _normalize(v.get("name", ""))
                if v_name == norm_query or norm_query in v_name:
                    return copy.deepcopy(v)
                v_class = _normalize(v.get("class", ""))
                if v_class == target_class_norm:
                    return copy.deepcopy(v)
        return None

    def get_all_heroes_lore(self) -> Dict[str, Dict[str, Any]]:
        """Retorna todo o compêndio de lore dos heróis."""
        return copy.deepcopy(self.heroes_lore_data)

    def inject_prologue_data(self, race: str, char_class: str, background: str) -> None:
        """Injeta os Fatos Crus no Beat 0 (Prólogo)."""
        self.campaign_log[0] = f"Prólogo: Herói {race} {char_class} com passado de {background}."
        print("[StoryEngine] Beat 0 (Prólogo) injetado dinamicamente com fatos crus.")

    def get_current_beat_lore(self) -> str:
        """Retorna os dados crus do beat atual (Layer 3)."""
        return self.campaign_log.get(self.current_beat, "Desconhecido")
        
    def get_environment_prompt(self) -> str:
        beat_str = str(self.current_beat)
        if beat_str in self.campaign_data:
            return self.campaign_data[beat_str].get("environment_prompt", "")
        return ""

    def is_climax(self) -> bool:
        """Verifica se o beat atual é estritamente o Clímax (Beat 15) e possui a flag 'is_climax' no JSON."""
        try:
            if int(self.current_beat) != 15:
                return False
        except (ValueError, TypeError):
            return False
        beat_str = str(self.current_beat)
        if beat_str in self.campaign_data:
            return bool(self.campaign_data[beat_str].get("is_climax", False))
        return False

    def advance_beat(self) -> None:
        max_beat = max(self.campaign_log.keys())
        if self.current_beat < max_beat:
            self.current_beat += 1
            print(f"[StoryEngine] Avançando para Beat {self.current_beat}: {self.campaign_log[self.current_beat]}")

    def set_beat(self, beat_id: int) -> None:
        if beat_id in self.campaign_log:
            self.current_beat = beat_id
            print(f"[StoryEngine] Beat alterado para {self.current_beat}: {self.campaign_log[self.current_beat]}")

    def unlock_ally(self, ally_id: str) -> bool:
        """Libera um membro do allies_pool garantindo registro da flag."""
        if not ally_id:
            return False
            
        target_id = ally_id
        if target_id == "wizard" and "wizard" not in self.allies_pool and "mage" in self.allies_pool:
            target_id = "mage"
            
        if target_id not in self.allies_pool:
            clean_q = target_id.lower().replace("_", "-")
            for k in self.allies_pool.keys():
                if k.lower() == clean_q or k.lower() == target_id.lower():
                    target_id = k
                    break

        flag_name = f"ally_{target_id}_unlocked"
        if target_id in self.allies_pool:
            self.flags[flag_name] = True
            ally_data = self.allies_pool[target_id]
            print(f"[StoryEngine] Aliado desbloqueado no Grupo: {ally_data['name']} ({ally_data['race']} {ally_data['class']})")
            return True
        elif ally_id in ["warlock"]:
            self.flags[f"ally_{ally_id}_unlocked"] = True
            return True
            
        # Busca por nome caso seja passado o nome em vez do ID
        norm_query = _normalize(ally_id)
        for k, v in self.allies_pool.items():
            if _normalize(v.get("name", "")) == norm_query:
                self.flags[f"ally_{k}_unlocked"] = True
                print(f"[StoryEngine] Aliado desbloqueado no Grupo por nome: {v['name']} ({v['race']} {v['class']})")
                return True
        return False

    def get_unlocked_allies(self) -> Dict[str, Dict[str, Any]]:
        """Retorna as fichas mecânicas prontas de todos os aliados liberados."""
        unlocked = {}
        for ally_id, ally_data in self.allies_pool.items():
            if self.flags.get(f"ally_{ally_id}_unlocked"):
                unlocked[ally_id] = copy.deepcopy(ally_data)
        return unlocked

    def get_available_allies_for_player(self, player_character: Dict[str, Any]) -> List[str]:
        """
        Filtra os aliados disponíveis no pool para que não repitam a classe do jogador
        e nem classes de aliados já recrutados.
        Itera sobre o pool canônico dos 42 heróis (HERO-01..HERO-42).
        """
        if not player_character:
            player_character = {}
            
        p_class_norm = _normalize(player_character.get("class", ""))
        
        # Classes já presentes na party (jogador + aliados já desbloqueados)
        classes_na_party = set()
        if p_class_norm:
            classes_na_party.add(p_class_norm)
            
        for ally_id, ally_data in self.allies_pool.items():
            if self.flags.get(f"ally_{ally_id}_unlocked"):
                classes_na_party.add(_normalize(ally_data.get("class", "")))
                
        # Itera sobre o pool canônico de heróis (HERO-01 a HERO-42)
        candidatos = []
        canonical_ids = [k for k in self.allies_pool.keys() if k.startswith("HERO-")]
        if not canonical_ids:
            canonical_ids = list(self.allies_pool.keys())

        for ally_id in canonical_ids:
            if not self.flags.get(f"ally_{ally_id}_unlocked"):
                a_class_norm = _normalize(self.allies_pool[ally_id].get("class", ""))
                if a_class_norm not in classes_na_party:
                    candidatos.append(ally_id)
        return candidatos

    def recruit_next_ally(self, player_character: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Seleciona adaptativamente o próximo aliado do pool, respeitando diversidade
        completa de classes e evitando repetição da classe e raça do jogador.
        """
        if not player_character or not isinstance(player_character, dict):
            player_character = {}
            
        candidatos = self.get_available_allies_for_player(player_character)
        if not candidatos:
            return None
            
        p_race_norm = _normalize(player_character.get("race", ""))
        
        # Raças já presentes na party
        racas_na_party = set()
        if p_race_norm:
            racas_na_party.add(p_race_norm)
        for ally_id, ally_data in self.allies_pool.items():
            if self.flags.get(f"ally_{ally_id}_unlocked"):
                racas_na_party.add(_normalize(ally_data.get("race", "")))
                
        # Prioriza candidato com raça ainda não representada na party
        candidato_escolhido = None
        for ally_id in candidatos:
            a_race = _normalize(self.allies_pool[ally_id].get("race", ""))
            if a_race not in racas_na_party:
                candidato_escolhido = ally_id
                break
                
        if not candidato_escolhido:
            candidato_escolhido = candidatos[0]
            
        self.unlock_ally(candidato_escolhido)
        return copy.deepcopy(self.allies_pool[candidato_escolhido])

    def recruit_ally_for_beat(self, beat_id: int, player_character: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Executa recrutamento se o beat tiver permissão ('recruitable_allies' == True).
        """
        beat_str = str(beat_id)
        beat_data = self.campaign_data.get(beat_str, {})
        if beat_data.get("recruitable_allies", False):
            # Limita a 1 recrutamento por beat através de flag
            flag_beat_recrutado = f"beat_{beat_id}_ally_recruited"
            if not self.flags.get(flag_beat_recrutado, False):
                novo_aliado = self.recruit_next_ally(player_character)
                if novo_aliado:
                    self.flags[flag_beat_recrutado] = True
                    return novo_aliado
        return None

    def create_snapshot(self, player_character: Dict[str, Any], combat_targets: Dict[str, Any], visual_npcs: Dict[str, str], extra_state: Optional[Dict[str, Any]] = None) -> None:
        """Salva o estado mecânico exato do jogador, aliados e contexto (Déjà Vu)."""
        self.snapshot = {
            "player_character": copy.deepcopy(player_character),
            "combat_targets": copy.deepcopy(combat_targets),
            "visual_npcs": copy.deepcopy(visual_npcs),
            "extra_state": copy.deepcopy(extra_state) if extra_state else {}
        }
        print("[StoryEngine] Snapshot (Déjà Vu) criado com sucesso.")

    def load_snapshot(self) -> Optional[Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]]:
        """Recupera o estado matematicamente intacto (HP, magias, itens, aliados)."""
        if self.snapshot:
            print("[StoryEngine] Carregando Snapshot (Déjà Vu) - Restaurando status matemático...")
            return (
                copy.deepcopy(self.snapshot["player_character"]),
                copy.deepcopy(self.snapshot["combat_targets"]),
                copy.deepcopy(self.snapshot["visual_npcs"])
            )
        return None

    def get_snapshot_extra(self) -> Dict[str, Any]:
        """Retorna o estado extra salvo no snapshot (ex: inventário global)."""
        if self.snapshot and "extra_state" in self.snapshot:
            return copy.deepcopy(self.snapshot["extra_state"])
        return {}

    def get_current_act(self) -> int:
        """Retorna o número do Ato atual (1 a 3) baseado no Beat."""
        if self.current_beat <= 5:
            return 1
        elif self.current_beat <= 10:
            return 2
        else:
            return 3

    def get_available_quests_for_current_act(self) -> List[Dict[str, Any]]:
        """Retorna as side quests disponíveis para o Ato atual do herói."""
        act = self.get_current_act()
        return self.get_available_side_quests(act=act)

    def spawn_enemies_from_list(self, enemies_to_spawn: List[str], active_combat_targets: Dict[str, Any], active_visual_npcs: Dict[str, str]) -> None:
        """Instancia e popula alvos de combate e sprites a partir de uma lista de IDs de inimigos."""
        import json
        import copy

        bestiary = {}
        try:
            with open("data/bestiary.json", "r", encoding="utf-8") as f:
                bestiary = json.load(f)
        except Exception as e:
            print(f"[StoryEngine] Erro ao carregar bestiary.json: {e}")

        monster_counts: Dict[str, int] = {}
        for enemy_id in enemies_to_spawn:
            monster_data = bestiary.get(enemy_id)

            # Failsafe
            if not monster_data:
                print(f"[StoryEngine] Aviso: Monstro '{enemy_id}' não encontrado no bestiário. Usando fallback.")
                monster_data = {
                    "name": "Erro/Missing",
                    "hp": 1,
                    "ac": 10,
                    "speed": 30,
                    "attributes": {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10},
                    "actions": [{"name": "Struggle", "hit_bonus": 0, "damage_dice": "1d4"}]
                }

            monster_instance = copy.deepcopy(monster_data)
            base_name = monster_instance.get("name", "Criatura")
            monster_counts[base_name] = monster_counts.get(base_name, 0) + 1
            while f"{base_name} {monster_counts[base_name]}" in active_combat_targets:
                monster_counts[base_name] += 1
            narrative_id = f"{base_name} {monster_counts[base_name]}"

            active_combat_targets[narrative_id] = {
                "name": narrative_id,
                "pv_atual": monster_instance.get("hp", 10),
                "pv_max": monster_instance.get("hp", 10),
                "ca": monster_instance.get("ac", 10),
                "tipo_bestiario": enemy_id,
                "faction": "enemy",
                "actions": monster_instance.get("actions", [])
            }
            visual_sprite = enemy_id.replace("m_", "") if enemy_id.startswith("m_") else enemy_id
            active_visual_npcs[narrative_id] = visual_sprite

    def spawn_enemies_for_current_beat(self, active_combat_targets: Dict[str, Any], active_visual_npcs: Dict[str, str]) -> None:
        beat_str = str(self.current_beat)
        beat_data = self.campaign_data.get(beat_str, {})
        enemies_to_spawn = beat_data.get("enemies", [])
        self.spawn_enemies_from_list(enemies_to_spawn, active_combat_targets, active_visual_npcs)
        print(f"[StoryEngine] Inimigos spawnados para o Beat {self.current_beat}: {enemies_to_spawn}")

    def spawn_enemies_for_side_quest(self, quest_id: str, active_combat_targets: Dict[str, Any], active_visual_npcs: Dict[str, str]) -> None:
        quest = self.get_side_quest(quest_id)
        if not quest:
            print(f"[StoryEngine] Side quest '{quest_id}' não encontrada para spawn de inimigos.")
            return
        enemies_to_spawn = quest.get("enemies", [])
        self.spawn_enemies_from_list(enemies_to_spawn, active_combat_targets, active_visual_npcs)
        print(f"[StoryEngine] Inimigos spawnados para a Side Quest '{quest_id}': {enemies_to_spawn}")
