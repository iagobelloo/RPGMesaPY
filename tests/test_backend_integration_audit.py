import json
import os
import unittest

from core.combat_system import CombatManager, resolve_action, resolve_skill_effect
from core.dnd_rules import (
    CLASSES,
    PROTAGONIST_CLASS_ORDER,
    PROTAGONIST_RACE_ORDER,
    SKILL_CANONICAL_TO_UI,
    SKILL_UI_TO_CANONICAL,
    CharacterCalculator,
    expand_unlocked_skills,
    get_protagonist_gender_info,
    normalize_skill_id,
)
from core.game_engine import SessionManager


class TestBackendIntegrationAudit(unittest.TestCase):
    """Testes de auditoria de integração do backend D&D 5e."""

    def test_01_teste_pericia_no_name_error_and_bilingual_attrs(self):
        """Garante que teste_pericia não lança NameError('prof') e lê atributos em PT e EN."""
        # Ficha com atributos apenas em PT
        pc_pt = {
            "name": "Aldric",
            "class": "Guerreiro",
            "level": 5,
            "proficiency_bonus": 3,
            "hp_current": 40,
            "hp_max": 40,
            "attributes": {"FOR": 18, "DES": 14, "CON": 16, "INT": 10, "SAB": 12, "CAR": 8},
            "skills": ["Atletismo", "Percepção"],
        }
        parsed_ath = {"tipo_acao": "teste_pericia", "recurso_utilizado": "Atletismo"}
        res_pt = resolve_action(parsed_ath, pc_pt, [], {}, {})
        self.assertIn("sys_log", res_pt)
        self.assertIn("Atletismo", res_pt["sys_log"])
        # FOR 18 (+4) + prof (+3) = +7
        self.assertIn("+ 7 =", res_pt["sys_log"])

        # Ficha com atributos apenas em EN
        pc_en = {
            "name": "Lyra",
            "class": "Ladino",
            "level": 1,
            "proficiency_bonus": 2,
            "hp_current": 10,
            "hp_max": 10,
            "attributes": {"STR": 10, "DEX": 18, "CON": 12, "INT": 14, "WIS": 14, "CHA": 12},
            "pericias_treinadas": ["Furtividade"],
        }
        parsed_stealth = {"tipo_acao": "teste_pericia", "recurso_utilizado": "Furtividade"}
        res_en = resolve_action(parsed_stealth, pc_en, [], {}, {})
        self.assertIn("Furtividade", res_en["sys_log"])
        # DEX 18 (+4) + prof (+2) = +6
        self.assertIn("+ 6 =", res_en["sys_log"])

    def test_02_all_42_allies_use_real_actions_in_combat(self):
        """Garante que os 42 aliados de heroes_lore.json usam suas actions reais no combate."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        lore_path = os.path.join(base_dir, "data", "heroes_lore.json")
        with open(lore_path, "r", encoding="utf-8") as f:
            raw_lore = json.load(f)
            heroes_data = raw_lore.get("heroes", raw_lore)

        self.assertEqual(len(heroes_data), 42, "O compêndio deve conter exatamente 42 aliados.")

        # Testa amostra representativa e valida estrutura de todos os 42
        for h_id, h_data in heroes_data.items():
            actions = h_data.get("actions", [])
            self.assertTrue(len(actions) > 0, f"Aliado {h_id} sem actions em heroes_lore.json")
            expected_action_names = [a.get("name") for a in actions]

            pc = {
                "name": "Protagonista",
                "class": "Guerreiro",
                "level": 3,
                "hp_current": 28,
                "hp_max": 28,
                "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "SAB": 10, "CAR": 10},
            }
            enemy = {
                "name": "Orc Batedor",
                "pv_atual": 50,
                "pv_max": 50,
                "ca": 8,
                "tipo_bestiario": "orc",
                "faction": "enemy",
            }
            ally = {
                "name": h_data["name"],
                "pv_atual": h_data.get("pv_max", 20),
                "pv_max": h_data.get("pv_max", 20),
                "ca": h_data.get("ca", 15),
                "tipo_bestiario": h_data.get("tipo_bestiario", "guerreiro"),
                "faction": "ally",
                "actions": actions,
            }
            active_targets = {
                "Orc Batedor": enemy,
                h_data["name"]: ally,
            }
            parsed = {"tipo_acao": "movimento", "alvo": ["nenhum"]}
            res = resolve_action(parsed, pc, [], active_targets, {})
            log = res["sys_log"]
            self.assertIn(f"[DADO - ALIADO] {h_data['name']} usou ", log)
            self.assertTrue(
                any(act_name in log for act_name in expected_action_names),
                f"Aliado {h_data['name']} ({h_id}) não usou nenhuma de suas actions reais {expected_action_names}. Log: {log}",
            )

    def test_03_skill_ids_mapping_and_passive_bonuses(self):
        """Testa mapeamento bidirecional sk_* <-> canônico e ativação de passivas com ambos os IDs."""
        self.assertEqual(len(SKILL_UI_TO_CANONICAL), 24)
        self.assertEqual(len(SKILL_CANONICAL_TO_UI), 24)

        for ui_id, can_id in SKILL_UI_TO_CANONICAL.items():
            self.assertEqual(normalize_skill_id(ui_id), can_id)
            expanded = expand_unlocked_skills([ui_id])
            self.assertIn(ui_id, expanded)
            self.assertIn(can_id, expanded)

        # Testa passiva do Ladino com ID canônico ("sneak_attack")
        rogue_pc = {
            "name": "Vex",
            "class": "Ladino",
            "level": 3,
            "hp_current": 24,
            "hp_max": 24,
            "attributes": {"FOR": 10, "DES": 18, "CON": 14, "INT": 12, "SAB": 12, "CAR": 14},
            "unlocked_skills": ["sneak_attack"],
        }
        dummy = {"name": "Alvo Treino", "pv_atual": 100, "pv_max": 100, "ca": 1, "faction": "enemy"}
        res_atk = resolve_action(
            {"tipo_acao": "ataque_fisico", "recurso_utilizado": "Adaga", "alvo": ["Alvo Treino"]},
            rogue_pc,
            [dummy],
            {"Alvo Treino": dummy},
            {},
        )
        # Se não tirou 1 natural, deve ativar Ataque Furtivo; testamos até acertar (máx 10 tentativas)
        for _ in range(10):
            if "Ataque Furtivo" in res_atk["sys_log"]:
                break
            res_atk = resolve_action(
                {"tipo_acao": "ataque_fisico", "recurso_utilizado": "Adaga", "alvo": ["Alvo Treino"]},
                rogue_pc,
                [dummy],
                {"Alvo Treino": dummy},
                {},
            )
        self.assertIn("Ataque Furtivo", res_atk["sys_log"])

    def test_04_active_skills_resolution_combat_and_exploration(self):
        """Testa resolução de habilidades ativas (Retomar o Fôlego, Cura pelas Mãos, Recuperação Arcana, Surto de Ação)."""
        # 1. Second Wind (Retomar o Fôlego) com ID canônico e sk_warrior_1
        warrior = {
            "name": "Kaelen",
            "class": "Guerreiro",
            "level": 3,
            "hp_current": 10,
            "hp_max": 30,
            "attributes": {"FOR": 16, "DES": 12, "CON": 16, "INT": 10, "SAB": 12, "CAR": 10},
            "unlocked_skills": ["second_wind", "action_surge"],
        }
        res_sw = resolve_action(
            {"tipo_acao": "habilidade", "recurso_utilizado": "second_wind"},
            warrior,
            [],
            {},
            {},
        )
        self.assertGreater(warrior["hp_current"], 10)
        self.assertIn("Retomar o Fôlego", res_sw["sys_log"])

        # 2. Lay on Hands (Cura pelas Mãos) -> level * 5
        paladin = {
            "name": "Thrain",
            "class": "Paladino",
            "level": 4,
            "hp_current": 5,
            "hp_max": 40,
            "attributes": {"FOR": 16, "DES": 10, "CON": 14, "INT": 10, "SAB": 12, "CAR": 16},
            "unlocked_skills": ["sk_paladin_1"],
        }
        res_loh = resolve_action(
            {"tipo_acao": "habilidade", "recurso_utilizado": "sk_paladin_1"},
            paladin,
            [],
            {},
            {},
        )
        self.assertEqual(paladin["hp_current"], 25)  # 5 + (4 * 5) = 25
        self.assertIn("Cura pelas Mãos", res_loh["sys_log"])

        # 3. Arcane Recovery (Recuperação Arcana) -> +1 slot nível 1
        mage = {
            "name": "Gale",
            "class": "Mago",
            "level": 2,
            "hp_current": 14,
            "hp_max": 14,
            "spell_slots": {"1": 0, "2": 0},
            "attributes": {"FOR": 8, "DES": 14, "CON": 14, "INT": 17, "SAB": 12, "CAR": 10},
            "unlocked_skills": ["arcane_recovery"],
        }
        res_arc = resolve_action(
            {"tipo_acao": "habilidade", "recurso_utilizado": "arcane_recovery"},
            mage,
            [],
            {},
            {},
        )
        self.assertEqual(mage["spell_slots"]["1"], 1)
        self.assertIn("Recuperação Arcana", res_arc["sys_log"])

        # 4. Action Surge (Surto de Ação) contra inimigo
        enemy = {"name": "Goblin", "pv_atual": 30, "pv_max": 30, "ca": 8, "faction": "enemy"}
        res_as = resolve_action(
            {"tipo_acao": "habilidade", "recurso_utilizado": "sk_warrior_2", "alvo": ["Goblin"]},
            warrior,
            [enemy],
            {"Goblin": enemy},
            {},
        )
        self.assertIn("Surto de Ação", res_as["sys_log"])

    def test_05_42_protagonists_sprites_and_derived_stats(self):
        """Valida os 42 protagonistas (PROT-01 a PROT-42), caminhos de sprites/ícones e calculate_derived_stats."""
        seen_ids = set()
        seen_filenames = set()

        for r_name in PROTAGONIST_RACE_ORDER:
            for c_name in PROTAGONIST_CLASS_ORDER:
                info = get_protagonist_gender_info(r_name, c_name)
                self.assertIn("prot_id", info)
                self.assertIn("sprite_filename", info)
                self.assertIn("sprite_path", info)
                self.assertIn("icon_path", info)
                self.assertTrue(info["prot_id"].startswith("PROT-"))
                self.assertTrue(info["sprite_filename"].endswith(".png"))
                self.assertTrue(info["sprite_path"].startswith("assets/sprites/heroes/"))
                self.assertTrue(info["icon_path"].startswith("assets/sprites/heroes/icones/"))

                seen_ids.add(info["prot_id"])
                seen_filenames.add(info["sprite_filename"])

                # Verifica chamada de calculate_derived_stats com 1 dict e com 4 args
                stats_dict = CharacterCalculator.calculate_derived_stats(
                    {
                        "race": r_name,
                        "class": c_name,
                        "background": "Soldado",
                        "attributes": {"STR": 15, "DEX": 14, "CON": 13, "INT": 12, "WIS": 10, "CHA": 8},
                    }
                )
                self.assertEqual(stats_dict["prot_id"], info["prot_id"])
                self.assertEqual(stats_dict["sprite_filename"], info["sprite_filename"])
                self.assertEqual(stats_dict["sprite_path"], info["sprite_path"])
                self.assertEqual(stats_dict["icon_path"], info["icon_path"])
                # Verifica sincronia PT/EN de atributos
                for k_pt, k_en in [("FOR", "STR"), ("DES", "DEX"), ("CON", "CON"), ("INT", "INT"), ("SAB", "WIS"), ("CAR", "CHA")]:
                    self.assertIn(k_pt, stats_dict["attributes"])
                    self.assertIn(k_en, stats_dict["attributes"])
                    self.assertEqual(stats_dict["attributes"][k_pt], stats_dict["attributes"][k_en])

        self.assertEqual(len(seen_ids), 42)
        self.assertEqual(len(seen_filenames), 42)

    def test_06_session_manager_level_up_syncs_attrs_and_skills(self):
        """Garante que apply_level_up no SessionManager sincroniza atributos PT/EN e aceita IDs sk_* e canônicos."""
        sm = SessionManager()
        sm.game_state["player_character"] = {
            "name": "Bram",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "xp": 350,
            "xp_to_next_level": 300,
            "hp_current": 12,
            "hp_max": 12,
            "ac": 16,
            "ca": 16,
            "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "SAB": 10, "CAR": 10},
            "unlocked_skills": [],
        }
        res = sm.apply_level_up(
            attr_bonuses={"FOR": 2},
            chosen_skill_id="sk_warrior_1",
        )
        self.assertTrue(res["success"])
        pc = sm.game_state["player_character"]
        self.assertEqual(pc["attributes"]["FOR"], 18)
        self.assertEqual(pc["attributes"]["STR"], 18)
        self.assertIn("sk_warrior_1", pc["unlocked_skills"])
        self.assertIn("second_wind", pc["unlocked_skills"])


if __name__ == "__main__":
    unittest.main()
