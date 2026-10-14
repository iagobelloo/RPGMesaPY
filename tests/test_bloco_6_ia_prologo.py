import pytest
import json
import os
from unittest.mock import MagicMock
from ai_master.ai_client import AIGameMaster

def test_cutscenes_prologue_has_tags():
    """Valida se data/game_cutscenes.json possui as tags de personalização."""
    with open("data/game_cutscenes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert "beat_1_prologue" in data
    prologue_full = "\n".join(data["beat_1_prologue"])
    for tag in ["{nome}", "{raca}", "{classe}", "{antecedente}", "{tendencia}"]:
        assert tag in prologue_full, f"Tag {tag} ausente no beat_1_prologue"

def test_get_personalized_prologue_formatting():
    """Valida se o prólogo injeta corretamente todos os dados da ficha do herói."""
    ai = AIGameMaster()
    char_mock = {
        "name": "Eldrin",
        "race": "Elfo",
        "class": "Mago",
        "background": "Sábio",
        "alignment": "Caótico e Bom"
    }
    
    prologue = ai.get_personalized_prologue(char_mock)
    assert "Eldrin" in prologue
    assert "Elfo" in prologue
    assert "Mago" in prologue
    assert "Sábio" in prologue
    assert "Caótico e Bom" in prologue
    
    # Nenhuma tag não-substituída deve sobrar
    for tag in ["{nome}", "{raca}", "{classe}", "{antecedente}", "{tendencia}"]:
        assert tag not in prologue

def test_visceral_fallbacks_generation():
    """Valida a geração contextual de fallbacks para diferentes eventos."""
    ai = AIGameMaster()
    
    # Dano em combate
    fb_dmg = ai._create_visceral_fallback("O orc sofreu 12 de dano.", "ataque com espada")
    assert isinstance(fb_dmg, str) and len(fb_dmg) > 10
    
    # Cura
    fb_heal = ai._create_visceral_fallback("Valeros recuperou 8 de HP.", "usar pocao")
    assert "poção" in fb_heal.lower() or "cura" in fb_heal.lower() or "feridas" in fb_heal.lower()
    
    # Descanso na Taverna
    fb_rest = ai._create_visceral_fallback("Descanso longo concluído.", "Descanso na Taverna com fogo e guisado")
    assert "calor" in fb_rest.lower() or "descanso" in fb_rest.lower() or "lareira" in fb_rest.lower()
    
    # Morte definitiva
    fb_death = ai._create_visceral_fallback("[SISTEMA FATAL] O jogador morreu.", "morte definitiva")
    assert "morte" in fb_death.lower() or "escuridão" in fb_death.lower()

def test_generate_narrative_from_math_never_raises():
    """Garante que falhas de rede/API nunca dêem crash na thread assíncrona."""
    ai = AIGameMaster()
    # Simula falha total da API do Google Gemini
    ai.client.models.generate_content = MagicMock(side_effect=RuntimeError("API Desconectada ou Sem Cota"))
    
    # Deve retornar fallback sem levantar exceção
    result = ai.generate_narrative_from_math("Goblin sofreu 5 de dano.", "ataque")
    assert isinstance(result, str)
    assert len(result) > 5

def test_parse_player_intent_never_raises():
    """Garante que a Fase 0 nunca dê crash e sempre retorne as chaves mínimas obrigatórias."""
    ai = AIGameMaster()
    ai.client.models.generate_content = MagicMock(side_effect=ConnectionError("Falha de DNS/Rede"))
    
    intent = ai.parse_player_intent("Atacar o goblin com minha espada", {})
    assert isinstance(intent, dict)
    assert "tipo_acao" in intent
    assert "recurso_utilizado" in intent
    assert "alvo" in intent
    assert "intencao_cena" in intent

def test_sliding_window_memory_limit():
    """Valida se o histórico de chat da IA respeita estritamente o limite de 5 turnos."""
    ai = AIGameMaster()
    ai._generate_text_with_retry = MagicMock(return_value='{"texto": "Narrativa de teste", "npc_falando": "Mestre"}')
    
    player_id = {"race": "Humano", "class": "Guerreiro"}
    scene = {"environment": "Taverna"}
    
    for i in range(10):
        ai.generate_narrative_from_log(
            system_log="Ação processada.",
            player_identity=player_id,
            scene_state=scene,
            player_action=f"Ação {i}"
        )
    
    # O tamanho máximo do histórico deve ser 5 (Sliding Window)
    assert len(ai.chat_history) <= 5


def test_maelor_canon_and_fallbacks():
    """Valida as diretrizes de Maelor das Cordas de Cinza e novos fallbacks canônicos."""
    ai = AIGameMaster()
    
    # 1. Valida se o system_instruction carregou as novas diretrizes de Maelor
    assert "Maelor das Cordas de Cinza" in ai.system_instruction
    assert "REGRA DE OURO DOS ALIADOS" in ai.system_instruction or "Beat 1 ao Beat 14" in ai.system_instruction

    # 2. Juramento de Aliados
    fb_ally = ai._create_visceral_fallback("HERO-01 selou juramento.", "juramento do aliado")
    assert "juramento" in fb_ally.lower() or "aliado" in fb_ally.lower()
    assert "batalha final" in fb_ally.lower() or "tirano" in fb_ally.lower()

    # 3. Viagem para Side Quest
    fb_sq = ai._create_visceral_fallback("Partindo para o covil dos saqueadores.", "viagem side_quest covil")
    assert "trilha" in fb_sq.lower() or "covil" in fb_sq.lower() or "solitários" in fb_sq.lower()

    # 4. Recuo Tático e Retorno ao Hub
    fb_retreat = ai._create_visceral_fallback("Retorno ao hub concluído.", "recuo tatico taverna")
    assert "taverna" in fb_retreat.lower() or "lareira" in fb_retreat.lower() or "recua" in fb_retreat.lower()

    # 5. Déjà Vu / Clímax Loop
    fb_deja = ai._create_visceral_fallback("O herói caiu no Beat 15.", "deja vu loop temporal")
    assert "morte" in fb_deja.lower() or "taverna" in fb_deja.lower() or "ciclo" in fb_deja.lower()

    # 6. Item 4.1: Reatividade de Aliados no Hub da Taverna
    fb_rumors = ai._create_visceral_fallback("[RUMORES DA TAVERNA] Boatos sobre Sir Alistair", "ouvir rumores na taverna")
    assert "maelor" in fb_rumors.lower() or "alaúde" in fb_rumors.lower() or "alaude" in fb_rumors.lower()
    assert "vigília leal" in fb_rumors.lower() or "vigilia leal" in fb_rumors.lower() or "contrafortes" in fb_rumors.lower()

    # 7. Item 4.2: Alternância e Equipamento de Armas (Fallback)
    fb_equip = ai._create_visceral_fallback("equipar arco curto", "trocar de arma")
    assert "arco curto" in fb_equip.lower() or "aço" in fb_equip.lower()
    assert "desembainhado" in fb_equip.lower() or "peso" in fb_equip.lower() or "cabo" in fb_equip.lower()


def test_item_4_2_equip_intent_parsing():
    """Valida se a Fase 0 extrai a intenção EQUIPAR_ITEM e nome da arma com robustez."""
    ai = AIGameMaster()
    ai.client.models.generate_content = MagicMock(side_effect=Exception("Simulação de fallback heurístico offline"))

    # Teste com empunhar espada longa
    intent_sword = ai.parse_player_intent("empunhar espada longa", {})
    assert intent_sword["tipo_acao"] == "EQUIPAR_ITEM"
    assert intent_sword["recurso_utilizado"] == "espada longa"
    assert "espada longa" in intent_sword["intencao_cena"]

    # Teste com trocar para arco curto
    intent_bow = ai.parse_player_intent("trocar para arco curto", {})
    assert intent_bow["tipo_acao"] == "EQUIPAR_ITEM"
    assert intent_bow["recurso_utilizado"] == "arco curto"
    assert "arco curto" in intent_bow["intencao_cena"]


def test_class_abilities_visceral_fallbacks():
    """Valida as reações sensoriais de Maelor para habilidades icônicas de classe."""
    ai = AIGameMaster()

    # 1. Smite Divino (Paladino)
    fb_smite = ai._create_visceral_fallback("Destruição Divina ativada com sucesso.", "usar divine smite no monstro")
    assert "clarão ofuscante" in fb_smite.lower() or "celestes" in fb_smite.lower() or "sagrado" in fb_smite.lower()

    # 2. Retomar o Fôlego / Second Wind (Guerreiro)
    fb_wind = ai._create_visceral_fallback("Jogador recuperou HP com Second Wind.", "retomar o folego com disciplina")
    assert "dentes cerrados" in fb_wind.lower() or "pulmões" in fb_wind.lower() or "disciplina" in fb_wind.lower()

    # 3. Marca do Caçador (Patrulheiro)
    fb_mark = ai._create_visceral_fallback("Alvo marcado com Marca do Caçador.", "ativar marca do caçador na presa")
    assert "runa espectral" in fb_mark.lower() or "flecha" in fb_mark.lower() or "sombra" in fb_mark.lower()

    # 4. Ataque Furtivo (Ladino)
    fb_sneak = ai._create_visceral_fallback("Dano extra de Ataque Furtivo aplicado.", "desferir sneak attack nas sombras")
    assert "jugular" in fb_sneak.lower() or "brecha" in fb_sneak.lower() or "silenciosa" in fb_sneak.lower()

    # 5. Surto de Ação (Guerreiro)
    fb_surge = ai._create_visceral_fallback("Surto de Ação concede novo ataque.", "ativar surto de acao")
    assert "adrenalina" in fb_surge.lower() or "carne" in fb_surge.lower() or "aço" in fb_surge.lower()

    # 6. Escudo Arcano (Mago)
    fb_shield = ai._create_visceral_fallback("Escudo Arcano defletiu ataque.", "conjurar escudo arcano de protecao")
    assert "barreira" in fb_shield.lower() or "arcana" in fb_shield.lower() or "ciano" in fb_shield.lower()


def test_class_abilities_intent_parsing():
    """Valida se a Fase 0 extrai USAR_HABILIDADE e identifica a habilidade de classe."""
    ai = AIGameMaster()
    ai.client.models.generate_content = MagicMock(side_effect=Exception("Simulação de fallback heurístico offline"))

    # Guerreiro: Retomar o Fôlego
    res_wind = ai.parse_player_intent("retomar o fôlego", {})
    assert res_wind["tipo_acao"] == "USAR_HABILIDADE"
    assert res_wind["recurso_utilizado"] == "retomar o fôlego"

    # Paladino: Divine Smite
    res_smite = ai.parse_player_intent("usar destruição divina no orc", {"active_combat_targets": {"Orc 1": {}}})
    assert res_smite["tipo_acao"] == "USAR_HABILIDADE"
    assert res_smite["recurso_utilizado"] == "destruição divina"
    assert res_smite["alvo"] == ["Orc 1"]

    # Patrulheiro: Marca do Caçador
    res_mark = ai.parse_player_intent("marca do caçador", {})
    assert res_mark["tipo_acao"] == "USAR_HABILIDADE"
    assert res_mark["recurso_utilizado"] == "marca do caçador"

    # Ladino: Ataque Furtivo
    res_sneak = ai.parse_player_intent("desferir ataque furtivo", {})
    assert res_sneak["tipo_acao"] == "USAR_HABILIDADE"
    assert res_sneak["recurso_utilizado"] == "ataque furtivo"


def test_personalized_prologue_racial_heritage_and_gender():
    """Valida a valorização das 7 relíquias raciais e a concordância de gênero ('female' / 'male') no prólogo."""
    ai = AIGameMaster()

    # 1. Protagonista feminina Tiefling
    char_female = {
        "name": "Lilith",
        "race": "Tiefling",
        "class": "Mago",
        "background": "Acólito",
        "alignment": "Caótico e Neutro",
        "gender": "female"
    }
    prologue_f = ai.get_personalized_prologue(char_female)
    assert "Lilith" in prologue_f
    assert "Selo de Brasas Abissais" in prologue_f
    assert "moldada pela dureza" in prologue_f

    # 2. Protagonista masculino Anão da Colina
    char_male = {
        "name": "Thorin",
        "race": "Anão da Colina",
        "class": "Clérigo",
        "background": "Soldado",
        "alignment": "Leal e Bom",
        "gender": "male"
    }
    prologue_m = ai.get_personalized_prologue(char_male)
    assert "Thorin" in prologue_m
    assert "Runa da Pedra-Forja" in prologue_m
    assert "moldado pela dureza" in prologue_m





