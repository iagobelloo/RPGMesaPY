import time
from ai_master.ai_client import AIGameMaster
from core.game_engine import SessionManager

def test_bloco_35():
    print("=== INICIANDO TESTE BLOCO 35 (PARTE 1): HUB E AGÊNCIA ===")
    
    ai = AIGameMaster()
    session = SessionManager(ai)
    
    # Simula estado inicial
    session.game_state["player_character"] = {
        "name": "Thrain",
        "race": "Anão",
        "class": "Guerreiro",
        "inventory": [],
        "hp_current": 10,
        "hp_max": 10
    }
    session.game_mode = "EXPLORACAO"
    
    print("\n[Turno 1] Jogador quer beber e conversar")
    session.process_action_async("Peço uma caneca de cerveja ao taverneiro e pergunto sobre os rumores da Trilha dos Enforcados.", [], [])
    
    time.sleep(10)
    
    while not session.ui_queue.empty():
        msg = session.ui_queue.get()
        print(f"> {msg}")
        
    print(f"\nBeat Atual: {session.story.current_beat}")
    
    print("\n[Turno 2] Jogador decide sair do Hub")
    session.process_action_async("Pego minhas coisas, coloco o capuz e saio pela porta principal da taverna.", [], [])
    
    time.sleep(10)
    
    while not session.ui_queue.empty():
        msg = session.ui_queue.get()
        print(f"> {msg}")
        
    print(f"\nBeat Atual: {session.story.current_beat}")

if __name__ == "__main__":
    test_bloco_35()

