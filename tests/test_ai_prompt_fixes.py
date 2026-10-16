import unittest
import os
from unittest.mock import MagicMock
from ai_master.ai_client import AIGameMaster

class TestAIPromptFixes(unittest.TestCase):
    def test_model_name_calibration(self):
        """Garante que o modelo oficial seja gemini-3.5-flash-lite e respeite a variável de ambiente GEMINI_MODEL."""
        ai = AIGameMaster()
        self.assertEqual(ai.model_name, "gemini-3.5-flash-lite")
        self.assertIn("gemini-3.5", ai.model_name)

        # Teste de override via variável de ambiente
        os.environ["GEMINI_MODEL"] = "gemini-flash-lite-latest"
        ai_custom = AIGameMaster()
        self.assertEqual(ai_custom.model_name, "gemini-flash-lite-latest")
        del os.environ["GEMINI_MODEL"]

    def test_parse_player_intent_tavern_dialogue_and_missions(self):
        """Valida que pedidos de missão, trabalho, diálogos e pedidos de cerveja sejam DIALOGAR/INTERAGIR_CENARIO e nunca AVANCAR_HISTORIA."""
        ai = AIGameMaster()
        ai.client.models.generate_content = MagicMock(side_effect=Exception("Simulação de fallback heurístico offline"))

        # 1. Procura de missão
        res_missao = ai.parse_player_intent("estava a procura de uma missão", {})
        self.assertIn(res_missao["tipo_acao"], ["DIALOGAR", "INTERAGIR_CENARIO"])
        self.assertNotEqual(res_missao["tipo_acao"], "AVANCAR_HISTORIA")
        self.assertTrue("missões" in res_missao["intencao_cena"] or "trabalhos" in res_missao["intencao_cena"])

        # 2. Procuro trabalho / contrato
        res_trab = ai.parse_player_intent("procuro trabalho ou contrato", {})
        self.assertIn(res_trab["tipo_acao"], ["DIALOGAR", "INTERAGIR_CENARIO"])
        self.assertNotEqual(res_trab["tipo_acao"], "AVANCAR_HISTORIA")

        # 3. Falar com taverneiro
        res_tav = ai.parse_player_intent("falar com taverneiro", {})
        self.assertIn(res_tav["tipo_acao"], ["DIALOGAR", "INTERAGIR_CENARIO"])
        self.assertNotEqual(res_tav["tipo_acao"], "AVANCAR_HISTORIA")

        # 4. Pedir cerveja
        res_beer = ai.parse_player_intent("pedir uma cerveja", {})
        self.assertIn(res_beer["tipo_acao"], ["DIALOGAR", "INTERAGIR_CENARIO"])
        self.assertNotEqual(res_beer["tipo_acao"], "AVANCAR_HISTORIA")

        # 5. Olhar ao redor na taverna
        res_look = ai.parse_player_intent("olhar ao redor na taverna", {})
        self.assertEqual(res_look["tipo_acao"], "INTERAGIR_CENARIO")

        # 6. Sair da mesa para conversar (não deve avançar a história)
        res_table = ai.parse_player_intent("sair da mesa e falar com o taverneiro", {})
        self.assertIn(res_table["tipo_acao"], ["DIALOGAR", "INTERAGIR_CENARIO"])
        self.assertNotEqual(res_table["tipo_acao"], "AVANCAR_HISTORIA")

        # 7. Avanço real pela estrada
        res_road = ai.parse_player_intent("viajar para a estrada e partir da taverna", {})
        self.assertEqual(res_road["tipo_acao"], "AVANCAR_HISTORIA")

    def test_visceral_fallback_tavern_missions_and_dialogues(self):
        """Valida que buscas de missões e conversas de taverna não caiam no dedilhar genérico padrão."""
        ai = AIGameMaster()

        # 1. Procura de missão
        fb_mission = ai._create_visceral_fallback("O herói procura trabalhos disponíveis.", "estava a procura de uma missão na taverna")
        self.assertNotIn("dedilhar melancólico", fb_mission.lower())
        self.assertIn("taverneiro", fb_mission.lower())
        self.assertTrue("contratos" in fb_mission.lower() or "pergaminhos" in fb_mission.lower() or "trabalho" in fb_mission.lower())

        # 2. Conversa com Taverneiro / Pedido de cerveja
        fb_beer = ai._create_visceral_fallback("Caneca servida.", "pedir uma cerveja ao taverneiro")
        self.assertNotIn("dedilhar melancólico", fb_beer.lower())
        self.assertIn("taverneiro", fb_beer.lower())
        self.assertIn("cerveja", fb_beer.lower())

        # 3. Conversa com Maelor
        fb_maelor = ai._create_visceral_fallback("Aproximação do menestrel.", "conversar com maelor")
        self.assertTrue("epitáfio" in fb_maelor.lower() or "tirano" in fb_maelor.lower() or "alaúde" in fb_maelor.lower())

        # 4. Observação / Rumores
        fb_rumors = ai._create_visceral_fallback("Ouvindo murmúrios.", "ouvir rumores e boatos da taverna")
        self.assertTrue("mercenários" in fb_rumors.lower() or "estrada" in fb_rumors.lower() or "cochicham" in fb_rumors.lower())

    def test_tactical_5e_actions_intent_and_fallbacks(self):
        """Valida a extração de ACAO_TATICA_5E e seus fallbacks viscerais dedicados."""
        ai = AIGameMaster()
        ai.client.models.generate_content = MagicMock(side_effect=Exception("Simulação de fallback heurístico offline"))

        # 1. Esquiva
        intent_dodge = ai.parse_player_intent("esquivar do golpe do inimigo", {})
        self.assertEqual(intent_dodge["tipo_acao"], "ACAO_TATICA_5E")
        self.assertEqual(intent_dodge["recurso_utilizado"], "esquiva")
        fb_dodge = ai._create_visceral_fallback("Inimigo desfere golpe.", "esquivar com reflexos aguçados")
        self.assertTrue("esquiva" in fb_dodge.lower() or "desvio" in fb_dodge.lower())

        # 2. Cobertura
        intent_cover = ai.parse_player_intent("tomar cobertura atrás das pedras", {})
        self.assertEqual(intent_cover["tipo_acao"], "ACAO_TATICA_5E")
        self.assertEqual(intent_cover["recurso_utilizado"], "cobertura")
        fb_cover = ai._create_visceral_fallback("Chuva de flechas.", "tomar cobertura atrás da rocha")
        self.assertTrue("cobertura" in fb_cover.lower() or "rocha" in fb_cover.lower())

        # 3. Postura Defensiva / Bloqueio
        intent_block = ai.parse_player_intent("bloquear com escudo e postura defensiva", {})
        self.assertEqual(intent_block["tipo_acao"], "ACAO_TATICA_5E")
        self.assertEqual(intent_block["recurso_utilizado"], "postura defensiva")
        fb_block = ai._create_visceral_fallback("Golpe violento do monstro.", "bloquear com escudo")
        self.assertTrue("guarda" in fb_block.lower() or "broquel" in fb_block.lower() or "bloqueio" in fb_block.lower())

        # 4. Desengajar
        intent_disengage = ai.parse_player_intent("desengajar da luta corpo a corpo", {})
        self.assertEqual(intent_disengage["tipo_acao"], "ACAO_TATICA_5E")
        self.assertEqual(intent_disengage["recurso_utilizado"], "desengajar")
        fb_disengage = ai._create_visceral_fallback("Combate cerrado.", "desengajar com cuidado")
        self.assertTrue("desengaja" in fb_disengage.lower() or "guarda alta" in fb_disengage.lower())

    def test_campaign_beats_and_tactical_micro_narrative_guidelines(self):
        """Valida que o system_instruction contém as diretrizes canônicas de micro-narrativa tática e coesão de Beats."""
        ai = AIGameMaster()
        sys = ai.system_instruction
        self.assertIn("MICRO-NARRATIVA DE COMBATE TÁTICO", sys)
        self.assertIn("Esquivar", sys)
        self.assertIn("Tomar Cobertura", sys)
        self.assertIn("COESÃO DE CAMPANHA (BEATS 1 AO 15)", sys)
        self.assertIn("Orbe Quebra-Chamas", sys)

# Standalone functions for pytest compatibility
def test_model_name_calibration():
    TestAIPromptFixes().test_model_name_calibration()

def test_parse_player_intent_tavern_dialogue_and_missions():
    TestAIPromptFixes().test_parse_player_intent_tavern_dialogue_and_missions()

def test_visceral_fallback_tavern_missions_and_dialogues():
    TestAIPromptFixes().test_visceral_fallback_tavern_missions_and_dialogues()

def test_tactical_5e_actions_intent_and_fallbacks():
    TestAIPromptFixes().test_tactical_5e_actions_intent_and_fallbacks()

def test_campaign_beats_and_tactical_micro_narrative_guidelines():
    TestAIPromptFixes().test_campaign_beats_and_tactical_micro_narrative_guidelines()

if __name__ == "__main__":
    unittest.main()
