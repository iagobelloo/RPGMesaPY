import unittest
import os
import shutil
import json
from core.game_engine import SessionManager

class DummyAI:
    def parse_player_intent(self, text, state=None):
        t_low = text.lower()
        if "descansar" in t_low:
            return {"tipo_acao": "DESCANSAR", "intencao_cena": "manter"}
        if "equipar" in t_low or "equip" in t_low:
            parts = text.split(":", 1)
            recurso = parts[1].strip() if len(parts) > 1 else text.replace("equipar", "").strip()
            return {"tipo_acao": "EQUIPAR", "recurso_utilizado": recurso, "intencao_cena": "manter"}
        if "conversar" in t_low or "falar" in t_low or "olhar" in t_low:
            return {"tipo_acao": "INTERAGIR_CENARIO", "intencao_cena": "manter"}
        return {"tipo_acao": "INTERAGIR_CENARIO", "intencao_cena": "manter"}

    def generate_narrative_from_math(self, sys_log, prompt_extra=""):
        return f"Narrativa AI: {prompt_extra} ({sys_log})"

class TestSaveSlotsAndTavern(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Cria backup da pasta saves caso já exista algum save
        cls.backup_saves = {}
        os.makedirs("saves", exist_ok=True)
        for i in range(1, 4):
            for pattern in [f"saves/slot{i}.json", f"saves/save_slot_{i}.json"]:
                if os.path.exists(pattern):
                    with open(pattern, "rb") as f:
                        cls.backup_saves[pattern] = f.read()

    @classmethod
    def tearDownClass(cls):
        # Restaura os saves de backup ou remove os criados pelo teste
        for i in range(1, 4):
            for pattern in [f"saves/slot{i}.json", f"saves/save_slot_{i}.json"]:
                if pattern in cls.backup_saves:
                    with open(pattern, "wb") as f:
                        f.write(cls.backup_saves[pattern])
                elif os.path.exists(pattern):
                    try:
                        os.remove(pattern)
                    except Exception:
                        pass

    def setUp(self):
        self.ai = DummyAI()
        self.session = SessionManager(self.ai)
        self.pc = {
            "name": "Valerius",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "hp_current": 12,
            "hp_max": 12,
            "xp": 0,
            "gold": 25,
            "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "SAB": 10, "CAR": 10},
            "inventory": {"i_potion_healing": 2},
            "equipment": ["Roupas Comuns"]
        }
        self.session.game_state["player_character"] = self.pc
        self.session.game_state["story_beat"] = 1
        self.session.story.current_beat = 1

    # ==========================================
    # 1. TESTES DOS 3 SAVE SLOTS (Item 4.3)
    # ==========================================
    def test_01_default_save_slot_is_1(self):
        """Valida que o slot padrão inicial é 1."""
        self.assertEqual(self.session.current_save_slot, 1)

    def test_02_save_and_load_slots_independently(self):
        """Valida salvamento e carregamento independentes nos slots 1, 2 e 3."""
        # Salva no Slot 1
        self.session.game_state["player_character"]["name"] = "Heroi_Slot_1"
        self.session.game_state["player_character"]["level"] = 1
        self.assertTrue(self.session.save_game(1))
        self.assertEqual(self.session.current_save_slot, 1)
        self.assertTrue(os.path.exists("saves/slot1.json"))

        # Salva no Slot 2 com outro personagem
        self.session.game_state["player_character"]["name"] = "Heroi_Slot_2"
        self.session.game_state["player_character"]["level"] = 2
        self.assertTrue(self.session.save_game(2))
        self.assertEqual(self.session.current_save_slot, 2)
        self.assertTrue(os.path.exists("saves/slot2.json"))

        # Salva no Slot 3
        self.session.game_state["player_character"]["name"] = "Heroi_Slot_3"
        self.session.game_state["player_character"]["level"] = 3
        self.assertTrue(self.session.save_game(3))
        self.assertEqual(self.session.current_save_slot, 3)
        self.assertTrue(os.path.exists("saves/slot3.json"))

        # Carrega Slot 1 e confere isolamento
        self.assertTrue(self.session.load_game(1))
        self.assertEqual(self.session.game_state["player_character"]["name"], "Heroi_Slot_1")
        self.assertEqual(self.session.game_state["player_character"]["level"], 1)

        # Carrega Slot 2
        self.assertTrue(self.session.load_game(2))
        self.assertEqual(self.session.game_state["player_character"]["name"], "Heroi_Slot_2")
        self.assertEqual(self.session.game_state["player_character"]["level"], 2)

        # Carrega Slot 3
        self.assertTrue(self.session.load_game(3))
        self.assertEqual(self.session.game_state["player_character"]["name"], "Heroi_Slot_3")
        self.assertEqual(self.session.game_state["player_character"]["level"], 3)

    def test_03_get_slot_metadata_and_summary(self):
        """Valida get_slot_metadata e get_all_slots_summary com timestamp e status."""
        self.session.game_state["player_character"]["name"] = "Alistair"
        self.session.game_state["player_character"]["level"] = 4
        self.session.save_game(1)

        meta1 = SessionManager.get_slot_metadata(1)
        self.assertFalse(meta1.get("is_empty"))
        self.assertEqual(meta1.get("name"), "Alistair")
        self.assertEqual(meta1.get("level"), 4)
        self.assertTrue("saved_at" in meta1 and len(meta1["saved_at"]) > 0)

        summary = SessionManager.get_all_slots_summary()
        self.assertEqual(len(summary), 3)
        self.assertEqual(summary[0]["slot"], 1)
        self.assertEqual(summary[1]["slot"], 2)
        self.assertEqual(summary[2]["slot"], 3)

    def test_04_delete_save_slot(self):
        """Valida a exclusão física do arquivo de save de um slot específico."""
        self.session.save_game(2)
        self.assertTrue(os.path.exists("saves/slot2.json"))

        deleted = SessionManager.delete_save_slot(2)
        self.assertTrue(deleted)
        self.assertFalse(os.path.exists("saves/slot2.json"))

        meta2 = SessionManager.get_slot_metadata(2)
        self.assertTrue(meta2.get("is_empty"))

    # ==========================================
    # 2. TESTES DE EQUIPAMENTO DE ARMAS E CA (Item 4.2)
    # ==========================================
    def test_05_equip_weapon_success(self):
        """Valida equipar arma existente no inventário e emitir log correto."""
        self.session.add_inventory_item("i_longsword", 1)
        self.assertTrue(self.session.equip_item("i_longsword"))

        pc = self.session.game_state["player_character"]
        self.assertEqual(pc.get("equipped_weapon"), "Espada Longa")
        self.assertIsInstance(pc.get("equipment"), dict)
        self.assertEqual(pc["equipment"].get("weapon"), "Espada Longa")

        # Verifica mensagem na fila
        msgs = []
        while not self.session.ui_queue.empty():
            msgs.append(self.session.ui_queue.get_nowait())
        log_found = any("empunha Espada Longa" in str(m) and "Ataques e reflexos agora utilizam este equipamento" in str(m) for m in msgs)
        self.assertTrue(log_found)

    def test_06_equip_item_not_in_inventory_fails(self):
        """Valida que tentar equipar um item que o jogador não possui retorna False."""
        success = self.session.equip_item("Espada Colossal Lendária Inexistente")
        self.assertFalse(success)

    def test_07_equip_armor_and_shield_recalculates_ac(self):
        """Valida que equipar armadura e escudo recalcula deterministicamente a CA (ac e ca)."""
        # Personagem com DES 12 (+1)
        # Sem armadura: 10 + 1 = 11
        pc = self.session.game_state["player_character"]
        self.assertEqual(self.session._recalculate_ac(pc), 11)

        # Adiciona e equipa Cota de Malha (CA 16 fixa, pesada, sem DES)
        self.session.add_inventory_item("i_chain_mail", 1)
        self.assertTrue(self.session.equip_item("i_chain_mail"))
        self.assertEqual(pc.get("ac"), 16)
        self.assertEqual(pc.get("ca"), 16)

        # Adiciona e equipa Escudo (+2 de CA -> 18)
        self.session.add_inventory_item("i_shield", 1)
        self.assertTrue(self.session.equip_item("i_shield"))
        self.assertEqual(pc.get("ac"), 18)
        self.assertEqual(pc.get("ca"), 18)

    def test_08_equip_commands_via_turn_processor(self):
        """Valida alternância de armas via comando direto e via tipo_acao no _async_turn_processor."""
        self.session.add_inventory_item("i_shortbow", 1)
        # Comando com prefixo equip_weapon:
        self.session._async_turn_processor("equip_weapon:i_shortbow", ["tavern"], [])
        pc = self.session.game_state["player_character"]
        self.assertEqual(pc.get("equipped_weapon"), "Arco Curto")

        # Comando via NLP/tipo_acao EQUIPAR
        self.session.add_inventory_item("i_dagger", 1)
        self.session._async_turn_processor("equipar i_dagger", ["tavern"], [])
        self.assertIn("Adaga", pc.get("equipped_weapon"))

    # ==========================================
    # 3. TESTES DE REATIVIDADE NA TAVERNA (Item 4.1)
    # ==========================================
    def test_09_tavern_rumors_none_without_allies(self):
        """Valida que sem aliados juramentados, get_tavern_allies_rumors retorna None."""
        self.assertIsNone(self.session.get_tavern_allies_rumors())

    def test_10_tavern_rumors_with_unlocked_allies(self):
        """Valida geração de rumor solene citando nomes dos heróis juramentados."""
        # Desbloqueia aliados na StoryEngine
        self.session.story.unlock_ally("hero_01")
        self.session.story.unlock_ally("hero_02")

        rumor = self.session.get_tavern_allies_rumors()
        self.assertIsNotNone(rumor)
        self.assertIn("[RUMORES DA TAVERNA]", rumor)
        self.assertIn("afiam suas armas e vigiam as rotas da montanha", rumor)
        # Confere que nomes dos heróis aparecem no rumor
        allies = self.session.story.get_unlocked_allies()
        for ally in allies.values():
            self.assertIn(ally["name"], rumor)

    def test_11_rest_in_tavern_dispatches_rumor_and_maelor_reaction(self):
        """Valida que descanso seguro no Beat 1 dispara rumor e narrativa enriquecida de Maelor se houver aliados."""
        self.session.story.unlock_ally("hero_01")
        self.session.story.current_beat = 1

        self.session._async_turn_processor("descansar", ["tavern"], [])

        msgs = []
        while not self.session.ui_queue.empty():
            msgs.append(self.session.ui_queue.get_nowait())

        # Verifica rumor da taverna emitido
        has_rumor = any("[RUMORES DA TAVERNA]" in str(m) for m in msgs)
        self.assertTrue(has_rumor)

        # Verifica fala solene de Maelor
        has_maelor = any("Maelor" in str(m) and ("vigilante" in str(m) or "atentos" in str(m) or "sombras" in str(m) or "sozinho" in str(m)) for m in msgs)
        self.assertTrue(has_maelor)

    def test_12_dialogue_in_tavern_dispatches_rumor_and_maelor_reaction(self):
        """Valida que interação/conversa no Beat 1 despacha rumores dos aliados no Hub."""
        self.session.story.unlock_ally("hero_03")
        self.session.story.current_beat = 1

        self.session._async_turn_processor("conversar com taverneiro", ["tavern"], [])

        msgs = []
        while not self.session.ui_queue.empty():
            msgs.append(self.session.ui_queue.get_nowait())

        has_rumor = any("[RUMORES DA TAVERNA]" in str(m) for m in msgs)
        self.assertTrue(has_rumor)
        has_maelor = any("Maelor" in str(m) for m in msgs)
        self.assertTrue(has_maelor)

if __name__ == "__main__":
    unittest.main()
