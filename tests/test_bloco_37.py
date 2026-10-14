import time
import json
import os
import sys

# Garante que os caminhos e arquivos estão acessíveis
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

class DummyAI(AIGameMaster):
    def parse_player_intent(self, user_input, game_state):
        if "atacar" in user_input.lower():
            return {"tipo_acao": "ATACAR", "alvo": ["Tirano"]}
        elif "interagir" in user_input.lower():
            return {"tipo_acao": "INTERAGIR_CENARIO"}
        elif "avancar" in user_input.lower():
            return {"tipo_acao": "AVANCAR_HISTORIA"}
        return {"tipo_acao": "exploracao"}

    def generate_narrative_from_math(self, sys_log, intent):
        return sys_log

def get_sys_logs(session):
    logs = []
    while not session.ui_queue.empty():
        msg = session.ui_queue.get()
        if msg.get("type") == "system_message":
            logs.append(msg["content"])
    return logs

def reset_saves():
    if os.path.exists("saves/slot1.json"):
        os.remove("saves/slot1.json")

def test_deja_vu():
    print("=== INICIANDO TESTE DO BLOCO 37 ===")
    reset_saves()
    
    # Backup dos arquivos originais em memória
    orig_bestiary = None
    orig_campaign = None
    if os.path.exists("data/bestiary.json"):
        with open("data/bestiary.json", "r", encoding="utf-8") as f:
            orig_bestiary = f.read()
    if os.path.exists("data/campaign.json"):
        with open("data/campaign.json", "r", encoding="utf-8") as f:
            orig_campaign = f.read()
            
    try:
        # Prepara mock de inimigos
        bestiary = {"boss_final": {"name": "Tirano", "hp": 10, "ac": 10}}
        with open("data/bestiary.json", "w", encoding="utf-8") as f:
            json.dump(bestiary, f)
            
        campaign = {
            "1": {"id": "hub", "type": "hub", "enemies": []},
            "12": {"id": "templo", "type": "exploration", "enemies": []},
            "15": {"id": "boss_room", "type": "combat", "enemies": ["boss_final"]}
        }
        with open("data/campaign.json", "w", encoding="utf-8") as f:
            json.dump(campaign, f)

        session = SessionManager(DummyAI())
        
        # Força estado inicial (Nível 5, XP 1000)
        session.game_state["player_character"] = {
            "name": "Heroi", "hp_current": 50, "hp_max": 50, "xp": 1000, "level": 5, 
            "attributes": {"STR": 16, "DEX": 14, "CON": 14, "INT": 10, "WIS": 10, "CHA": 10},
            "weapon": {"damage_dice": "1d8", "hit_bonus": 3}
        }
        session.save_game()
        
        # Avança pro Boss (Loop 0)
        session.story.campaign_log[15] = "Boss Room"
        session.story.current_beat = 14
        session._async_turn_processor("avancar", [], [])
        
        logs = get_sys_logs(session)
        boss_intro_0 = any("O Tirano das Cinzas emerge do vulcão! Sua escama é inquebrável" in l for l in logs)
        print(f"Boss Intro (Loop 0): {boss_intro_0}")
        
        # Morre
        session.game_state["player_character"]["hp_current"] = 0
        session.resolve_player_death()
        
        logs = get_sys_logs(session)
        deja_vu_msg = any("O fogo aniquila o seu corpo, mas o tempo se estilhaça e retrocede" in l for l in logs)
        print(f"Mensagem Déjà Vu: {deja_vu_msg}")
        print(f"XP retido: {session.game_state['player_character']['xp'] == 1000}")
        print(f"Loop Count: {session.game_state['meta']['loop_count']}")
        
        # Avança pro Boss de novo (Loop 1 - Hardcore)
        session.story.current_beat = 14
        session._async_turn_processor("avancar", [], [])
        
        logs = get_sys_logs(session)
        boss_intro_1 = any("A batalha é real e excruciante!" in l for l in logs)
        print(f"Boss Intro (Loop 1 Hardcore): {boss_intro_1}")
        
        # Pega o Orbe (Beat 12)
        session.game_mode = "EXPLORACAO"
        session.active_combat_targets.clear()
        session.story.current_beat = 12
        session._async_turn_processor("interagir com o altar", [], [])
        
        logs = get_sys_logs(session)
        orbe_msg = any("Orbe Quebra-Chamas" in l for l in logs)
        print(f"Encontrou Orbe: {orbe_msg}")
        
        # Avança pro Boss de novo (Loop 1 - Weakened)
        session.story.current_beat = 14
        session._async_turn_processor("avancar", [], [])
        
        logs = get_sys_logs(session)
        boss_intro_2 = any("O Orbe ressoa, rachando a armadura impenetrável do dragão" in l for l in logs)
        print(f"Boss Intro (Loop 1 Weakened): {boss_intro_2}")
        
        print("=== TESTE CONCLUÍDO ===")
    finally:
        if orig_bestiary is not None:
            with open("data/bestiary.json", "w", encoding="utf-8") as f:
                f.write(orig_bestiary)
        if orig_campaign is not None:
            with open("data/campaign.json", "w", encoding="utf-8") as f:
                f.write(orig_campaign)

if __name__ == "__main__":
    test_deja_vu()
