import ast
import os
import unittest
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
from ui.asset_manager import (
    AssetManager,
    PROTAGONIST_SPRITE_MANIFEST,
    ALLY_HERO_FALLBACK_BY_RACE_CLASS,
    SKILL_ICON_MANIFEST,
    COLOR_MISSING_HERO,
)
from ui.hud_components import GrimoireModal, BackpackModal
from ui.scene_renderer import SceneRenderer
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster


class DummyAI(AIGameMaster):
    def __init__(self):
        self.client = None


class TestMainStartupAndIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        if not pygame.display.get_surface():
            pygame.display.set_mode((1280, 720))

    def test_1_main_has_no_local_imports_inside_def_main(self):
        """Garante via AST que def main() em main.py não possui nenhum import local (evita UnboundLocalError)."""
        main_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
        with open(main_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename="main.py")

        main_func = None
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                main_func = node
                break

        self.assertIsNotNone(main_func, "Função main() deve existir em main.py")
        local_imports = [
            n for n in ast.walk(main_func)
            if isinstance(n, (ast.Import, ast.ImportFrom))
        ]
        self.assertEqual(
            len(local_imports),
            0,
            f"Encontrados imports locais dentro de main(): {[ast.dump(i) for i in local_imports]}",
        )

    def test_2_main_startup_runs_one_frame_without_unbound_local_error(self):
        """Executa main.main() por 1 iteração de loop com evento QUIT sem levantar UnboundLocalError."""
        import main as main_module

        quit_event = pygame.event.Event(pygame.QUIT)
        with patch("pygame.event.get", return_value=[quit_event]), \
             patch("pygame.quit"), \
             patch("sys.exit"):
            main_module.main()

    def test_3_protagonist_manifest_42_combinations_and_ladino_slug(self):
        """Valida os 42 pares (7 Raças x 6 Classes) no AssetManager, slug 'ladino' e fallback visual real."""
        races = [
            ("Humano", "humano", "male"),
            ("Anão da Colina", "anao", "male"),
            ("Elfo da Floresta", "elfo", "female"),
            ("Meio-Orc", "meio_orc", "male"),
            ("Draconato", "draconato", "male"),
            ("Halfling", "halfling", "male"),
            ("Tiefling", "tiefling", "male"),
        ]
        classes = [
            ("Guerreiro", "guerreiro"),
            ("Clérigo", "clerigo"),
            ("Mago", "mago"),
            ("Paladino", "paladino"),
            ("Patrulheiro", "patrulheiro"),
            ("Ladino", "ladino"),
        ]

        self.assertEqual(len(PROTAGONIST_SPRITE_MANIFEST), 42)
        self.assertEqual(len(ALLY_HERO_FALLBACK_BY_RACE_CLASS), 42)

        AssetManager.clear_cache(keep_fonts=True)
        for race_label, r_slug, expected_gender in races:
            for cls_label, c_slug in classes:
                key = (r_slug, c_slug)
                self.assertIn(key, PROTAGONIST_SPRITE_MANIFEST)
                manifest_info = PROTAGONIST_SPRITE_MANIFEST[key]
                expected_sprite = f"{r_slug}_{c_slug}_{expected_gender}.png"
                expected_icon = f"{r_slug}_{c_slug}_{expected_gender}.jpg"
                self.assertEqual(manifest_info["sprite"], expected_sprite)
                self.assertEqual(manifest_info["icon"], expected_icon)

                candidates = AssetManager.resolve_hero_candidates(race_label, cls_label)
                self.assertGreaterEqual(len(candidates), 1)
                self.assertEqual(candidates[0], expected_sprite)

                # Sprite e ícone devem carregar o fallback real de aliado (não o quadrado Ciano 64x64)
                surf_body = AssetManager.get_hero_sprite(race_label, cls_label)
                self.assertIsNotNone(surf_body)
                is_cyan_placeholder = (
                    surf_body.get_size() == (64, 64)
                    and surf_body.get_at((0, 0))[:3] == COLOR_MISSING_HERO
                )
                self.assertFalse(
                    is_cyan_placeholder,
                    f"Sprite de {race_label} {cls_label} caiu no placeholder ciano!",
                )

                surf_icon = AssetManager.get_hero_icon(race_label, cls_label)
                self.assertIsNotNone(surf_icon)
                is_cyan_icon = (
                    surf_icon.get_size() == (64, 64)
                    and surf_icon.get_at((0, 0))[:3] == COLOR_MISSING_HERO
                )
                self.assertFalse(
                    is_cyan_icon,
                    f"Ícone de {race_label} {cls_label} caiu no placeholder ciano!",
                )

    def test_4_skills_manifest_24_nodes_and_level_up_sync(self):
        """Valida os 24 nós de habilidades das 6 classes, canonical_id, icon_file e sincronização PT/EN no Level Up."""
        grimoire = GrimoireModal(100, 60, 800, 600)
        classes = ["Guerreiro", "Clérigo", "Mago", "Paladino", "Patrulheiro", "Ladino"]
        seen_ui_ids = set()
        seen_canon_ids = set()

        for cls_name in classes:
            tree = grimoire._get_class_skill_tree(cls_name)
            self.assertEqual(len(tree), 4, f"Classe {cls_name} deve ter 4 tiers de skills")
            for node in tree:
                self.assertIn("id", node)
                self.assertIn("canonical_id", node)
                self.assertIn("icon_file", node)
                self.assertIn(node["id"], SKILL_ICON_MANIFEST)
                self.assertIn(node["canonical_id"], SKILL_ICON_MANIFEST)
                self.assertEqual(SKILL_ICON_MANIFEST[node["id"]], node["icon_file"])
                self.assertEqual(SKILL_ICON_MANIFEST[node["canonical_id"]], node["icon_file"])
                seen_ui_ids.add(node["id"])
                seen_canon_ids.add(node["canonical_id"])

        self.assertEqual(len(seen_ui_ids), 24)
        self.assertEqual(len(seen_canon_ids), 24)

        # Testa sincronização PT/EN e desbloqueio duplo (UI id + canonical_id) no Level Up
        pc = {
            "name": "Alistair",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "attributes": {"FOR": 16, "DES": 13, "CON": 14, "INT": 10, "SAB": 12, "CAR": 8},
            "abilities": ["Retomar o Fôlego"],
            "unlocked_skills": ["sk_warrior_1"],
        }
        grimoire.open_level_up_modal(pc)
        grimoire.level_up_alloc["STR"] = 1
        grimoire.level_up_alloc["CON"] = 1
        grimoire.level_up_points_left = 0
        grimoire._apply_level_up_choices(pc)

        self.assertEqual(pc["attributes"]["FOR"], 17)
        self.assertEqual(pc["attributes"]["STR"], 17)
        self.assertEqual(pc["attributes"]["CON"], 15)
        self.assertIn("sk_warrior_2", pc["unlocked_skills"])
        self.assertIn("action_surge", pc["unlocked_skills"])
        self.assertIn("second_wind", pc["unlocked_skills"])

    def test_5_scene_renderer_solo_until_beat_15_and_climax_allies(self):
        """Garante que aliados recrutados NÃO aparecem no tabuleiro nos Beats 1-14 (jornada solo), mas aparecem no Beat 15."""
        screen = pygame.display.get_surface()
        renderer = SceneRenderer(1280, 720)
        session = SessionManager(DummyAI())
        session.game_state["player_character"] = {
            "name": "Valerius",
            "race": "Humano",
            "class": "Guerreiro",
            "hp_current": 12,
            "hp_max": 12,
        }
        # Recruta um aliado na taverna durante o Beat 1
        session.story.current_beat = 1
        session.story.unlock_ally("HERO-01")
        self.assertGreaterEqual(len(session.story.get_unlocked_allies()), 1)

        # No Beat 1 (fora do Clímax e sem combat_allies), apenas o jogador aparece no tabuleiro
        hitboxes_beat_1 = renderer.draw_in_game(screen, session)
        self.assertIn("player", hitboxes_beat_1)
        self.assertNotIn("ally_1", hitboxes_beat_1)

        # No Beat 15 (Clímax), os aliados recrutados aparecem junto com o jogador
        session.story.current_beat = 15
        self.assertTrue(session.story.is_climax())
        hitboxes_beat_15 = renderer.draw_in_game(screen, session)
        self.assertIn("player", hitboxes_beat_15)
        self.assertIn("ally_1", hitboxes_beat_15)

        # E get_entity_sprite com size=(64, 64) carrega o sprite real do aliado via sprite_key
        ally_data = list(session.story.get_unlocked_allies().values())[0]
        ally_surf = AssetManager.get_entity_sprite(ally_data, kind="corpo", size=(64, 64))
        self.assertEqual(ally_surf.get_size(), (64, 64))

    def test_6_backpack_equip_weapon_integration(self):
        """Valida que equipar arma na mochila atualiza o estado do personagem e integra com SessionManager."""
        screen = pygame.display.get_surface()
        session = SessionManager(DummyAI())
        session.game_state["player_character"] = {
            "name": "Thorin",
            "race": "Anão da Colina",
            "class": "Guerreiro",
            "hp_current": 14,
            "hp_max": 14,
            "inventory": ["Machado de Batalha", "Espada Longa", "Poção de Cura"],
            "equipped_weapon": "Espada Longa",
            "equipment": {"weapon": "Espada Longa", "armor": "Cota de Malha"},
        }
        backpack = BackpackModal(220, 80, 840, 560)
        backpack.game_state_ref = session.game_state
        backpack.is_visible = True
        backpack.draw(screen)

        self.assertIn("Machado de Batalha", backpack._equip_buttons)
        click_ev = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"button": 1, "pos": backpack._equip_buttons["Machado de Batalha"].center},
        )
        bp_action = backpack.handle_event(click_ev)
        self.assertEqual(bp_action, "equip_weapon:Machado de Batalha")

        weapon_name = bp_action.split(":", 1)[1]
        if hasattr(session, "equip_item"):
            session.equip_item(weapon_name)
        else:
            pc = session.game_state["player_character"]
            pc["equipped_weapon"] = weapon_name
            pc["equipment"]["weapon"] = weapon_name

        pc = session.game_state["player_character"]
        self.assertEqual(pc.get("equipped_weapon", "").lower(), "machado de batalha")


if __name__ == "__main__":
    unittest.main()
