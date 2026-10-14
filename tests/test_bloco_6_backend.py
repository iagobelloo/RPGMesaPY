"""
Teste de Validação da Fase 1 do Bloco 6 - Backend & Dados
Valida:
1. data/races.json (stat_bonuses, speed, size, description_pt sem bônus concatenado)
2. data/classes.json (hit_dice, description_pt sem Dado de Vida concatenado)
3. data/bestiary.json (remoção do boss_final órfão, integridade dos monstros)
4. data/campaign.json (beat 15 com O_Covil_do_Tirano_bg.jpg)
5. Integração do RestSystem no game_engine.py para a ação DESCANSAR
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))
import json
from core.time_manager import RestSystem
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster


def test_races_json():
    with open("data/races.json", "r", encoding="utf-8") as f:
        races = json.load(f)

    assert len(races) >= 7, "Deveriam existir pelo menos 7 raças cadastradas."
    for race_id, data in races.items():
        assert "stat_bonuses" in data, f"{race_id} não possui stat_bonuses"
        assert isinstance(data["stat_bonuses"], dict), f"{race_id} stat_bonuses deve ser dict"
        assert len(data["stat_bonuses"]) > 0, f"{race_id} stat_bonuses vazio"
        assert "speed" in data, f"{race_id} não possui speed"
        assert isinstance(data["speed"], (int, float)), f"{race_id} speed deve ser numérico"
        assert "size" in data, f"{race_id} não possui size"
        assert isinstance(data["size"], str), f"{race_id} size deve ser string"
        assert " | Bônus:" not in data["description_pt"], f"{race_id} ainda tem bônus concatenado no texto"
    print("[OK] test_races_json passou com sucesso!")


def test_classes_json():
    with open("data/classes.json", "r", encoding="utf-8") as f:
        classes = json.load(f)

    assert len(classes) >= 5, "Deveriam existir pelo menos 5 classes cadastradas."
    for class_id, data in classes.items():
        assert "hit_dice" in data, f"{class_id} não possui hit_dice"
        assert " | Dado de Vida:" not in data["description_pt"], f"{class_id} ainda tem dado concatenado no texto"
    print("[OK] test_classes_json passou com sucesso!")


def test_bestiary_json():
    with open("data/bestiary.json", "r", encoding="utf-8") as f:
        bestiary = json.load(f)

    assert "boss_final" not in bestiary, "boss_final ainda está presente no bestiary.json"
    assert "m_supreme_dragon" in bestiary, "m_supreme_dragon deve estar no bestiary"
    assert "m_dire_wolf" in bestiary, "m_dire_wolf deve estar no bestiary"
    assert bestiary["m_supreme_dragon"]["hp"] == 300, "HP do boss supremo alterado indevidamente"
    print("[OK] test_bestiary_json passou com sucesso!")


def test_campaign_json():
    with open("data/campaign.json", "r", encoding="utf-8") as f:
        campaign = json.load(f)

    beat_15 = campaign.get("15")
    assert beat_15 is not None, "Beat 15 não encontrado na campanha"
    assert beat_15["bg_image"] == "O_Covil_do_Tirano_bg.jpg", f"bg_image inesperado: {beat_15['bg_image']}"
    assert beat_15.get("is_climax") is True, "Flag is_climax deve ser True no Beat 15"
    print("[OK] test_campaign_json passou com sucesso!")


def test_descansar_rest_system():
    ai = AIGameMaster()
    session = SessionManager(ai)

    # Configura personagem machucado
    session.game_state["player_character"] = {
        "name": "Thorin",
        "race": "Humano",
        "class": "Guerreiro",
        "hp_max": 25,
        "hp_current": 10,
        "mp_max": 10,
        "mp_current": 2
    }
    session.game_state["current_day"] = 1
    session.game_state["suprimentos_acampamento"] = 1
    session.game_state["suprimentos_maximos"] = 1
    session.story.current_beat = 1 # Taverna (Hub)
    session.game_mode = "EXPLORACAO"

    # 1. Teste de descanso na Taverna
    session._async_turn_processor("descansar", [], [])
    pc = session.game_state["player_character"]
    assert pc["hp_current"] == 25, f"HP não recuperado totalmente na Taverna: {pc['hp_current']}"
    assert pc["mp_current"] == 10, f"MP não recuperado totalmente na Taverna: {pc['mp_current']}"
    assert session.game_state["current_day"] == 2, f"Dia não avançou: {session.game_state['current_day']}"
    print("[OK] Descanso na Taverna utilizou RestSystem e avançou current_day!")

    # 2. Teste de descanso no Ermo com sucesso
    import random
    original_randint = random.randint
    random.randint = lambda a, b: 15 # Garante sucesso (>= 11)

    session.story.current_beat = 3
    pc["hp_current"] = 8
    pc["mp_current"] = 0
    session.game_state["suprimentos_acampamento"] = 1

    session._async_turn_processor("descansar", [], [])
    assert pc["hp_current"] == 25, f"HP não recuperado no Ermo: {pc['hp_current']}"
    assert pc["mp_current"] == 10, f"MP não recuperado no Ermo: {pc['mp_current']}"
    assert session.game_state["current_day"] == 3, f"Dia não avançou no Ermo: {session.game_state['current_day']}"
    assert session.game_state["suprimentos_acampamento"] == 0, "Suprimento não consumido no Ermo"
    print("[OK] Descanso no Ermo utilizou RestSystem e consumiu suprimentos!")

    random.randint = original_randint


if __name__ == "__main__":
    test_races_json()
    test_classes_json()
    test_bestiary_json()
    test_campaign_json()
    test_descansar_rest_system()
    print("\nTODOS OS TESTES DO BLOCO 6 - FASE 1 PASSARAM COM SUCESSO!")
