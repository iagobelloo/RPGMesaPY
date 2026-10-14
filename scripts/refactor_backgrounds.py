import os
import json

def rename_backgrounds():
    base_path = os.path.join("assets", "backgrounds", "Fases")
    
    if not os.path.exists(base_path):
        print(f"[AVISO] O diretório {base_path} não foi encontrado. As imagens não serão renomeadas.")
        return

    bg_map = {
        "Acampamento de Bandidos no Cânion_bg.jpg": "bandit_camp_canyon_bg.jpg",
        "Acampamento_Goblin_bg.jpg": "goblin_camp_bg.jpg",
        "As_Minas_de_Ferro_Negro_bg.jpg": "black_iron_mines_bg.jpg",
        "Caverna de Lava_bg.jpg": "lava_cave_bg.jpg",
        "Caverna_Úmida_e_Escura_bg.jpg": "dark_damp_cave_bg.jpg",
        "Cemitério Antigo_bg.jpg": "ancient_cemetery_bg.jpg",
        "Floresta_Sombria_(Noite)_bg.jpg": "dark_forest_night_bg.jpg",
        "Floresta_Verdejante_(Dia)_bg.jpg": "green_forest_day_bg.jpg",
        "O_Castelo_da_Capital_bg.jpg": "capital_castle_bg.jpg",
        "O_Grande_Bazar_bg.jpg": "grand_bazaar_bg.jpg",
        "O_Observatório_Arcano_bg.jpg": "arcane_observatory_bg.jpg",
        "O_Templo_Esquecido_bg.jpg": "forgotten_temple_bg.jpg",
        "Pântano Nebuloso e Tóxico_bg.jpg": "toxic_swamp_bg.jpg",
        "Passagem da Montanha Nevada_bg.jpg": "snowy_mountain_pass_bg.jpg",
        "Planície_com_Estrada_de_Terra_bg.jpg": "dirt_road_plains_bg.jpg",
        "Ruínas do Forte Esquecido_bg.jpg": "forgotten_fort_ruins_bg.jpg",
        "Ruínas_na_Floresta_Antiga_bg.jpg": "ancient_forest_ruins_bg.jpg",
        "O_Covil_do_Tirano_bg.jpg": "tyrants_lair_bg.jpg"
    }

    print("=== INICIANDO OPERAÇÃO 1: RENOMEAR BACKGROUNDS ===")
    for old_name, new_name in bg_map.items():
        old_path = os.path.join(base_path, old_name)
        new_path = os.path.join(base_path, new_name)

        if os.path.exists(old_path):
            try:
                os.rename(old_path, new_path)
                print(f"[OK] Renomeado: {old_name} -> {new_name}")
            except Exception as e:
                print(f"[ERRO] Falha ao renomear {old_name}: {e}")
        else:
            print(f"[PULOU] Arquivo não encontrado: {old_name} (Talvez já tenha sido renomeado?)")

def inject_visuals_to_campaign():
    campaign_path = os.path.join("data", "campaign.json")
    
    print("\n=== INICIANDO OPERAÇÃO 2: INJETAR BACKGROUNDS NO ROTEIRO ===")
    if not os.path.exists(campaign_path):
        print(f"[ERRO] Arquivo {campaign_path} não encontrado!")
        return
        
    try:
        with open(campaign_path, "r", encoding="utf-8") as f:
            campaign_data = json.load(f)
            
        bg_assignments = {
            "1": "capital_castle_bg.jpg",
            "2": "dirt_road_plains_bg.jpg",
            "3": "green_forest_day_bg.jpg",
            "4": "bandit_camp_canyon_bg.jpg",
            "5": "toxic_swamp_bg.jpg",
            "6": "dark_forest_night_bg.jpg",
            "7": "ancient_cemetery_bg.jpg",
            "8": "ancient_forest_ruins_bg.jpg",
            "9": "snowy_mountain_pass_bg.jpg",
            "10": "dark_damp_cave_bg.jpg",
            "11": "black_iron_mines_bg.jpg",
            "12": "forgotten_temple_bg.jpg",
            "13": "lava_cave_bg.jpg",
            "14": "arcane_observatory_bg.jpg",
            "15": "tyrants_lair_bg.jpg"
        }
        
        for beat_id, bg_image in bg_assignments.items():
            if beat_id in campaign_data:
                campaign_data[beat_id]["bg_image"] = bg_image
                
        with open(campaign_path, "w", encoding="utf-8") as f:
            json.dump(campaign_data, f, indent=4, ensure_ascii=False)
            
        print("[OK] Arquivo campaign.json atualizado com sucesso com as chaves visuais.")
    except Exception as e:
        print(f"[ERRO] Falha ao atualizar campaign.json: {e}")

if __name__ == "__main__":
    rename_backgrounds()
    inject_visuals_to_campaign()
    print("\n=== SCRIPT FINALIZADO ===")

