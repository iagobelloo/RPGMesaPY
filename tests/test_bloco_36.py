import asyncio
import json
import uuid

from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

async def run_test():
    print("=== INICIANDO TESTE BLOCO 36: O ROTEIRO ÉPICO E SPAWNER ===")
    
    # Inicializa a engine
    ai_master = AIGameMaster()
    engine = SessionManager(ai_master)
    
    # Mock do estado do jogador
    engine.game_state["player_character"] = {
        "name": "Herói Teste",
        "hp_current": 20,
        "hp_max": 20,
        "ac": 15,
        "level": 3,
        "inventory": ["Espada Longa"]
    }
    engine.story.current_beat = 1
    engine.game_mode = "EXPLORACAO"
    
    # Esvazia a UI Queue inicial
    while not engine.ui_queue.empty():
        engine.ui_queue.get_nowait()
        
    print("\n[Turno 1] Jogador decide sair do Hub (Beat 1 para Beat 2)")
    
    # Mock direto do input simulando a resposta do AI_CLIENT Fase 0
    original_parse = engine.ai.parse_player_intent
    def mock_parse(player_input, state):
        print("[AI_MASTER NLP] Intenção Mockada: AVANCAR_HISTORIA")
        return {
            "tipo_acao": "AVANCAR_HISTORIA",
            "recurso_utilizado": None,
            "alvo": [],
            "intencao_cena": "O herói sai da taverna e pega a estrada."
        }
    engine.ai.parse_player_intent = mock_parse
    
    original_narrative = engine.ai.generate_narrative_from_math
    def mock_narrative(math_str, context):
        return f"[MOCK NARRADOR]: {context}. (Math origin: {math_str})"
    engine.ai.generate_narrative_from_math = mock_narrative
    
    # Processa a intenção
    engine._async_turn_processor("Eu pego a estrada e viajo.", [], [])
    
    print(f"\nBeat Atual: {engine.story.current_beat}")
    print(f"Modo Atual: {engine.game_mode}")
    print(f"Inimigos em Combate: {len(engine.active_combat_targets)}")
    for key, target in engine.active_combat_targets.items():
        print(f" - {target['name']} (HP: {target['pv_atual']}, CA: {target['ca']}, Bestiário: {target['tipo_bestiario']})")
        
    print("\nLendo fila de UI:")
    while not engine.ui_queue.empty():
        msg = engine.ui_queue.get_nowait()
        if "type" in msg:
            print(f"> [{msg['type']}] {msg['content']}")

if __name__ == "__main__":
    asyncio.run(run_test())
