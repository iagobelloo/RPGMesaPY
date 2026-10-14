import unittest
import pygame
from core.game_engine import SessionManager
from ui.hud_components import GrimoireModal


class DummyAI:
    def call_ai(self, prompt, **kwargs):
        return '{"narrativa": "Teste", "tipo": "narrative"}'

    def generate_narrative_from_math(self, *args, **kwargs):
        return "Narrativa de teste"


class TestGrimoireQuestJournal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        # Surface dummy sem janela
        cls.screen = pygame.Surface((800, 600))

    def setUp(self):
        self.ai = DummyAI()
        self.session = SessionManager(self.ai)
        self.pc = {
            "name": "Alistair",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "hp_current": 12,
            "hp_max": 12,
            "xp": 0,
            "gold": 20,
            "inventory": {}
        }
        self.session.game_state["player_character"] = self.pc
        self.grimoire = GrimoireModal(0, 0, 800, 600)
        self.grimoire.game_state_ref = self.session.game_state
        self.grimoire.session_ref = self.session
        self.grimoire.is_visible = True

    def test_01_tab_switching_to_diario(self):
        """Valida a troca de aba para 'diario' via clique ou programático."""
        self.grimoire.active_tab = "diario"
        self.assertEqual(self.grimoire.active_tab, "diario")

        # Teste de evento de clique na aba
        dummy_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": self.grimoire.tab_journal_rect.center
        })
        self.grimoire.active_tab = "habilidades"
        action = self.grimoire.handle_event(dummy_event)
        self.assertEqual(action, "")
        self.assertEqual(self.grimoire.active_tab, "diario")

    def test_02_structured_objectives_on_accept_quest(self):
        """Valida que aceitar uma quest popula a lista estruturada de objetivos com caixas de verificação."""
        ok = self.session.accept_side_quest("sq_goblin_clearing")
        self.assertTrue(ok)

        active = self.session.get_active_quests()
        self.assertEqual(len(active), 1)
        q = active[0]
        self.assertIn("objectives", q)
        self.assertIsInstance(q["objectives"], list)
        self.assertGreater(len(q["objectives"]), 0)

        # Cada objetivo deve ser um dict com 'text' e 'done'
        for obj in q["objectives"]:
            self.assertIn("text", obj)
            self.assertIn("done", obj)
            self.assertFalse(obj["done"], "Objetivo novo não deve iniciar concluído!")

        self.assertEqual(q["progress"], 0)
        self.assertEqual(q["target_progress"], len(q["objectives"]))

    def test_03_update_quest_objective_progress(self):
        """Valida a atualização de objetivos individuais e incremento do progresso."""
        self.session.accept_side_quest("sq_goblin_clearing")
        
        # Marca primeiro objetivo como concluído
        updated = self.session.update_quest_objective("sq_goblin_clearing", 0, done=True)
        self.assertTrue(updated)

        active = self.session.get_active_quests()[0]
        self.assertTrue(active["objectives"][0]["done"])
        self.assertFalse(active["objectives"][1]["done"])
        self.assertEqual(active["progress"], 1)

    def test_04_complete_quest_marks_all_objectives_and_delivers_rewards(self):
        """Valida que concluir a quest marca todos os objetivos como concluídos e transfere recompensas."""
        self.session.accept_side_quest("sq_goblin_clearing")
        res = self.session.complete_side_quest("sq_goblin_clearing")
        self.assertTrue(res["success"])

        # Deve estar no filtro de concluídas
        completed = self.session.get_completed_quests()
        self.assertEqual(len(completed), 1)
        q = completed[0]
        self.assertEqual(q["status"], "concluida")
        for obj in q["objectives"]:
            self.assertTrue(obj["done"], "Todos os objetivos devem estar concluídos ao finalizar a quest!")
        self.assertEqual(q["progress"], q["target_progress"])

    def test_05_grimoire_rendering_without_crashing(self):
        """Valida a renderização gráfica da aba Diário / Missões em múltiplos estados."""
        self.grimoire.active_tab = "diario"

        # 1. Sem quests secundárias (Apenas Campanha Principal)
        self.grimoire.selected_quest_id = "main_campaign"
        self.grimoire.draw(self.screen)

        # 2. Com quest ativa selecionada
        self.session.accept_side_quest("sq_goblin_clearing")
        self.grimoire.selected_quest_id = "sq_goblin_clearing"
        self.grimoire.journal_filter = "ativas"
        self.grimoire.draw(self.screen)

        # 3. Com quest concluída no filtro de concluídas
        self.session.complete_side_quest("sq_goblin_clearing")
        self.grimoire.journal_filter = "concluidas"
        self.grimoire.selected_quest_id = "sq_goblin_clearing"
        self.grimoire.draw(self.screen)

    def test_06_filter_and_selection_event_handling(self):
        """Valida cliques nos filtros e na seleção de missões no Diário."""
        self.grimoire.active_tab = "diario"
        self.session.accept_side_quest("sq_goblin_clearing")
        # Desenha uma vez para inicializar os rects dos botões
        self.grimoire.draw(self.screen)

        # Clica no filtro de Concluídas
        ev_filter_comp = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": self.grimoire.btn_filter_completed.center
        })
        self.grimoire.handle_event(ev_filter_comp)
        self.assertEqual(self.grimoire.journal_filter, "concluidas")

        # Clica no filtro de Ativas
        ev_filter_act = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": self.grimoire.btn_filter_active.center
        })
        self.grimoire.handle_event(ev_filter_act)
        self.assertEqual(self.grimoire.journal_filter, "ativas")

        # Clica na Campanha Principal
        ev_main = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": self.grimoire.btn_main_campaign.center
        })
        self.grimoire.selected_quest_id = "sq_goblin_clearing"
        self.grimoire.handle_event(ev_main)
        self.assertEqual(self.grimoire.selected_quest_id, "main_campaign")


if __name__ == "__main__":
    unittest.main()

