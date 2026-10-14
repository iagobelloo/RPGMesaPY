import queue
import random
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

def test_bloco_34():
    print("[TESTE BLOCO 34] Inicializando Mock...")
    ai = AIGameMaster()
    session = SessionManager(ai)
    
    # Simular estado
    session.game_state["player_character"] = {
        "name": "Kael", "race": "Humano", "class": "Guerreiro",
        "attributes": {"FOR": 16, "DES": 14}, 
        "inventory": ["Espada Longa"],
        "hp_max": 20, "hp_current": 5, # Machucado, precisa de cura
        "ca": 14,
        "xp": 0
    }
    
    # Injetando poção no inventário lógico de estado
    session.game_state["inventory"] = {"i_potion_healing": 3}
    
    session.game_mode = "COMBATE"
    session.active_combat_targets = {
        "goblin": {"name": "Goblin", "pv_atual": 10, "pv_max": 10, "ca": 12, "faction": "enemy"}
    }
    
    # Forçar dados: poção de cura (2d4+2)
    # Se travarmos o randint em 4, 2d4+2 = 4+4+2 = 10 de cura. HP vai de 5 a 15.
    original_randint = random.randint
    random.randint = lambda a, b: 4
    
    print("[TESTE BLOCO 34] Jogador (5/20 HP) tenta usar Poção de Cura em COMBATE.")
    session._async_turn_processor("eu bebo uma poção de cura", ["tavern"], ["goblin"])
    
    print("\n[RESULTADOS DA FILA]")
    while not session.ui_queue.empty():
        msg = session.ui_queue.get_nowait()
        print(f">> MENSAGEM: {msg}")
        
    print("\n[ESTADO DO JOGO PÓS-TURNO]")
    print(f"Modo: {session.game_mode}")
    # Com o ataque do goblin (também rolando randint=4). 
    # Atk = 4 + 2 = 6 vs CA 14 (Erro). Então o goblin erra.
    # O HP deve terminar em 15.
    print(f"HP Atual do Jogador: {session.game_state['player_character']['hp_current']}/20 (Esperado: 15)")
    print(f"Poções Restantes: {session.game_state['inventory']['i_potion_healing']} (Esperado: 2)")
    
    random.randint = original_randint

if __name__ == "__main__":
    test_bloco_34()
