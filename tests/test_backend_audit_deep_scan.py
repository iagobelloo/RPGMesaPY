import json
import os
import unittest
import copy

from core.game_engine import SessionManager
from core.time_manager import RestSystem
from core.combat_system import resolve_action, resolve_skill_effect, process_enemies_turn_batch
from core.dnd_rules import get_racial_speed, RACAS_5E, CLASSES, PROTAGONIST_GENDER_MAP
from core.story_engine import StoryManager


class DummyAI:
    def parse_player_intent(self, text, state):
        return {"tipo_acao": "INTERAGIR_AMBIENTE", "recurso_utilizado": None, "alvo": [], "intencao_cena": "observar"}

    def generate_narrative_from_math(self, log, intent):
        return f"[Narrativa]: {intent}"


class TestBackendAuditDeepScan(unittest.TestCase):
    """Testes exaustivos de auditoria profunda para o backend do RPGMesaPY."""

    def setUp(self):
        self.session = SessionManager(DummyAI())
        self.test_save_path = "saves/test_audit_deep_slot.json"
        self.pc = {
            "name": "Kaelen",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "hp_current": 12,
            "hp_max": 12,
            "xp": 0,
            "gold": 25,
            "attributes": {"FOR": 16, "DES": 14, "CON": 15, "INT": 10, "SAB": 12, "CAR": 10},
            "inventory": {"i_potion_healing": 2, "i_rations": 4}
        }
        self.session.game_state["player_character"] = self.pc

    def tearDown(self):
        if os.path.exists(self.test_save_path):
            try:
                os.remove(self.test_save_path)
            except OSError:
                pass

    def test_01_beat1_starts_clean_rumors_and_monsters(self):
        """Valida que uma nova sessão inicia com rumores e bestiário totalmente limpos no Beat 1."""
        new_session = SessionManager(DummyAI())
        self.assertEqual(new_session.story.current_beat, 1)
        self.assertEqual(new_session.game_state.get("discovered_rumors"), [])
        self.assertEqual(new_session.game_state.get("discovered_monsters"), [])
        self.assertEqual(new_session.get_discovered_rumors(), [])
        self.assertEqual(new_session.get_discovered_monsters(), [])

    def test_02_organic_rumor_discovery_via_tavern_keywords(self):
        """Valida que rumores são descobertos organicamente através de interação/diálogo/mural na Taverna."""
        self.assertEqual(len(self.session.get_discovered_rumors()), 0)
        
        # Interação orgânica com o balcão / mural
        self.session._async_turn_processor("ouvir rumores com o taverneiro no balcão", [], [])
        self.assertIn("sq_goblin_clearing", self.session.get_discovered_rumors())
        
        # Idempotência (não duplica na lista)
        self.session._async_turn_processor("perguntar sobre missões no mural", [], [])
        self.assertEqual(self.session.get_discovered_rumors().count("sq_goblin_clearing"), 1)

    def test_03_racial_speed_and_marching_costs(self):
        """Valida mecânica de Deslocamento Racial (7.5m, 9m, 10.5m) e custo de marcha/suprimentos."""
        # 1. Elfo da Floresta (10.5m) -> 1 dia, 1 suprimento
        pc_elf = {"race": "Elfo da Floresta", "inventory": {}}
        days, supplies, eff_speed, enc = self.session.calculate_travel_cost(pc_elf)
        self.assertEqual(eff_speed, 10.5)
        self.assertEqual(days, 1)
        self.assertEqual(supplies, 1)
        self.assertFalse(enc)

        # 2. Humano / Draconato / Meio-Orc / Tiefling (9.0m) -> 2 dias, 2 suprimentos
        pc_human = {"race": "Humano", "inventory": {}}
        days, supplies, eff_speed, enc = self.session.calculate_travel_cost(pc_human)
        self.assertEqual(eff_speed, 9.0)
        self.assertEqual(days, 2)
        self.assertEqual(supplies, 2)
        self.assertFalse(enc)

        # 3. Anão da Colina / Halfling (7.5m) -> 3 dias, 3 suprimentos
        pc_dwarf = {"race": "Anão da Colina", "inventory": {}}
        days, supplies, eff_speed, enc = self.session.calculate_travel_cost(pc_dwarf)
        self.assertEqual(eff_speed, 7.5)
        self.assertEqual(days, 3)
        self.assertEqual(supplies, 3)
        self.assertFalse(enc)

        # 4. Sobrecarga de inventário (penalidade de -1.5m, +1 dia, +1 suprimento)
        # Limite padrão com mod FOR 0 = 10 slots. Injeta 12 itens de 1 slot cada
        pc_encumbered = {
            "race": "Humano",
            "attributes": {"FOR": 10},
            "inventory": {f"item_heavy_{i}": 1 for i in range(12)}
        }
        days, supplies, eff_speed, enc = self.session.calculate_travel_cost(pc_encumbered)
        self.assertTrue(enc)
        self.assertEqual(eff_speed, 7.5) # 9.0 - 1.5
        self.assertEqual(days, 3)        # 2 + 1
        self.assertEqual(supplies, 3)    # 2 + 1

    def test_04_save_and_load_persistence_complete(self):
        """Valida que save_game e load_game persistem discovered_rumors, discovered_monsters, background e atributos."""
        self.session.discover_rumor("sq_goblin_clearing")
        self.session.discover_monster("m_goblin")
        self.session.game_state["current_background"] = "ancient_cemetery_bg.jpg"
        self.session.current_background_key = "ancient_cemetery_bg"

        saved = self.session.save_game(save_path=self.test_save_path)
        self.assertTrue(saved)
        self.assertTrue(os.path.exists(self.test_save_path))

        new_session = SessionManager(DummyAI())
        loaded = new_session.load_game(save_path=self.test_save_path)
        self.assertTrue(loaded)

        self.assertIn("sq_goblin_clearing", new_session.get_discovered_rumors())
        self.assertIn("m_goblin", new_session.get_discovered_monsters())
        self.assertEqual(new_session.game_state.get("current_background"), "ancient_cemetery_bg.jpg")
        self.assertEqual(new_session.current_background_key, "ancient_cemetery_bg")
        self.assertEqual(new_session.game_state["player_character"]["name"], "Kaelen")
        # Garante que atributos PT e EN continuam sincronizados
        attrs = new_session.game_state["player_character"]["attributes"]
        self.assertEqual(attrs["FOR"], attrs["STR"])
        self.assertEqual(attrs["DES"], attrs["DEX"])

    def test_05_load_game_legacy_resilience(self):
        """Valida restauração de save legado que não possuía discovered_rumors ou discovered_monsters."""
        legacy_data = {
            "player_character": {
                "name": "Velho Aventureiro",
                "race": "Humano",
                "class": "Guerreiro",
                "level": 1,
                "attributes": {"FOR": 15, "CON": 14}
            },
            "story_beat": 2,
            "quest_log": []
        }
        with open(self.test_save_path, "w", encoding="utf-8") as f:
            json.dump(legacy_data, f)

        new_session = SessionManager(DummyAI())
        loaded = new_session.load_game(save_path=self.test_save_path)
        self.assertTrue(loaded)
        self.assertEqual(new_session.get_discovered_rumors(), [])
        self.assertEqual(new_session.get_discovered_monsters(), [])
        self.assertEqual(new_session.story.current_beat, 2)
        # Sincronizou atributos ausentes com chaves padrão
        attrs = new_session.game_state["player_character"]["attributes"]
        self.assertIn("STR", attrs)
        self.assertIn("FOR", attrs)

    def test_06_defensive_programming_none_inputs_no_crashes(self):
        """Valida que métodos do backend não lançam AttributeError, KeyError ou TypeError com inputs None ou anômalos."""
        # 1. RestSystem
        res_short = RestSystem.short_rest(None, 1)
        self.assertEqual(res_short, {})
        c_state, camp_state = RestSystem.long_rest(None, None)
        self.assertIsInstance(c_state, dict)
        self.assertIsInstance(camp_state, dict)

        # 2. Combat resolution
        action_res = resolve_action(None, None)
        self.assertIsInstance(action_res, dict)
        skill_res = resolve_skill_effect({}, None, [], {})
        self.assertIsInstance(skill_res, str)
        batch_res = process_enemies_turn_batch(None, None)
        self.assertIsInstance(batch_res, str)

        # 3. Game Engine helpers
        ac = self.session._recalculate_ac(None)
        self.assertGreaterEqual(ac, 10)

        # 4. StoryManager
        story = StoryManager()
        ally = story.recruit_next_ally(None)
        self.assertTrue(ally is None or isinstance(ally, dict))

        # 5. _async_turn_processor sem player_character
        empty_session = SessionManager(DummyAI())
        empty_session.game_state["player_character"] = None
        # Não deve lançar exceção
        empty_session._async_turn_processor("atacar", [], [])
        msg = empty_session.ui_queue.get_nowait()
        self.assertIn("[SISTEMA]", msg.get("content", ""))

    def test_07_compendiums_integrity_and_manual_do_jogador(self):
        """Valida a integridade referencial dos JSONs de compêndio e do Manual do Jogador."""
        with open("data/manual_do_jogador.json", "r", encoding="utf-8") as f:
            manual = json.load(f)

        self.assertIn("secoes", manual)
        secoes = manual["secoes"]
        for sec in ["regras_basicas", "atributos_e_pericias", "deslocamento_e_viagem", "capacidade_e_inventario", "racas", "classes"]:
            self.assertIn(sec, secoes, f"Seção {sec} ausente no Manual do Jogador")

        # Verifica consistência das 7 raças
        for raca in ["Humano", "Elfo da Floresta", "Anão da Colina", "Halfling", "Draconato", "Meio-Orc", "Tiefling"]:
            self.assertIn(raca, secoes["racas"])
            self.assertIn("deslocamento_m", secoes["racas"][raca])
            self.assertEqual(secoes["racas"][raca]["deslocamento_m"], get_racial_speed(raca))

        # Verifica consistência das 6 classes
        for classe in CLASSES.keys():
            self.assertIn(classe, secoes["classes"])
            self.assertEqual(secoes["classes"][classe]["dado_vida"], CLASSES[classe]["dado_vida"])


if __name__ == "__main__":
    unittest.main()
