import unittest
import json
import os
import sys
import copy
from typing import Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.story_engine import StoryManager
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

class MockAI(AIGameMaster):
    """Mock da IA para testes desacoplados e puramente matemáticos."""
    def parse_player_intent(self, user_input: str, game_state: Dict[str, Any]) -> Dict[str, Any]:
        low = user_input.lower()
        if "atacar" in low:
            return {"tipo_acao": "ATACAR", "alvo": ["Tirano"], "recurso_utilizado": "espada"}
        elif "curar" in low or "pocao" in low:
            return {"tipo_acao": "USAR_ITEM", "recurso_utilizado": "Poção de Cura"}
        elif "antidoto" in low:
            return {"tipo_acao": "USAR_ITEM", "recurso_utilizado": "Antídoto Menor"}
        elif "avancar" in low:
            return {"tipo_acao": "AVANCAR_HISTORIA"}
        return {"tipo_acao": "exploracao"}

    def generate_narrative_from_math(self, sys_log: str, intent: str) -> str:
        return f"[MOCK NARRATIVA] {sys_log}"


class TestBloco7Backend(unittest.TestCase):
    def setUp(self):
        self.ai = MockAI()
        self.session = SessionManager(self.ai)

    def test_01_compendio_itens_data_integrity(self):
        """Valida a estrutura, balanceamento e variações de itens.json (Item C)."""
        with open("data/items.json", "r", encoding="utf-8") as f:
            items = json.load(f)

        # 1. Checa categorias obrigatórias
        required_categories = ["weapons", "armor", "accessories", "consumables"]
        for cat in required_categories:
            self.assertIn(cat, items, f"Categoria '{cat}' ausente em items.json")

        # 2. Preservação estrita dos itens legados vitais
        self.assertIn("healing_potion", items["consumables"])
        self.assertEqual(items["consumables"]["healing_potion"]["id"], "i_potion_healing")
        self.assertIn("scroll_of_revivify", items["consumables"])
        self.assertEqual(items["consumables"]["scroll_of_revivify"]["id"], "i_scroll_revive")

        # 3. Presença de variações (básica e aprimorada/rúnica)
        # Armas
        self.assertIn("longsword", items["weapons"])
        self.assertIn("runic_longsword", items["weapons"])
        self.assertIn("shortbow", items["weapons"])
        self.assertIn("elven_shortbow", items["weapons"])

        # Armaduras
        self.assertIn("leather_armor", items["armor"])
        self.assertIn("shadow_leather", items["armor"])
        self.assertIn("chain_mail", items["armor"])
        self.assertIn("dwarven_chain_mail", items["armor"])
        self.assertIn("shield", items["armor"])
        self.assertIn("heraldic_shield", items["armor"])

        # Acessórios (anéis, amuletos, mantos, botas)
        self.assertIn("ring_protection", items["accessories"])
        self.assertIn("ring_warding", items["accessories"])
        self.assertIn("amulet_health", items["accessories"])
        self.assertIn("amulet_radiance", items["accessories"])
        self.assertIn("cloak_elvenkind", items["accessories"])
        self.assertIn("cloak_displacement", items["accessories"])
        self.assertIn("boots_speed", items["accessories"])
        self.assertIn("boots_striding", items["accessories"])

        # Consumíveis (antídotos, poção maior, rações)
        self.assertIn("greater_healing_potion", items["consumables"])
        self.assertIn("antidote", items["consumables"])
        self.assertIn("elixir_purity", items["consumables"])
        self.assertIn("rations", items["consumables"])
        self.assertIn("hearty_rations", items["consumables"])

        # 4. Equilíbrio de números contra o Bestiário (sem inflação absurda)
        for w_id, w_data in items["weapons"].items():
            self.assertIn(w_data.get("bonus_hit", 0), [0, 1, 2], f"Arma {w_id} tem bônus de acerto desbalanceado!")
            self.assertIn(w_data.get("bonus_damage", 0), [0, 1, 2], f"Arma {w_id} tem bônus de dano desbalanceado!")

        for a_id, a_data in items["accessories"].items():
            ac_bon = a_data.get("ac_bonus", 0)
            self.assertTrue(ac_bon <= 2, f"Acessório {a_id} tem bônus de CA desbalanceado ({ac_bon})!")

    def test_02_allies_pool_classes_and_races(self):
        """Valida que o pool de aliados cobre todas as 6 classes e 7 raças oficiais (Item A)."""
        story = StoryManager()
        pool = story.allies_pool

        # 6 Classes Oficiais
        expected_classes = {"Guerreiro", "Clérigo", "Paladino", "Mago", "Patrulheiro", "Ladino"}
        classes_no_pool = {a["class"] for a in pool.values()}
        for c in expected_classes:
            self.assertIn(c, classes_no_pool, f"Classe '{c}' não encontrada no allies_pool!")

        # 7 Raças Oficiais
        expected_races = {"Humano", "Anão da Colina", "Elfo da Floresta", "Halfling", "Draconato", "Meio-Orc", "Tiefling"}
        races_no_pool = {a["race"] for a in pool.values()}
        for r in expected_races:
            self.assertIn(r, races_no_pool, f"Raça '{r}' não encontrada no allies_pool!")

        # Validação de ficha D&D 5e completa
        for ally_id, sheet in pool.items():
            self.assertIn("name", sheet)
            self.assertIn("race", sheet)
            self.assertIn("class", sheet)
            self.assertIn("pv_atual", sheet)
            self.assertIn("pv_max", sheet)
            self.assertIn("ca", sheet)
            self.assertIn("actions", sheet)
            self.assertIn("abilities", sheet)
            self.assertEqual(sheet.get("faction"), "ally")
            self.assertTrue(len(sheet["actions"]) > 0, f"Aliado {ally_id} não possui ações de combate configuradas!")

    def test_03_recrutamento_organico_sem_duplicar_classe_do_jogador(self):
        """Valida que o recrutamento adaptativo exclui a classe do herói e forma party completa de 6 classes."""
        story = StoryManager()
        
        # Jogador é um Mago Tiefling
        player_mage = {
            "name": "Ignis",
            "class": "Mago",
            "race": "Tiefling",
            "hp_current": 16,
            "hp_max": 16
        }

        recrutados = []
        for beat in [1, 4, 8, 10, 12]:
            ally = story.recruit_ally_for_beat(beat, player_mage)
            if ally:
                recrutados.append(ally)

        # Deve recrutar exatamente 5 aliados
        self.assertEqual(len(recrutados), 5, f"Esperado 5 aliados recrutados, obteve {len(recrutados)}")

        # NENHUM aliado pode ser Mago!
        classes_recrutadas = [a["class"] for a in recrutados]
        self.assertNotIn("Mago", classes_recrutadas, "Aliado Mago foi recrutado quando o jogador já era Mago!")

        # Todas as 5 classes recrutadas devem ser distintas
        self.assertEqual(len(set(classes_recrutadas)), 5, "Houve repetição de classe entre os aliados recrutados!")

        # A Party Completa (Jogador + 5 Aliados) cobre as 6 classes oficiais
        party_classes = set(classes_recrutadas) | {player_mage["class"]}
        expected_all = {"Guerreiro", "Clérigo", "Paladino", "Mago", "Patrulheiro", "Ladino"}
        self.assertEqual(party_classes, expected_all, "A party final não cobre as 6 classes oficiais!")

    def test_04_recrutamento_para_jogador_guerreiro(self):
        """Valida que jogador Guerreiro recruta as outras 5 classes sem duplicação de Guerreiro."""
        story = StoryManager()
        player_fighter = {
            "name": "Krag",
            "class": "Guerreiro",
            "race": "Meio-Orc",
            "hp_current": 28,
            "hp_max": 28
        }

        recrutados = []
        for beat in [1, 4, 8, 10, 12]:
            ally = story.recruit_ally_for_beat(beat, player_fighter)
            if ally:
                recrutados.append(ally)

        self.assertEqual(len(recrutados), 5)
        classes_recrutadas = [a["class"] for a in recrutados]
        self.assertNotIn("Guerreiro", classes_recrutadas, "Aliado Guerreiro não deve ser recrutado por jogador Guerreiro!")
        party_classes = set(classes_recrutadas) | {"Guerreiro"}
        expected_all = {"Guerreiro", "Clérigo", "Paladino", "Mago", "Patrulheiro", "Ladino"}
        self.assertEqual(party_classes, expected_all)

    def test_05_sincronizacao_inventario_e_consumiveis(self):
        """Valida manipulação segura de itens quando pc['inventory'] é lista ou dict (Item D)."""
        session = SessionManager(self.ai)
        
        # Caso A: pc['inventory'] como lista de strings (formato comum em character sheets)
        session.game_state["player_character"] = {
            "name": "Aventureiro",
            "hp_current": 10,
            "hp_max": 20,
            "inventory": ["Espada Longa", "Poção de Cura", "Poção de Cura", "Pergaminho de Ressurreição"]
        }
        session.game_state["inventory"] = {
            "i_potion_healing": 2,
            "i_scroll_revive": 1,
            "i_antidote": 1,
            "i_rations": 3
        }

        # Contagem agnóstica sem AttributeError
        qtd_pot = session.get_inventory_item_count("i_potion_healing")
        self.assertEqual(qtd_pot, 2)
        qtd_rev = session.get_inventory_item_count("i_scroll_revive")
        self.assertEqual(qtd_rev, 1)

        # Consumo seguro
        consumed = session.consume_inventory_item("i_potion_healing", 1)
        self.assertTrue(consumed)
        self.assertEqual(session.get_inventory_item_count("i_potion_healing"), 1)

        # Uso de antídoto no condition manager
        session.condition_manager.apply_condition("poisoned")
        self.assertIn("poisoned", session.condition_manager.active_conditions)

        # Simula ação USAR_ITEM com antídoto
        session._async_turn_processor("usar antidoto", [], [])
        self.assertNotIn("poisoned", session.condition_manager.active_conditions)

        # Uso de poção de cura
        session.game_state["player_character"]["hp_current"] = 5
        session._async_turn_processor("usar pocao de cura", [], [])
        self.assertGreater(session.game_state["player_character"]["hp_current"], 5)

    def test_06_revive_scroll_automatic_on_player_death(self):
        """Valida que o Pergaminho de Ressurreição salva o jogador sem disparar AttributeError."""
        session = SessionManager(self.ai)
        session.game_state["player_character"] = {
            "name": "Guerreiro",
            "hp_current": 0,
            "hp_max": 30,
            "status": "morto",
            "inventory": ["Espada Longa", "Pergaminho de Ressurreição"]
        }
        session.game_state["inventory"] = {
            "i_scroll_revive": 1
        }
        session.story.current_beat = 3  # Não é clímax

        session.resolve_player_death()

        # O jogador deve reviver com metade do HP
        pc = session.game_state["player_character"]
        self.assertEqual(pc.get("status"), "vivo")
        self.assertEqual(pc.get("hp_current"), 15)
        self.assertEqual(session.get_inventory_item_count("i_scroll_revive"), 0)

    def test_07_climax_snapshot_and_deja_vu_restoration(self):
        """Valida a mecânica completa do Beat 15 (Clímax): entrada da party, wipe e Déjà Vu intacto (Item B)."""
        session = SessionManager(self.ai)
        
        # 1. Configura herói no nível 5 com 1500 XP
        pc = {
            "name": "Herói Lendário",
            "class": "Paladino",
            "race": "Humano",
            "level": 5,
            "xp": 1500,
            "hp_current": 45,
            "hp_max": 45,
            "ca": 18,
            "spell_slots": {"1": 4, "2": 2},
            "inventory": {"i_potion_healing": 3}
        }
        session.game_state["player_character"] = pc
        session.game_state["inventory"] = {"i_potion_healing": 3}

        # 2. Desbloqueia aliados previamente recrutados ao longo da campanha
        session.story.unlock_ally("fighter")  # Thorgar
        session.story.unlock_ally("cleric")   # Karg
        session.story.unlock_ally("mage")     # Azaroth

        # 3. Avança para o Beat 15 (Clímax)
        session.story.set_beat(14)
        session._async_turn_processor("avancar", [], [])

        self.assertEqual(session.story.current_beat, 15)
        self.assertTrue(session.story.is_climax())
        self.assertEqual(session.game_mode, "COMBATE")

        # 4. Todos os aliados devem estar em campo como faction 'ally'
        aliados_em_campo = [k for k, v in session.active_combat_targets.items() if v.get("faction") == "ally"]
        self.assertEqual(len(aliados_em_campo), 3)
        self.assertIn("Thorgar, o Implacável", aliados_em_campo)
        self.assertIn("Karg, o Devoto", aliados_em_campo)
        self.assertIn("Azaroth, o Arcanista", aliados_em_campo)

        # 5. O Dragão Supremo no Loop 0 deve ter estatísticas imbatíveis
        dragao = next(v for v in session.active_combat_targets.values() if v.get("faction") == "enemy")
        self.assertEqual(dragao["pv_max"], 999)
        self.assertEqual(dragao["ca"], 99)

        # 6. O Snapshot foi criado no momento de entrada
        self.assertIsNotNone(session.story.snapshot)

        # 7. Simula Wipe mortal do Sopro do Fim do Mundo (todos a 0 HP)
        session.game_state["player_character"]["hp_current"] = 0
        session.game_state["player_character"]["status"] = "morto"
        for v in session.active_combat_targets.values():
            if v.get("faction") == "ally":
                v["pv_atual"] = 0
                v["status"] = "morto"

        # 8. Aciona resolve_player_death no Clímax (Loop 0)
        session.resolve_player_death()

        # 9. O DÉJÀ VU É ACIONADO!
        meta = session.game_state.get("meta", {})
        self.assertEqual(meta.get("loop_count"), 1, "Loop count deveria ter sido incrementado para 1!")
        self.assertTrue(meta.get("segredo_tirano"), "O segredo do tirano deveria ter sido ativado!")

        # 10. O Jogador deve estar EXATAMENTE como entrou na batalha
        pc_restaurado = session.game_state["player_character"]
        self.assertEqual(pc_restaurado["hp_current"], 45, "HP do jogador não foi restaurado pelo snapshot!")
        self.assertEqual(pc_restaurado["status"], "vivo")
        self.assertEqual(pc_restaurado["xp"], 1500, "XP do jogador foi perdido no déjà vu!")
        self.assertEqual(pc_restaurado["level"], 5, "Nível do jogador foi alterado no déjà vu!")
        self.assertEqual(session.get_inventory_item_count("i_potion_healing"), 3, "Itens do jogador foram perdidos!")

        # 11. TODOS os Aliados retornam INTACTOS com HP cheio e vivos
        for k, v in session.active_combat_targets.items():
            if v.get("faction") == "ally":
                self.assertEqual(v["status"], "vivo", f"Aliado {k} não foi revivido pelo déjà vu!")
                self.assertEqual(v["pv_atual"], v["pv_max"], f"Aliado {k} não retornou com HP cheio!")

        # 12. O Dragão Supremo agora tem a armadura quebrada para a vitória da party!
        dragao_pos_loop = next(v for v in session.active_combat_targets.values() if v.get("faction") == "enemy")
        self.assertEqual(dragao_pos_loop["ca"], 14, "Armadura do dragão não foi quebrada para CA 14!")
        self.assertEqual(dragao_pos_loop["pv_max"], 100, "PV do dragão não foi reduzido para 100!")
        self.assertEqual(dragao_pos_loop["pv_atual"], 100)

        # 13. O combate continua ativo (não volta pra taverna no Déjà Vu!)
        self.assertEqual(session.game_mode, "COMBATE")

        # 14. Mensagem de Déjà Vu registrada na fila da UI
        msgs = []
        while not session.ui_queue.empty():
            msg = session.ui_queue.get()
            if msg.get("type") == "system_message":
                msgs.append(msg["content"])
        deja_vu_logged = any("DÉJÀ VU" in m or "tempo se estilhaça e retrocede" in m for m in msgs)
        self.assertTrue(deja_vu_logged, "Mensagem do Déjà Vu não foi encontrada nos logs do sistema!")

if __name__ == "__main__":
    unittest.main()
