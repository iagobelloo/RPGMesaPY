import os
import unittest
import pygame

# Garante ambiente headless para testes unitários
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.font.init()
_ = pygame.display.set_mode((1280, 720))

from ui.menu_components import (
    CharacterCreationPanel,
    RaceSelectionPanel,
    ClassSelectionPanel,
    BackgroundSelectionPanel,
    AlignmentSelectionPanel,
    GenericSelectionPanel
)
from ui.asset_manager import AssetManager
from core.dnd_rules import RACAS_5E, CLASSES, ANTECEDENTES_5E, TENDENCIAS_5E


class TestCharacterCreationUI(unittest.TestCase):
    """Suite de testes para a UI de Criação de Personagem e Modais de Seleção."""

    def setUp(self):
        self.screen = pygame.display.get_surface()
        if self.screen is None:
            self.screen = pygame.display.set_mode((1280, 720))
        self.panel = CharacterCreationPanel(0, 0, 1280, 720)
        self.panel.is_visible = True

    def test_instantiation_and_preallocated_rects(self):
        """Valida a instanciação, hitboxes pré-alocadas e integridade do painel."""
        p = self.panel
        self.assertEqual(p.player_name, "")
        self.assertEqual(p.selected_race, "")
        self.assertEqual(p.selected_class, "")
        self.assertEqual(p.selected_background, "")
        self.assertEqual(p.selected_alignment, "")
        self.assertFalse(p._is_ready())

        # Hitboxes delimitadas pré-alocadas para eliminar NameError e zero garbage
        self.assertIsInstance(p.hb_nome, pygame.Rect)
        self.assertIsInstance(p.hb_raca, pygame.Rect)
        self.assertIsInstance(p.hb_classe, pygame.Rect)
        self.assertIsInstance(p.hb_bg, pygame.Rect)
        self.assertIsInstance(p.hb_align, pygame.Rect)
        self.assertIsInstance(p.btn_cancel, pygame.Rect)
        self.assertIsInstance(p.btn_start, pygame.Rect)
        self.assertIsInstance(p._modal_overlay, pygame.Surface)

        # Atributos base sorteados
        for attr in ["STR", "FOR", "DEX", "CON", "INT", "WIS", "CHA"]:
            self.assertIn(attr, p.base_attributes)
            self.assertGreaterEqual(p.base_attributes[attr], 3)
            self.assertLessEqual(p.base_attributes[attr], 18)

    def test_draw_lifecycle_without_name_error_or_crashes(self):
        """Garante que draw() executa com sucesso em todos os estágios do ciclo de vida."""
        p = self.panel

        # 1. Desenho com campos vazios (recém aberto)
        try:
            p.draw(self.screen)
        except Exception as e:
            self.fail(f"draw() falhou no estado inicial vazio: {e}")

        # 2. Desenho com preenchimento parcial
        p.player_name = "Thorgar"
        p.selected_race = "Meio-Orc"
        p._stats_dirty = True
        try:
            p.draw(self.screen)
        except Exception as e:
            self.fail(f"draw() falhou com preenchimento parcial: {e}")

        # 3. Desenho com preenchimento completo e pronto
        p.selected_class = "Guerreiro"
        p.selected_background = "Soldado"
        p.selected_alignment = "Caótico e Bom"
        p._stats_dirty = True
        self.assertTrue(p._is_ready())
        try:
            p.draw(self.screen)
        except Exception as e:
            self.fail(f"draw() falhou com todos os campos preenchidos: {e}")

        # 4. Desenho com modal ativo
        p.active_modal = RaceSelectionPanel(p.data_lists["race"])
        p.active_modal.is_visible = True
        try:
            p.draw(self.screen)
        except Exception as e:
            self.fail(f"draw() falhou com modal ativo aberto: {e}")

    def test_selection_modals_lifecycle_and_hover(self):
        """Valida que todos os 4 modais abrem, desenham sem erro e respondem a cliques."""
        test_cases = [
            (RaceSelectionPanel, list(RACAS_5E.keys()), "Humano"),
            (ClassSelectionPanel, list(CLASSES.keys()), "Mago"),
            (BackgroundSelectionPanel, list(ANTECEDENTES_5E.keys()), "Soldado"),
            (AlignmentSelectionPanel, list(TENDENCIAS_5E.keys()), "Neutro e Bom"),
        ]

        for modal_cls, items, target_item in test_cases:
            modal = modal_cls(items)
            modal.is_visible = True

            # Simula hover no item alvo
            target_rect = None
            for r, item in modal.rects:
                if item == target_item:
                    target_rect = r
                    break
            self.assertIsNotNone(target_rect, f"Item {target_item} não encontrado no modal {modal_cls.__name__}")

            # Desenho com hover ativo
            modal.hover_item = target_item
            modal.draw(self.screen)

            # Simula clique no item
            click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": target_rect.center})
            selected = modal.handle_event(click_event)
            self.assertEqual(selected, target_item)

            # Simula cancelamento via botão Voltar
            back_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": modal.btn_back.center})
            self.assertEqual(modal.handle_event(back_click), "CANCEL")

            # Simula cancelamento via tecla ESC
            esc_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
            self.assertEqual(modal.handle_event(esc_event), "CANCEL")

    def test_full_character_creation_event_flow(self):
        """Simula o fluxo completo de criação do personagem até o clique em Iniciar."""
        p = self.panel

        # 1. Clicar no campo Nome e digitar "Alistair"
        click_name = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.hitbox_map["nome"].center})
        p.handle_event(click_name)
        self.assertTrue(p.active_input)

        for char in "Alistair":
            key_event = pygame.event.Event(pygame.KEYDOWN, {"key": ord(char), "unicode": char})
            p.handle_event(key_event)
        self.assertEqual(p.player_name, "Alistair")

        # 2. Clicar no slot Raça -> abre RaceSelectionPanel
        click_race_slot = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.hitbox_map["race"].center})
        p.handle_event(click_race_slot)
        self.assertIsInstance(p.active_modal, RaceSelectionPanel)
        self.assertEqual(p.target_slot, "race")

        # Seleciona "Draconato"
        drag_rect = [r for r, item in p.active_modal.rects if item == "Draconato"][0]
        select_race = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": drag_rect.center})
        p.handle_event(select_race)
        self.assertIsNone(p.active_modal)
        self.assertEqual(p.selected_race, "Draconato")

        # 3. Clicar no slot Classe -> abre ClassSelectionPanel
        click_class_slot = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.hitbox_map["class"].center})
        p.handle_event(click_class_slot)
        self.assertIsInstance(p.active_modal, ClassSelectionPanel)
        self.assertEqual(p.target_slot, "class")

        pal_rect = [r for r, item in p.active_modal.rects if item == "Paladino"][0]
        select_class = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": pal_rect.center})
        p.handle_event(select_class)
        self.assertIsNone(p.active_modal)
        self.assertEqual(p.selected_class, "Paladino")

        # 4. Clicar no slot Antecedente -> abre BackgroundSelectionPanel
        click_bg_slot = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.hitbox_map["background"].center})
        p.handle_event(click_bg_slot)
        self.assertIsInstance(p.active_modal, BackgroundSelectionPanel)

        sold_rect = [r for r, item in p.active_modal.rects if item == "Soldado"][0]
        select_bg = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": sold_rect.center})
        p.handle_event(select_bg)
        self.assertIsNone(p.active_modal)
        self.assertEqual(p.selected_background, "Soldado")

        # 5. Clicar no slot Tendência -> abre AlignmentSelectionPanel
        click_al_slot = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.hitbox_map["alignment"].center})
        p.handle_event(click_al_slot)
        self.assertIsInstance(p.active_modal, AlignmentSelectionPanel)

        lg_rect = [r for r, item in p.active_modal.rects if item == "Leal e Bom"][0]
        select_al = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": lg_rect.center})
        p.handle_event(select_al)
        self.assertIsNone(p.active_modal)
        self.assertEqual(p.selected_alignment, "Leal e Bom")

        # Todos os campos preenchidos: ficha pronta!
        self.assertTrue(p._is_ready())

        # 6. Clicar em "Iniciar Sessão Zero"
        click_start = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.btn_start.center})
        result = p.handle_event(click_start)
        self.assertIsNotNone(result)
        self.assertEqual(result.get("action"), "start")

        char = result.get("char")
        self.assertIsNotNone(char)
        self.assertEqual(char["name"], "Alistair")
        self.assertEqual(char["race"], "Draconato")
        self.assertEqual(char["class"], "Paladino")
        self.assertEqual(char["background"], "Soldado")
        self.assertEqual(char["alignment"], "Leal e Bom")
        self.assertGreater(char["hp_max"], 0)
        self.assertGreater(char["ac"], 0)
        self.assertIn("attributes", char)
        self.assertIn("inventory", char)
        self.assertIn("gold", char)

    def test_cancel_button_returns_cancel_action(self):
        """Valida que o botão Cancelar retorna a ação cancel."""
        p = self.panel
        click_cancel = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.btn_cancel.center})
        result = p.handle_event(click_cancel)
        self.assertEqual(result, {"action": "cancel"})

    def test_panel_reset_clears_state(self):
        """Valida que o método reset() limpa completamente o estado anterior."""
        p = self.panel
        p.player_name = "Hero"
        p.selected_race = "Elfo da Floresta"
        p.selected_class = "Patrulheiro"
        p.selected_background = "Sábio"
        p.selected_alignment = "Caótico e Bom"

        p.reset()
        self.assertEqual(p.player_name, "")
        self.assertEqual(p.selected_race, "")
        self.assertEqual(p.selected_class, "")
        self.assertEqual(p.selected_background, "")
        self.assertEqual(p.selected_alignment, "")
        self.assertFalse(p._is_ready())
        self.assertIsNone(p.active_modal)

    def test_dragonborn_wizard_attributes_and_racial_equipment(self):
        """Valida os atributos de Draconato Mago (INT 15, CON 14, FOR 10, CAR 11) e o 3º item sendo o Item Único Racial."""
        p = self.panel
        p.player_name = "Ignisrax"
        p.selected_race = "Draconato"
        p.selected_class = "Mago"
        p.selected_background = "Sábio"
        p.selected_alignment = "Neutro"

        stats = p.get_current_stats()
        attrs = stats["attributes"]
        self.assertEqual(attrs["INT"], 15)
        self.assertEqual(attrs["CON"], 14)
        self.assertEqual(attrs["FOR"], 10)
        self.assertEqual(attrs["STR"], 10)
        self.assertEqual(attrs["CAR"], 11)
        self.assertEqual(attrs["CHA"], 11)
        self.assertEqual(attrs["DES"], 13)
        self.assertEqual(attrs["SAB"], 12)

        # O 3º item (índice 2) de stats["equipment"] deve ser o Item Único Racial do Draconato
        self.assertGreaterEqual(len(stats["equipment"]), 3)
        self.assertEqual(stats["equipment"][2], "Escama Ancestral Incandescente")
        self.assertEqual(stats["equipped_accessory"], "Escama Ancestral Incandescente")

        # Testa clique em Iniciar para validar final_char
        click_start = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.btn_start.center})
        res = p.handle_event(click_start)
        self.assertIsNotNone(res)
        char = res["char"]
        self.assertEqual(char["gender"], "male")
        self.assertEqual(char["equipped_accessory"], "Escama Ancestral Incandescente")
        self.assertEqual(char["equipment"]["accessory"], "Escama Ancestral Incandescente")

    def test_gender_indicator_and_assignment_human_cleric_vs_dragonborn_wizard(self):
        """Valida indicativo visual e atribuição de gender='female' para Humano+Clérigo e 'male' para Draconato+Mago."""
        p = self.panel
        self.assertIsInstance(p._badge_male_surf, pygame.Surface)
        self.assertIsInstance(p._badge_female_surf, pygame.Surface)

        # Caso 1: Humano + Clérigo -> female (Clériga ♀) e Sinete da Coroa Partida
        p.player_name = "Faen"
        p.selected_race = "Humano"
        p.selected_class = "Clérigo"
        p.selected_background = "Acólito"
        p.selected_alignment = "Leal e Bom"
        p.draw(self.screen)

        cls_modal = ClassSelectionPanel(p.data_lists["class"], selected_race="Humano")
        self.assertIn("♀", cls_modal.button_labels["Clérigo"])
        self.assertIn("Clériga", cls_modal.button_labels["Clérigo"])

        click_start = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": p.btn_start.center})
        res_fem = p.handle_event(click_start)
        char_fem = res_fem["char"]
        self.assertEqual(char_fem["gender"], "female")
        self.assertEqual(char_fem["class_display"], "Clériga")
        self.assertEqual(char_fem["equipped_accessory"], "Sinete da Coroa Partida")
        self.assertEqual(char_fem["gold"], 25)  # 15 base + 10 PO do Sinete da Coroa Partida

        # Caso 2: Draconato + Mago -> male (Mago ♂)
        p.reset()
        p.player_name = "Ignisrax"
        p.selected_race = "Draconato"
        p.selected_class = "Mago"
        p.selected_background = "Sábio"
        p.selected_alignment = "Neutro"
        p.draw(self.screen)

        res_male = p.handle_event(click_start)
        char_male = res_male["char"]
        self.assertEqual(char_male["gender"], "male")
        self.assertEqual(char_male["class_display"], "Mago")

    def test_loading_dice_animation_frames_and_roll_result(self):
        """Valida os 12 frames PNG gerados em assets/ui/dice_loading/ e o comportamento de LoadingDiceAnimation."""
        from ui.hud_components import LoadingDiceAnimation
        base_dir = os.path.normpath("assets/ui/dice_loading")
        self.assertTrue(os.path.isdir(base_dir))
        for i in range(1, 13):
            fpath = os.path.join(base_dir, f"frame_{i}.png")
            self.assertTrue(os.path.isfile(fpath), f"Frame ausente: {fpath}")

        anim = LoadingDiceAnimation()
        self.assertEqual(len(anim.frames), 12)
        self.assertIsInstance(anim._tray_surf, pygame.Surface)
        self.assertIsInstance(anim._banner_surf, pygame.Surface)

        # Desenho no modo de giro contínuo
        anim.draw(self.screen, 640, 360)

        # Modo de resultado: 20 Natural (Crítico), 1 Natural (Falha Crítica) e valor intermediário
        for roll_val, lbl in [(20, "Ataque"), (1, "Furtividade"), (14, "Percepção")]:
            anim.trigger_roll_result(roll_val, label=lbl, duration_ms=1200)
            self.assertTrue(anim.is_showing_result())
            self.assertEqual(anim.result_value, roll_val)
            anim.draw(self.screen, 640, 360)


if __name__ == "__main__":
    unittest.main()
