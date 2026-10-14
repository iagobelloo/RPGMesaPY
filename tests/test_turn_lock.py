import queue
import time
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

def test_turn_lock():
    print("[TESTE] Inicializando o GM e Engine...")
    ai = AIGameMaster()
    session = SessionManager(ai)
    
    # Prepara o PC minimo
    session.game_state["player_character"] = {
        "name": "Thorin", "race": "Anão", "class": "Guerreiro", 
        "background": "Soldado", "inventory": ["Machado de Batalha"]
    }
    
    # Garante que não há alvos (Fantasma/Morto/Não spawnado)
    session.game_mode = "EXPLORACAO"
    session.active_combat_targets = {}
    
    print("[TESTE] Situação: Modo EXPLORACAO, nenhum alvo ativo.")
    print("[TESTE] Input do jogador: 'ataco o lacaio goblin com meu machado'")
    
    # Chama o processor diretamente (síncrono para o teste)
    session._async_turn_processor("ataco o lacaio goblin com meu machado", ["tavern"], ["goblin"])
    
    # Checa o log na fila (Resgate da UI)
    print("\n[TESTE] Lendo fila de UI...")
    try:
        msg = session.ui_queue.get_nowait()
        print(f"Mensagem recebida na UI: {msg}")
        if "não encontrado no combate" in msg.get("narrativa", "") or "Alvo inválido" in msg.get("narrativa", ""):
            print("[SUCESSO] Turn Lock (Trava de Turno) funcionou! Ação abortada.")
    except queue.Empty:
        print("[FALHA] Nenhuma mensagem retornada na UI Queue.")

if __name__ == "__main__":
    test_turn_lock()
