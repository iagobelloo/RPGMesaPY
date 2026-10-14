import unittest
import pygame
from core.game_engine import SessionManager
from ui.hud_components import GrimoireModal


class DummyAI:
    def call_ai(self, prompt, **kwargs):
        return '{"narrativa": "Teste", "tipo": "narrative"}'

    def generate_narrative_from_math(self, *args, **kwargs):
        return "Narrativa de teste"


class TestSideQuestTravel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.Surface((800, 600))

    def setUp(self):
        self.ai = DummyAI()
        self.session = SessionManager(self.ai)
        self.pc = {
            "name": "Kaelen",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 2,
            "hp_current": 20,
            "hp_max": 20,
            "xp": 100,
            "gold": 50,
            "inventory": {}
        }
        self.session.game_state["player_character"] = self.pc
        self.session.game_state["story_beat"] = 1
        self.session.story.current_beat = 1
        self.session.game_mode = "EXPLORACAO"
        self.session.current_background_key = "tavern_interior_bg.jpg"
        self.session.game_state["current_background"] = "tavern_interior_bg.jpg"
        self.session.active_combat_targets = {}
        self.session.active_visual_npcs = {}

        self.grimoire = GrimoireModal(0, 0, 800, 600)
        self.grimoire.game_state_ref = self.session.game_state
        self.grimoire.session_ref = self.session
        self.grimoire.is_visible = True

    def test_01_is_safe_hub_conditions(self):
        """Valida que is_safe_hub só retorna True em beats seguros sem combate."""
        # Beat 1 (Taverna) em EXPLORACAO -> True
        self.assertTrue(self.session.is_safe_hub())

        # Beat 1 em COMBATE -> False
        self.session.game_mode = "COMBATE"
        self.assertFalse(self.session.is_safe_hub())
        self.session.game_mode = "EXPLORACAO"

        # Beat 2 (Dungeon/hostil) -> False
        self.session.story.current_beat = 2
        self.session.game_state["story_beat"] = 2
        self.assertFalse(self.session.is_safe_hub())

        # Beat 4 (Acampamento) -> True
        self.session.story.current_beat = 4
        self.session.game_state["story_beat"] = 4
        self.assertTrue(self.session.is_safe_hub())

        # Beat 15 (Clímax) -> False
        self.session.story.current_beat = 15
        self.session.game_state["story_beat"] = 15
        self.assertFalse(self.session.is_safe_hub())

    def test_02_travel_to_side_quest_success(self):
        """Valida viagem para Side Quest: muda background, spawna inimigos, entra em combate e salva checkpoint."""
        self.session.story.current_beat = 1
        self.session.game_state["story_beat"] = 1
        self.session.accept_side_quest("sq_goblin_clearing")

        success = self.session.travel_to_side_quest("sq_goblin_clearing")
        self.assertTrue(success)
        self.assertEqual(self.session.game_mode, "COMBATE")
        self.assertEqual(self.session.game_state.get("active_side_quest"), "sq_goblin_clearing")
        self.assertIsNotNone(self.session.game_state.get("side_quest_origin"))
        self.assertEqual(self.session.game_state["side_quest_origin"]["beat"], 1)
        self.assertEqual(self.session.game_state["side_quest_origin"]["background"], "tavern_interior_bg.jpg")
        self.assertEqual(self.session.current_background_key, "goblin_camp_bg")
        self.assertEqual(self.session.game_state["current_background"], "goblin_camp_bg.jpg")
        self.assertGreater(len(self.session.active_combat_targets), 0)

    def test_03_ally_preservation_during_travel(self):
        """Valida que aliados recrutados no grupo sobrevivem e acompanham o jogador na viagem de side quest."""
        self.session.story.current_beat = 1
        self.session.game_state["story_beat"] = 1
        # Injeta um aliado no grupo
        self.session.active_combat_targets["ally_elora"] = {
            "name": "Elora",
            "faction": "ally",
            "hp_current": 15,
            "hp_max": 15
        }
        self.session.active_visual_npcs["ally_elora"] = "sprites/heroes/elora.png"

        self.session.accept_side_quest("sq_goblin_clearing")
        self.session.travel_to_side_quest("sq_goblin_clearing")

        # Aliado deve permanecer
        self.assertIn("ally_elora", self.session.active_combat_targets)
        self.assertIn("ally_elora", self.session.active_visual_npcs)
        # E deve haver inimigos goblins adicionados
        enemy_targets = [tid for tid, t in self.session.active_combat_targets.items() if t.get("faction") != "ally"]
        self.assertGreater(len(enemy_targets), 0)

    def test_04_combat_victory_returns_to_hub_and_completes_quest(self):
        """Valida que a vitória em combate retorna automaticamente ao Hub de origem e conclui a quest com recompensas."""
        self.session.story.current_beat = 1
        self.session.game_state["story_beat"] = 1
        initial_gold = self.pc["gold"]
        initial_xp = self.pc["xp"]

        self.session.accept_side_quest("sq_goblin_clearing")
        self.session.travel_to_side_quest("sq_goblin_clearing")

        # Simula vitória: derrota todos os inimigos
        for t in self.session.active_combat_targets.values():
            if t.get("faction") != "ally":
                t["pv_atual"] = 0
                t["hp_current"] = 0
                t["status"] = "morto"

        # Dispara resolução de combate
        self.session.check_combat_resolution()

        # Deve ter voltado ao Hub em modo EXPLORACAO
        self.assertEqual(self.session.game_mode, "EXPLORACAO")
        self.assertIsNone(self.session.game_state.get("active_side_quest"))
        self.assertEqual(self.session.current_background_key, "tavern_interior_bg")
        self.assertEqual(self.session.game_state["current_background"], "tavern_interior_bg.jpg")

        # Quest deve estar concluída no log
        q_record = next(q for q in self.session.game_state["quest_log"] if q["id"] == "sq_goblin_clearing")
        self.assertEqual(q_record["status"], "concluida")

        # Recompensas entregues
        self.assertGreater(self.pc["gold"], initial_gold)
        self.assertGreater(self.pc["xp"], initial_xp)

    def test_05_flee_returns_to_hub_and_keeps_quest_active(self):
        """Valida que fugir da batalha retorna ao Hub sem avançar a quest, mantendo-a ativa."""
        self.session.story.current_beat = 1
        self.session.game_state["story_beat"] = 1
        self.session.accept_side_quest("sq_goblin_clearing")
        self.session.travel_to_side_quest("sq_goblin_clearing")

        # Fuga
        self.session.return_from_side_quest(victory=False)

        self.assertEqual(self.session.game_mode, "EXPLORACAO")
        self.assertIsNone(self.session.game_state.get("active_side_quest"))
        self.assertEqual(self.session.current_background_key, "tavern_interior_bg")
        self.assertEqual(self.session.game_state["current_background"], "tavern_interior_bg.jpg")

        q_record = next(q for q in self.session.game_state["quest_log"] if q["id"] == "sq_goblin_clearing")
        self.assertEqual(q_record["status"], "ativa")

    def test_06_grimoire_rumor_filter_and_accept_button(self):
        """Valida exibição de rumores no Grimório e clique no botão Aceitar Missão."""
        self.grimoire.active_tab = "diario"
        self.grimoire.journal_filter = "rumores"
        self.grimoire.selected_quest_id = "sq_goblin_clearing"

        # Desenha a tela para posicionar retângulos de botões
        self.grimoire.draw(self.screen)

        self.assertGreater(self.grimoire.btn_accept_quest.width, 0)
        self.assertEqual(self.grimoire.btn_travel_quest.width, 0)

        # Simula clique no botão Aceitar
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": self.grimoire.btn_accept_quest.center
        })
        action = self.grimoire.handle_event(click_event)
        self.assertEqual(action, "accept_side_quest:sq_goblin_clearing")

    def test_07_grimoire_travel_button_in_hub(self):
        """Valida exibição do botão Partir em Viagem no Grimório quando em local seguro."""
        self.session.accept_side_quest("sq_goblin_clearing")
        self.grimoire.active_tab = "diario"
        self.grimoire.journal_filter = "ativas"
        self.grimoire.selected_quest_id = "sq_goblin_clearing"

        self.grimoire.draw(self.screen)

        self.assertGreater(self.grimoire.btn_travel_quest.width, 0)
        self.assertEqual(self.grimoire.btn_accept_quest.width, 0)

        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": self.grimoire.btn_travel_quest.center
        })
        action = self.grimoire.handle_event(click_event)
        self.assertEqual(action, "travel_side_quest:sq_goblin_clearing")

    def test_08_save_and_load_with_active_side_quest(self):
        """Valida persistência do estado de side quest e origem no save/load."""
        import os
        backup_save = None
        if os.path.exists("savegame.json"):
            with open("savegame.json", "rb") as f:
                backup_save = f.read()

        try:
            self.session.story.current_beat = 1
            self.session.accept_side_quest("sq_goblin_clearing")
            self.session.travel_to_side_quest("sq_goblin_clearing")

            saved = self.session.save_game()
            self.assertTrue(saved)

            # Novo session manager para carregar
            new_session = SessionManager(self.ai)
            loaded = new_session.load_game()
            self.assertTrue(loaded)
            self.assertEqual(new_session.game_state.get("active_side_quest"), "sq_goblin_clearing")
            self.assertIsNotNone(new_session.game_state.get("side_quest_origin"))
            self.assertEqual(new_session.game_state["side_quest_origin"]["background"], "tavern_interior_bg.jpg")
        finally:
            if backup_save is not None:
                with open("savegame.json", "wb") as f:
                    f.write(backup_save)
            elif os.path.exists("savegame.json"):
                os.remove("savegame.json")


if __name__ == "__main__":
    unittest.main()
