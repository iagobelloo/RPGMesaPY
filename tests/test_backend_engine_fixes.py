import unittest
import os
import json
import copy
from core.game_engine import SessionManager
from core.dnd_rules import BESTIARIO_5E, get_monster_bestiary_entry


class MockAI:
    def parse_player_intent(self, text, state):
        t_low = text.lower()
        if "atacar" in t_low:
            alvo = t_low.replace("atacar", "").strip() or "nenhum"
            return {
                "tipo_acao": "ATACAR",
                "recurso_utilizado": "espada longa",
                "alvo": [alvo],
                "intencao_cena": "Atacar com lâmina"
            }
        elif any(k in t_low for k in ["sair da mesa", "ir ao balcão", "ir ao balcao", "procurar missão", "procurar missao"]):
            return {
                "tipo_acao": "AVANCAR_HISTORIA",
                "recurso_utilizado": "nenhum",
                "alvo": ["nenhum"],
                "intencao_cena": "Sair da mesa e procurar afazeres"
            }
        elif any(k in t_low for k in ["viajar para a estrada", "partir para a estrada"]):
            return {
                "tipo_acao": "AVANCAR_HISTORIA",
                "recurso_utilizado": "nenhum",
                "alvo": ["nenhum"],
                "intencao_cena": "Partir para a estrada"
            }
        return {
            "tipo_acao": "INTERAGIR_AMBIENTE",
            "recurso_utilizado": "nenhum",
            "alvo": ["nenhum"],
            "intencao_cena": "Observar"
        }

    def generate_narrative_from_math(self, log, intent):
        return f"[Narrativa]: {intent} -> {log[:40]}"


class TestBackendEngineFixes(unittest.TestCase):
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
        self.session = SessionManager()
        self.session.ai = MockAI()
        self.session.game_state["player_character"] = {
            "name": "Valerius",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "hp_max": 20,
            "hp_current": 20,
            "ca": 16,
            "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "WIS": 10, "CHA": 10},
            "proficiency_bonus": 2,
            "equipped_weapon": "espada longa",
            "inventory": {"i_potion_healing": 2}
        }
        # Limpa fila
        while not self.session.ui_queue.empty():
            self.session.ui_queue.get_nowait()

    def tearDown(self):
        test_save = "saves/test_fixes_slot.json"
        if os.path.exists(test_save):
            try:
                os.remove(test_save)
            except OSError:
                pass

    def test_01_single_narrative_message_dispatched_in_combat_turn(self):
        """Tarefa 1: Garante que apenas 1 mensagem estruturada 'type: narrative' é despachada por turno."""
        self.session.game_mode = "COMBATE"
        self.session.active_combat_targets = {
            "Lobo Atroz (1)": {
                "name": "Lobo Atroz (1)",
                "tipo_bestiario": "m_dire_wolf",
                "pv_atual": 30,
                "pv_max": 30,
                "ca": 14,
                "faction": "enemy",
                "status": "vivo"
            }
        }

        self.session._async_turn_processor("atacar m_dire_wolf", [], [])

        messages = []
        while not self.session.ui_queue.empty():
            messages.append(self.session.ui_queue.get_nowait())

        narrative_msgs = [m for m in messages if m.get("type") in ["narrative", "dialogue"]]
        legacy_narrative_msgs = [m for m in messages if "narrativa" in m]

        self.assertEqual(len(legacy_narrative_msgs), 0, "Nenhuma mensagem no formato legado {'narrativa': ...} deve ser emitida.")
        self.assertEqual(len(narrative_msgs), 1, "Exatamente UMA mensagem do tipo 'narrative' deve ser emitida no final do turno.")
        self.assertEqual(narrative_msgs[0].get("npc_falando"), "Mestre")
        self.assertTrue(len(narrative_msgs[0].get("content", "")) > 0)

    def test_02_equip_item_does_not_duplicate_narrative(self):
        """Tarefa 1: Valida equip_item sem mensagens legadas duplicadas."""
        self.session.game_state["inventory"]["w_shortsword"] = 1
        self.session.equip_item("w_shortsword")

        messages = []
        while not self.session.ui_queue.empty():
            messages.append(self.session.ui_queue.get_nowait())

        legacy_msgs = [m for m in messages if "narrativa" in m]
        narrative_msgs = [m for m in messages if m.get("type") == "narrative"]

        self.assertEqual(len(legacy_msgs), 0)
        self.assertEqual(len(narrative_msgs), 1)

    def test_03_anti_involuntary_beat_advance_in_tavern(self):
        """Tarefa 2: Trava anti-avanço involuntário impede que sair da mesa ou procurar missão avance Beat."""
        self.session.story.current_beat = 1
        self.session.game_mode = "EXPLORACAO"

        # Tenta sair da mesa
        self.session._async_turn_processor("sair da mesa", [], [])
        self.assertEqual(self.session.story.current_beat, 1, "Comando 'sair da mesa' não pode avançar o Beat 1 da Taverna.")

        # Tenta procurar missão
        self.session._async_turn_processor("procurar missão no balcão", [], [])
        self.assertEqual(self.session.story.current_beat, 1, "Comando 'procurar missão' não pode avançar o Beat 1 da Taverna.")

        # Comando explícito de viagem para a estrada deve avançar para o Beat 2
        self.session._async_turn_processor("viajar para a estrada", [], [])
        self.assertEqual(self.session.story.current_beat, 2, "Comando explícito de viagem deve avançar para o Beat 2.")

    def test_04_progressive_bestiary_discovery(self):
        """Tarefa 3: Sistema de Descoberta Progressiva no Bestiário (métodos e persistência)."""
        # Limpa descobertas
        self.session.game_state["discovered_monsters"] = []

        # Descoberta inicial
        added = self.session.discover_monster("m_dire_wolf")
        self.assertTrue(added)
        self.assertIn("m_dire_wolf", self.session.get_discovered_monsters())

        # Idempotência (não duplica)
        added_again = self.session.discover_monster("m_dire_wolf")
        self.assertFalse(added_again)
        self.assertEqual(self.session.get_discovered_monsters().count("m_dire_wolf"), 1)

        # Salva e recarrega
        self.session.discover_monster("m_bandit")
        test_save = "saves/test_fixes_slot.json"
        self.session.save_game(test_save)

        new_session = SessionManager()
        new_session.load_game(test_save)
        loaded_monsters = new_session.get_discovered_monsters()
        self.assertIn("m_dire_wolf", loaded_monsters)
        self.assertIn("m_bandit", loaded_monsters)

    def test_05_side_quest_and_beat_auto_discover_monsters(self):
        """Tarefa 3: Inimigos spawnados em side quests e beats são auto-registrados no bestiário."""
        self.session.game_state["discovered_monsters"] = []
        available_sq = self.session.story.get_available_side_quests()
        if available_sq:
            target_sq = available_sq[0]
            self.session.accept_side_quest(target_sq["id"])
            self.session.travel_to_side_quest(target_sq["id"])

            discovered = self.session.get_discovered_monsters()
            for enemy_id in target_sq.get("enemies", []):
                self.assertIn(enemy_id, discovered)

    def test_06_bestiary_enrichment_fields(self):
        """Tarefa 4: Verifica campos 'descricao', 'pontos_fortes', 'fraquezas' e helper get_monster_bestiary_entry."""
        # Todos os monstros do BESTIARIO_5E devem conter os 3 campos enriquecidos
        for m_id, data in BESTIARIO_5E.items():
            self.assertIn("descricao", data, f"Monstro {m_id} não possui 'descricao'")
            self.assertIn("pontos_fortes", data, f"Monstro {m_id} não possui 'pontos_fortes'")
            self.assertIn("fraquezas", data, f"Monstro {m_id} não possui 'fraquezas'")
            self.assertTrue(isinstance(data["pontos_fortes"], list), f"'pontos_fortes' em {m_id} deve ser lista")
            self.assertTrue(isinstance(data["fraquezas"], list), f"'fraquezas' em {m_id} deve ser lista")

        # Teste de resolução do helper
        entry_dire_wolf = get_monster_bestiary_entry("m_dire_wolf")
        self.assertIsNotNone(entry_dire_wolf)
        self.assertEqual(entry_dire_wolf.get("nome"), "Lobo Atroz")

        # Resolução por alias em português
        entry_pt = get_monster_bestiary_entry("lobo atroz")
        self.assertIsNotNone(entry_pt)
        self.assertEqual(entry_pt.get("nome"), "Lobo Atroz")

        # Resolução do Dragão Supremo
        entry_dragon = get_monster_bestiary_entry("dragao supremo")
        self.assertIsNotNone(entry_dragon)
        self.assertIn("Orbe Quebra-Chamas", " ".join(entry_dragon.get("fraquezas", [])))

    def test_07_deterministic_attack_target_resolution(self):
        """Tarefa 5: Resolução determinística de alvos por clique/ID ou texto genérico."""
        self.session.game_mode = "COMBATE"
        self.session.active_combat_targets = {
            "Lobo Atroz (1)": {
                "name": "Lobo Atroz (1)",
                "tipo_bestiario": "m_dire_wolf",
                "pv_atual": 30,
                "pv_max": 30,
                "ca": 14,
                "faction": "enemy",
                "status": "vivo"
            }
        }

        # 1. Ataque usando o ID de bestiário do clique da UI ("atacar m_dire_wolf")
        self.session._async_turn_processor("atacar m_dire_wolf", [], [])
        target = self.session.active_combat_targets.get("Lobo Atroz (1)")
        self.assertIsNotNone(target, "O Lobo Atroz original deve ter permanecido como alvo, sem instanciar clones.")
        self.assertNotIn("m_dire_wolf", self.session.active_combat_targets, "Não deve instanciar novo alvo fictício com o ID bruto.")

        # 2. Ataque usando o nome em português ("atacar lobo atroz")
        self.session._async_turn_processor("atacar lobo atroz", [], [])
        self.assertNotIn("lobo atroz", self.session.active_combat_targets)

        # 3. Ataque genérico sem alvo especificado ("atacar")
        self.session._async_turn_processor("atacar", [], [])
        self.assertNotIn("Inimigo", self.session.active_combat_targets)

    def test_08_chat_save_command_slots(self):
        """Valida comandos de salvamento via chat nos 3 slots com metadados completos."""
        # Limpa fila
        while not self.session.ui_queue.empty():
            self.session.ui_queue.get_nowait()
        self.session.ui_event_queue.clear()

        # Salva no Slot 2 via comando em linguagem natural
        self.session._async_turn_processor("salvar no slot 2", [], [])
        self.assertEqual(self.session.current_save_slot, 2)
        self.assertTrue(os.path.exists("saves/save_slot_2.json"))
        self.assertTrue(os.path.exists("saves/slot2.json"))

        meta2 = SessionManager.get_slot_metadata(2)
        self.assertFalse(meta2.get("is_empty"))
        self.assertEqual(meta2.get("name"), "Valerius")
        self.assertEqual(meta2.get("slot"), 2)

        # Salva no Slot 3 via comando de atalho
        self.session._async_turn_processor("save_slot:3", [], [])
        self.assertEqual(self.session.current_save_slot, 3)
        self.assertTrue(os.path.exists("saves/save_slot_3.json"))
        self.assertTrue(os.path.exists("saves/slot3.json"))

        # Mensagens na fila UI
        messages = []
        while not self.session.ui_queue.empty():
            messages.append(self.session.ui_queue.get_nowait())
        self.assertTrue(any("Slot 3" in m.get("content", "") for m in messages if m.get("type") == "system_message"))
        self.assertTrue(any(m.get("type") == "narrative" for m in messages))

    def test_09_quick_action_observation(self):
        """Valida Ação Rápida de Observação com rolagem de Percepção (CD 12) e dual-channel."""
        # 1. Modo Exploração na Taverna (Beat 1)
        self.session.game_mode = "EXPLORACAO"
        self.session.story.current_beat = 1
        self.session.game_state["discovered_rumors"] = []

        obs_text = "Observo atentamente o cenário ao redor, procurando detalhes, pistas e perigos."
        self.session._async_turn_processor(obs_text, [], [])

        messages = []
        while not self.session.ui_queue.empty():
            messages.append(self.session.ui_queue.get_nowait())

        sys_msgs = [m for m in messages if m.get("type") == "system_message"]
        narrative_msgs = [m for m in messages if m.get("type") == "narrative"]

        self.assertTrue(len(sys_msgs) >= 1)
        self.assertTrue(any("Percepção CD 12" in m.get("content", "") for m in sys_msgs))
        self.assertTrue(any("d20 (" in m.get("content", "") for m in sys_msgs))
        self.assertEqual(len(narrative_msgs), 1)
        self.assertEqual(narrative_msgs[0].get("npc_falando"), "Taverneiro")

        # 2. Modo Combate (não deve quebrar)
        self.session.game_mode = "COMBATE"
        self.session.active_combat_targets = {
            "Lobo Atroz (1)": {"name": "Lobo Atroz (1)", "pv_atual": 15, "pv_max": 30, "status": "vivo", "faction": "enemy"}
        }
        self.session._async_turn_processor(obs_text, [], [])

        c_messages = []
        while not self.session.ui_queue.empty():
            c_messages.append(self.session.ui_queue.get_nowait())
        self.assertTrue(any("Percepção CD 12" in m.get("content", "") for m in c_messages if m.get("type") == "system_message"))

    def test_10_quick_action_dialogue(self):
        """Valida Ação Rápida de Diálogo com rolagem de Persuasão (CD 11) e dual-channel."""
        # 1. Modo Exploração na Taverna (Beat 1)
        self.session.game_mode = "EXPLORACAO"
        self.session.story.current_beat = 1
        self.session.game_state["discovered_rumors"] = []

        talk_text = "Aproximo-me e tento conversar com quem estiver por perto para obter informações."
        self.session._async_turn_processor(talk_text, [], [])

        messages = []
        while not self.session.ui_queue.empty():
            messages.append(self.session.ui_queue.get_nowait())

        sys_msgs = [m for m in messages if m.get("type") == "system_message"]
        narrative_msgs = [m for m in messages if m.get("type") == "narrative"]

        self.assertTrue(len(sys_msgs) >= 1)
        self.assertTrue(any("Persuasão CD 11" in m.get("content", "") for m in sys_msgs))
        self.assertTrue(any("d20 (" in m.get("content", "") for m in sys_msgs))
        self.assertEqual(len(narrative_msgs), 1)
        self.assertEqual(narrative_msgs[0].get("npc_falando"), "Taverneiro")

        # 2. Modo Combate (parley / intimidação sem quebras)
        self.session.game_mode = "COMBATE"
        self.session.active_combat_targets = {
            "Lobo Atroz (1)": {"name": "Lobo Atroz (1)", "pv_atual": 20, "pv_max": 30, "status": "vivo", "faction": "enemy"}
        }
        self.session._async_turn_processor(talk_text, [], [])

        c_messages = []
        while not self.session.ui_queue.empty():
            c_messages.append(self.session.ui_queue.get_nowait())
        self.assertTrue(any("Persuasão CD 11" in m.get("content", "") for m in c_messages if m.get("type") == "system_message"))

    def test_11_clean_start_bestiary_and_rumors(self):
        """Garante que Bestiário e Rumores iniciam totalmente vazios no Beat 1."""
        fresh_session = SessionManager()
        self.assertEqual(fresh_session.game_state.get("discovered_monsters"), [])
        self.assertEqual(fresh_session.game_state.get("discovered_rumors"), [])
        self.assertEqual(fresh_session.get_discovered_monsters(), [])
        self.assertEqual(fresh_session.get_discovered_rumors(), [])

    def test_12_racial_speed_travel_mechanics(self):
        """Valida custos de marcha e suprimentos com base no deslocamento racial oficial D&D 5e."""
        # 1. Anão (Speed 7.5m): 3 dias, 3 suprimentos
        pc_dwarf = {"race": "Anão", "speed_m": 7.5, "equipment": [], "attributes": {"FOR": 10}}
        days, sup, spd, enc = self.session.calculate_travel_cost(pc_dwarf)
        self.assertEqual(days, 3)
        self.assertEqual(sup, 3)
        self.assertEqual(spd, 7.5)
        self.assertFalse(enc)

        # 2. Humano (Speed 9.0m): 2 dias, 2 suprimentos
        pc_human = {"race": "Humano", "speed_m": 9.0, "equipment": [], "attributes": {"FOR": 10}}
        days, sup, spd, enc = self.session.calculate_travel_cost(pc_human)
        self.assertEqual(days, 2)
        self.assertEqual(sup, 2)
        self.assertEqual(spd, 9.0)

        # 3. Elfo da Floresta (Speed 10.5m): 1 dia, 1 suprimento
        pc_elf = {"race": "Elfo dos Bosques", "speed_m": 10.5, "equipment": [], "attributes": {"FOR": 10}}
        days, sup, spd, enc = self.session.calculate_travel_cost(pc_elf)
        self.assertEqual(days, 1)
        self.assertEqual(sup, 1)
        self.assertEqual(spd, 10.5)

    def test_13_manual_do_jogador_content(self):
        """Valida que o Manual do Jogador D&D 5e está integrado e acessível estruturadamente."""
        from core.dnd_rules import get_manual_do_jogador
        manual = get_manual_do_jogador()
        self.assertIsInstance(manual, dict)
        self.assertTrue("secoes" in manual or "racas" in manual or "classes" in manual)


if __name__ == "__main__":
    unittest.main()
