import queue
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

def test_bloco_31():
    print("[TESTE BLOCO 31] Inicializando Mock...")
    ai = AIGameMaster()
    session = SessionManager(ai)
    
    # Prepara o PC com muito pouco HP
    session.game_state["player_character"] = {
        "name": "Kael", "race": "Humano", "class": "Guerreiro",
        "attributes": {"FOR": 16, "DES": 14}, 
        "inventory": ["Espada Longa"],
        "hp_current": 1,  # PC morre com 1 golpe
        "ca": 10
    }
    
    session.game_mode = "COMBATE"
    session.active_combat_targets = {
        "aliado clérigo": {"name": "Karg", "pv_atual": 15, "pv_max": 15, "ca": 12, "faction": "ally"},
        "goblin a": {"name": "Goblin A", "pv_atual": 10, "pv_max": 10, "ca": 12, "tipo_bestiario": "goblin", "faction": "enemy"},
        "goblin b": {"name": "Goblin B", "pv_atual": 10, "pv_max": 10, "ca": 12, "tipo_bestiario": "goblin", "faction": "enemy"}
    }
    
    # O Player ataca, mas os inimigos sobrevivem e revidam
    # O Jogador (Kael) tem 1 HP e o Aliado (Karg) tem 15 HP
    # Goblin A vai focar Kael (menor HP), vai dar dano, Kael cai pra 0.
    # Goblin B reavalia, não ataca o Kael (pois HP == 0), ataca o Karg.
    
    print("[TESTE BLOCO 31] Situação: Jogador tem 1 HP, Aliado tem 15 HP.")
    print("[TESTE BLOCO 31] Enviando intenção: 'ataco o goblin a com minha espada longa'")
    session._async_turn_processor("ataco o goblin a com minha espada longa", ["tavern"], ["goblin"])
    
    print("\n[TESTE BLOCO 31] --- RESULTADOS DA FILA ---")
    while not session.ui_queue.empty():
        try:
            msg = session.ui_queue.get_nowait()
            print(f">> MENSAGEM CAPTURADA: {msg}")
        except queue.Empty:
            break
            
if __name__ == "__main__":
    test_bloco_31()
