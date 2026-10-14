import queue
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

def test_bloco_32():
    print("[TESTE BLOCO 32] Inicializando Mock...")
    ai = AIGameMaster()
    session = SessionManager(ai)
    
    # Simular estado salvo em slot1.json
    session.game_state["player_character"] = {
        "name": "Aragorn", "race": "Humano", "class": "Guerreiro",
        "attributes": {"FOR": 16, "DES": 14}, 
        "inventory": ["Espada Longa"],
        "hp_max": 20, "hp_current": 20,
        "ca": 14,
        "xp": 0
    }
    session.game_state["last_checkpoint_type"] = "TAVERNA"
    session.game_state["last_checkpoint_beat"] = 0
    session.save_game()
    
    print("[TESTE BLOCO 32] Cenario A: Condicao C (Morte Definitiva).")
    # Força HP 0 no jogador e o coloca em combate
    session.game_state["player_character"]["hp_current"] = 0
    session.game_mode = "COMBATE"
    session.story.current_beat = 2 # Não é o boss final (beat 4)
    session.active_combat_targets = {
        "goblin": {"name": "Goblin", "pv_atual": 10, "pv_max": 10, "ca": 12, "faction": "enemy"}
    }
    
    # Processa um input genérico (como se um Goblin o tivesse atacado e zerado sua vida)
    session._async_turn_processor("ataco o goblin", ["tavern"], ["goblin"])
    
    print("\n[RESULTADOS DA FILA]")
    while not session.ui_queue.empty():
        msg = session.ui_queue.get_nowait()
        print(f">> MENSAGEM: {msg}")

if __name__ == "__main__":
    test_bloco_32()
