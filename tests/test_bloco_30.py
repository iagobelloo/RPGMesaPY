import queue
import time
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

def test_bloco_30():
    print("[TESTE BLOCO 30] Inicializando Mock...")
    ai = AIGameMaster()
    session = SessionManager(ai)
    
    # Preparando estado falso para forçar o ataque
    session.game_state["player_character"] = {
        "name": "Kael", "race": "Humano", "class": "Guerreiro",
        "attributes": {"FOR": 16, "DES": 14}, # +3 FOR
        "inventory": ["Espada Longa"]
    }
    
    session.game_mode = "COMBATE"
    session.active_combat_targets = {
        "lacaio goblin": {"name": "Lacaio Goblin", "pv_atual": 10, "pv_max": 10, "ca": 12, "tipo_bestiario": "goblin", "faction": "enemy"}
    }
    
    print("[TESTE BLOCO 30] Enviando intenção: 'ataco o lacaio goblin com minha espada longa'")
    session._async_turn_processor("ataco o lacaio goblin com minha espada longa", ["tavern"], ["goblin"])
    
    print("\n[TESTE BLOCO 30] --- RESULTADOS DA FILA ---")
    while not session.ui_queue.empty():
        try:
            msg = session.ui_queue.get_nowait()
            print(f">> MENSAGEM CAPTURADA: {msg}")
        except queue.Empty:
            break
            
if __name__ == "__main__":
    test_bloco_30()
