import os
import unittest
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.font.init()

from ui.hud_components import GrimoireModal, BackpackModal, calculate_backpack_load


class TestGrimoireCharacterSheetUI(unittest.TestCase):
    """Suíte de validação da Ficha do Herói no Grimório, Pedestal 2.5D, 4 Slots, Carga, Árvore de Habilidades (4 Tiers) e Level Up."""

    def setUp(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.grimoire = GrimoireModal(240, 60, 800, 600)
        self.backpack = BackpackModal(220, 80, 840, 560)

        self.mock_state = {
            "player_character": {
                "name": "Alistair Valerius",
                "race": "Humano",
                "class": "Guerreiro",
                "gender": "male",
                "level": 1,
                "hp_current": 12,
                "hp_max": 12,
                "ac": 18,
                "initiative": 2,
                "speed": 9,
                "proficiency_bonus": 2,
                "xp": 350,
                "xp_to_next_level": 300,
                "has_pending_level_up": True,
                "gold": 45,
                "attributes": {
                    "STR": 16,
                    "DEX": 14,
                    "CON": 14,
                    "INT": 10,
                    "WIS": 12,
                    "CHA": 11,
                    "LUCK": 12
                },
                "equipped_weapon": "Espada Longa",
                "equipped_armor": "Cota de Malha",
                "has_shield": True,
                "equipment": {
                    "weapon": "Espada Longa",
                    "armor": "Cota de Malha",
                    "shield": "Escudo Heráldico",
                    "accessory": "Anel de Proteção"
                },
                "inventory": ["Espada Longa", "Cota de Malha", "Corda de Cânhamo"],
                "abilities": ["Retomar o Fôlego"]
            },
            "inventory": {
                "i_potion_healing": 4,
                "i_ration": 6
            },
            "story_beat": 1
        }
        self.grimoire.game_state_ref = self.mock_state
        self.grimoire.is_visible = True
        self.backpack.game_state_ref = self.mock_state
        self.backpack.is_visible = True

    def test_01_pre_rendered_surfaces_and_zero_garbage(self):
        """Valida que as superfícies do pedestal, slots de equipamento, ícones 40x40 e modal de Level Up são pré-alocadas."""
        self.assertIsNotNone(self.grimoire._pedestal_surf)
        self.assertEqual(self.grimoire._pedestal_surf.get_size(), (190, 48))

        self.assertIsNotNone(self.grimoire._equip_slot_surf)
        self.assertIsNotNone(self.grimoire._equip_slot_hover_surf)
        self.assertIsNotNone(self.grimoire._attr_box_surf)

        for state in ("acquired", "available", "locked"):
            self.assertIn(state, self.grimoire._skill_icon_frames)
            self.assertEqual(self.grimoire._skill_icon_frames[state].get_size(), (40, 40))

        self.assertIsNotNone(self.grimoire._levelup_overlay_surf)
        self.assertIsNotNone(self.grimoire._levelup_card_surf)

    def test_02_status_tab_standing_hero_and_4_equip_slots(self):
        """Valida renderização da aba 'status' (Ficha & Equipamentos), 4 slots visuais e botão de abrir mochila."""
        self.grimoire.active_tab = "status"
        self.grimoire.draw(self.screen)

        # Deve popular os 4 slots de equipamento (weapon, armor, shield, accessory)
        for slot_key in ("weapon", "armor", "shield", "accessory"):
            self.assertIn(slot_key, self.grimoire._equip_slot_rects)
            self.assertGreater(self.grimoire._equip_slot_rects[slot_key].width, 100)
            self.assertEqual(self.grimoire._equip_slot_rects[slot_key].height, 42)

        # Botão de abrir mochila deve estar ativo
        self.assertGreater(self.grimoire.btn_open_backpack.width, 200)

        # Clique no botão de abrir mochila deve retornar 'open_backpack'
        ev_bp = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": self.grimoire.btn_open_backpack.center, "button": 1})
        action = self.grimoire.handle_event(ev_bp)
        self.assertEqual(action, "open_backpack")

        # Clique em um slot de equipamento também deve retornar 'open_backpack'
        ev_slot = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": self.grimoire._equip_slot_rects["weapon"].center, "button": 1})
        action_slot = self.grimoire.handle_event(ev_slot)
        self.assertEqual(action_slot, "open_backpack")

    def test_03_backpack_and_grimoire_load_capacity_calculation(self):
        """Valida o cálculo de capacidade de carga (10 base + mod FOR, mín 10, máx 14) e lotes de poções/rações."""
        pc = self.mock_state["player_character"]
        # FOR = 16 -> Mod +3 -> Max slots = 13
        # Itens: 3 gerais na lista + 4 poções (ceil(4/3)=2 slots) + 6 rações (ceil(6/5)=2 slots) = 7 slots usados
        used, max_s = self.grimoire.get_load_capacity(pc)
        self.assertEqual(max_s, 13)
        self.assertEqual(used, 7)

        self.grimoire.active_tab = "status"
        self.grimoire.draw(self.screen)
        self.assertIn("7 / 13 Slots", self.grimoire.last_load_str)

        self.backpack.draw(self.screen)
        self.assertEqual(self.backpack.last_load_info, (7, 13))
        self.assertIn("7 / 13 Slots", self.backpack.last_load_str)

        # Testa limites mínimo (10) e máximo (14)
        pc["attributes"]["STR"] = 8  # Mod -1 -> min 10
        _, max_min = calculate_backpack_load(pc, self.mock_state)
        self.assertEqual(max_min, 10)

        pc["attributes"]["STR"] = 20  # Mod +5 -> max 14
        _, max_cap = calculate_backpack_load(pc, self.mock_state)
        self.assertEqual(max_cap, 14)

    def test_04_visual_skill_tree_all_6_classes_4_tiers(self):
        """Valida a Árvore de Habilidades Visual (4 Tiers: Nv 1, 2, 3, 5) para todas as 6 classes e seus 3 estados."""
        expected_classes = {
            "Guerreiro": ["Retomar o Fôlego", "Surto de Ação", "Foco do Campeão", "Ataque Extra"],
            "Clérigo": ["Bênção da Cura", "Canalizar Divindade", "Escudo da Fé", "Fogo Radiante"],
            "Mago": ["Recuperação Arcana", "Evocação Potente", "Escudo Arcano", "Mestre dos Elementos"],
            "Paladino": ["Cura pelas Mãos", "Destruição Divina", "Aura de Coragem", "Golpe Abençoado Extra"],
            "Patrulheiro": ["Marca do Caçador", "Estilo Arquearia", "Matador de Colossos", "Rajada de Flechas"],
            "Ladino": ["Ataque Furtivo", "Ação Ardilosa", "Emboscada Mortal", "Esquiva Sobrenatural"],
        }

        for cls_name, expected_names in expected_classes.items():
            tree = self.grimoire._get_class_skill_tree(cls_name)
            self.assertEqual(len(tree), 4, f"Classe {cls_name} deve ter 4 tiers")
            self.assertEqual([t["level"] for t in tree], [1, 2, 3, 5])
            self.assertEqual([t["name"] for t in tree], expected_names)

        # Verifica estados para herói Nível 1 com Level Up pendente
        pc = self.mock_state["player_character"]
        tree_w = self.grimoire._get_class_skill_tree("Guerreiro")
        self.assertEqual(self.grimoire._get_skill_state(tree_w[0], pc), "acquired")   # Nv 1
        self.assertEqual(self.grimoire._get_skill_state(tree_w[1], pc), "available")  # Nv 2 (pendente)
        self.assertEqual(self.grimoire._get_skill_state(tree_w[2], pc), "locked")     # Nv 3
        self.assertEqual(self.grimoire._get_skill_state(tree_w[3], pc), "locked")     # Nv 5

        # Desenha aba habilidades e verifica hitboxes 40x40 dos ícones quadrados
        self.grimoire.active_tab = "habilidades"
        self.grimoire.draw(self.screen)
        self.assertEqual(len(self.grimoire._skill_icon_rects), 4)
        for sk_id, icon_rect in self.grimoire._skill_icon_rects.items():
            self.assertEqual(icon_rect.size, (40, 40))

        # Simula clique no 2º tier para inspecionar e ver botão 'Aprender Habilidade'
        ev_click_node = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": self.grimoire._skill_node_rects["sk_warrior_2"].center, "button": 1})
        self.grimoire.handle_event(ev_click_node)
        self.assertEqual(self.grimoire.selected_skill_node, "sk_warrior_2")

        self.grimoire.draw(self.screen)
        self.assertGreater(self.grimoire.btn_learn_skill.width, 100)

    def test_05_interactive_level_up_modal_attribute_allocation_and_unlock(self):
        """Valida o fluxo completo do Modal Interativo de Level Up (+1 em 2 ou +2 em 1 atributo + nova habilidade)."""
        pc = self.mock_state["player_character"]
        self.grimoire.active_tab = "status"
        self.grimoire.draw(self.screen)

        # Clica em 'Subir de Nível ★' para abrir o modal de Level Up
        ev_lvl = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": self.grimoire.btn_level_up.center, "button": 1})
        res = self.grimoire.handle_event(ev_lvl)
        self.assertEqual(res, "open_level_up_modal")
        self.assertTrue(self.grimoire.level_up_modal_open)
        self.assertEqual(self.grimoire.level_up_points_left, 2)

        # Renderiza com o modal aberto para calcular hitboxes [+] e [-]
        self.grimoire.draw(self.screen)
        self.assertIn("STR", self.grimoire._lvlup_plus_rects)
        self.assertIn("CON", self.grimoire._lvlup_plus_rects)

        # Aloca +1 em STR e +1 em CON
        ev_plus_str = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": self.grimoire._lvlup_plus_rects["STR"].center, "button": 1})
        self.grimoire.handle_event(ev_plus_str)
        self.assertEqual(self.grimoire.level_up_alloc["STR"], 1)
        self.assertEqual(self.grimoire.level_up_points_left, 1)

        ev_plus_con = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": self.grimoire._lvlup_plus_rects["CON"].center, "button": 1})
        self.grimoire.handle_event(ev_plus_con)
        self.assertEqual(self.grimoire.level_up_alloc["CON"], 1)
        self.assertEqual(self.grimoire.level_up_points_left, 0)

        # Confirma evolução no modal
        ev_confirm = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": self.grimoire.btn_confirm_level_up.center, "button": 1})
        final_action = self.grimoire.handle_event(ev_confirm)
        self.assertEqual(final_action, "level_up")
        self.assertFalse(self.grimoire.level_up_modal_open)

        # Atributos devem ter subido (STR: 16->17, CON: 14->15) e 'Surto de Ação' desbloqueada
        self.assertEqual(pc["attributes"]["STR"], 17)
        self.assertEqual(pc["attributes"]["CON"], 15)
        self.assertIn("Surto de Ação", pc["abilities"])
        self.assertIn("sk_warrior_2", pc["unlocked_skills"])


if __name__ == "__main__":
    unittest.main()
