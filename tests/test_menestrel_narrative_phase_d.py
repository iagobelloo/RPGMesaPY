import unittest
import json
import os
import sys
import copy
from typing import Dict, Any

# Assegura que o diretório raiz esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.story_engine import StoryManager
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

class DummyAI(AIGameMaster):
    """Subclasse de mock para testes seguros e offline."""
    def parse_player_intent(self, user_input: str, game_state: Dict[str, Any]) -> Dict[str, Any]:
        return {"tipo_acao": "AVANCAR_HISTORIA", "recurso_utilizado": None, "alvo": [], "intencao_cena": "avançar"}

    def generate_narrative_from_math(self, sys_log: str, intent: str) -> str:
        return self._create_visceral_fallback(sys_log, intent)


class TestMenestrelNarrativePhaseD(unittest.TestCase):
    """
    Suíte de testes da FASE D:
    - Validação das diretrizes de Maelor (docs/dm_guidelines.md) em AIGameMaster.
    - Fallbacks viscerais de Maelor (_create_visceral_fallback).
    - Injeção contextual no prólogo ({nome}, {raca}, {classe}, {antecedente}, {tendencia}).
    - Regra canônica de aliados juramentados (solitário nos Beats 1-14, grupo no Beat 15).
    - Recompensas de side quests e narrativa de juramento de heróis resgatados.
    - Robustez contra colisões e entradas atípicas.
    """

    def setUp(self):
        self.ai = DummyAI()
        self.session = SessionManager(self.ai)
        self.session.game_state["player_character"] = {
            "name": "Valerius",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 1,
            "hp_current": 12,
            "hp_max": 12,
            "xp": 0,
            "gold": 25,
            "inventory": {}
        }
        self.session.game_state["inventory"] = {}
        self.session.game_state["suprimentos_acampamento"] = 2
        self.session.game_state["suprimentos_maximos"] = 5
        self.session.game_state["quest_log"] = []

    def test_01_dm_guidelines_loaded_into_system_instruction(self):
        """Valida que AIGameMaster carrega com fidelidade as diretrizes de Maelor de docs/dm_guidelines.md."""
        self.assertTrue(os.path.exists("docs/dm_guidelines.md"), "docs/dm_guidelines.md deve existir!")
        with open("docs/dm_guidelines.md", "r", encoding="utf-8") as f:
            guidelines_content = f.read()

        ai = AIGameMaster()
        self.assertIn("Maelor das Cordas de Cinza", ai.system_instruction)
        self.assertIn("Grounded Dark Fantasy", ai.system_instruction)
        self.assertIn("Classes Válidas", ai.system_instruction)

    def test_02_visceral_fallback_ally_oath(self):
        """Valida fallback visceral para juramento de aliado resgatado ou recrutado."""
        fallback = self.ai._create_visceral_fallback(
            combat_log="[JURAMENTO] Herói prestou juramento de lealdade",
            intencao_cena="O aliado faz seu juramento para marchar na batalha final"
        )
        self.assertIn("juramento", fallback.lower())
        self.assertIn("aliado", fallback.lower())

    def test_03_visceral_fallback_side_quest(self):
        """Valida fallback visceral para side quest e conclusão de contratos."""
        fallback = self.ai._create_visceral_fallback(
            combat_log="Missão concluída com sucesso no acampamento",
            intencao_cena="Conclusão da side quest de resgate e contrato"
        )
        self.assertIn("contrato", fallback.lower())
        self.assertIn("recompensa", fallback.lower())

    def test_04_visceral_fallback_tactical_retreat(self):
        """Valida fallback visceral para recuo tático e fuga com sobrevivência."""
        fallback = self.ai._create_visceral_fallback(
            combat_log="Recuo tático ordenado pelo herói",
            intencao_cena="O herói decide recuar e fugir pela mata"
        )
        self.assertIn("recua", fallback.lower())
        self.assertIn("fuga", fallback.lower())

    def test_05_visceral_fallback_deja_vu_and_loop(self):
        """Valida fallback visceral para déjà vu e reinício do loop temporal."""
        fallback = self.ai._create_visceral_fallback(
            combat_log="Loop 1 reiniciado após sopro fatal",
            intencao_cena="Uma sensação de déjà vu e loop temporal queima a mente"
        )
        self.assertTrue("déjà vu" in fallback.lower() or "ciclo" in fallback.lower() or "tempo" in fallback.lower())

    def test_06_visceral_fallback_rest_and_lethal_combat(self):
        """Valida fallbacks viscerais para descanso revigorante e combate letal."""
        # Descanso
        fallback_rest = self.ai._create_visceral_fallback(
            combat_log="Recuperou HP após repouso",
            intencao_cena="O herói procura descanso seguro na taverna"
        )
        self.assertIn("descanso", fallback_rest.lower())

        # Combate Letal
        fallback_death = self.ai._create_visceral_fallback(
            combat_log="0 HP. Dano fatal sofrido na garganta",
            intencao_cena="Morte iminente no chão lamacento"
        )
        self.assertIn("morte", fallback_death.lower())

    def test_07_personalized_prologue_variable_injection(self):
        """Valida formatação do prólogo com injeção estrita de {nome}, {raca}, {classe}, {antecedente}, {tendencia}."""
        char_data = {
            "name": "Alden Sol-Negro",
            "race": "Elfo da Floresta",
            "class": "Patrulheiro",
            "background": "Soldado",
            "alignment": "Caótico e Bom"
        }

        prologue = self.ai.get_personalized_prologue(char_data)
        self.assertIn("Alden Sol-Negro", prologue)
        self.assertIn("Elfo da Floresta", prologue)
        self.assertIn("Patrulheiro", prologue)
        self.assertIn("Soldado", prologue)
        self.assertIn("Caótico e Bom", prologue)

        # Nenhuma variável não formatada pode sobrar no texto
        for placeholder in ["{nome}", "{raca}", "{classe}", "{antecedente}", "{tendencia}"]:
            self.assertNotIn(placeholder, prologue)

    def test_08_allies_adventuring_solo_beats_1_to_14_and_join_climax_beat_15(self):
        """
        Garante a regra mecânica:
        Nos Beats 1 a 14 o herói viaja e luta estritamente sozinho.
        Aliados juramentados só entram em combate ativo no Beat 15 (Clímax).
        """
        # Desbloqueia aliados na jornada
        self.session.story.unlock_ally("HERO-01")
        self.session.story.unlock_ally("cleric")
        
        unlocked = self.session.story.get_unlocked_allies()
        self.assertGreaterEqual(len(unlocked), 2)

        # Beat 4 (Acampamento Devastado - combate regular)
        self.session.story.current_beat = 3
        self.session.game_mode = "EXPLORACAO"
        self.session._async_turn_processor("avancar na estrada", [], [])

        self.assertEqual(self.session.story.current_beat, 4)
        allies_in_combat_beat_4 = [t for t in self.session.active_combat_targets.values() if t.get("faction") == "ally"]
        self.assertEqual(len(allies_in_combat_beat_4), 0, "Aliados juramentados não devem entrar em combate no Beat 4!")

        # Beat 15 (Clímax do Tirano)
        self.session.active_combat_targets.clear()
        self.session.story.current_beat = 14
        self.session.game_mode = "EXPLORACAO"
        self.session._async_turn_processor("avancar para o covil do tirano", [], [])

        self.assertEqual(self.session.story.current_beat, 15)
        self.assertTrue(self.session.story.is_climax())
        allies_in_climax = [t for t in self.session.active_combat_targets.values() if t.get("faction") == "ally"]
        self.assertGreaterEqual(len(allies_in_climax), 2, "Todos os aliados juramentados devem lutar no Clímax!")

    def test_09_side_quest_completion_rewards_and_rescued_hero_oath(self):
        """Valida que side quests entregam recompensas de XP, ouro, itens e registram o juramento do herói resgatado."""
        quest_data = {
            "id": "sq_test_rescue",
            "title": "Resgate nas Criptas",
            "act": 1,
            "source": "Rumor da Taverna",
            "associated_hero_id": "HERO-05",
            "rewards": {
                "xp": 300,
                "gold": 50,
                "items": ["i_potion_healing"],
                "supplies": 2
            }
        }
        self.session.story.side_quests_data["sq_test_rescue"] = quest_data
        self.session.accept_side_quest("sq_test_rescue")

        initial_xp = self.session.game_state["player_character"]["xp"]
        initial_gold = self.session.game_state["player_character"]["gold"]

        # Conclui a side quest
        res = self.session.complete_side_quest("sq_test_rescue")
        self.assertTrue(res["success"])

        # Recompensas entregues
        self.assertEqual(self.session.game_state["player_character"]["xp"], initial_xp + 300)
        self.assertEqual(self.session.game_state["player_character"]["gold"], initial_gold + 50)
        self.assertGreaterEqual(self.session.get_inventory_item_count("i_potion_healing"), 1)

        # Herói HERO-05 juramentado no StoryManager
        self.assertTrue(self.session.story.flags.get("ally_HERO-05_unlocked"))
        self.assertIn("HERO-05", self.session.story.get_unlocked_allies())

        # Mensagem de juramento presente na ui_queue
        found_oath_message = False
        while not self.session.ui_queue.empty():
            msg = self.session.ui_queue.get()
            content = str(msg.get("content", "")) + str(msg.get("narrativa", {}).get("texto", ""))
            if "juramento" in content.lower() or "HERO-05" in content or "Garrick" in content:
                found_oath_message = True
                break
        self.assertTrue(found_oath_message, "A narrativa/log de juramento do herói resgatado deve ser emitida na fila da UI!")

    def test_10_narrative_methods_no_collisions_or_exceptions(self):
        """Valida robustez extrema de métodos de narrativa contra entradas nulas, vazias e não convencionais."""
        # Teste com entradas atípicas em _create_visceral_fallback
        res_empty = self.ai._create_visceral_fallback("", "")
        self.assertIsInstance(res_empty, str)
        self.assertTrue(len(res_empty) > 0)

        res_none = self.ai._create_visceral_fallback(None, None)
        self.assertIsInstance(res_none, str)
        self.assertTrue(len(res_none) > 0)

        # Teste com dados parciais em get_personalized_prologue
        res_prologue_empty = self.ai.get_personalized_prologue({})
        self.assertIsInstance(res_prologue_empty, str)
        self.assertTrue(len(res_prologue_empty) > 0)


if __name__ == "__main__":
    unittest.main()
