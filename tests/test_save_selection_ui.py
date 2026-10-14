import os
import unittest
import pygame

# Ambiente headless para testes unitários
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.font.init()
_ = pygame.display.set_mode((1280, 720))

from ui.menu_components import SaveSelectionPanel
from ui.hud_components import BackpackModal
from core.game_engine import SessionManager


class TestSaveSelectionUI(unittest.TestCase):
    """Suite de testes para a UI de Seleção de Saves e Botões de Equipamento."""

    def setUp(self):
        self.screen = pygame.display.get_surface()
        if self.screen is None:
            self.screen = pygame.display.set_mode((1280, 720))
        self.panel = SaveSelectionPanel(0, 0, 1280, 720)
        self.panel.is_visible = True

    def test_instantiation_and_cards_geometry(self):
        """Valida que o painel possui 3 cards e botões devidamente posicionados."""
        p = self.panel
        self.assertEqual(len(p.cards_rects), 3)
        self.assertEqual(len(p.slot_buttons), 3)

        for slot_num in [1, 2, 3]:
            btns = p.slot_buttons[slot_num]
            self.assertIn("load", btns)
            self.assertIn("delete", btns)
            self.assertIn("new", btns)
            self.assertIsInstance(btns["load"], pygame.Rect)
            self.assertIsInstance(btns["delete"], pygame.Rect)
            self.assertIsInstance(btns["new"], pygame.Rect)

        self.assertIsInstance(p.btn_back, pygame.Rect)
        self.assertIsInstance(p._card_bg_surf, pygame.Surface)
        self.assertEqual(len(p.slots_data), 3)

    def test_draw_headless_execution(self):
        """Garante que draw() executa com sucesso sem nenhum crash de renderização."""
        try:
            self.panel.draw(self.screen)
        except Exception as e:
            self.fail(f"draw() no SaveSelectionPanel falhou: {e}")

    def test_event_handling_back_and_escape(self):
        """Valida que o botão Voltar e a tecla ESC retornam 'back_to_menu'."""
        p = self.panel

        # Clique no botão Voltar
        back_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.btn_back.center})
        self.assertEqual(p.handle_event(back_click), "back_to_menu")

        # Tecla ESC
        esc_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
        self.assertEqual(p.handle_event(esc_event), "back_to_menu")

    def test_event_handling_with_mocked_slots(self):
        """Valida eventos de carregar, excluir e nova campanha com dados simulados."""
        p = self.panel
        # Mock de 3 slots: Slot 1 ocupado, Slot 2 vazio, Slot 3 ocupado
        p.slots_data = [
            {
                "slot": 1,
                "is_empty": False,
                "name": "Valerius",
                "race": "Humano",
                "class": "Guerreiro",
                "level": 2,
                "hp_current": 18,
                "hp_max": 20,
                "gold": 120,
                "location": "Ato I • Planície",
                "current_day": 3,
                "quests_completed": 1
            },
            {
                "slot": 2,
                "is_empty": True
            },
            {
                "slot": 3,
                "is_empty": False,
                "name": "Sylas",
                "race": "Elfo da Floresta",
                "class": "Patrulheiro",
                "level": 1,
                "hp_current": 12,
                "hp_max": 12,
                "gold": 45,
                "location": "Ato I • Taverna",
                "current_day": 1,
                "quests_completed": 0
            }
        ]

        # 1. Clique em 'Continuar Jornada' no Slot 1
        btn_load_1 = p.slot_buttons[1]["load"]
        click_load = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": btn_load_1.center})
        self.assertEqual(p.handle_event(click_load), ("load_slot", 1))

        # 2. Clique em 'Excluir' no Slot 1
        btn_del_1 = p.slot_buttons[1]["delete"]
        click_del = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": btn_del_1.center})
        self.assertEqual(p.handle_event(click_del), ("delete_slot", 1))

        # 3. Clique em '+ Nova Campanha' no Slot 2 (Vazio)
        btn_new_2 = p.slot_buttons[2]["new"]
        click_new = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": btn_new_2.center})
        self.assertEqual(p.handle_event(click_new), ("new_game_slot", 2))

        # 4. Renderização com os dados mockados
        p.draw(self.screen)

    def test_backpack_modal_equip_weapon_button(self):
        """Valida que BackpackModal exibe botão Empunhar/Equipar e responde ao clique."""
        backpack = BackpackModal(100, 100, 840, 560)
        backpack.is_visible = True
        backpack.game_state_ref = {
            "player_character": {
                "name": "Herói",
                "class": "Guerreiro",
                "equipped_weapon": "Desarmado",
                "equipped_armor": "Trajes",
                "has_shield": False,
                "gold": 50,
                "inventory": ["Espada Longa", "Arco Curto", "Roupas Comuns"]
            },
            "inventory": {"i_potion_healing": 2}
        }

        # Desenho da mochila
        backpack.draw(self.screen)
        self.assertIn("Espada Longa", backpack._equip_buttons)

        # Simula clique no botão "Empunhar" da Espada Longa
        btn_sword = backpack._equip_buttons["Espada Longa"]
        click_equip = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": btn_sword.center})
        action = backpack.handle_event(click_equip)
        self.assertEqual(action, "equip_weapon:Espada Longa")


if __name__ == "__main__":
    unittest.main()
