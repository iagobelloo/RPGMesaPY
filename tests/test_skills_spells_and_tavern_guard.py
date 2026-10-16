import unittest
import json
from core.game_engine import SessionManager
from core.combat_system import resolve_action, process_enemies_turn_batch


class DummyAI:
    def __init__(self):
        self.last_prompt = ""

    def parse_player_intent(self, text, state):
        t_low = text.lower().strip()
        if any(w in t_low for w in ["sair", "estrada", "partir", "porta"]):
            return {"tipo_acao": "AVANCAR_HISTORIA", "intencao_cena": "avancar", "alvo": []}
        return {"tipo_acao": "INTERAGIR_CENARIO", "intencao_cena": "explorar", "alvo": []}

    def generate_narrative_from_math(self, sys_log, intent=""):
        return f"Narrativa: {intent}"


import os

class TestSkillsSpellsAndTavernGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backup_files = {}
        for p in [
            "saves/save_slot_1.json", "saves/slot1.json",
            "saves/save_slot_2.json", "saves/slot2.json",
            "saves/save_slot_3.json", "saves/slot3.json"
        ]:
            if os.path.exists(p):
                with open(p, "rb") as f:
                    cls.backup_files[p] = f.read()

    @classmethod
    def tearDownClass(cls):
        slots = [
            "saves/save_slot_1.json", "saves/slot1.json",
            "saves/save_slot_2.json", "saves/slot2.json",
            "saves/save_slot_3.json", "saves/slot3.json"
        ]
        for p in slots:
            if p in cls.backup_files:
                with open(p, "wb") as f:
                    f.write(cls.backup_files[p])
            elif os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

    def setUp(self):
        self.ai = DummyAI()
        self.session = SessionManager(self.ai)
        self.session.game_state["player_character"] = {
            "name": "Valerius",
            "class": "Guerreiro",
            "level": 1,
            "hp_current": 10,
            "hp_max": 12,
            "unlocked_skills": ["second_wind"]
        }
        self.session.game_state["story_beat"] = 1
        self.session.story.current_beat = 1
        self.session.game_mode = "EXPLORACAO"

    def test_01_get_available_skills_for_warrior_ranger_rogue(self):
        """Valida que get_available_skills retorna habilidades com formato exigido e habilidades canônicas."""
        # Guerreiro
        self.session.game_state["player_character"] = {
            "name": "Valerius", "class": "Guerreiro", "level": 1,
            "hp_current": 10, "hp_max": 12, "unlocked_skills": ["second_wind"]
        }
        warrior_skills = self.session.get_available_skills()
        self.assertTrue(len(warrior_skills) >= 1)
        sw = next((s for s in warrior_skills if s["id"] == "second_wind"), None)
        self.assertIsNotNone(sw)
        self.assertEqual(sw["cost"], "Ação Bônus")
        self.assertEqual(sw["tier"], 1)
        self.assertTrue(sw["acquired"])

        # Patrulheiro (deve conter Marca do Caçador)
        self.session.game_state["player_character"] = {
            "name": "Sylas", "class": "Patrulheiro", "level": 1,
            "hp_current": 10, "hp_max": 10, "unlocked_skills": ["favored_enemy"]
        }
        ranger_skills = self.session.get_available_skills()
        hm = next((s for s in ranger_skills if s["id"] == "hunters_mark"), None)
        self.assertIsNotNone(hm)
        self.assertEqual(hm["cost"], "Ação Bônus")
        self.assertEqual(hm["tier"], 1)

        # Ladino (deve conter Ataque Furtivo)
        self.session.game_state["player_character"] = {
            "name": "Finn", "class": "Ladino", "level": 1,
            "hp_current": 8, "hp_max": 8, "unlocked_skills": ["sneak_attack"]
        }
        rogue_skills = self.session.get_available_skills()
        sa = next((s for s in rogue_skills if s["id"] == "sneak_attack"), None)
        self.assertIsNotNone(sa)
        self.assertEqual(sa["cost"], "Ação Bônus")
        self.assertEqual(sa["tier"], 1)

    def test_02_get_available_spells_strict_5e(self):
        """Valida que apenas Mago e Clérigo possuem magias no Nv 1, enquanto marciais retornam []."""
        # Marciais Nv 1 -> []
        for martial_cls in ["Guerreiro", "Ladino", "Patrulheiro"]:
            self.session.game_state["player_character"] = {
                "name": "Hero", "class": martial_cls, "level": 1, "spell_slots": {}
            }
            spells = self.session.get_available_spells()
            self.assertEqual(spells, [], f"{martial_cls} Nv 1 não deveria ter magias")

        # Mago Nv 1 -> Raio de Fogo e Mísseis Mágicos
        self.session.game_state["player_character"] = {
            "name": "Ignisrax", "class": "Mago", "level": 1, "spell_slots": {"1": 2}
        }
        mage_spells = self.session.get_available_spells()
        self.assertTrue(any(s["id"] == "fire_bolt" and s["level"] == 0 for s in mage_spells))
        self.assertTrue(any(s["id"] == "magic_missile" and s["level"] == 1 for s in mage_spells))

        # Clérigo Nv 1 -> Chama Sagrada e Curar Ferimentos
        self.session.game_state["player_character"] = {
            "name": "Faen", "class": "Clérigo", "level": 1, "spell_slots": {"1": 2}
        }
        cleric_spells = self.session.get_available_spells()
        self.assertTrue(any(s["id"] == "sacred_flame" and s["level"] == 0 for s in cleric_spells))
        self.assertTrue(any(s["id"] == "cure_wounds" and s["level"] == 1 for s in cleric_spells))

    def test_03_use_skill_mechanics(self):
        """Valida execução mecânica de Retomar o Fôlego e Marca do Caçador com ui_queue."""
        # 1. Retomar o Fôlego cura e atualiza hp_current
        self.session.game_state["player_character"] = {
            "name": "Valerius", "class": "Guerreiro", "level": 1,
            "hp_current": 4, "hp_max": 12, "unlocked_skills": ["second_wind"]
        }
        res_sw = self.session.use_skill("second_wind")
        self.assertTrue(res_sw["success"])
        self.assertGreater(self.session.game_state["player_character"]["hp_current"], 4)
        self.assertFalse(self.session.ui_queue.empty())

        # 2. Marca do Caçador marca alvo ativo
        self.session.active_combat_targets = {
            "m_dire_wolf_01": {"name": "Lobo Terrível", "faction": "enemy", "pv_atual": 20, "pv_max": 20, "status": "vivo"}
        }
        res_hm = self.session.use_skill("hunters_mark", target="m_dire_wolf_01")
        self.assertTrue(res_hm["success"])
        self.assertTrue(self.session.active_combat_targets["m_dire_wolf_01"].get("_marked_by_hunters_mark"))
        self.assertEqual(self.session.game_state["player_character"].get("_active_hunters_mark_target"), "Lobo Terrível")

    def test_04_cast_spell_consumption_and_effect(self):
        """Valida consumo de slots de magia e efeitos reais de cura e dano."""
        # Curar Ferimentos consome slot de nível 1
        self.session.game_state["player_character"] = {
            "name": "Faen", "class": "Clérigo", "level": 1,
            "hp_current": 3, "hp_max": 10, "spell_slots": {"1": 2},
            "attributes": {"SAB": 14}
        }
        res_heal = self.session.cast_spell("cure_wounds")
        self.assertTrue(res_heal["success"])
        self.assertGreater(self.session.game_state["player_character"]["hp_current"], 3)
        self.assertEqual(self.session.game_state["player_character"]["spell_slots"]["1"], 1)

        # Segundo cast esgota os slots
        self.session.cast_spell("cure_wounds")
        self.assertEqual(self.session.game_state["player_character"]["spell_slots"]["1"], 0)

        # Terceiro cast deve falhar por falta de slots
        res_fail = self.session.cast_spell("cure_wounds")
        self.assertFalse(res_fail["success"])
        self.assertIn("não possui espaços de magia", res_fail["message"])

        # Mísseis Mágicos com alvo hostil
        self.session.game_state["player_character"]["spell_slots"]["1"] = 1
        self.session.active_combat_targets = {
            "m_goblin_01": {"name": "Goblin", "faction": "enemy", "pv_atual": 10, "pv_max": 10, "status": "vivo"}
        }
        res_mm = self.session.cast_spell("magic_missile", target="m_goblin_01")
        self.assertTrue(res_mm["success"])
        self.assertLess(self.session.active_combat_targets["m_goblin_01"]["pv_atual"], 10)

    def test_05_tavern_anti_advance_guard_on_dialogue(self):
        """Valida que diálogos e interações com o ambiente na Taverna NÃO avançam o beat involuntariamente."""
        self.session.story.current_beat = 1
        self.session.game_state["story_beat"] = 1

        # Diálogo mencionando estrada não deve avançar beat
        self.session._async_turn_processor("Pergunto ao taverneiro sobre os perigos da estrada", ["tavern"], [])
        self.assertEqual(self.session.story.current_beat, 1, "Diálogo sobre estrada na taverna não pode avançar beat")
        self.assertEqual(self.session.game_state["story_beat"], 1)

        # Falar sobre partir no balcão
        self.session._async_turn_processor("Converso no balcao com o estalajadeiro antes de viajar", ["tavern"], [])
        self.assertEqual(self.session.story.current_beat, 1)

        # Comando explícito e direto de saída deve avançar
        self.session._async_turn_processor("vou para a estrada", ["tavern"], [])
        self.assertEqual(self.session.story.current_beat, 2, "Comando explícito de saída deve avançar para Beat 2")

    def test_06_simplified_combat_logs(self):
        """Valida a simplificação e ordem dos logs de combate (ataque do jogador e do inimigo)."""
        pc = {
            "name": "Valerius", "class": "Guerreiro", "level": 1,
            "hp_current": 10, "hp_max": 12, "ca": 14, "ac": 14,
            "equipped_weapon": "Arco Curto", "attributes": {"DES": 16, "FOR": 10},
            "unlocked_skills": []
        }
        target = {
            "name": "Lobo Atroz", "faction": "enemy", "ca": 12, "pv_atual": 15, "pv_max": 15
        }
        action = {"tipo_acao": "ataque", "recurso_utilizado": "Arco Curto"}
        res = resolve_action(action, pc, [target], {"Lobo Atroz": target})
        # Verifica formato sintético do ataque do jogador
        self.assertIn("🎲 Ataque com Arco Curto:", res["sys_log"])
        self.assertIn("vs CA 12 ➔", res["sys_log"])

        # Ataque inimigo em lote
        enemy_targets = {
            "m_dire_wolf_01": {
                "name": "Lobo Atroz",
                "faction": "enemy",
                "ca": 12,
                "pv_atual": 15,
                "pv_max": 15,
                "actions": [{"name": "Mordida", "hit_bonus": 5, "damage_dice": "1d6+2"}]
            }
        }
        enemy_log = process_enemies_turn_batch(enemy_targets, pc)
        self.assertTrue("🐺" in enemy_log)
        self.assertTrue("Lobo" in enemy_log)
        self.assertTrue("o ataque (" in enemy_log)


if __name__ == "__main__":
    unittest.main()
