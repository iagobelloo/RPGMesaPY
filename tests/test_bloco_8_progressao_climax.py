import copy
import pytest
from core.dnd_rules import CharacterCalculator, BESTIARIO_5E
from core.game_engine import SessionManager
from core.story_engine import StoryManager
from ai_master.ai_client import AIGameMaster

class MockAI(AIGameMaster):
    def parse_player_intent(self, user_input, game_state):
        u = user_input.lower()
        if "atacar goblin" in u:
            return {"tipo_acao": "ATACAR", "alvo": ["Goblin 1"], "recurso_utilizado": "Espada", "intencao_cena": "Ataque"}
        elif "atacar" in u:
            return {"tipo_acao": "ATACAR", "alvo": ["Tirano"], "recurso_utilizado": "Espada", "intencao_cena": "Ataque"}
        elif "subir" in u or "level" in u:
            return {"tipo_acao": "SUBIR_NIVEL", "recurso_utilizado": None, "alvo": [], "intencao_cena": "Evolução"}
        elif "avancar" in u:
            return {"tipo_acao": "AVANCAR_HISTORIA", "recurso_utilizado": None, "alvo": [], "intencao_cena": "Avanço"}
        return {"tipo_acao": "INTERAGIR_CENARIO", "recurso_utilizado": None, "alvo": [], "intencao_cena": "Olhar"}

    def generate_narrative_from_math(self, sys_log, intent):
        return f"Narrativa: {intent} baseada em {sys_log[:30]}"

def test_character_calculator_level_up_guerreiro():
    """Valida subida de nível para Guerreiro (d10 de vida)."""
    pc = {
        "name": "Valeros",
        "race": "Humano",
        "class": "Guerreiro",
        "level": 1,
        "xp": 350,
        "xp_to_next_level": 300,
        "hp_max": 12,
        "hp_current": 10,
        "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "SAB": 10, "CAR": 10},
        "has_pending_level_up": True
    }
    # CON 14 = Mod +2. Dado de vida d10 -> base_pv = 6. Total gain = 6 + 2 = 8
    res = CharacterCalculator.apply_level_up(pc)
    assert res["new_level"] == 2
    assert res["hp_gained"] == 8
    assert pc["level"] == 2
    assert pc["hp_max"] == 20
    assert pc["hp_current"] == 18
    assert res["proficiency_bonus"] == 2
    assert pc["xp_to_next_level"] == 900
    assert pc["has_pending_level_up"] is False

def test_character_calculator_level_up_mago_spell_slots():
    """Valida subida de nível para Mago (d6 de vida e expansão de spell slots)."""
    pc = {
        "name": "Raistlin",
        "race": "Elfo da Floresta",
        "class": "Mago",
        "level": 2,
        "xp": 950,
        "xp_to_next_level": 900,
        "hp_max": 12,
        "hp_current": 12,
        "attributes": {"FOR": 8, "DES": 14, "CON": 12, "INT": 16, "SAB": 12, "CAR": 10},
        "spell_slots": {"1": 3},
        "has_pending_level_up": True
    }
    # CON 12 = Mod +1. Dado de vida d6 -> base_pv = 4. Total gain = 4 + 1 = 5
    res = CharacterCalculator.apply_level_up(pc)
    assert res["new_level"] == 3
    assert res["hp_gained"] == 5
    assert pc["hp_max"] == 17
    # Mago nível 3 ganha slots de 2º círculo
    assert pc["spell_slots"].get("2") == 2
    assert res["slots_unlocked"].get("2") == 2
    assert pc["xp_to_next_level"] == 2700

def test_calculate_monster_loot():
    """Valida cálculo de ouro e possíveis drops por monstro."""
    loot_goblin = CharacterCalculator.calculate_monster_loot("m_goblin", {"cr": "1/4"})
    assert 2 <= loot_goblin["gold"] <= 8
    
    loot_boss = CharacterCalculator.calculate_monster_loot("boss", {"cr": "20"})
    assert 200 <= loot_boss["gold"] <= 500

def test_async_monster_kill_rewards():
    """Valida concessão dinâmica de XP e ouro ao abater inimigos."""
    session = SessionManager(MockAI())
    session.game_state["player_character"] = {
        "name": "Thorin",
        "class": "Guerreiro",
        "race": "Anão",
        "hp_max": 25,
        "hp_current": 25,
        "xp": 0,
        "gold": 10,
        "xp_to_next_level": 300,
        "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "SAB": 10, "CAR": 10}
    }
    pc = session.game_state["player_character"]
    session.game_mode = "COMBATE"
    
    # Simula monstro com PV zerado
    session.active_combat_targets = {
        "Goblin 1": {
            "name": "Goblin 1",
            "tipo_bestiario": "lacaio goblin",
            "faction": "enemy",
            "pv_atual": 0,
            "pv_max": 7,
            "ca": 15
        }
    }
    
    # Processa uma rodada
    session._async_turn_processor("atacar goblin", [], [])
    
    # Monstro concedeu XP real (50) e ouro
    assert pc["xp"] >= 50
    assert pc["gold"] > 10
    assert "Goblin 1" not in session.active_combat_targets

def test_climax_allies_and_deja_vu_flow():
    """
    Valida a simulação do Clímax:
    1. Entrada no Beat 15 com aliados recrutados
    2. Snapshot na entrada
    3. Wipeout do dragão no Loop 0
    4. Ativação do Déjà Vu (fundo deja_vu_bg.jpg, status idêntico, armadura quebrada)
    5. Derrota do dragão no Loop 1 e transição para EPILOGO.
    """
    session = SessionManager(MockAI())
    session.game_state["player_character"] = {
        "name": "Thorin",
        "class": "Guerreiro",
        "race": "Anão",
        "hp_max": 35,
        "hp_current": 35,
        "gold": 50,
        "xp": 2000,
        "attributes": {"FOR": 16, "DES": 12, "CON": 14, "INT": 10, "SAB": 10, "CAR": 10}
    }
    pc = session.game_state["player_character"]
    
    # Desbloqueia aliados na party
    session.story.unlock_ally("cleric")
    session.story.unlock_ally("rogue")
    unlocked = session.story.get_unlocked_allies()
    assert len(unlocked) == 2
    
    # Entra no Clímax (Beat 15)
    session.story.current_beat = 15
    session.game_mode = "COMBATE"
    session.active_combat_targets.clear()
    session.active_visual_npcs.clear()
    
    # Spawn manual do Boss e inclusão dos aliados
    session.active_combat_targets["Tirano"] = {
        "name": "Tirano",
        "tipo_bestiario": "m_supreme_dragon",
        "faction": "enemy",
        "pv_atual": 999,
        "pv_max": 999,
        "ca": 99,
        "charge_turn": 0
    }
    for a_id, a_data in unlocked.items():
        session.active_combat_targets[a_data["name"]] = copy.deepcopy(a_data)
        session.active_combat_targets[a_data["name"]]["faction"] = "ally"
        
    # Tira snapshot da entrada
    session.story.create_snapshot(pc, session.active_combat_targets, session.active_visual_npcs)
    assert session.story.snapshot is not None
    
    # Loop 0: Dragão atinge wipeout (player zerado)
    pc["hp_current"] = 0
    session.resolve_player_death()
    
    # Déjà Vu deve ter sido ativado!
    assert session.game_state["current_background"] == "deja_vu_bg.jpg"
    assert session.game_state["meta"]["loop_count"] == 1
    assert session.game_state["meta"]["segredo_tirano"] is True
    
    # Jogador e aliados retornaram intactos
    pc_restaurado = session.game_state["player_character"]
    assert pc_restaurado["hp_current"] == 35
    assert pc_restaurado["status"] == "vivo"
    
    # Armadura do dragão despedaçada para o confronto real
    dragao = session.active_combat_targets["Tirano"]
    assert dragao["pv_max"] == 100
    assert dragao["pv_atual"] == 100
    assert dragao["ca"] == 14
    
    # Vitória no confronto real (dragão zerado)
    dragao["pv_atual"] = 0
    dragao["status"] = "morto"
    session.check_combat_resolution()
    
    # Fim épico: modo EPILOGO ativado com sucesso!
    assert session.game_mode == "EPILOGO"
