import json
import os

def load_character_creation_jsons():
    # Carrega Raças
    try:
        with open('data/races.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            mapping = {"race_human": "Humano", "race_halfling": "Halfling", "race_dragonborn": "Draconato", "race_half_orc": "Meio-Orc", "race_tiefling": "Tiefling"}
            for key, val in data.items():
                if key in mapping and mapping[key] in RACAS_5E:
                    RACAS_5E[mapping[key]]["descricao_ui"] = val.get("description_pt", "")
    except Exception: pass

    # Carrega Classes
    try:
        with open('data/classes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            mapping = {"class_fighter": "Guerreiro", "class_cleric": "Clérigo", "class_paladin": "Paladino", "class_wizard": "Mago", "class_ranger": "Patrulheiro"}
            for key, val in data.items():
                if key in mapping and mapping[key] in CLASSES:
                    CLASSES[mapping[key]]["descricao_ui"] = val.get("description_pt", "")
    except Exception: pass

    # Carrega Antecedentes
    try:
        with open('data/backgrounds.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            mapping = {"bg_mercenary": "Mercenário", "bg_acolyte": "Acólito", "bg_criminal": "Criminoso", "bg_noble": "Nobre", "bg_outlander": "Forasteiro"}
            for key, val in data.items():
                if key in mapping and mapping[key] in ANTECEDENTES_5E:
                    ANTECEDENTES_5E[mapping[key]]["descricao_ui"] = val.get("description_pt", "")
    except Exception: pass

    # Carrega Tendências
    try:
        with open('data/alignments.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            mapping = {
                "al_lg": "Leal e Bom", "al_ng": "Neutro e Bom", "al_cg": "Caótico e Bom",
                "al_ln": "Leal e Neutro", "al_n": "Neutro", "al_cn": "Caótico e Neutro",
                "al_le": "Leal e Mau", "al_ne": "Neutro e Mau", "al_ce": "Caótico e Mau"
            }
            for key, val in data.items():
                if key in mapping and mapping[key] in TENDENCIAS_5E:
                    TENDENCIAS_5E[mapping[key]]["descricao_ui"] = val.get("description_pt", "")
    except Exception: pass

load_character_creation_jsons()

