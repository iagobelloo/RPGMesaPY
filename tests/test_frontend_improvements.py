import unittest
import pygame
from ui.scene_renderer import SceneRenderer
from ui.hud_components import QuickActionBar, GrimoireModal
from ui.menu_components import CharacterCreationPanel


class TestFrontendImprovements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.Surface((1280, 720))

    # 1. Smart Anchor no Chat
    def test_smart_anchor_chat(self):
        renderer = SceneRenderer(1280, 720)
        
        # Insere mensagem anterior passando pelo painel
        msg1 = {"text": "Mensagem curta anterior.", "npc_falando": "Mestre", "type": "narrative"}
        renderer.draw_side_dialog_panel(self.screen, msg1)
        h1 = sum(pmsg["h"] + 15 for pmsg in renderer._formatted_messages)
        
        # Insere mensagem longa nova de Maelor (10 linhas)
        long_text = "Primeira linha do parágrafo épico.\n" + ("História continuando pelo pergaminho e estendendo além do limite...\n" * 8)
        msg2 = {"text": long_text, "npc_falando": "Maelor", "type": "narrative"}
        renderer.draw_side_dialog_panel(self.screen, msg2)
        
        # O scroll_y deve estar ancorado exatamente no topo da nova mensagem (h1)
        self.assertEqual(renderer.scroll_y, h1)

    # 2. Despoluição e Pílulas Visuais nos Logs Mecânicos
    def test_mechanical_logs_pills(self):
        renderer = SceneRenderer(1280, 720)
        
        # Adiciona rolagem de ataque com acerto
        log_hit = "🎲 [DADO - ATAQUE] Espada Longa: d20 (18) + Mod/Prof (+5) = 23 vs CA 14 ➔ ACERTO!"
        renderer.add_combat_log(log_hit)
        formatted_hit = renderer._formatted_messages[-1]
        self.assertFalse(formatted_hit["has_portrait"])
        self.assertEqual(formatted_hit["accent_color"], (55, 205, 95)) # Verde esmeralda para acerto
        self.assertTrue(len(formatted_hit["parsed_lines"]) > 0)
        
        # Adiciona rolagem de dano
        log_dmg = "🎲 [DADO - DANO] 12 de dano em Goblin (PV: 0/10)!"
        renderer.add_combat_log(log_dmg)
        formatted_dmg = renderer._formatted_messages[-1]
        self.assertEqual(formatted_dmg["accent_color"], (225, 65, 65)) # Vermelho carmesim para dano
        
        # Adiciona rolagem d20 neutra
        log_d20 = "🎲 [DADO - INICIATIVA] Rolagem de d20 (14) + Mod (+2) = 16"
        renderer.add_combat_log(log_d20)
        formatted_d20 = renderer._formatted_messages[-1]
        self.assertEqual(formatted_d20["accent_color"], (240, 195, 60)) # Ouro para d20
        
        # Renderização das pílulas sem exceções
        renderer.draw_side_dialog_panel(self.screen, None)

    # 3. QuickActionBar com Botões de Habilidades, Magias e Flyout
    def test_quick_action_bar_totems_and_flyout(self):
        bar = QuickActionBar(12, 644, 512, 28)
        
        # Modo exploração
        btn_ids = [b["id"] for b in bar.buttons]
        self.assertIn("skills", btn_ids)
        self.assertIn("spells", btn_ids)
        
        # Modo combate
        bar.set_combat_mode(True)
        combat_ids = [b["id"] for b in bar.buttons]
        self.assertIn("attack", combat_ids)
        self.assertIn("skills", combat_ids)
        self.assertIn("spells", combat_ids)
        
        # Configura herói com Guerreiro Nível 1
        hero = {
            "name": "Valerius",
            "class": "Guerreiro",
            "level": 1,
            "unlocked_skills": ["sk_warrior_1"],
            "abilities": ["Retomar o Fôlego"]
        }
        bar.player = hero
        active = bar.get_active_skills()
        self.assertTrue(any(s["name"] == "Retomar o Fôlego" for s in active))
        
        # Clique no botão skills abre flyout
        skills_btn = next(b for b in bar.buttons if b["id"] == "skills")
        evt_click_skills = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": skills_btn["rect"].center})
        res = bar.handle_event(evt_click_skills)
        self.assertEqual(res, "")
        self.assertTrue(bar.flyout_open)
        
        # Desenha flyout para registrar hitboxes dos itens
        bar.draw(self.screen, is_combat=True, player=hero)
        self.assertTrue(len(bar.flyout_items) > 0)
        
        # Clique no item de habilidade do flyout dispara ação
        first_item = bar.flyout_items[0]
        evt_click_item = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": first_item["rect"].center})
        action = bar.handle_event(evt_click_item)
        self.assertTrue(action.startswith("use_skill:"))
        self.assertIn("Retomar o Fôlego", action)
        self.assertFalse(bar.flyout_open)

    # 4. GrimoireModal com Botão Usar Habilidade quando Adquirida
    def test_grimoire_modal_use_skill_button(self):
        grimoire = GrimoireModal(50, 50, 800, 600)
        hero = {
            "name": "Valerius",
            "class": "Guerreiro",
            "level": 1,
            "unlocked_skills": ["sk_warrior_1"],
            "abilities": ["Retomar o Fôlego"]
        }
        grimoire.game_state_ref = {"player_character": hero}
        grimoire.is_visible = True
        grimoire.active_tab = "habilidades"
        grimoire.selected_skill_node = "sk_warrior_1"
        
        # Desenha a aba de habilidades
        grimoire.draw(self.screen)
        self.assertGreater(grimoire.btn_use_skill.width, 0)
        self.assertEqual(grimoire.btn_learn_skill.width, 0)
        
        # Clique no botão Usar Habilidade
        evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": grimoire.btn_use_skill.center})
        action = grimoire.handle_event(evt)
        self.assertTrue(action.startswith("use_skill:"))
        self.assertIn("Retomar o Fôlego", action)

    # 5. Ficha de Criação: Total na Coluna 1 e Modificador D&D 5e na Coluna 2
    def test_character_creation_total_and_mod(self):
        panel = CharacterCreationPanel()
        panel.is_visible = True
        panel.selected_class = "Guerreiro"
        panel.selected_race = "Anão"
        
        stats = panel.get_current_stats()
        # Guerreiro base FOR=15, CON=14; Anão ganha +2 CON
        # Total CON deve ser 16, Modificador D&D 5e (16 - 10) // 2 = +3
        con_total = stats["attributes"]["CON"]
        self.assertEqual(con_total, 16)
        con_mod = (con_total - 10) // 2
        self.assertEqual(con_mod, 3)
        
        # Renderiza a ficha sem exceções
        panel.draw(self.screen)

    # 6. Posicionamento de Combate em tavern_bg.jpg afastado da lareira
    def test_tavern_positioning_avoids_fireplace(self):
        renderer = SceneRenderer(1280, 720)
        
        # Em tavern_bg.jpg:
        # Lareira detectada entre X: 0.58 e 0.77 (742 a 985 px)
        # Inimigos devem ficar no flanco direito (>= 0.77 * 1280 = 985 px)
        # Jogador deve ficar no flanco esquerdo (0.42 a 0.58 * 1280 = 537 a 742 px)
        class MockSession:
            game_state = {
                "current_background": "tavern_bg.jpg",
                "player_character": {"name": "Herói", "race": "Humano", "class": "Guerreiro"}
            }
            active_visual_npcs = {"bandido": "m_bandit"}
            active_combat_targets = {"bandido": {"id": "bandido", "pv_atual": 10, "pv_max": 10, "faction": "enemy"}}
            game_mode = "COMBATE"
        
        hitboxes = renderer.draw_in_game(self.screen, MockSession())
        
        player_rect = hitboxes.get("player")
        enemy_rect = hitboxes.get("enemy_bandido") or hitboxes.get("bandido")
        
        self.assertIsNotNone(player_rect)
        self.assertIsNotNone(enemy_rect)
        
        # Jogador deve estar à esquerda da lareira (< 742 px)
        self.assertLess(player_rect.centerx, 742)
        # Inimigo deve estar à direita da lareira (>= 985 px)
        self.assertGreaterEqual(enemy_rect.x, 980)


if __name__ == "__main__":
    unittest.main()
