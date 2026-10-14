import os
import json

def rename_sprites():
    base_path = os.path.join("assets", "sprites", "enemies")
    
    # Criar o diretório se não existir (apenas para evitar erros em testes locais, 
    # embora a instrução implique que ele já existe)
    if not os.path.exists(base_path):
        print(f"[AVISO] O diretório {base_path} não foi encontrado. As imagens não serão renomeadas.")
        return

    sprite_map = {
        "aparicao.png": "wraith.png",
        "aranha_gigante.png": "giant_spider.png",
        "armadura_enfeiticada.png": "animated_armor.png",
        "bandido.png": "bandit.png",
        "cria_vampiro.png": "vampire_spawn.png",
        "esqueleto.png": "skeleton.png",
        "gargula.png": "gargoyle.png",
        "gigante_fogo.png": "fire_giant.png",
        "goblin.png": "goblin.png",
        "kobold.png": "kobold.png",
        "kraken.png": "kraken.png",
        "lich.png": "lich.png",
        "limo_ocre.png": "ochre_jelly.png",
        "lobo_atroz.png": "dire_wolf.png",
        "manticora.png": "manticore.png",
        "mimico.png": "mimic.png",
        "ogro_1.png": "ogre_brute.png",
        "ogro.png": "ogre.png",
        "orc.png": "orc.png",
        "quimera.png": "chimera.png",
        "rakshasa.png": "rakshasa.png",
        "solar.png": "solar.png",
        "sombra.png": "shadow.png",
        "veterano.png": "veteran.png",
        "zumbi_1.png": "zombie_fast.png",
        "zumbi.png": "zombie.png"
    }

    print("=== INICIANDO OPERAÇÃO 1: RENOMEAR SPRITES ===")
    for old_name, new_name in sprite_map.items():
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

def generate_flat_bestiary():
    bestiary_path = os.path.join("data", "bestiary.json")
    
    print("\n=== INICIANDO OPERAÇÃO 2: GERAR BESTIÁRIO FLAT ===")
    
    bestiary_dict = {
        "m_wraith": {
            "name": "Wraith",
            "hp": 67,
            "ac": 13,
            "speed": 60,
            "attributes": {"STR": 6, "DEX": 16, "CON": 16, "INT": 12, "WIS": 14, "CHA": 15},
            "actions": [
                {"name": "Life Drain", "hit_bonus": 6, "damage_dice": "4d8+3"}
            ]
        },
        "m_giant_spider": {
            "name": "Giant Spider",
            "hp": 26,
            "ac": 14,
            "speed": 30,
            "attributes": {"STR": 14, "DEX": 16, "CON": 12, "INT": 2, "WIS": 11, "CHA": 4},
            "actions": [
                {"name": "Bite", "hit_bonus": 5, "damage_dice": "1d8+3"}
            ]
        },
        "m_animated_armor": {
            "name": "Animated Armor",
            "hp": 33,
            "ac": 18,
            "speed": 25,
            "attributes": {"STR": 14, "DEX": 11, "CON": 13, "INT": 1, "WIS": 3, "CHA": 1},
            "actions": [
                {"name": "Slam", "hit_bonus": 4, "damage_dice": "1d6+2"}
            ]
        },
        "m_bandit": {
            "name": "Bandit",
            "hp": 11,
            "ac": 12,
            "speed": 30,
            "attributes": {"STR": 11, "DEX": 12, "CON": 12, "INT": 10, "WIS": 10, "CHA": 10},
            "actions": [
                {"name": "Scimitar", "hit_bonus": 3, "damage_dice": "1d6+1"},
                {"name": "Light Crossbow", "hit_bonus": 3, "damage_dice": "1d8+1"}
            ]
        },
        "m_vampire_spawn": {
            "name": "Vampire Spawn",
            "hp": 82,
            "ac": 15,
            "speed": 30,
            "attributes": {"STR": 16, "DEX": 16, "CON": 16, "INT": 11, "WIS": 10, "CHA": 12},
            "actions": [
                {"name": "Claws", "hit_bonus": 6, "damage_dice": "2d4+3"},
                {"name": "Bite", "hit_bonus": 6, "damage_dice": "1d6+3"}
            ]
        },
        "m_skeleton": {
            "name": "Skeleton",
            "hp": 13,
            "ac": 13,
            "speed": 30,
            "attributes": {"STR": 10, "DEX": 14, "CON": 15, "INT": 6, "WIS": 8, "CHA": 5},
            "actions": [
                {"name": "Shortsword", "hit_bonus": 4, "damage_dice": "1d6+2"}
            ]
        },
        "m_gargoyle": {
            "name": "Gargoyle",
            "hp": 52,
            "ac": 15,
            "speed": 30,
            "attributes": {"STR": 15, "DEX": 11, "CON": 16, "INT": 6, "WIS": 11, "CHA": 7},
            "actions": [
                {"name": "Bite", "hit_bonus": 4, "damage_dice": "1d6+2"},
                {"name": "Claws", "hit_bonus": 4, "damage_dice": "1d6+2"}
            ]
        },
        "m_fire_giant": {
            "name": "Fire Giant",
            "hp": 162,
            "ac": 18,
            "speed": 30,
            "attributes": {"STR": 25, "DEX": 9, "CON": 23, "INT": 10, "WIS": 14, "CHA": 13},
            "actions": [
                {"name": "Greatsword", "hit_bonus": 11, "damage_dice": "6d6+7"}
            ]
        },
        "m_goblin": {
            "name": "Goblin",
            "hp": 7,
            "ac": 15,
            "speed": 30,
            "attributes": {"STR": 8, "DEX": 14, "CON": 10, "INT": 10, "WIS": 8, "CHA": 8},
            "actions": [
                {"name": "Scimitar", "hit_bonus": 4, "damage_dice": "1d6+2"}
            ]
        },
        "m_kobold": {
            "name": "Kobold",
            "hp": 5,
            "ac": 12,
            "speed": 30,
            "attributes": {"STR": 7, "DEX": 15, "CON": 9, "INT": 8, "WIS": 7, "CHA": 8},
            "actions": [
                {"name": "Dagger", "hit_bonus": 4, "damage_dice": "1d4+2"}
            ]
        },
        "m_kraken": {
            "name": "Kraken",
            "hp": 472,
            "ac": 18,
            "speed": 20,
            "attributes": {"STR": 30, "DEX": 11, "CON": 25, "INT": 22, "WIS": 18, "CHA": 20},
            "actions": [
                {"name": "Tentacle", "hit_bonus": 17, "damage_dice": "3d8+10"},
                {"name": "Lightning Storm", "hit_bonus": 17, "damage_dice": "4d10"}
            ]
        },
        "m_lich": {
            "name": "Lich",
            "hp": 135,
            "ac": 17,
            "speed": 30,
            "attributes": {"STR": 11, "DEX": 16, "CON": 16, "INT": 20, "WIS": 14, "CHA": 16},
            "actions": [
                {"name": "Paralyzing Touch", "hit_bonus": 12, "damage_dice": "3d6"},
                {"name": "Necrotic Ray", "hit_bonus": 12, "damage_dice": "8d6"}
            ]
        },
        "m_ochre_jelly": {
            "name": "Ochre Jelly",
            "hp": 45,
            "ac": 8,
            "speed": 10,
            "attributes": {"STR": 15, "DEX": 6, "CON": 14, "INT": 2, "WIS": 6, "CHA": 1},
            "actions": [
                {"name": "Pseudopod", "hit_bonus": 4, "damage_dice": "2d6+2"}
            ]
        },
        "m_dire_wolf": {
            "name": "Dire Wolf",
            "hp": 37,
            "ac": 14,
            "speed": 50,
            "attributes": {"STR": 17, "DEX": 15, "CON": 15, "INT": 3, "WIS": 12, "CHA": 7},
            "actions": [
                {"name": "Bite", "hit_bonus": 5, "damage_dice": "2d6+3"}
            ]
        },
        "m_manticore": {
            "name": "Manticore",
            "hp": 68,
            "ac": 14,
            "speed": 30,
            "attributes": {"STR": 17, "DEX": 16, "CON": 17, "INT": 7, "WIS": 12, "CHA": 8},
            "actions": [
                {"name": "Bite", "hit_bonus": 5, "damage_dice": "1d8+3"},
                {"name": "Tail Spike", "hit_bonus": 5, "damage_dice": "1d8+3"}
            ]
        },
        "m_mimic": {
            "name": "Mimic",
            "hp": 58,
            "ac": 12,
            "speed": 15,
            "attributes": {"STR": 17, "DEX": 12, "CON": 15, "INT": 5, "WIS": 13, "CHA": 8},
            "actions": [
                {"name": "Pseudopod", "hit_bonus": 5, "damage_dice": "1d8+3"},
                {"name": "Bite", "hit_bonus": 5, "damage_dice": "1d8+3"}
            ]
        },
        "m_ogre_brute": {
            "name": "Ogre Brute",
            "hp": 70,
            "ac": 12,
            "speed": 40,
            "attributes": {"STR": 19, "DEX": 8, "CON": 18, "INT": 5, "WIS": 7, "CHA": 7},
            "actions": [
                {"name": "Heavy Mace", "hit_bonus": 6, "damage_dice": "2d8+4"}
            ]
        },
        "m_ogre": {
            "name": "Ogre",
            "hp": 59,
            "ac": 11,
            "speed": 40,
            "attributes": {"STR": 19, "DEX": 8, "CON": 16, "INT": 5, "WIS": 7, "CHA": 7},
            "actions": [
                {"name": "Greatclub", "hit_bonus": 6, "damage_dice": "2d8+4"}
            ]
        },
        "m_orc": {
            "name": "Orc",
            "hp": 15,
            "ac": 13,
            "speed": 30,
            "attributes": {"STR": 16, "DEX": 12, "CON": 16, "INT": 7, "WIS": 11, "CHA": 10},
            "actions": [
                {"name": "Greataxe", "hit_bonus": 5, "damage_dice": "1d12+3"}
            ]
        },
        "m_chimera": {
            "name": "Chimera",
            "hp": 114,
            "ac": 14,
            "speed": 30,
            "attributes": {"STR": 19, "DEX": 11, "CON": 19, "INT": 3, "WIS": 14, "CHA": 10},
            "actions": [
                {"name": "Bite", "hit_bonus": 7, "damage_dice": "2d6+4"},
                {"name": "Fire Breath", "hit_bonus": 7, "damage_dice": "7d8"}
            ]
        },
        "m_rakshasa": {
            "name": "Rakshasa",
            "hp": 110,
            "ac": 16,
            "speed": 40,
            "attributes": {"STR": 14, "DEX": 17, "CON": 18, "INT": 13, "WIS": 16, "CHA": 20},
            "actions": [
                {"name": "Claw", "hit_bonus": 7, "damage_dice": "2d6+3"}
            ]
        },
        "m_solar": {
            "name": "Solar",
            "hp": 243,
            "ac": 21,
            "speed": 50,
            "attributes": {"STR": 26, "DEX": 22, "CON": 26, "INT": 25, "WIS": 25, "CHA": 30},
            "actions": [
                {"name": "Greatsword", "hit_bonus": 15, "damage_dice": "4d6+8"},
                {"name": "Slaying Longbow", "hit_bonus": 13, "damage_dice": "2d8+6"}
            ]
        },
        "m_shadow": {
            "name": "Shadow",
            "hp": 16,
            "ac": 12,
            "speed": 40,
            "attributes": {"STR": 6, "DEX": 14, "CON": 13, "INT": 6, "WIS": 10, "CHA": 8},
            "actions": [
                {"name": "Strength Drain", "hit_bonus": 4, "damage_dice": "2d6+2"}
            ]
        },
        "m_veteran": {
            "name": "Veteran",
            "hp": 58,
            "ac": 17,
            "speed": 30,
            "attributes": {"STR": 16, "DEX": 13, "CON": 14, "INT": 10, "WIS": 11, "CHA": 10},
            "actions": [
                {"name": "Longsword", "hit_bonus": 5, "damage_dice": "1d8+3"},
                {"name": "Shortsword", "hit_bonus": 5, "damage_dice": "1d6+3"}
            ]
        },
        "m_zombie_fast": {
            "name": "Fast Zombie",
            "hp": 22,
            "ac": 10,
            "speed": 40,
            "attributes": {"STR": 13, "DEX": 12, "CON": 16, "INT": 3, "WIS": 6, "CHA": 5},
            "actions": [
                {"name": "Slam", "hit_bonus": 3, "damage_dice": "1d6+1"}
            ]
        },
        "m_zombie": {
            "name": "Zombie",
            "hp": 22,
            "ac": 8,
            "speed": 20,
            "attributes": {"STR": 13, "DEX": 6, "CON": 16, "INT": 3, "WIS": 6, "CHA": 5},
            "actions": [
                {"name": "Slam", "hit_bonus": 3, "damage_dice": "1d6+1"}
            ]
        }
    }

    try:
        # Garantir que o diretório data existe
        if not os.path.exists("data"):
            os.makedirs("data")
            
        with open(bestiary_path, "w", encoding="utf-8") as file:
            json.dump(bestiary_dict, file, indent=4, ensure_ascii=False)
        print(f"[OK] Arquivo JSON gerado e sobrescrito com sucesso em {bestiary_path}")
    except Exception as e:
        print(f"[ERRO] Falha ao escrever em {bestiary_path}: {e}")

if __name__ == "__main__":
    rename_sprites()
    generate_flat_bestiary()
    print("\n=== SCRIPT FINALIZADO ===")

