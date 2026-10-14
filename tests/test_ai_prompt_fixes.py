import pytest
import os
from unittest.mock import MagicMock
from ai_master.ai_client import AIGameMaster

def test_model_name_calibration():
    """Garante que o modelo oficial seja gemini-2.5-flash e respeite a variável de ambiente GEMINI_MODEL."""
    ai = AIGameMaster()
    assert ai.model_name == "gemini-2.5-flash"
    assert "gemini-3.5" not in ai.model_name

    # Teste de override via variável de ambiente
    os.environ["GEMINI_MODEL"] = "gemini-2.5-pro"
    ai_custom = AIGameMaster()
    assert ai_custom.model_name == "gemini-2.5-pro"
    del os.environ["GEMINI_MODEL"]


def test_parse_player_intent_tavern_dialogue_and_missions():
    """Valida que pedidos de missão, trabalho, diálogos e pedidos de cerveja sejam DIALOGAR/INTERAGIR_CENARIO e nunca AVANCAR_HISTORIA."""
    ai = AIGameMaster()
    ai.client.models.generate_content = MagicMock(side_effect=Exception("Simulação de fallback heurístico offline"))

    # 1. Procura de missão
    res_missao = ai.parse_player_intent("estava a procura de uma missão", {})
    assert res_missao["tipo_acao"] in ["DIALOGAR", "INTERAGIR_CENARIO"]
    assert res_missao["tipo_acao"] != "AVANCAR_HISTORIA"
    assert "missões" in res_missao["intencao_cena"] or "trabalhos" in res_missao["intencao_cena"]

    # 2. Procuro trabalho / contrato
    res_trab = ai.parse_player_intent("procuro trabalho ou contrato", {})
    assert res_trab["tipo_acao"] in ["DIALOGAR", "INTERAGIR_CENARIO"]
    assert res_trab["tipo_acao"] != "AVANCAR_HISTORIA"

    # 3. Falar com taverneiro
    res_tav = ai.parse_player_intent("falar com taverneiro", {})
    assert res_tav["tipo_acao"] in ["DIALOGAR", "INTERAGIR_CENARIO"]
    assert res_tav["tipo_acao"] != "AVANCAR_HISTORIA"

    # 4. Pedir cerveja
    res_beer = ai.parse_player_intent("pedir uma cerveja", {})
    assert res_beer["tipo_acao"] in ["DIALOGAR", "INTERAGIR_CENARIO"]
    assert res_beer["tipo_acao"] != "AVANCAR_HISTORIA"

    # 5. Olhar ao redor na taverna
    res_look = ai.parse_player_intent("olhar ao redor na taverna", {})
    assert res_look["tipo_acao"] == "INTERAGIR_CENARIO"

    # 6. Sair da mesa para conversar (não deve avançar a história)
    res_table = ai.parse_player_intent("sair da mesa e falar com o taverneiro", {})
    assert res_table["tipo_acao"] in ["DIALOGAR", "INTERAGIR_CENARIO"]
    assert res_table["tipo_acao"] != "AVANCAR_HISTORIA"

    # 7. Avanço real pela estrada
    res_road = ai.parse_player_intent("viajar para a estrada e partir da taverna", {})
    assert res_road["tipo_acao"] == "AVANCAR_HISTORIA"


def test_visceral_fallback_tavern_missions_and_dialogues():
    """Valida que buscas de missões e conversas de taverna não caiam no dedilhar genérico padrão."""
    ai = AIGameMaster()

    # 1. Procura de missão
    fb_mission = ai._create_visceral_fallback("O herói procura trabalhos disponíveis.", "estava a procura de uma missão na taverna")
    assert "dedilhar melancólico" not in fb_mission.lower()
    assert "taverneiro" in fb_mission.lower()
    assert "contratos" in fb_mission.lower() or "pergaminhos" in fb_mission.lower() or "trabalho" in fb_mission.lower()

    # 2. Conversa com Taverneiro / Pedido de cerveja
    fb_beer = ai._create_visceral_fallback("Caneca servida.", "pedir uma cerveja ao taverneiro")
    assert "dedilhar melancólico" not in fb_beer.lower()
    assert "taverneiro" in fb_beer.lower()
    assert "cerveja" in fb_beer.lower()

    # 3. Conversa com Maelor
    fb_maelor = ai._create_visceral_fallback("Aproximação do menestrel.", "conversar com maelor")
    assert "epitáfio" in fb_maelor.lower() or "tirano" in fb_maelor.lower() or "alaúde" in fb_maelor.lower()

    # 4. Observação / Rumores
    fb_rumors = ai._create_visceral_fallback("Ouvindo murmúrios.", "ouvir rumores e boatos da taverna")
    assert "mercenários" in fb_rumors.lower() or "estrada" in fb_rumors.lower() or "cochicham" in fb_rumors.lower()
