import queue
import random
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

def test_bloco_33():
    print("[TESTE BLOCO 33] Inicializando Mock...")
    ai = AIGameMaster()
    session = SessionManager(ai)
    
    # Simular estado
    session.game_state["player_character"] = {
        "name": "Kael", "race": "Humano", "class": "Guerreiro",
        "attributes": {"FOR": 16, "DES": 14}, 
        "inventory": ["Espada Longa"],
        "hp_max": 20, "hp_current": 5, # Machucado
        "ca": 14,
        "xp": 0
    }
    session.game_state["suprimentos_acampamento"] = 1
    session.game_state["suprimentos_maximos"] = 1
    
    # Simular que estamos no Ermo
    session.story.current_beat = 2 
    session.game_mode = "EXPLORACAO"
    
    # Forçar a rolagem para dar 5 (falha garantida na emboscada)
    original_randint = random.randint
    random.randint = lambda a, b: 5
    
    print("[TESTE BLOCO 33] Jogador tenta descansar com 5/20 HP no Ermo.")
    session._async_turn_processor("eu quero descansar", ["tavern"], ["goblin"])
    
    print("\n[RESULTADOS DA FILA]")
    while not session.ui_queue.empty():
        msg = session.ui_queue.get_nowait()
        print(f">> MENSAGEM: {msg}")
        
    print("\n[ESTADO DO JOGO PÓS-DESCANSO]")
    print(f"Modo: {session.game_mode}")
    print(f"HP Atual: {session.game_state['player_character']['hp_current']}/20 (Esperado: 16 que é 80%)")
    print(f"Suprimentos: {session.game_state['suprimentos_acampamento']}")
    print(f"Alvos Ativos (Monstro Spawnado): {list(session.active_combat_targets.keys())}")
    
    random.randint = original_randint

if __name__ == "__main__":
    test_bloco_33()
