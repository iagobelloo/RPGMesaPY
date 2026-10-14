import os
import time
import json
from ai_master.ai_client import AIGameMaster
from core.game_engine import SessionManager

def test_bloco_34_fase2():
    print("=== INICIANDO TESTE BLOCO 34 FASE 2: CONJURAR_MAGIA ===")
    
    ai_master = AIGameMaster()
    session = SessionManager(ai_master)
    
    # Prepara o estado
    session.game_state["player_character"] = {
        "name": "Gandalf",
        "class": "Mago",
        "hp_max": 20,
        "hp_current": 20,
        "attributes": {"FOR": 8, "DES": 14, "CON": 12, "INT": 18, "SAB": 14, "CAR": 10},
        "spell_save_dc": 14,
        "spell_slots": {"1": 2, "2": 1, "3": 1}
    }
    
    session.game_mode = "COMBATE"
    session.active_combat_targets = {
        "Goblin 1": {"name": "Goblin 1", "pv_atual": 15, "pv_max": 15, "ca": 13, "tipo_bestiario": "lacaio goblin", "faction": "enemy"},
        "Goblin 2": {"name": "Goblin 2", "pv_atual": 15, "pv_max": 15, "ca": 13, "tipo_bestiario": "lacaio goblin", "faction": "enemy"},
        "Orc": {"name": "Orc", "pv_atual": 30, "pv_max": 30, "ca": 13, "tipo_bestiario": "lacaio orc", "faction": "enemy"}
    }
    
    print("\n--- Teste 1: Bola de Fogo (AoE) ---")
    session.process_action_async("Lanço uma Bola de Fogo em cima dos goblins e do orc!", [], [])
    
    time.sleep(10) # Aguarda processamento assíncrono (incluindo IA)
    
    print("Mensagens na fila UI:")
    while not session.ui_queue.empty():
        msg = session.ui_queue.get()
        print(f"> {msg}")
        
    print("\nEstado do Combate:")
    for t_id, t_data in session.active_combat_targets.items():
        print(f"  {t_id}: {t_data['pv_atual']} PV")
        
    print(f"Spell Slots restantes: {session.game_state['player_character']['spell_slots']}")
    
    print("\n--- Teste 2: Mísseis Mágicos (Direct) no Orc ---")
    session.process_action_async("Uso Mísseis Mágicos no Orc", [], [])
    
    time.sleep(10)
    
    print("Mensagens na fila UI:")
    while not session.ui_queue.empty():
        msg = session.ui_queue.get()
        print(f"> {msg}")
        
    print("\nEstado do Combate:")
    for t_id, t_data in session.active_combat_targets.items():
        print(f"  {t_id}: {t_data['pv_atual']} PV")
        
    print(f"Spell Slots restantes: {session.game_state['player_character']['spell_slots']}")

if __name__ == "__main__":
    test_bloco_34_fase2()
