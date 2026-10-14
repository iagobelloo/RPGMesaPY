import unittest
import copy
from core.game_engine import SessionManager
from core.dnd_rules import (
    RACAS_5E,
    get_base_attributes,
    get_class_base_attributes,
    get_racial_bonus,
    get_racial_speed,
    get_manual_do_jogador,
    MANUAL_DO_JOGADOR_5E
)


class DummyAI:
    def parse_player_intent(self, text, state):
        t_low = text.lower()
        if "atacar" in t_low:
            return {
                "tipo_acao": "ATACAR",
                "recurso_utilizado": "espada longa",
                "alvo": ["m_dire_wolf"],
                "intencao_cena": "Atacar inimigo"
            }
        return {
            "tipo_acao": "DIALOGAR" if any(w in t_low for w in ["falar", "conversar", "ouvir"]) else "INTERAGIR_CENARIO",
            "recurso_utilizado": "nenhum",
            "alvo": ["nenhum"],
            "intencao_cena": "Interagir com o ambiente"
        }

    def generate_narrative_from_math(self, log, intent):
        return f"[Narrativa]: {intent} -> {log[:40]}"


class TestGameEngineBackend(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI()
        self.session = SessionManager(self.ai)
        self.session.game_state["player_character"] = {
            "name": "Valerius",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "hp_max": 20,
            "hp_current": 20,
            "ca": 16,
            "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "WIS": 10, "CHA": 10},
            "proficiency_bonus": 2,
            "speed": "9.0m",
            "speed_m": 9.0,
            "inventory": {"i_rations": 5, "i_potion_healing": 2}
        }
        self.session.story.current_beat = 1
        self.session.game_state["story_beat"] = 1
        self.session.game_mode = "EXPLORACAO"
        # Limpa fila UI
        while not self.session.ui_queue.empty():
            self.session.ui_queue.get_nowait()

    def test_01_game_state_initializes_empty_rumors_and_monsters(self):
        """Valida que novos jogos iniciam com discovered_rumors e discovered_monsters vazios."""
        new_session = SessionManager()
        self.assertEqual(new_session.game_state.get("discovered_rumors"), [])
        self.assertEqual(new_session.game_state.get("discovered_monsters"), [])
        self.assertEqual(new_session.get_discovered_rumors(), [])
        self.assertEqual(new_session.get_discovered_monsters(), [])

    def test_02_discover_rumor_validation_and_idempotency(self):
        """Valida que discover_rumor valida side_quests.json, despacha mensagem e é idempotente."""
        # Quest válida
        res1 = self.session.discover_rumor("sq_goblin_clearing")
        self.assertTrue(res1)
        self.assertIn("sq_goblin_clearing", self.session.get_discovered_rumors())

        # Idempotência (não duplica)
        res2 = self.session.discover_rumor("sq_goblin_clearing")
        self.assertFalse(res2)
        self.assertEqual(self.session.get_discovered_rumors().count("sq_goblin_clearing"), 1)

        # Quest inexistente
        res_fail = self.session.discover_rumor("sq_inexistente_999")
        self.assertFalse(res_fail)
        self.assertNotIn("sq_inexistente_999", self.session.get_discovered_rumors())

    def test_03_accept_side_quest_does_not_teleport(self):
        """Valida que aceitar uma side quest a move para ativa sem realizar teletransporte instantâneo."""
        accepted = self.session.accept_side_quest("sq_goblin_clearing")
        self.assertTrue(accepted)

        # Modo continua EXPLORACAO no Beat 1
        self.assertEqual(self.session.game_mode, "EXPLORACAO")
        self.assertEqual(self.session.story.current_beat, 1)
        self.assertIsNone(self.session.game_state.get("active_side_quest"))

        # Quest registrada como ativa no quest_log
        log = self.session.game_state.get("quest_log", [])
        entry = next((q for q in log if q.get("id") == "sq_goblin_clearing"), None)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.get("status"), "ativa")

    def test_04_travel_to_side_quest_consumes_days_and_supplies_by_speed(self):
        """Valida mecânica de Deslocamento e Viagem para 10.5m, 9.0m e 7.5m."""
        # 1. Elfo (10.5m) -> 1 dia, 1 suprimento
        pc_elf = copy.deepcopy(self.session.game_state["player_character"])
        pc_elf["race"] = "Elfo da Floresta"
        pc_elf["speed"] = "10.5m"
        pc_elf["speed_m"] = 10.5
        days, sup, eff_spd, is_enc = self.session.calculate_travel_cost(pc_elf)
        self.assertEqual(days, 1)
        self.assertEqual(sup, 1)
        self.assertEqual(eff_spd, 10.5)
        self.assertFalse(is_enc)

        # 2. Humano (9.0m) -> 2 dias, 2 suprimentos
        pc_human = copy.deepcopy(self.session.game_state["player_character"])
        pc_human["race"] = "Humano"
        pc_human["speed"] = "9.0m"
        pc_human["speed_m"] = 9.0
        days, sup, eff_spd, is_enc = self.session.calculate_travel_cost(pc_human)
        self.assertEqual(days, 2)
        self.assertEqual(sup, 2)
        self.assertEqual(eff_spd, 9.0)
        self.assertFalse(is_enc)

        # 3. Anão (7.5m) -> 3 dias, 3 suprimentos
        pc_dwarf = copy.deepcopy(self.session.game_state["player_character"])
        pc_dwarf["race"] = "Anão da Colina"
        pc_dwarf["speed"] = "7.5m"
        pc_dwarf["speed_m"] = 7.5
        days, sup, eff_spd, is_enc = self.session.calculate_travel_cost(pc_dwarf)
        self.assertEqual(days, 3)
        self.assertEqual(sup, 3)
        self.assertEqual(eff_spd, 7.5)
        self.assertFalse(is_enc)

    def test_05_encumbrance_applies_speed_penalty_and_increases_supplies(self):
        """Valida que sobrecarga no inventário reduz deslocamento em 1.5m e consome +1 suprimento."""
        pc_overloaded = copy.deepcopy(self.session.game_state["player_character"])
        pc_overloaded["race"] = "Humano"
        pc_overloaded["speed"] = "9.0m"
        pc_overloaded["speed_m"] = 9.0
        # Força de 10 -> limite de 10 slots. Injeta 15 espadas (15 slots)
        pc_overloaded["attributes"]["FOR"] = 10
        pc_overloaded["inventory"] = {"w_greatsword": 15, "i_rations": 5}

        days, sup, eff_spd, is_enc = self.session.calculate_travel_cost(pc_overloaded)
        self.assertTrue(is_enc)
        self.assertEqual(eff_spd, 7.5, "Deslocamento deve sofrer penalidade de -1.5m (9.0m -> 7.5m)")
        self.assertEqual(sup, 3, "Suprimentos consumidos devem ter +1 penalidade (2 + 1 = 3)")
        self.assertEqual(days, 3, "Dias de viagem devem aumentar para 3 dias")

    def test_06_travel_to_side_quest_execution_and_integer_beat_transition(self):
        """Valida execução da viagem: consome suprimentos, avança dias e envia beat inteiro na transição."""
        initial_day = self.session.game_state.get("current_day", 1)
        initial_rations = self.session.get_inventory_item_count("i_rations")

        success = self.session.travel_to_side_quest("sq_goblin_clearing")
        self.assertTrue(success)
        self.assertEqual(self.session.game_mode, "COMBATE")
        self.assertEqual(self.session.game_state.get("active_side_quest"), "sq_goblin_clearing")

        # Humano 9m consome 2 dias e 2 suprimentos
        self.assertEqual(self.session.game_state.get("current_day"), initial_day + 2)
        self.assertEqual(self.session.get_inventory_item_count("i_rations"), initial_rations - 2)

        # Inspeciona mensagens da ui_queue
        messages = []
        while not self.session.ui_queue.empty():
            messages.append(self.session.ui_queue.get_nowait())

        transition_msgs = [m for m in messages if m.get("type") == "beat_transition"]
        self.assertEqual(len(transition_msgs), 1)
        # Beat deve ser inteiro, não string quebrada
        self.assertIsInstance(transition_msgs[0].get("beat"), int)

        # Mensagem narrativa contextual registrando dias e rações
        narrative_msgs = [m for m in messages if m.get("type") == "narrative"]
        self.assertEqual(len(narrative_msgs), 1)
        content = narrative_msgs[0].get("content", "")
        self.assertIn("dias", content.lower())
        self.assertIn("raç", content.lower())

    def test_07_no_duplicate_narrative_in_dialogue_and_combat(self):
        """Valida que diálogo e turnos de combate não enviam mensagens narrativas duplicadas."""
        # 1. Diálogo / Interação na Taverna
        self.session._async_turn_processor("ouvir rumores com o taverneiro", [], [])
        msgs = []
        while not self.session.ui_queue.empty():
            msgs.append(self.session.ui_queue.get_nowait())

        narrative_msgs = [m for m in msgs if m.get("type") in ["narrative", "dialogue"]]
        self.assertEqual(len(narrative_msgs), 1, "Exatamente UMA mensagem narrativa deve ser despachada por turno de diálogo.")

        # 2. Resolução de Combate com Vitória
        self.session.game_mode = "COMBATE"
        self.session.active_combat_targets = {
            "Lobo Fraco": {
                "name": "Lobo Fraco",
                "tipo_bestiario": "m_dire_wolf",
                "pv_atual": 1,
                "pv_max": 1,
                "ca": 10,
                "faction": "enemy",
                "status": "vivo"
            }
        }
        # Finaliza o combate
        self.session.active_combat_targets["Lobo Fraco"]["pv_atual"] = 0
        self.session.active_combat_targets["Lobo Fraco"]["status"] = "morto"
        self.session.check_combat_resolution()

        combat_msgs = []
        while not self.session.ui_queue.empty():
            combat_msgs.append(self.session.ui_queue.get_nowait())

        combat_narratives = [m for m in combat_msgs if m.get("type") in ["narrative", "dialogue"]]
        self.assertEqual(len(combat_narratives), 1, "Exatamente UMA mensagem narrativa na vitória de combate.")

    def test_08_dnd_rules_and_player_handbook_compendium(self):
        """Valida atributos base, bônus raciais, deslocamento e compêndio do Manual do Jogador."""
        # Atributos base (Standard Array 15, 14, 13, 12, 10, 8)
        fighter_attrs = get_base_attributes("Guerreiro")
        self.assertEqual(fighter_attrs["FOR"], 15)
        self.assertEqual(fighter_attrs["CON"], 14)
        self.assertEqual(fighter_attrs["INT"], 8)

        # Bônus racial estruturado
        human_bonus = get_racial_bonus("Humano")
        self.assertEqual(human_bonus["FOR"], 1)
        self.assertEqual(human_bonus["DES"], 1)

        elf_bonus = get_racial_bonus("Elfo da Floresta")
        self.assertEqual(elf_bonus["DES"], 2)
        self.assertEqual(elf_bonus["SAB"], 1)
        self.assertEqual(elf_bonus["FOR"], 0)

        # Deslocamento racial
        self.assertEqual(get_racial_speed("Elfo da Floresta"), 10.5)
        self.assertEqual(get_racial_speed("Humano"), 9.0)
        self.assertEqual(get_racial_speed("Anão da Colina"), 7.5)
        self.assertEqual(get_racial_speed("Halfling"), 7.5)

        # Manual do Jogador
        manual = get_manual_do_jogador()
        self.assertIn("secoes", manual)
        self.assertIn("deslocamento_e_viagem", manual["secoes"])
        self.assertIn("atributos_e_pericias", manual["secoes"])


if __name__ == "__main__":
    unittest.main()
