from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

class MockAI(AIGameMaster):
    def parse_player_intent(self, text, state):
        return {"tipo_acao": "atacar", "alvo": text.split()[1], "intencao_cena": "atacar"}
    def generate_narrative_from_math(self, log, intent):
        return "NARRATIVA MOCK"

def test_bloco_40():
    ai = MockAI()
    session = SessionManager(ai)
    
    # Setup test pc
    session.game_state["player_character"] = {
        "name": "Hero",
        "hp_current": 100,
        "hp_max": 100,
        "attributes": {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10},
        "ac": 15,
        "equipment": ["Espada Larga"],
        "proficiencies": [],
        "abilities": ["Atacar"]
    }
    
    # TESTE 1 e 2: Combate Normal
    print("--- TESTE 1: Combate Normal Beat 1 ---")
    session.story.current_beat = 1
    session.game_mode = "COMBATE"
    
    session.active_combat_targets = {
        "Goblin_A": {"name": "Goblin_A", "pv_atual": 10, "pv_max": 10, "faction": "enemy", "ac": 10, "actions": [{"name": "Ataque", "hit_bonus": 2, "damage_dice": "1d4"}]},
        "Goblin_B": {"name": "Goblin_B", "pv_atual": 10, "pv_max": 10, "faction": "enemy", "ac": 10, "actions": [{"name": "Ataque", "hit_bonus": 2, "damage_dice": "1d4"}]}
    }
    session.active_visual_npcs = {"Goblin_A": "goblin", "Goblin_B": "goblin"}
    
    # Matar Goblin_A
    session.active_combat_targets["Goblin_A"]["pv_atual"] = 0
    # Simular turno player (ele ataca Goblin_B mas erra ou algo, só roda a pipeline)
    session._async_turn_processor("atacar Goblin_B", [], [])
    
    assert "Goblin_A" not in session.active_combat_targets, "Goblin_A não foi removido!"
    assert "Goblin_A" not in session.active_visual_npcs, "Goblin_A visual não foi removido!"
    assert "Goblin_B" in session.active_combat_targets, "Goblin_B sumiu prematuramente!"
    assert session.game_mode == "COMBATE", "Modo devia continuar COMBATE!"
    print("Passou matar 1 de 2.")
    
    # Matar Goblin_B
    session.active_combat_targets["Goblin_B"]["pv_atual"] = 0
    session._async_turn_processor("atacar Goblin_B", [], [])
    
    assert len(session.active_combat_targets) == 0, "Alvos não zeraram!"
    assert session.game_mode == "EXPLORACAO", "Modo devia voltar para EXPLORACAO!"
    print("Passou vitória combate normal.")
    
    # TESTE 3: Boss Beat 15
    print("--- TESTE 3: Boss Beat 15 ---")
    session.story.current_beat = 15
    session.game_mode = "COMBATE"
    
    session.active_combat_targets = {
        "Boss": {"name": "Boss", "pv_atual": 100, "pv_max": 100, "faction": "enemy", "ac": 10, "actions": []}
    }
    session.active_visual_npcs = {"Boss": "boss"}
    
    # Matar Boss
    session.active_combat_targets["Boss"]["pv_atual"] = 0
    session._async_turn_processor("atacar Boss", [], [])
    
    assert len(session.active_combat_targets) == 0, "Alvos do Boss não zeraram!"
    assert session.game_mode == "EPILOGO", f"Modo devia ser EPILOGO, mas é {session.game_mode}!"
    print("Passou Boss Beat 15 (Epílogo).")

if __name__ == "__main__":
    test_bloco_40()

