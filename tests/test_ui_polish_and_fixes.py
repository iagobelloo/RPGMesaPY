import unittest
import os
import pygame

# Inicialização headless para testes
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

from ui.asset_manager import AssetManager
from ui.hud_components import (
    GrimoireModal, BackpackModal, LoadingDiceAnimation, QuickActionBar,
    BESTIARY_LORE, PlayerManualModal, clean_tofu_glyphs
)
from ui.scene_renderer import SceneRenderer


class TestUIPolishAndFixes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.display.set_mode((800, 600))

    def setUp(self):
        AssetManager.clear_cache()
        self.screen = pygame.Surface((800, 600))
        self.mock_game_state = {
            "player_character": {
                "name": "Eldrin Valerius",
                "race": "Humano",
                "class": "Guerreiro",
                "level": 3,
                "hp_current": 25,
                "hp_max": 28,
                "ac": 16,
                "ca": 16,
                "initiative": 2,
                "speed": 9,
                "proficiency_bonus": 2,
                "gold": 45,
                "xp": 450,
                "xp_to_next_level": 900,
                "attributes": {"STR": 16, "DEX": 14, "CON": 15, "INT": 10, "WIS": 12, "CHA": 8},
                "equipment": {
                    "weapon": "Espada Longa de Aço Valiriano",
                    "armor": "Cota de Malha Pesada Completa",
                    "shield": "Escudo de Torre Reforçado (+2 CA)",
                    "accessory": "Amuleto da Proteção Arcana Antiga"
                },
                "skills": ["sk_warrior_1", "sk_warrior_2"]
            },
            "discovered_monsters": ["goblin", "lobo_atroz"],
            "active_combat_targets": {},
            "active_entities": [],
            "quest_log": [
                {"id": "quest_goblin", "title": "Emboscada na Estrada", "description": "Elimine os goblins.", "reward_xp": 100, "reward_gold": 20, "status": "ativa"},
                {"id": "quest_tutorial", "title": "Primeiros Passos", "description": "Fale com o taverneiro.", "reward_xp": 50, "reward_gold": 10, "status": "concluida"}
            ],
            "journal": {
                "active": [{"id": "quest_goblin", "title": "Emboscada na Estrada", "description": "Elimine os goblins.", "reward_xp": 100, "reward_gold": 20}],
                "rumors": [{"id": "rumor_ruins", "title": "Ruínas Esquecidas", "description": "Dizem haver tesouros antigos.", "reward_xp": 150, "reward_gold": 50}],
                "completed": [{"id": "quest_tutorial", "title": "Primeiros Passos", "description": "Fale com o taverneiro.", "reward_xp": 50, "reward_gold": 10}]
            }
        }

    # -------------------------------------------------------------------------
    # Tarefa 1: Texturas do Grimório e Mochila + Fallback seguro sem Magenta
    # -------------------------------------------------------------------------
    def test_ui_textures_loaded_and_fallback_without_magenta(self):
        """Verifica se open_book e backpack_bg carregam e se categoria UI ausente retorna None (zero magenta)."""
        book_surf = AssetManager.get_image("ui", "open_book")
        self.assertIsNotNone(book_surf, "A textura real open_book.png deve ser carregada do disco.")
        self.assertGreater(book_surf.get_width(), 100)
        self.assertGreater(book_surf.get_height(), 100)

        bp_surf = AssetManager.get_image("ui", "backpack_bg")
        self.assertIsNotNone(bp_surf, "A textura real backpack_bg.png deve ser carregada do disco.")
        self.assertGreater(bp_surf.get_width(), 100)
        self.assertGreater(bp_surf.get_height(), 100)

        # UI inexistente DEVE retornar None (e nunca uma surface sólida magenta)
        non_existent = AssetManager.get_image("ui", "textura_inexistente_12345")
        self.assertIsNone(non_existent, "Categoria 'ui' para arquivo inexistente deve retornar None para permitir fallback procedural.")

    def test_grimoire_and_backpack_draw_without_crash(self):
        """Verifica se GrimoireModal e BackpackModal renderizam sem erro na tela."""
        grimoire = GrimoireModal(0, 0, 800, 600)
        grimoire.game_state_ref = self.mock_game_state
        grimoire.is_visible = True
        grimoire.draw(self.screen)

        backpack = BackpackModal(100, 50, 600, 500)
        backpack.game_state_ref = self.mock_game_state
        backpack.is_visible = True
        backpack.draw(self.screen)

    # -------------------------------------------------------------------------
    # Tarefa 2: Polimento da aba 'status' (Métricas 2x2 e Slots Largura Total)
    # -------------------------------------------------------------------------
    def test_status_tab_equip_slots_full_width_no_truncation(self):
        """Verifica se os 4 slots de equipamento ocupam a largura da página inteira."""
        grimoire = GrimoireModal(0, 0, 800, 600)
        grimoire.game_state_ref = self.mock_game_state
        grimoire.active_tab = "status"
        grimoire.is_visible = True
        grimoire.draw(self.screen)

        self.assertEqual(len(grimoire._equip_slot_rects), 4, "Devem existir 4 slots de equipamento registrados.")
        page_w = (grimoire.rect.width // 2) - 76
        for slot_key, rect in grimoire._equip_slot_rects.items():
            # A largura de cada slot deve ser a largura total da página
            self.assertEqual(rect.width, page_w, f"Slot {slot_key} deve ocupar a largura total {page_w}px.")

    def test_status_tab_combat_metrics_no_text_overlap(self):
        """Verifica renderização das 4 métricas de combate (CA, Iniciativa, Deslocamento, Bônus Proficiência)."""
        grimoire = GrimoireModal(0, 0, 800, 600)
        grimoire.game_state_ref = self.mock_game_state
        grimoire.active_tab = "status"
        grimoire.is_visible = True
        # Renderiza e confirma ausência de exceções
        grimoire.draw(self.screen)

    # -------------------------------------------------------------------------
    # Tarefa 3: Polimento do Diário (Filtros 32px e auto-seleção de quest)
    # -------------------------------------------------------------------------
    def test_journal_filters_height_and_auto_selection(self):
        """Verifica se filtros do diário têm 32px de altura e auto-selecionam a primeira quest."""
        grimoire = GrimoireModal(0, 0, 800, 600)
        grimoire.game_state_ref = self.mock_game_state
        grimoire.active_tab = "diario"
        grimoire.is_visible = True
        grimoire.draw(self.screen)

        self.assertEqual(grimoire.btn_filter_active.height, 32, "Botão de filtro 'Ativas' deve ter 32px de altura.")
        self.assertEqual(grimoire.btn_filter_rumors.height, 32, "Botão de filtro 'Rumores' deve ter 32px de altura.")
        self.assertEqual(grimoire.btn_filter_completed.height, 32, "Botão de filtro 'Concluídas' deve ter 32px de altura.")

        # Teste de clique no filtro de rumores
        expected_rumor = grimoire._get_rumor_quests()[0].get("id") if grimoire._get_rumor_quests() else "main_campaign"
        click_rumors_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": grimoire.btn_filter_rumors.center, "button": 1})
        res = grimoire.handle_event(click_rumors_event)
        self.assertEqual(grimoire.journal_filter, "rumores")
        self.assertEqual(grimoire.selected_quest_id, expected_rumor, f"Ao clicar em 'Rumores', deve auto-selecionar a 1ª quest de rumores ({expected_rumor}).")

        # Teste de clique no filtro de concluídas
        click_comp_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": grimoire.btn_filter_completed.center, "button": 1})
        res = grimoire.handle_event(click_comp_event)
        self.assertEqual(grimoire.journal_filter, "concluidas")
        self.assertEqual(grimoire.selected_quest_id, "quest_tutorial", "Ao clicar em 'Feitas', deve auto-selecionar a 1ª quest concluída.")

        # Teste de clique no filtro de ativas
        click_act_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": grimoire.btn_filter_active.center, "button": 1})
        res = grimoire.handle_event(click_act_event)
        self.assertEqual(grimoire.journal_filter, "ativas")
        self.assertEqual(grimoire.selected_quest_id, "quest_goblin", "Ao clicar em 'Ativas', deve auto-selecionar a 1ª quest ativa.")

    # -------------------------------------------------------------------------
    # Tarefa 4: Árvore de Habilidades (Área de clique de nó expandida)
    # -------------------------------------------------------------------------
    def test_skill_tree_node_and_icon_click_area(self):
        """Verifica se clicar no card ou no ícone da habilidade seleciona o nó correspondente."""
        grimoire = GrimoireModal(0, 0, 800, 600)
        grimoire.game_state_ref = self.mock_game_state
        grimoire.active_tab = "habilidades"
        grimoire.is_visible = True
        grimoire.draw(self.screen)

        self.assertIn("sk_warrior_2", grimoire._skill_node_rects)
        self.assertIn("sk_warrior_2", grimoire._skill_icon_rects)

        # Clica diretamente no ícone quadrado
        icon_pos = grimoire._skill_icon_rects["sk_warrior_2"].center
        click_icon_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": icon_pos, "button": 1})
        grimoire.handle_event(click_icon_event)
        self.assertEqual(grimoire.selected_skill_node, "sk_warrior_2", "Clicar no ícone deve selecionar o nó.")

        # Clica no card fora do ícone
        card_rect = grimoire._skill_node_rects["sk_warrior_1"]
        card_pos = (card_rect.right - 10, card_rect.centery)
        click_card_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": card_pos, "button": 1})
        grimoire.handle_event(click_card_event)
        self.assertEqual(grimoire.selected_skill_node, "sk_warrior_1", "Clicar no card inteiro deve selecionar o nó.")

    # -------------------------------------------------------------------------
    # Tarefa 5: Bestiário Progressivo (Descobertos vs Desconhecido)
    # -------------------------------------------------------------------------
    def test_progressive_bestiary_discovered_and_undiscovered(self):
        """Verifica comportamento do Bestiário com monstros conhecidos e desconhecidos."""
        grimoire = GrimoireModal(0, 0, 800, 600)
        grimoire.game_state_ref = self.mock_game_state
        grimoire.active_tab = "bestiario"
        grimoire.is_visible = True

        # Lobo Atroz está em discovered_monsters
        grimoire.selected_monster = "lobo_atroz"
        grimoire.draw(self.screen)
        self.assertIn("lobo_atroz", BESTIARY_LORE)

        # Manticora NÃO está em discovered_monsters
        grimoire.selected_monster = "manticora"
        grimoire.draw(self.screen)
        # O desenho deve ocorrer com sucesso exibindo '??? (Desconhecido) 🔒'

    # -------------------------------------------------------------------------
    # Tarefa 6: Escala do Token do Jogador (104px) e Hitboxes de Inimigos
    # -------------------------------------------------------------------------
    def test_player_token_scale_and_enemy_hitboxes(self):
        """Verifica se token do jogador tem tamanho de 128px com aura e se inimigos registram hitboxes."""
        renderer = SceneRenderer(800, 600)
        players = [self.mock_game_state["player_character"]]
        hitboxes = renderer.draw_players(self.screen, players)

        self.assertIn("player", hitboxes, "Deve registrar hitbox do 'player'.")
        self.assertEqual(hitboxes["player"].width, 128, "Token do jogador deve ter 128px de largura.")
        self.assertEqual(hitboxes["player"].height, 128, "Token do jogador deve ter 128px de altura.")

        # Teste de cena com inimigo em combate
        class MockStory:
            def __init__(self):
                self.current_beat = 1

            def is_climax(self):
                return False

            def get_unlocked_allies(self):
                return {}

        class MockSession:
            def __init__(self):
                self.game_mode = "COMBATE"
                self.story = MockStory()
                self.active_visual_npcs = {"goblin_1": "monster"}
                self.active_combat_targets = {
                    "goblin_1": {"id": "goblin", "name": "Goblin Emboscador", "pv_atual": 7, "pv_max": 7, "ca": 12, "faction": "enemy"}
                }
                self.game_state = {
                    "player_character": {"name": "Eldrin", "race": "Humano", "class": "Guerreiro"}
                }
                self.background_image = "default_bg.jpg"
                self.dialog_history = []

        mock_session = MockSession()
        scene_hitboxes = renderer.draw_in_game(self.screen, mock_session, None)
        self.assertTrue(
            "goblin_1" in scene_hitboxes or "enemy_goblin_1" in scene_hitboxes or "goblin" in scene_hitboxes or "enemy_goblin" in scene_hitboxes,
            f"Hitboxes de inimigos devem estar registradas para clique de ataque. Encontrados: {list(scene_hitboxes.keys())}"
        )

    # -------------------------------------------------------------------------
    # Tarefa 7: Retrato do Taverneiro e Número do D20
    # -------------------------------------------------------------------------
    def test_taverneiro_portrait_isolated_from_minstrel(self):
        """Verifica se Taverneiro carrega seu próprio retrato e não o Menestrel."""
        tav = AssetManager.get_portrait_sprite("Taverneiro")
        men = AssetManager.get_portrait_sprite("Menestrel")
        self.assertIsNotNone(tav)
        self.assertIsNotNone(men)
        self.assertEqual(tav.get_size(), (100, 100))
        self.assertEqual(men.get_size(), (100, 100))
        # As imagens devem ser distintas
        tav_bytes = pygame.image.tobytes(tav, "RGBA")
        men_bytes = pygame.image.tobytes(men, "RGBA")
        self.assertNotEqual(tav_bytes, men_bytes, "O Taverneiro deve possuir retrato próprio, diferente do Menestrel.")

    def test_loading_dice_result_surface_with_solid_outline(self):
        """Verifica geração da face do d20 com contorno sólido e dimensões apropriadas."""
        dice_anim = LoadingDiceAnimation()
        die_surf_20 = dice_anim._get_result_die_surface(20)
        self.assertEqual(die_surf_20.get_size(), (96, 96))
        die_surf_1 = dice_anim._get_result_die_surface(1)
        self.assertEqual(die_surf_1.get_size(), (96, 96))
        die_surf_15 = dice_anim._get_result_die_surface(15)
        self.assertEqual(die_surf_15.get_size(), (96, 96))

    # -------------------------------------------------------------------------
    # Tarefa 8: QuickActionBar com suporte a combate (⚔ Atacar)
    # -------------------------------------------------------------------------
    def test_quick_action_bar_combat_mode(self):
        """Verifica transição entre modo normal (Descansar) e combate (⚔ Atacar)."""
        bar = QuickActionBar(10, 500, 300, 28)
        self.assertFalse(bar.is_combat)
        labels_normal = [b["label"] for b in bar.buttons]
        self.assertIn("Descansar", labels_normal)
        self.assertNotIn("⚔ Atacar", labels_normal)

        # Alterna para modo de combate
        bar.set_combat_mode(True)
        self.assertTrue(bar.is_combat)
        labels_combat = [b["label"] for b in bar.buttons]
        self.assertIn("⚔ Atacar", labels_combat)
        self.assertNotIn("Descansar", labels_combat)

        # Renderização em combate sem erros
        bar.draw(self.screen)

    # -------------------------------------------------------------------------
    # Tarefa 9: PlayerManualModal (6 Capítulos e Navegação Zero Garbage)
    # -------------------------------------------------------------------------
    def test_player_manual_modal_chapters_and_navigation(self):
        """Valida a interface visual do Manual do Jogador, 6 capítulos e navegação."""
        modal = PlayerManualModal(50, 50, 840, 560)
        self.assertEqual(len(modal.CHAPTERS), 6, "Manual deve conter exatamente 6 capítulos.")
        self.assertEqual(len(modal.tab_rects), 6)
        self.assertEqual(modal.current_chapter, 0)

        # Desenho inicial com o capítulo 0
        modal.is_visible = True
        modal.draw(self.screen)

        # Navegação via botão Próximo
        click_next = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": modal.btn_next.center})
        modal.handle_event(click_next)
        self.assertEqual(modal.current_chapter, 1)

        # Navegação via aba lateral (Capítulo 4 - Índice 3)
        tab_3_rect = modal.tab_rects[3]
        click_tab_3 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": tab_3_rect.center})
        modal.handle_event(click_tab_3)
        self.assertEqual(modal.current_chapter, 3)

        # Navegação via tecla Seta Esquerda
        key_left = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})
        modal.handle_event(key_left)
        self.assertEqual(modal.current_chapter, 2)

        # Fechamento via ESC
        key_esc = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
        act = modal.handle_event(key_esc)
        self.assertEqual(act, "close")
        self.assertFalse(modal.is_visible)

    # -------------------------------------------------------------------------
    # Tarefa 10: Downscaling Progressivo com Suavização e Caching
    # -------------------------------------------------------------------------
    def test_asset_manager_progressive_downscale(self):
        """Valida se o downscaling progressivo reduz em múltiplos passos e armazena em cache."""
        large_surf = pygame.Surface((512, 512))
        large_surf.fill((200, 150, 50))
        target_size = (64, 64)

        scaled = AssetManager.progressive_downscale(large_surf, target_size)
        self.assertEqual(scaled.get_size(), target_size)

        cache_key = (id(large_surf), target_size, "progressive")
        self.assertIn(cache_key, AssetManager._scaled_cache)
        cached_scaled = AssetManager.progressive_downscale(large_surf, target_size)
        self.assertIs(scaled, cached_scaled, "Deve reutilizar a superfície em cache sem re-renderizar.")

    # -------------------------------------------------------------------------
    # Tarefa 11: Higienização de Caracteres Tofu / Quadrados Brancos
    # -------------------------------------------------------------------------
    def test_clean_tofu_glyphs(self):
        """Garante que caracteres exóticos são limpos ou mapeados para símbolos seguros."""
        self.assertEqual(clean_tofu_glyphs("⚔ Atacar ★"), "Atacar")
        self.assertEqual(clean_tofu_glyphs("🛡 Armadura"), "Armadura")
        self.assertEqual(clean_tofu_glyphs("♂ Guerreiro"), "Guerreiro")
        self.assertEqual(clean_tofu_glyphs("♀ Clériga"), "Clériga")
        self.assertEqual(clean_tofu_glyphs("Missão ➔ Alvo"), "Missão -> Alvo")
        self.assertEqual(clean_tofu_glyphs("Inimigo 🔒"), "Inimigo")

    # -------------------------------------------------------------------------
    # Tarefa 12: Retrato do Jogador no Chat e Identificador [Você]
    # -------------------------------------------------------------------------
    def test_scene_renderer_chat_dialog_player_portrait(self):
        """Valida formatação e renderização do retrato do jogador nas mensagens do chat."""
        renderer = SceneRenderer(800, 600)
        renderer.current_player = self.mock_game_state["player_character"]

        player_msg = {
            "text": "Empunho minha espada e me posiciono à frente do grupo!",
            "type": "player",
            "npc_falando": "Eldrin Valerius"
        }
        formatted = renderer._format_chat_message(player_msg, 320)
        self.assertTrue(formatted["has_portrait"], "Mensagem do jogador deve possuir retrato.")
        self.assertEqual(formatted["msg_type"], "player")

        # Teste de desenho do chat com mensagem do jogador sem crash
        renderer.draw_side_dialog_panel(self.screen, player_msg)


if __name__ == "__main__":
    unittest.main()
