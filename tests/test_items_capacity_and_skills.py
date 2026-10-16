import unittest
import json
from unittest.mock import patch
from core.game_engine import SessionManager
from core.combat_system import resolve_action


class DummyAI:
    def parse_player_intent(self, text, state=None):
        return {"tipo_acao": "INTERAGIR_CENARIO", "intencao_cena": "manter"}

    def generate_narrative_from_math(self, sys_log, prompt_extra=""):
        return sys_log


class TestItemsCapacityAndSkills(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI()
        self.session = SessionManager(self.ai)
        self.pc = {
            "name": "Garrick",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "hp_current": 12,
            "hp_max": 12,
            "xp": 300,
            "xp_to_next_level": 300,
            "gold": 50,
            "attributes": {"FOR": 14, "DES": 14, "CON": 14, "INT": 10, "SAB": 10, "CAR": 10},
            "inventory": {"i_potion_healing": 1, "i_rations": 2},
            "unlocked_skills": [],
            "abilities": []
        }
        self.session.game_state["player_character"] = self.pc

    # ==========================================================
    # 1. COMPÊNDIO DE ARMAS & ITENS (data/items.json)
    # ==========================================================
    def test_01_seven_weapon_families_present(self):
        """Valida que as 7 famílias de armas (21 variações) estão presentes e configuradas."""
        with open("data/items.json", "r", encoding="utf-8") as f:
            items_data = json.load(f)

        weapons = items_data.get("weapons", {})
        expected_ids = [
            # 1. Espadas
            "i_shortsword", "i_longsword", "i_forged_longsword",
            # 2. Armas Pesadas
            "i_greatsword", "i_greataxe", "i_adamantine_greatsword",
            # 3. Lâminas Ágeis
            "i_dagger", "i_rapier", "i_serrated_dagger",
            # 4. Impacto / Sagradas
            "i_mace", "i_warhammer", "i_blessed_hammer",
            # 5. Arcos
            "i_shortbow", "i_longbow", "i_elven_longbow",
            # 6. Bestas
            "i_light_crossbow", "i_hand_crossbow", "i_reinforced_crossbow",
            # 7. Focos / Bastões
            "i_wand", "i_quarterstaff", "i_arcane_staff"
        ]

        found_ids = {v.get("id") for v in weapons.values() if isinstance(v, dict)}
        for req_id in expected_ids:
            self.assertIn(req_id, found_ids, f"Arma '{req_id}' ausente de data/items.json")

        # Verifica propriedades específicas das armas +1
        serrated = next(v for v in weapons.values() if v.get("id") == "i_serrated_dagger")
        self.assertEqual(serrated.get("bonus_hit"), 1)
        self.assertEqual(serrated.get("bonus_damage"), 1)
        self.assertEqual(serrated.get("crit_threshold"), 19)

        arcane_staff = next(v for v in weapons.values() if v.get("id") == "i_arcane_staff")
        self.assertEqual(arcane_staff.get("bonus_spell_dc"), 1)
        self.assertEqual(arcane_staff.get("bonus_spell_hit"), 1)

        # Verifica chaves legadas
        for legacy_key in ["longsword", "shortbow", "greatsword", "dagger", "mace"]:
            self.assertIn(legacy_key, weapons)

    def test_02_initial_inventory_and_legendary_revive_scroll(self):
        """Valida que o inventário inicial não tem pergaminho de reviver e que este custa 200 PO."""
        fresh_session = SessionManager(self.ai)
        init_inv = fresh_session.game_state["inventory"]
        self.assertEqual(init_inv, {"i_potion_healing": 1, "i_rations": 2})
        self.assertNotIn("i_scroll_revive", init_inv)

        scroll_data = fresh_session.items_db["consumables"]["scroll_of_revivify"]
        self.assertEqual(scroll_data["id"], "i_scroll_revive")
        self.assertEqual(scroll_data["rarity"], "legendary")
        self.assertEqual(scroll_data["price_gold"], 200)

    # ==========================================================
    # 2. LIMITE DE CARGA DA MOCHILA
    # ==========================================================
    def test_03_inventory_max_slots_scaling_with_str(self):
        """Valida cálculo de slots máximos (10 + max(0, mod_FOR), min 10, max 14)."""
        # FOR 8 (mod -1) -> 10 slots
        self.pc["attributes"]["FOR"] = 8
        _, max_s = self.session.get_inventory_capacity(self.pc)
        self.assertEqual(max_s, 10)

        # FOR 14 (mod +2) -> 12 slots
        self.pc["attributes"]["FOR"] = 14
        _, max_s = self.session.get_inventory_capacity(self.pc)
        self.assertEqual(max_s, 12)

        # FOR 18 (mod +4) -> 14 slots
        self.pc["attributes"]["FOR"] = 18
        _, max_s = self.session.get_inventory_capacity(self.pc)
        self.assertEqual(max_s, 14)

        # FOR 20 (mod +5) -> travado no teto de 14 slots
        self.pc["attributes"]["FOR"] = 20
        _, max_s = self.session.get_inventory_capacity(self.pc)
        self.assertEqual(max_s, 14)

    def test_04_inventory_stacking_rules_and_can_add_item(self):
        """Valida regras de empilhamento (armas=1, poções=3/slot, rações=5/slot, acessórios=2/slot)."""
        self.pc["attributes"]["FOR"] = 10  # 10 slots máx
        self.pc["inventory"] = {
            "i_longsword": 1,       # 1 slot
            "i_chain_mail": 1,      # 1 slot
            "i_shield": 1,          # 1 slot
            "i_potion_healing": 3,  # 3 poções = 1 slot
            "i_rations": 5,         # 5 rações = 1 slot
            "i_ring_protection": 2  # 2 acessórios = 1 slot
        }
        used, max_s = self.session.get_inventory_capacity(self.pc)
        self.assertEqual(used, 6)
        self.assertEqual(max_s, 10)

        # Adicionar +1 poção abre um 2º slot de poções (total 7 slots)
        self.pc["inventory"]["i_potion_healing"] = 4
        used, _ = self.session.get_inventory_capacity(self.pc)
        self.assertEqual(used, 7)

        # Adicionar +1 ração abre um 2º slot de rações (total 8 slots)
        self.pc["inventory"]["i_rations"] = 6
        used, _ = self.session.get_inventory_capacity(self.pc)
        self.assertEqual(used, 8)

        # Testando can_add_item: restam 2 slots livres (8/10)
        self.assertTrue(self.session.can_add_item("i_greatsword", 2, self.pc))
        self.assertFalse(self.session.can_add_item("i_greatsword", 3, self.pc))

    # ==========================================================
    # 3. ÁRVORE DE HABILIDADES & LEVEL UP
    # ==========================================================
    def test_05_class_skills_json_structure(self):
        """Valida que data/class_skills.json possui as 6 classes com 4 tiers (1, 2, 3 e 5)."""
        with open("data/class_skills.json", "r", encoding="utf-8") as f:
            skills_db = json.load(f)

        classes_6 = ["Guerreiro", "Clérigo", "Mago", "Paladino", "Patrulheiro", "Ladino"]
        for c_name in classes_6:
            self.assertIn(c_name, skills_db)
            skills_list = skills_db[c_name]
            self.assertEqual(len(skills_list), 4)
            tiers = [s.get("tier") for s in skills_list]
            self.assertEqual(tiers, [1, 2, 3, 5])
            for sk in skills_list:
                self.assertIn(sk.get("type"), ["ativa", "passiva"])
                self.assertTrue(sk.get("id"))
                self.assertTrue(sk.get("name"))
                self.assertTrue(sk.get("description"))

    def test_06_apply_level_up_mechanics(self):
        """Valida subida de nível, ganho de PV, aumento de atributo e desbloqueio de skill."""
        # Guerreiro Nv 1 (HP 12, CON 14 -> mod +2, dado d10 -> média 6 + 2 = +8 PV)
        res = self.session.apply_level_up(
            attr_bonuses={"FOR": 2},
            chosen_skill_id="action_surge",
            pc=self.pc
        )
        self.assertTrue(res["success"])
        self.assertEqual(self.pc["level"], 2)
        self.assertEqual(self.pc["attributes"]["FOR"], 16)
        self.assertEqual(self.pc["hp_max"], 20)
        self.assertEqual(self.pc["hp_current"], 20)
        self.assertIn("action_surge", self.pc["unlocked_skills"])
        self.assertIn("Surto de Ação", self.pc["abilities"])
        self.assertEqual(self.pc["xp_to_next_level"], 900)

    def test_07_combat_integration_with_class_passives(self):
        """Valida integração das passivas de classe (champion_focus crit 19, archery_style +2) no combate."""
        # Configura Guerreiro com Foco do Campeão (Crítico no 19)
        self.pc["unlocked_skills"] = ["champion_focus"]
        self.pc["equipped_weapon"] = "Espada Longa"
        target = {"name": "Orc", "pv_atual": 30, "pv_max": 30, "ca": 12, "faction": "enemy", "status": "vivo"}
        active_targets = {"orc": target}

        parsed = {
            "tipo_acao": "ataque",
            "arma_usada": "espada longa",
            "alvo": ["orc"]
        }

        # Força o d20 do ataque do jogador a rolar 19
        with patch("core.dice_engine.DiceEngine.roll_d20", return_value=19):
            out = resolve_action(parsed, self.pc, [target], active_targets, self.session.game_state)
            self.assertIn("ACERTO CRÍTICO", out["log_mecanico"].upper())

        # Configura Patrulheiro com Estilo de Arquearia (+2 acerto com Arco)
        self.pc["unlocked_skills"] = ["archery_style"]
        parsed_bow = {
            "tipo_acao": "ataque",
            "arma_usada": "arco longo",
            "alvo": ["orc"]
        }
        # DES 14 (+2) + Prof (+2) + Archery (+2) = +6 total de modificador
        with patch("core.dice_engine.DiceEngine.roll_d20", return_value=10):
            out_bow = resolve_action(parsed_bow, self.pc, [target], active_targets, self.session.game_state)
            self.assertIn("+ 6 = 16", out_bow["log_mecanico"])

    # ==========================================================
    # 4. STANDARD ARRAY, ITENS RACIAIS, GÊNERO E ACENTUAÇÃO
    # ==========================================================
    def test_08_standard_array_and_racial_bonuses(self):
        """Valida Standard Array por classe somado aos bônus raciais e sincronização PT/EN."""
        from core.dnd_rules import CharacterCalculator

        # Draconato (+2 FOR, +1 CAR) + Mago (INT 15, CON 14, DES 13, SAB 12, CAR 10, FOR 8)
        stats_drac_wiz = CharacterCalculator.calculate_derived_stats(
            {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10},
            "Draconato",
            "Mago",
            "Sábio"
        )
        attrs = stats_drac_wiz["attributes"]
        self.assertEqual(attrs["FOR"], 10)
        self.assertEqual(attrs["STR"], 10)
        self.assertEqual(attrs["DES"], 13)
        self.assertEqual(attrs["DEX"], 13)
        self.assertEqual(attrs["CON"], 14)
        self.assertEqual(attrs["INT"], 15)
        self.assertEqual(attrs["SAB"], 12)
        self.assertEqual(attrs["WIS"], 12)
        self.assertEqual(attrs["CAR"], 11)
        self.assertEqual(attrs["CHA"], 11)

        # Anão da Colina (+2 CON, +1 SAB, +1 PV Tenacidade, +3 PV Runa) + Guerreiro (FOR 15, CON 14 -> 16)
        stats_dwarf_ftr = CharacterCalculator.calculate_derived_stats(
            {},
            "Anão da Colina",
            "Guerreiro",
            "Soldado"
        )
        self.assertEqual(stats_dwarf_ftr["attributes"]["FOR"], 15)
        self.assertEqual(stats_dwarf_ftr["attributes"]["CON"], 16)
        self.assertEqual(stats_dwarf_ftr["attributes"]["SAB"], 13)
        # PV = 10 (base) + 3 (mod CON 16) + 1 (Tenacidade Anã) + 3 (Runa da Pedra-Forja) = 17
        self.assertEqual(stats_dwarf_ftr["hp_max"], 17)

    def test_09_seven_racial_unique_items_and_equipment_order(self):
        """Valida os 7 Itens Únicos Raciais na 3ª posição de equipment e no data/items.json."""
        from core.dnd_rules import CharacterCalculator, ITENS_UNICOS_RACIAIS

        with open("data/items.json", "r", encoding="utf-8") as f:
            items_data = json.load(f)
        acc_ids = {v.get("id") for v in items_data.get("accessories", {}).values() if isinstance(v, dict)}

        expected_racial = {
            "Humano": ("i_racial_human_signet", "Sinete da Coroa Partida"),
            "Elfo da Floresta": ("i_racial_elf_cloak", "Manto de Folhas Cinzentas"),
            "Anão da Colina": ("i_racial_dwarf_rune", "Runa da Pedra-Forja"),
            "Halfling": ("i_racial_halfling_coin", "Moeda da Sorte Antiga"),
            "Draconato": ("i_racial_dragon_scale", "Escama Ancestral Incandescente"),
            "Meio-Orc": ("i_racial_orc_tusk", "Presa de Ferro Sangrento"),
            "Tiefling": ("i_racial_tiefling_seal", "Selo de Brasas Abissais")
        }

        for race_name, (item_id, item_name) in expected_racial.items():
            self.assertIn(item_id, acc_ids, f"Item racial {item_id} ausente de data/items.json")
            self.assertIn(race_name, ITENS_UNICOS_RACIAIS)
            calc = CharacterCalculator.calculate_derived_stats({}, race_name, "Paladino", "Nobre")
            self.assertGreaterEqual(len(calc["equipment"]), 3)
            self.assertEqual(calc["equipment"][0], "Cota de Malha")
            self.assertEqual(calc["equipment"][1], "Espada Longa")
            self.assertEqual(calc["equipment"][2], item_name)
            self.assertEqual(calc["equipped_accessory"], item_name)

    def test_10_protagonist_gender_matrix_42_combinations(self):
        """Valida a matriz canônica de gênero para todos os 42 protagonistas (7 raças x 6 classes)."""
        from core.dnd_rules import PROTAGONIST_GENDER_MAP, get_protagonist_gender_info

        races = ["Humano", "Elfo da Floresta", "Anão da Colina", "Halfling", "Tiefling", "Draconato", "Meio-Orc"]
        classes = ["Guerreiro", "Clérigo", "Paladino", "Mago", "Patrulheiro", "Ladino"]

        total = 0
        for r in races:
            self.assertIn(r, PROTAGONIST_GENDER_MAP)
            for c in classes:
                self.assertIn(c, PROTAGONIST_GENDER_MAP[r])
                info = get_protagonist_gender_info(r, c)
                self.assertIn(info["gender"], ["male", "female"])
                self.assertIn(info["symbol"], ["♂", "♀"])
                self.assertIn(info["label"], ["Masculino", "Feminino"])
                total += 1
        self.assertEqual(total, 42)

        # Verifica casos específicos canônicos (PROT-01 a PROT-42)
        human_ranger = get_protagonist_gender_info("Humano", "Patrulheiro")
        self.assertEqual(human_ranger["gender"], "female")
        self.assertEqual(human_ranger["symbol"], "♀")
        self.assertEqual(human_ranger["class_display"], "Patrulheira")

        human_cleric = get_protagonist_gender_info("Humano", "Clérigo")
        self.assertEqual(human_cleric["gender"], "female")
        self.assertEqual(human_cleric["class_display"], "Clériga")

        orc_rogue = get_protagonist_gender_info("Meio-Orc", "Ladino")
        self.assertEqual(orc_rogue["gender"], "female")
        self.assertEqual(orc_rogue["class_display"], "Ladina")

    def test_11_no_corrupted_accents_in_dnd_rules(self):
        """Garante que não restaram palavras com acentuação corrompida em dnd_rules.py."""
        import core.dnd_rules as rules
        dump = json.dumps({
            "racas": rules.RACAS_5E,
            "classes": rules.CLASSES,
            "antecedentes": rules.ANTECEDENTES_5E,
            "tendencias": rules.TENDENCIAS_5E,
            "bestiario": rules.BESTIARIO_5E
        }, ensure_ascii=False)

        corrupted_tokens = [
            "Méódio", "iódiomas", "Estuódioso", "dracnica", "Constituião",
            "Viso no Escuro", "Inteligncia", "Múúltiplos", "Bnus", "Mordióda"
        ]
        for token in corrupted_tokens:
            self.assertNotIn(token, dump, f"Token corrompido encontrado em dnd_rules.py: {token}")


if __name__ == "__main__":
    unittest.main()

