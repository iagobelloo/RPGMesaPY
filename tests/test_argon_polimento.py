import json
import re
from unittest.mock import MagicMock
import pygame
from ai_master.ai_client import AIGameMaster
from core.story_engine import StoryManager
from core.game_engine import SessionManager
from core.combat_system import process_enemies_turn_batch, resolve_action, resolve_skill_effect
from ui.widgets.theme import Layout
from ui.widgets.base import UIButton
from ui.widgets.hud.action_bar import TacticalActionBarWidget
from ui.widgets.hud.chat_console import NarrativeLogView


def test_gemini_models_cascade_includes_expanded_fallbacks():
    gm = AIGameMaster(api_key="dummy_key")
    cascade = gm._get_models_cascade()
    assert "gemini-3.5-flash-lite" in cascade
    assert "gemini-2.5-flash" in cascade
    assert "gemini-2.0-flash" in cascade
    assert "gemini-flash-lite-latest" in cascade
    assert "gemini-flash-latest" in cascade
    assert gm.fallback_models == [
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
    ]


def test_extract_intent_and_narrative_use_chats_create():
    gm = AIGameMaster(api_key="dummy_key")
    mock_client = MagicMock()
    gm.client = mock_client

    # Mock para parse_player_intent
    mock_chat_intent = MagicMock()
    mock_resp_intent = MagicMock()
    mock_resp_intent.text = '{"tipo_acao": "ATACAR", "alvo": ["Bandido 1"], "recurso_utilizado": "espada longa", "intencao_cena": "Ataca o bandido."}'
    mock_chat_intent.send_message.return_value = mock_resp_intent

    # Mock para generate_narrative_from_math e generate_narrative_from_log
    mock_chat_narr = MagicMock()
    mock_resp_narr = MagicMock()
    mock_resp_narr.text = '{"texto": "A lâmina corta o ar. O que você faz?", "npc_falando": "Mestre"}'
    mock_chat_narr.send_message.return_value = mock_resp_narr

    mock_client.chats.create.side_effect = [mock_chat_intent, mock_chat_narr, mock_chat_narr]

    intent = gm.parse_player_intent("atacar bandido 1", {"game_mode": "COMBATE", "active_combat_targets": {"Bandido 1": {}}})
    assert intent["tipo_acao"] == "ATACAR"

    narr_math = gm.generate_narrative_from_math("Acerto!", "Atacar Bandido 1")
    assert "O que você faz?" in narr_math

    narr_log = gm.generate_narrative_from_log("Acerto!", {"race": "Humano", "class": "Guerreiro"}, {"environment": "Planície"}, "atacar")
    assert "O que você faz?" in narr_log.get("texto", "")

    assert mock_client.chats.create.call_count == 3
    mock_client.models.generate_content.assert_not_called()


def test_enemy_counter_attack_fallback():
    gm = AIGameMaster(api_key="dummy_key")

    hit_text = gm._create_visceral_fallback("⚔️ [Bandido 1]: d20 (15) + 4 = 19 vs CA 16 ➔ Acerto! (5 dano)", "Contra-ataque inimigo")
    assert "contragolpe feroz" in hit_text
    assert "O que você faz?" in hit_text

    miss_text = gm._create_visceral_fallback("⚔️ [Bandido 1]: d20 (4) + 4 = 8 vs CA 16 ➔ Erro! (0 dano)", "Contra-ataque inimigo")
    assert "contra-ataque inimigo sibila" in miss_text
    assert "O que você faz?" in miss_text


def test_beat_2_enemies_balance():
    with open("data/campaign.json", "r", encoding="utf-8") as f:
        campaign = json.load(f)
    assert campaign["2"]["enemies"] == ["m_bandit", "m_bandit"]


def test_monster_spawn_clean_sequential_names():
    story = StoryManager()
    targets = {}
    visuals = {}
    story.spawn_enemies_from_list(["m_bandit", "m_bandit"], targets, visuals)

    keys = list(targets.keys())
    assert keys == ["Bandido 1", "Bandido 2"]
    for k in keys:
        assert not re.search(r"[a-f0-9]{4}$", k)

    sm = SessionManager()
    sm.active_combat_targets = targets
    assert sm.find_combat_target("Bandido 1") is targets["Bandido 1"]
    assert sm.find_combat_target("Bandido 2") is targets["Bandido 2"]
    assert sm.find_combat_target("1") is targets["Bandido 1"]
    assert sm.find_combat_target("2") is targets["Bandido 2"]
    assert sm.find_combat_target("Bandido") is targets["Bandido 1"]


def test_combat_player_ca_ac_synchronization():
    pc = {"name": "Herói", "hp_current": 20, "hp_max": 20, "ac": 16}
    targets = {
        "Bandido 1": {
            "name": "Bandido 1",
            "pv_atual": 11,
            "pv_max": 11,
            "ca": 12,
            "tipo_bestiario": "m_bandit",
            "faction": "enemy",
            "actions": [{"name": "Cimitarra", "hit_bonus": 3, "damage_dice": "1d6+1"}],
        }
    }
    log = process_enemies_turn_batch(targets, pc)
    assert pc["ac"] == 16
    assert pc["ca"] == 16
    assert "CA 16" in log

    resolve_skill_effect({"recurso_utilizado": "cunning_action"}, pc, [], targets)
    assert pc["ac"] == 18
    assert pc["ca"] == 18


def test_death_in_beat_1_to_14_reloads_checkpoint():
    sm = SessionManager()
    sm.story.current_beat = 2
    sm.game_state["story_beat"] = 2
    sm.game_state["last_checkpoint_beat"] = 1
    sm.game_state["last_checkpoint_bg"] = "tavern_bg.jpg"
    sm.game_state["meta"] = {"loop_count": 0, "segredo_tirano": False}
    sm.game_state["inventory"] = {}
    sm.game_state["player_character"] = {
        "name": "Kaelen",
        "race": "Humano",
        "class": "Guerreiro",
        "hp_current": 0,
        "hp_max": 14,
        "ac": 16,
        "ca": 16,
        "status": "morto",
    }
    sm.game_mode = "COMBATE"
    sm.active_combat_targets = {"Bandido 1": {"name": "Bandido 1", "pv_atual": 11, "pv_max": 11, "faction": "enemy"}}
    sm.active_visual_npcs = {"Bandido 1": "m_bandit"}

    # Enfileira uma narrativa de combate residual que deve ser descartada ao morrer
    sm.ui_queue.put({"type": "narrative", "content": "Narrativa de combate que deve ser descartada", "npc_falando": "Mestre"})

    sm.resolve_player_death()

    assert sm.game_state["meta"]["loop_count"] == 0
    assert sm.game_state["meta"]["segredo_tirano"] is False
    assert sm.active_combat_targets == {}
    assert sm.active_visual_npcs == {}
    assert sm.game_mode == "EXPLORACAO"
    assert sm.story.current_beat == 1
    assert sm.game_state["player_character"]["hp_current"] == 14
    assert sm.game_state["player_character"]["status"] == "vivo"

    events = []
    while not sm.ui_queue.empty():
        events.append(sm.ui_queue.get_nowait())
    assert any(e.get("type") == "beat_transition" and e.get("beat") == 1 for e in events)
    narratives = [e for e in events if e.get("type") == "narrative"]
    assert len(narratives) == 1
    assert "Taverna do Dragão Acordado" in narratives[0]["content"]


def test_death_in_beat_15_triggers_deja_vu():
    sm = SessionManager()
    sm.story.current_beat = 15
    sm.game_state["story_beat"] = 15
    sm.game_state["meta"] = {"loop_count": 0, "segredo_tirano": False}
    sm.game_state["player_character"] = {
        "name": "Kaelen",
        "race": "Humano",
        "class": "Guerreiro",
        "hp_current": 0,
        "hp_max": 25,
        "ac": 18,
        "ca": 18,
        "status": "morto",
    }
    sm.active_combat_targets = {
        "Tirano das Cinzas": {
            "name": "Tirano das Cinzas",
            "pv_atual": 500,
            "pv_max": 500,
            "ca": 22,
            "tipo_bestiario": "m_supreme_dragon",
            "faction": "enemy",
            "charge_turn": 2,
        }
    }
    assert sm.story.is_climax() is True

    sm.resolve_player_death()

    assert sm.game_state["meta"]["loop_count"] == 1
    assert sm.game_state["meta"]["segredo_tirano"] is True
    assert sm.game_mode == "COMBATE"
    dragon = sm.active_combat_targets["Tirano das Cinzas"]
    assert dragon["ca"] == 14
    assert dragon["pv_max"] == 100
    assert dragon["pv_atual"] == 100
    assert sm.game_state["player_character"]["hp_current"] == 25
    assert sm.game_state["player_character"]["status"] == "vivo"


def test_hotbar_slot_dimensions_and_icon_size():
    pygame.init()
    if not pygame.display.get_surface():
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

    assert Layout.SLOT == (104, 52)
    assert Layout.SLOT_WIDE == (152, 52)

    bar = TacticalActionBarWidget()
    bar.set_mode("combat")
    assert bar._combat_w == 620
    assert bar.rect.width == 620

    btn = UIButton((0, 0, Layout.SLOT[0], Layout.SLOT[1]), "Habilidade", "btn_skill", variant="action", icon="skill", hotkey="2")
    assert btn._icon_sz == 16
    assert btn.font_size == 11


def test_narrative_log_view_typewriter_and_flush():
    pygame.init()
    if not pygame.display.get_surface():
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

    log_view = NarrativeLogView((0, 0, 500, 300))
    assert log_view._typing_speed == 45.0

    texto = "As brasas da lareira crepitam na penumbra da taverna."
    log_view.append_entry("Mestre", texto, "narration")
    assert log_view.is_typing is True
    assert log_view._typing_index == 0.0

    # Avança 0.2s -> ~9 caracteres revelados
    log_view.update(0.2)
    assert 8.0 <= log_view._typing_index <= 10.0
    assert log_view.is_typing is True
    assert len(log_view._active_typing_lines) >= 1

    # Flush instantâneo completa a mensagem e move para _lines
    log_view.flush_typewriter()
    assert log_view.is_typing is False
    assert len(log_view._lines) >= 1


def test_clean_combat_and_skill_logs_format():
    pc = {
        "name": "Kaelen",
        "hp_current": 20,
        "hp_max": 20,
        "ac": 16,
        "ca": 16,
        "proficiency_bonus": 2,
        "equipped_weapon": "espada longa",
        "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "SAB": 14, "CAR": 10},
    }
    target = {
        "name": "Bandido 1",
        "pv_atual": 11,
        "pv_max": 11,
        "ca": 12,
        "tipo_bestiario": "m_bandit",
        "faction": "enemy",
        "actions": [{"name": "Cimitarra", "hit_bonus": 4, "damage_dice": "1d6+2"}],
    }
    targets_map = {"Bandido 1": target}

    # 1. Ataque do Herói
    res_atk = resolve_action({"tipo_acao": "ataque", "arma_usada": "espada longa"}, pc, [target], targets_map)
    assert "🎲 [Ataque] Espada Longa: d20 (" in res_atk["sys_log"]
    assert "vs CA 12 ➔" in res_atk["sys_log"]
    assert "dano)" in res_atk["sys_log"]

    # 2. Contra-Ataque Inimigo
    target["pv_atual"] = 11
    target["status"] = "vivo"
    pc["hp_current"] = 20
    pc["status"] = "vivo"
    enemy_log = process_enemies_turn_batch(targets_map, pc)
    assert "⚔️ [Bandido 1]: d20 (" in enemy_log
    assert "vs CA 16 ➔" in enemy_log
    assert "dano)" in enemy_log

    # 3. Teste de Perícia
    pc["hp_current"] = 15
    pc["status"] = "vivo"
    res_skill = resolve_action({"tipo_acao": "teste_pericia", "pericia_sugerida": "percepcao", "cd_sugerida": 12}, pc, [], {})
    assert "🎲 [Perícia] Percepcao CD 12: d20 (" in res_skill["sys_log"]
    assert "➔" in res_skill["sys_log"]

    # 4. Cura
    heal_log = resolve_skill_effect({"recurso_utilizado": "second_wind"}, pc, [], {})
    assert "✨ [Cura] Retomar o Fôlego: +" in heal_log
    assert "PV recuperados (PV:" in heal_log
