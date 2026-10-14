import unittest
import json
import os
import sys
import copy
from typing import Dict, Any

# Assegura que o diretório raiz esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.story_engine import StoryManager
from core.game_engine import SessionManager, GameEngine
from ai_master.ai_client import AIGameMaster

class MockAI(AIGameMaster):
    """Mock da IA para testes de motor e regras."""
    def parse_player_intent(self, user_input: str, game_state: Dict[str, Any]) -> Dict[str, Any]:
        return {"tipo_acao": "exploracao"}

    def generate_narrative_from_math(self, sys_log: str, intent: str) -> str:
        return f"[MOCK NARRATIVA] {sys_log}"


class TestSideQuestsAndHeroesLore(unittest.TestCase):
    def setUp(self):
        self.ai = MockAI()
        self.session = SessionManager(self.ai)
        self.session.game_state["player_character"] = {
            "name": "Herói dos Ermos",
            "class": "Guerreiro",
            "race": "Humano",
            "level": 1,
            "xp": 0,
            "gold": 20,
            "hp_current": 12,
            "hp_max": 12,
            "inventory": ["Espada Longa"]
        }
        self.session.game_state["inventory"] = {}
        self.session.game_state["suprimentos_acampamento"] = 1
        self.session.game_state["suprimentos_maximos"] = 10
        self.session.game_state["quest_log"] = []

    def test_01_story_manager_loading_side_quests(self):
        """Valida carregamento seguro e filtragem de side quests por Ato."""
        story = StoryManager()
        
        # Teste de carregamento geral
        all_quests = story.get_available_side_quests()
        self.assertGreater(len(all_quests), 0, "Nenhuma side quest carregada do JSON!")
        
        # Filtragem por Ato 1
        act1_quests = story.get_available_side_quests(act=1)
        self.assertTrue(all(q.get("act") == 1 for q in act1_quests))
        self.assertGreater(len(act1_quests), 0)
        
        # Filtragem por Ato 2
        act2_quests = story.get_available_side_quests(act=2)
        self.assertTrue(all(q.get("act") == 2 for q in act2_quests))
        
        # Filtragem por Ato 3
        act3_quests = story.get_available_side_quests(act=3)
        self.assertTrue(all(q.get("act") == 3 for q in act3_quests))
        
        # Busca individual por ID
        quest = story.get_side_quest("sq_goblin_clearing")
        self.assertIsNotNone(quest)
        self.assertEqual(quest["title"], "O Covil dos Saqueadores")
        self.assertIn("rewards", quest)
        self.assertIn("xp", quest["rewards"])

    def test_02_story_manager_loading_heroes_lore(self):
        """Valida o compêndio de lore dos heróis e busca por ID, Nome e Classe."""
        story = StoryManager()
        
        all_lore = story.get_all_heroes_lore()
        self.assertGreater(len(all_lore), 0, "Compêndio de lore de heróis vazio!")
        
        # Busca direta por ID de herói
        hero01 = story.get_hero_lore("HERO-01")
        self.assertIsNotNone(hero01)
        self.assertEqual(hero01["class"], "Guerreiro")
        self.assertIn("Alistair", hero01["name"])
        self.assertIn("lore", hero01)
        self.assertIn("personality", hero01)
        
        # Busca por nome do herói
        hero_by_name = story.get_hero_lore("Alistair")
        self.assertIsNotNone(hero_by_name)
        self.assertEqual(hero_by_name["id"], "HERO-01")
        
        # Busca por classe mapeada (ex: fighter, cleric)
        fighter_lore = story.get_hero_lore("fighter")
        self.assertIsNotNone(fighter_lore)
        self.assertEqual(fighter_lore["class"], "Guerreiro")
        
        cleric_lore = story.get_hero_lore("cleric")
        self.assertIsNotNone(cleric_lore)
        self.assertEqual(cleric_lore["class"], "Clérigo")

    def test_03_accept_side_quest_flow(self):
        """Valida o registro de missões secundárias ativas no quest_log."""
        # Aceita uma quest válida
        success = self.session.accept_side_quest("sq_goblin_clearing")
        self.assertTrue(success, "Falha ao aceitar side quest válida!")
        
        # Verifica se entrou no quest_log com status ativa
        active = self.session.get_active_quests()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["id"], "sq_goblin_clearing")
        self.assertEqual(active[0]["status"], "ativa")
        
        # Evita duplicação se tentar aceitar de novo
        duplicate_success = self.session.accept_side_quest("sq_goblin_clearing")
        self.assertFalse(duplicate_success, "Permitiu aceitar quest duplicada!")
        self.assertEqual(len(self.session.get_active_quests()), 1)
        
        # Tenta aceitar quest inexistente
        fake_success = self.session.accept_side_quest("sq_inexistente_123")
        self.assertFalse(fake_success)

    def test_04_complete_side_quest_and_rewards_delivery(self):
        """Valida a conclusão e entrega matemática de XP, ouro, suprimentos e itens."""
        # Aceita a quest
        self.session.accept_side_quest("sq_forest_shrine")
        
        # Valores prévios
        xp_antigo = self.session.game_state["player_character"]["xp"]
        ouro_antigo = self.session.game_state["player_character"]["gold"]
        sup_antigo = self.session.game_state["suprimentos_acampamento"]
        
        # Conclui a quest (recompensas de sq_forest_shrine: xp 450, gold 90, supplies 8, items: i_elven_shortbow, i_amulet_health)
        result = self.session.complete_side_quest("sq_forest_shrine")
        self.assertTrue(result["success"])
        self.assertEqual(result["quest_id"], "sq_forest_shrine")
        
        # Verifica transição de status no quest_log
        self.assertEqual(len(self.session.get_active_quests()), 0)
        completed = self.session.get_completed_quests()
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0]["status"], "concluida")
        
        # Verifica entrega de XP
        self.assertEqual(
            self.session.game_state["player_character"]["xp"],
            xp_antigo + 450,
            "XP da recompensa não foi somado corretamente!"
        )
        
        # Verifica entrega de Ouro
        self.assertEqual(
            self.session.game_state["player_character"]["gold"],
            ouro_antigo + 90,
            "Ouro da recompensa não foi somado corretamente!"
        )
        
        # Verifica entrega de Suprimentos
        self.assertEqual(
            self.session.game_state["suprimentos_acampamento"],
            sup_antigo + 8,
            "Suprimentos não foram somados corretamente!"
        )
        
        # Verifica entrega de Item no inventário sincronizado
        item_count = self.session.get_inventory_item_count("i_elven_shortbow")
        self.assertEqual(item_count, 1, "Item 'i_elven_shortbow' não foi adicionado ao inventário!")

    def test_05_quest_log_save_and_persistence(self):
        """Valida que o quest_log persiste corretamente no save_game e load_game."""
        # Aceita uma quest e conclui outra
        self.session.accept_side_quest("sq_goblin_clearing")
        self.session.accept_side_quest("sq_forest_shrine")
        self.session.complete_side_quest("sq_goblin_clearing")
        
        # Salva o jogo
        save_ok = self.session.save_game()
        self.assertTrue(save_ok, "Falha ao salvar jogo!")
        
        # Cria uma nova instância de SessionManager e recarrega
        nova_sessao = SessionManager(self.ai)
        load_ok = nova_sessao.load_game()
        self.assertTrue(load_ok, "Falha ao carregar save!")
        
        # Verifica persistência do quest_log
        active = nova_sessao.get_active_quests()
        completed = nova_sessao.get_completed_quests()
        
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["id"], "sq_forest_shrine")
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0]["id"], "sq_goblin_clearing")

    def test_06_game_engine_alias_compatibility(self):
        """Valida que o alias GameEngine aponta para SessionManager."""
        self.assertIs(GameEngine, SessionManager)
        inst = GameEngine(self.ai)
        self.assertIsInstance(inst, SessionManager)

if __name__ == "__main__":
    unittest.main()
