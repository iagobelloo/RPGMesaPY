import unittest
import os
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.font.init()

from core.dnd_rules import RACAS_5E, CLASSES, ANTECEDENTES_5E, TENDENCIAS_5E, MATRIZ_DE_PERICIAS
from ui.menu_components import CharacterCreationPanel
from ui.hud_components import BackpackModal, GrimoireModal
from ui.scene_renderer import SceneRenderer


class TestBloco8OpcaoB(unittest.TestCase):

    def test_orthography_and_no_mojibake(self):
        """Valida que dnd_rules não possui caracteres quebrados (Ã, Â, etc.)."""
        for raca, data in RACAS_5E.items():
            desc = data.get("descricao_ui", "")
            self.assertNotIn("Ã", desc, f"Mojibake na raça {raca}")
            self.assertNotIn("Â", desc, f"Mojibake na raça {raca}")

        for cls, data in CLASSES.items():
            desc = data.get("descricao_ui", "")
            self.assertNotIn("Ã", desc, f"Mojibake na classe {cls}")
            self.assertNotIn("Â", desc, f"Mojibake na classe {cls}")

        for tend, data in TENDENCIAS_5E.items():
            desc = data.get("descricao_ui", "")
            self.assertNotIn("Ã", desc, f"Mojibake na tendência {tend}")
            self.assertNotIn("Â", desc, f"Mojibake na tendência {tend}")
            self.assertTrue(len(desc) > 10)

        self.assertIn("Caótico e Bom", TENDENCIAS_5E)
        self.assertIn("Percepção", MATRIZ_DE_PERICIAS)
        self.assertIn("Prestidigitação", MATRIZ_DE_PERICIAS)

    def test_character_creation_hitboxes_and_padding(self):
        """Valida as hitboxes completas da ficha e suporte a textos longos."""
        panel = CharacterCreationPanel(0, 0, 1280, 720)
        self.assertIn("nome", panel.hitbox_map)
        self.assertIn("race", panel.hitbox_map)
        self.assertIn("class", panel.hitbox_map)
        self.assertIn("background", panel.hitbox_map)
        self.assertIn("alignment", panel.hitbox_map)

        # Hitbox de Antecedentes cobre a largura total da caixa na arte (> 250px)
        self.assertGreater(panel.hitbox_map["background"].width, 250)
        # Hitbox de Tendência cobre a largura total da caixa (> 250px)
        self.assertGreater(panel.hitbox_map["alignment"].width, 250)

    def test_backpack_modal(self):
        """Valida o funcionamento isolado da Mochila do Aventureiro."""
        bp = BackpackModal(100, 100, 800, 500)
        mock_game_state = {
            "player_character": {
                "name": "Valeros",
                "race": "Humano",
                "class": "Guerreiro",
                "gold": 25,
                "ac": 16,
                "equipped_weapon": "Espada Longa",
                "equipped_armor": "Cota de Malha",
                "has_shield": True,
                "inventory": ["Poção de Cura", "Corda de Cânhamo"]
            },
            "inventory": {"i_potion_healing": 2}
        }
        bp.game_state_ref = mock_game_state
        bp.is_visible = True

        consumables = bp._get_player_consumables()
        self.assertTrue(len(consumables) >= 1)

        # Simula clique fora para fechar
        dummy_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (10, 10), "button": 1})
        res = bp.handle_event(dummy_event)
        self.assertEqual(res, "close_backpack")

    def test_grimoire_modal_tabs_and_skill_tree(self):
        """Valida o Grimório aberto em 4 abas e a Árvore de Habilidades simplificada."""
        gm = GrimoireModal(100, 100, 800, 600)
        mock_game_state = {
            "player_character": {
                "name": "Elminster",
                "race": "Humano",
                "class": "Mago",
                "level": 2,
                "hp_current": 14,
                "hp_max": 14,
                "ac": 13,
                "xp": 350,
                "xp_to_next_level": 900,
                "attributes": {"STR": 10, "DEX": 14, "CON": 12, "INT": 18, "WIS": 13, "CHA": 11, "LUCK": 10},
                "spell_slots": {1: 3, 2: 1}
            },
            "prologue": "Nascido sob as estrelas arcanas...",
            "story_beat": 1
        }
        gm.game_state_ref = mock_game_state
        gm.is_visible = True

        # Teste de Árvore de Habilidades por classe (4 Tiers)
        skills_mago = gm._get_class_skill_tree("Mago")
        self.assertEqual(len(skills_mago), 4)
        self.assertEqual(skills_mago[0]["level"], 1)
        self.assertEqual(skills_mago[1]["level"], 2)

        skills_guerreiro = gm._get_class_skill_tree("Guerreiro")
        self.assertIn("Retomar o Fôlego", skills_guerreiro[0]["name"])
        self.assertIn("Surto de Ação", skills_guerreiro[1]["name"])

        # Troca de abas via clique
        event_tab_bestiary = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": gm.tab_bestiary_rect.center, "button": 1})
        gm.handle_event(event_tab_bestiary)
        self.assertEqual(gm.active_tab, "bestiario")

        event_tab_journal = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": gm.tab_journal_rect.center, "button": 1})
        gm.handle_event(event_tab_journal)
        self.assertEqual(gm.active_tab, "diario")

        event_tab_status = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": gm.tab_status_rect.center, "button": 1})
        gm.handle_event(event_tab_status)
        self.assertEqual(gm.active_tab, "status")

    def test_scene_renderer_chat_margins(self):
        """Valida as margens e dimensões calibradas do painel de chat."""
        renderer = SceneRenderer(1280, 720)
        panel_w = int(1280 * 0.40)
        msg_pc = {"text": "Avanço com cautela pela névoa fria da floresta.", "npc_falando": "Valeros", "type": "narrative"}
        formatted_pc = renderer._format_chat_message(msg_pc, panel_w)
        # Com retrato: largura menor que panel_w - 110 para respeitar scrollbar
        self.assertLessEqual(formatted_pc["msg_w"], panel_w - 115)

        msg_sys = {"text": "🎲 [DADO - TESTE] Percepção: 16 vs CD 12 ➔ SUCESSO!", "npc_falando": "nenhum", "type": "combat"}
        formatted_sys = renderer._format_chat_message(msg_sys, panel_w)
        # Sem retrato: largura menor que panel_w - 50 para respeitar scrollbar
        self.assertLessEqual(formatted_sys["msg_w"], panel_w - 50)


if __name__ == "__main__":
    unittest.main()

