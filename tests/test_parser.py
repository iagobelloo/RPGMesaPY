import sys
import pygame
from ai_master.ai_client import AIGameMaster

def test_parser():
    print("Iniciando o AI Game Master...")
    pygame.init()
    pygame.display.set_mode((100, 100))
    ai = AIGameMaster()
    print("=== SIMULAÇÃO DA FASE 0, 1 E 2 DO MÓDULO DE COMBATE ===")
    
    # Ficha Mockada do Jogador
    mock_player = {
        "race": "Halfling",
        "class": "Ladino",
        "attributes": {"FOR": 8, "DES": 18, "CON": 14, "INT": 12, "SAB": 10, "CAR": 14},
        "proficiencies": ["Adaga", "Furtividade", "Acrobacia"],
        "inventory": ["Adaga (1d4 perfurante)", "Armadura de Couro", "Ferramentas de Ladrão"]
    }
    
    # Inimigo Mockado e Cenário
    mock_target = {
        "nome": "Goblin Ladrão",
        "ca": 13,
        "pv_max": 7,
        "pv_atual": 7
    }
    
    scene_state = {
        "environment": "Taverna escura cheirando a sangue velho e cerveja choca, chovendo pesadamente lá fora",
        "living_enemies": "1 Goblin Ladrão"
    }
    
    print("--- FASE 0: PARSER DE INTENÇÃO E CASTING (Temperatura 0.0) ---")
    from ui.asset_manager import AssetManager
    AssetManager.load_backgrounds()
    AssetManager.load_character_sprites()
    bgs = AssetManager.get_narrative_backgrounds()
    
    # Cosplays possíveis (extraídos do AssetManager dinamicamente ou fixados)
    available_cosplays = "Raças: Humano, Anão, Halfling, Elfo, Draconato, Meio-Orc, Tiefling. Classes: Guerreiro, Ladino, Mago, Paladino, Clérigo, Patrulheiro."
    
    current_background_key = "tavern"
    active_visual_npcs = {} # Estado visual persistente
    
    complex_input = "O mestre de taverna aponta para a porta, onde dois Orcs brutais acabam de entrar brandindo machados. Eu saco minha espada e grito!"
    print(f"\n[INPUT DO JOGADOR]:\n{complex_input}")
    
    parsed_json = ai.parse_player_action(complex_input, available_backgrounds=bgs, available_cosplays=available_cosplays)
    
    # Gancho de Transição de Cena (Limpa NPCs se mudar de sala)
    if parsed_json.get("mudanca_cenario") != "manter" and parsed_json.get("mudanca_cenario") in bgs:
        current_background_key = parsed_json["mudanca_cenario"]
        active_visual_npcs.clear()
        print(f"\n[ORQUESTRADOR] Transição de Cena! Limpando NPCs. Novo Cenário: '{current_background_key}'")
        
    # Gancho do Diretor Visual (Casting de Novos Atores)
    novos_atores = parsed_json.get("novos_atores_visuais", [])
    if novos_atores:
        print("\n[DIRETOR VISUAL] Escalando 'Cosplays' para novos NPCs...")
        for ator in novos_atores:
            id_narrativo = ator.get("id_narrativo")
            raca = ator.get("raca_visual", "Humano")
            classe = ator.get("classe_visual", "Guerreiro")
            gen = ator.get("genero", "M")
            
            # Puxa o cosplay (se falhar, cai no DEFAULT_NPC_FALLBACK de forma transparente)
            sprite = AssetManager.get_npc_sprite(raca, classe, gen)
            active_visual_npcs[id_narrativo] = sprite
            print(f" -> {id_narrativo} será renderizado como: {raca} {classe} ({gen}).")

    print("\n--- LOOP DE RENDERIZAÇÃO (DRAW) ---")
    print(f"Cenário desenhado: {current_background_key}")
    for index, (npc_id, sprite) in enumerate(active_visual_npcs.items()):
        # Lógica de espaçamento no eixo X
        x_pos = 800 - (index * 120)
        y_pos = 350
        print(f" -> Desenhando NPC [{npc_id}] na posição (X: {x_pos}, Y: {y_pos}).")
        
    print("\n=== FIM DA SIMULAÇÃO ===")

if __name__ == "__main__":
    test_parser()
