import unittest
import json
import os
import queue
from core.game_engine import SessionManager
from core.dnd_rules import CharacterCalculator


class DummyAI:
    def __init__(self):
        self.last_prompt = ""

    def parse_player_intent(self, text, state):
        t_low = text.lower().strip()
        if any(w in t_low for w in ["sair", "estrada", "partir", "porta"]):
            return {"tipo_acao": "AVANCAR_HISTORIA", "intencao_cena": "avancar", "alvo": []}
        if "atacar" in t_low or "ataco" in t_low or "golpe" in t_low:
            return {"tipo_acao": "ATACAR", "intencao_cena": "atacar", "alvo": ["Taverneiro"]}
        if "curar" in t_low or "cura" in t_low:
            return {"tipo_acao": "CONJURAR_MAGIA", "recurso_utilizado": "Curar Ferimentos", "alvo": [], "intencao_cena": "curar"}
        return {"tipo_acao": "INTERAGIR_CENARIO", "intencao_cena": "explorar", "alvo": []}

    def generate_narrative_from_math(self, sys_log, intent=""):
        return f"Narrativa de teste: {intent}"


class TestDndBackendImprovements(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI()
        self.session = SessionManager(self.ai)
        self.pc = {
            "name": "Valerius",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "hp_current": 10,
            "hp_max": 12,
            "xp": 0,
            "gold": 15,
            "attributes": {"FOR": 15, "CON": 14, "DES": 13, "SAB": 12, "CAR": 10, "INT": 8},
            "inventory": {"i_potion_healing": 1},
            "unlocked_skills": ["second_wind", "sk_warrior_1"],
            "abilities": ["Estilo de Luta", "Retomar o Fôlego"]
        }
        self.session.game_state["player_character"] = self.pc
        self.session.game_state["story_beat"] = 1
        self.session.story.current_beat = 1
        self.session.game_mode = "EXPLORACAO"
        self.session.active_combat_targets = {}
        self.session.active_visual_npcs = {}

    def test_01_leave_tavern_natural_commands_advances_to_beat_2(self):
        """Valida que comandos naturais e em 1ª pessoa destravam a saída da taverna para Beat 2."""
        natural_commands = [
            "sair", "saio", "saio da taverna", "deixar a taverna",
            "abro a porta", "abrir a porta", "vou para a estrada",
            "pegar a estrada", "seguir viagem", "partir", "ir embora"
        ]
        for cmd in natural_commands:
            # Reseta para Beat 1
            self.session.story.current_beat = 1
            self.session.game_state["story_beat"] = 1
            self.session.game_mode = "EXPLORACAO"
            self.session.active_combat_targets.clear()
            self.session.active_visual_npcs.clear()

            self.session._async_turn_processor(cmd, [], [])

            self.assertEqual(self.session.story.current_beat, 2, f"Falha ao avançar para Beat 2 com comando: '{cmd}'")
            self.assertEqual(self.session.game_state["story_beat"], 2)
            self.assertEqual(self.session.game_mode, "COMBATE")

            # Verifica evento de beat_transition na fila da UI
            events = []
            while not self.session.ui_queue.empty():
                events.append(self.session.ui_queue.get_nowait())

            beat_trans = next((e for e in events if e.get("type") == "beat_transition"), None)
            self.assertIsNotNone(beat_trans, f"beat_transition ausente para comando '{cmd}'")
            self.assertEqual(beat_trans["beat"], 2)
            self.assertEqual(beat_trans["name"], "Planície dos Uivos")

    def test_02_tavern_internal_actions_do_not_advance_beat(self):
        """Valida que comandos internos como 'sair da mesa' não causam avanço involuntário de beat."""
        false_commands = ["sair da mesa", "sair da cadeira", "levantar", "ir ao balcão"]
        for cmd in false_commands:
            self.session.story.current_beat = 1
            self.session.game_state["story_beat"] = 1
            self.session.game_mode = "EXPLORACAO"

            self.session._async_turn_processor(cmd, [], [])

            self.assertEqual(self.session.story.current_beat, 1, f"Beat avançou indevidamente com: '{cmd}'")
            self.assertEqual(self.session.game_mode, "EXPLORACAO")

    def test_03_tavern_safe_zone_prevents_civilian_attack_and_no_goblin_spawn(self):
        """Valida que atacar NPC na taverna não gera goblin nem entra em combate bugado."""
        self.session.story.current_beat = 1
        self.session.game_state["story_beat"] = 1
        self.session.game_mode = "EXPLORACAO"
        self.session.active_combat_targets.clear()

        self.session._async_turn_processor("atacar taverneiro", [], [])

        # Modo permanece EXPLORACAO
        self.assertEqual(self.session.game_mode, "EXPLORACAO")
        # Nenhum goblin instanciado
        self.assertEqual(len(self.session.active_combat_targets), 0)

        events = []
        while not self.session.ui_queue.empty():
            events.append(self.session.ui_queue.get_nowait())

        narrative_evt = next((e for e in events if e.get("type") == "narrative"), None)
        self.assertIsNotNone(narrative_evt)
        self.assertIn("Guarde o aço", narrative_evt["content"])
        self.assertEqual(narrative_evt["npc_falando"], "Taverneiro")

    def test_04_cure_wounds_spell_and_auto_target_healing_out_of_combat(self):
        """Valida conjuração de Curar Ferimentos fora de combate com auto-alvo no herói."""
        # Configura clérigo ferido
        self.pc["class"] = "Clérigo"
        self.pc["hp_current"] = 5
        self.pc["hp_max"] = 15
        self.pc["spell_slots"] = {"1": 2}
        self.session.game_mode = "EXPLORACAO"
        self.session.active_combat_targets.clear()

        # Conjuração via comando do Grimório sem alvo especificado
        self.session._async_turn_processor("cast_spell:cure_wounds", [], [])

        # Deve ter curado o próprio herói e descontado o slot
        self.assertGreater(self.pc["hp_current"], 5)
        self.assertEqual(self.pc["spell_slots"]["1"], 1)
        self.assertEqual(self.session.game_mode, "EXPLORACAO")

        # Verifica presença de cure_wounds no spells.json
        with open("data/spells.json", "r", encoding="utf-8") as f:
            spells = json.load(f)
        evoc = spells.get("evocation", {})
        self.assertIn("cure_wounds", evoc)
        self.assertEqual(evoc["cure_wounds"]["mechanical_action"], "heal")
        self.assertEqual(evoc["cure_wounds"]["target_type"], "single_ally")

    def test_05_calculate_derived_stats_initializes_level_1_skills_for_all_classes(self):
        """Valida que CharacterCalculator inicializa unlocked_skills no Nível 1 para as 6 classes."""
        expected_class_skills = {
            "Guerreiro": ["second_wind", "sk_warrior_1"],
            "Clérigo": ["disciple_of_life", "sk_cleric_1"],
            "Paladino": ["lay_on_hands", "sk_paladin_1"],
            "Mago": ["arcane_recovery", "sk_mage_1"],
            "Patrulheiro": ["favored_enemy", "sk_ranger_1"],
            "Ladino": ["sneak_attack", "sk_rogue_1"]
        }

        for class_name, skills in expected_class_skills.items():
            res = CharacterCalculator.calculate_derived_stats({}, "Humano", class_name)
            self.assertIn("unlocked_skills", res, f"unlocked_skills ausente em {class_name}")
            for sk in skills:
                self.assertIn(sk, res["unlocked_skills"], f"Skill {sk} ausente para {class_name} nv 1")

    def test_06_travel_quest_commands_support(self):
        """Valida que comandos de viagem para missões secundárias funcionam com múltiplos prefixos."""
        prefixes = ["travel_side_quest:", "travel_quest:", "btn_travel_quest:"]
        for p in prefixes:
            self.session.story.current_beat = 1
            self.session.game_state["story_beat"] = 1
            self.session.game_mode = "EXPLORACAO"
            self.session.game_state["active_side_quest"] = None

            self.session._async_turn_processor(f"{p}sq_goblin_clearing", [], [])

            self.assertEqual(self.session.game_state.get("active_side_quest"), "sq_goblin_clearing")
            self.assertEqual(self.session.game_mode, "COMBATE")
            # Conclui ou reseta a side quest
            self.session.return_from_side_quest(victory=False)

    def test_07_tactical_dodge_action_imposes_disadvantage(self):
        """Valida que a ação Esquivar (Dodge) ativa o estado tático e impõe desvantagem nos ataques inimigos."""
        from core.combat_system import resolve_action, process_enemies_turn_batch
        
        # 1. Jogador usa ação de Esquivar
        res = resolve_action({"tipo_acao": "ESQUIVAR"}, self.pc, [], {})
        self.assertTrue(self.pc.get("_tactical_dodge_active"))
        self.assertIn("ESQUIVAR (DODGE)", res["sys_log"])

        # 2. Inimigo ataca jogador com Dodge ativo
        active_targets = {
            "Goblin 1": {
                "name": "Goblin 1",
                "faction": "enemy",
                "pv_atual": 10,
                "pv_max": 10,
                "ca": 13,
                "actions": [{"name": "Cimitarra", "hit_bonus": 4, "damage_dice": "1d6+2"}]
            }
        }
        batch_log = process_enemies_turn_batch(active_targets, self.pc)
        self.assertIn("DESVANTAGEM", batch_log)
        # O estado deve ser consumido/limpo ao final da rodada de reações
        self.assertFalse(self.pc.get("_tactical_dodge_active"))

    def test_08_tactical_disengage_action(self):
        """Valida que a ação Desengajar (Disengage) ativa postura tática segura sem provocar ataques de oportunidade."""
        from core.combat_system import resolve_action
        
        res = resolve_action({"tipo_acao": "DESENGAJAR"}, self.pc, [], {})
        self.assertTrue(self.pc.get("_tactical_disengage_active"))
        self.assertEqual(self.pc.get("tactical_stance"), "distancia")
        self.assertIn("DESENGAJAR (DISENGAGE)", res["sys_log"])

    def test_09_explicit_initiative_order(self):
        """Valida que a ordem de iniciativa explícita é calculada e retornada no combate."""
        from core.combat_system import resolve_action, CombatManager
        
        targets = {
            "Lobo Terrível a1b2": {
                "name": "Lobo Terrível a1b2",
                "faction": "enemy",
                "pv_atual": 37,
                "pv_max": 37,
                "ca": 13,
                "attributes": {"DES": 15}
            },
            "Bandido c3d4": {
                "name": "Bandido c3d4",
                "faction": "enemy",
                "pv_atual": 11,
                "pv_max": 11,
                "ca": 12,
                "attributes": {"DES": 12}
            }
        }
        
        res = resolve_action({"tipo_acao": "ataque"}, self.pc, [targets["Bandido c3d4"]], targets)
        self.assertIn("initiative_order", res)
        init_order = res["initiative_order"]
        self.assertIsInstance(init_order, list)
        self.assertEqual(len(init_order), 3) # Player + 2 monstros
        
        # Valida que está ordenado decrescente por iniciativa
        inits = [item["init"] for item in init_order]
        self.assertEqual(inits, sorted(inits, reverse=True))

        # Testa também a fachada CombatManager.roll_initiative_order
        facade_order = CombatManager.roll_initiative_order(self.pc, targets)
        self.assertEqual(len(facade_order), 3)
        self.assertTrue(all("name" in item and "init" in item for item in facade_order))

    def test_10_target_selection_by_id_index_and_suffix(self):
        """Valida a resolução de seleção de alvos específicos por ID, índice numérico e sufixo."""
        self.session.active_combat_targets = {
            "Lobo Terrível a1b2": {
                "id": "m_dire_wolf_1",
                "name": "Lobo Terrível a1b2",
                "faction": "enemy",
                "pv_atual": 37,
                "pv_max": 37,
                "ca": 13,
                "tipo_bestiario": "m_dire_wolf"
            },
            "Bandido c3d4": {
                "id": "m_bandit_1",
                "name": "Bandido c3d4",
                "faction": "enemy",
                "pv_atual": 11,
                "pv_max": 11,
                "ca": 12,
                "tipo_bestiario": "m_bandit"
            }
        }

        # 1. Seleção por sufixo único
        t_suffix = self.session.find_combat_target("c3d4")
        self.assertIsNotNone(t_suffix)
        self.assertEqual(t_suffix["name"], "Bandido c3d4")

        # 2. Seleção por índice numérico (1 = primeiro, 2 = segundo)
        t_idx2 = self.session.find_combat_target("2")
        self.assertIsNotNone(t_idx2)
        self.assertEqual(t_idx2["name"], "Bandido c3d4")

        # 3. Seleção por campo 'id'
        t_id = self.session.find_combat_target("m_dire_wolf_1")
        self.assertIsNotNone(t_id)
        self.assertEqual(t_id["name"], "Lobo Terrível a1b2")

        # 4. Seleção de 'self'
        t_self = self.session.find_combat_target("self")
        self.assertIs(t_self, self.session.game_state["player_character"])

    def test_11_tactical_movement_and_kiting(self):
        """Valida que o deslocamento tático e kiting têm peso real no combate."""
        from core.combat_system import resolve_action, process_enemies_turn_batch
        
        # 1. Elfo da Floresta com 10.5m executando recuo/kiting
        self.pc["speed"] = "10.5m"
        self.pc["speed_m"] = 10.5
        res = resolve_action({"tipo_acao": "movimento", "recurso_utilizado": "manter_distancia"}, self.pc, [], {})
        self.assertTrue(self.pc.get("_tactical_kiting_active"))
        self.assertIn("10.5m", res["sys_log"])

        # Monstro corpo a corpo não alcança
        targets = {
            "Zumbi Lento": {
                "name": "Zumbi Lento",
                "faction": "enemy",
                "pv_atual": 22,
                "pv_max": 22,
                "ca": 8,
                "actions": [{"name": "Pancada", "hit_bonus": 3, "damage_dice": "1d6+1"}]
            }
        }
        hp_before = self.pc["hp_current"]
        log = process_enemies_turn_batch(targets, self.pc)
        self.assertIn("manteve distância", log)
        self.assertEqual(self.pc["hp_current"], hp_before)

        # 2. Movimento para Cobertura (+2 CA vs ataques à distância)
        resolve_action({"tipo_acao": "movimento", "recurso_utilizado": "cobertura"}, self.pc, [], {})
        self.assertTrue(self.pc.get("_tactical_cover_active"))

    def test_12_data_integrity_check(self):
        """Valida a integridade semântica de campaign.json, bestiary.json, side_quests.json e spells.json."""
        with open("data/campaign.json", "r", encoding="utf-8") as f:
            camp = json.load(f)
        with open("data/bestiary.json", "r", encoding="utf-8") as f:
            best = json.load(f)
        with open("data/side_quests.json", "r", encoding="utf-8") as f:
            sq = json.load(f)
        with open("data/spells.json", "r", encoding="utf-8") as f:
            spells = json.load(f)

        # 1. 15 Beats da Campanha
        self.assertEqual(len(camp), 15)
        for beat_num in range(1, 16):
            self.assertIn(str(beat_num), camp)
            beat_enemies = camp[str(beat_num)].get("enemies", [])
            for e in beat_enemies:
                self.assertIn(e, best, f"Inimigo '{e}' do Beat {beat_num} ausente no bestiário")

        # 2. Side Quests e seus inimigos
        self.assertGreaterEqual(len(sq), 6)
        for q_id, q_data in sq.items():
            self.assertIn("title", q_data)
            self.assertIn("enemies", q_data)
            self.assertIn("rewards", q_data)
            for e in q_data["enemies"]:
                self.assertIn(e, best, f"Inimigo '{e}' da Side Quest '{q_id}' ausente no bestiário")

        # 3. Spells iniciais D&D 5e
        all_spells = {}
        for cat in spells.values():
            all_spells.update(cat)
        for expected in ["magic_missile", "fireball", "cure_wounds", "fire_bolt", "sacred_flame", "guiding_bolt", "shield"]:
            self.assertIn(expected, all_spells, f"Magia essencial '{expected}' ausente no spells.json")


if __name__ == "__main__":
    unittest.main()

