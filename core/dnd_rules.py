"""
Mini-SRD (System Reference Document) para D&D 5e.
Fornece regras bases, modificadores e compêndios para Raças, Classes, Equipamentos e Protagonistas.
"""

def get_modifier(score: int) -> int:
    return (score - 10) // 2

# MATRIZ DA VERDADE (Perícias -> Atributos 5e)
MATRIZ_DE_PERICIAS = {
    "Atletismo": "FOR", "Acrobacia": "DES", "Furtividade": "DES", "Prestidigitação": "DES",
    "Arcanismo": "INT", "História": "INT", "Investigação": "INT", "Natureza": "INT", "Religião": "INT",
    "Adestrar Animais": "SAB", "Intuição": "SAB", "Medicina": "SAB", "Percepção": "SAB", "Sobrevivência": "SAB",
    "Atuação": "CAR", "Enganação": "CAR", "Intimidação": "CAR", "Persuasão": "CAR"
}

# STANDARD ARRAY D&D 5E POR CLASSE (15, 14, 13, 12, 10, 8)
CLASS_STANDARD_ARRAY = {
    "Guerreiro": {"FOR": 15, "CON": 14, "DES": 13, "SAB": 12, "CAR": 10, "INT": 8},
    "Clérigo": {"SAB": 15, "CON": 14, "FOR": 13, "CAR": 12, "INT": 10, "DES": 8},
    "Paladino": {"FOR": 15, "CAR": 14, "CON": 13, "SAB": 12, "DES": 10, "INT": 8},
    "Mago": {"INT": 15, "CON": 14, "DES": 13, "SAB": 12, "CAR": 10, "FOR": 8},
    "Patrulheiro": {"DES": 15, "SAB": 14, "CON": 13, "FOR": 12, "INT": 10, "CAR": 8},
    "Ladino": {"DES": 15, "INT": 14, "CON": 13, "CAR": 12, "SAB": 10, "FOR": 8},
}

def get_class_base_attributes(class_name: str) -> dict:
    """Retorna os atributos base do Standard Array D&D 5e da classe com chaves PT e EN sincronizadas."""
    base_pt = CLASS_STANDARD_ARRAY.get(
        class_name,
        {"FOR": 15, "CON": 14, "DES": 13, "SAB": 12, "CAR": 10, "INT": 8}
    ).copy()
    pt_to_en = {"FOR": "STR", "DES": "DEX", "CON": "CON", "INT": "INT", "SAB": "WIS", "CAR": "CHA"}
    result = {}
    for pt_k, val in base_pt.items():
        result[pt_k] = val
        result[pt_to_en[pt_k]] = val
    result["LUCK"] = 10
    return result

def get_base_attributes(class_name: str) -> dict:
    """Retorna os atributos base do Standard Array D&D 5e (15, 14, 13, 12, 10, 8) sem forçar raça ou antecedentes pré-selecionados."""
    return get_class_base_attributes(class_name)

def get_standard_array(class_name: str) -> dict:
    """Retorna os atributos base do Standard Array D&D 5e da classe."""
    return get_class_base_attributes(class_name)

# 7 ITENS ÚNICOS RACIAIS (HERANÇA DE ORIGEM)
ITENS_UNICOS_RACIAIS = {
    "Humano": {
        "id": "i_racial_human_signet",
        "name": "Sinete da Coroa Partida",
        "slot": "accessory",
        "save_bonus": 1,
        "gold_bonus": 10,
        "effect": "+1 em Testes de Resistência e +10 PO iniciais."
    },
    "Elfo da Floresta": {
        "id": "i_racial_elf_cloak",
        "name": "Manto de Folhas Cinzentas",
        "slot": "accessory",
        "initiative_bonus": 1,
        "stealth_bonus": 2,
        "effect": "+1 na Iniciativa e +2 em Furtividade."
    },
    "Anão da Colina": {
        "id": "i_racial_dwarf_rune",
        "name": "Runa da Pedra-Forja",
        "slot": "accessory",
        "hp_max_bonus": 3,
        "effect": "+3 Pontos de Vida Máximos adicionais."
    },
    "Halfling": {
        "id": "i_racial_halfling_coin",
        "name": "Moeda da Sorte Antiga",
        "slot": "accessory",
        "ac_bonus": 1,
        "luck_bonus": 2,
        "effect": "+1 na Classe de Armadura (CA) e +2 em Sorte."
    },
    "Draconato": {
        "id": "i_racial_dragon_scale",
        "name": "Escama Ancestral Incandescente",
        "slot": "accessory",
        "damage_bonus": 1,
        "effect": "+1 no Dano de ataques e Arma de Sopro."
    },
    "Meio-Orc": {
        "id": "i_racial_orc_tusk",
        "name": "Presa de Ferro Sangrento",
        "slot": "accessory",
        "melee_damage_bonus": 1,
        "intimidation_bonus": 2,
        "effect": "+1 no Dano corpo a corpo e +2 em Intimidação."
    },
    "Tiefling": {
        "id": "i_racial_tiefling_seal",
        "name": "Selo de Brasas Abissais",
        "slot": "accessory",
        "spell_bonus": 1,
        "effect": "+1 no Acerto e CD de Magias."
    }
}

# MAPEAMENTO BIDIRECIONAL DE HABILIDADES (UI sk_* <-> Canônicos class_skills.json)
SKILL_UI_TO_CANONICAL = {
    "sk_warrior_1": "second_wind",
    "sk_warrior_2": "action_surge",
    "sk_warrior_3": "champion_focus",
    "sk_warrior_4": "extra_attack_fighter",
    "sk_cleric_1": "disciple_of_life",
    "sk_cleric_2": "channel_divinity_preserve_life",
    "sk_cleric_3": "destroy_undead",
    "sk_cleric_4": "divine_strike",
    "sk_paladin_1": "lay_on_hands",
    "sk_paladin_2": "divine_smite",
    "sk_paladin_3": "aura_of_protection",
    "sk_paladin_4": "improved_divine_smite",
    "sk_mage_1": "arcane_recovery",
    "sk_mage_2": "sculpt_spells",
    "sk_mage_3": "potent_cantrip",
    "sk_mage_4": "empowered_evocation",
    "sk_ranger_1": "favored_enemy",
    "sk_ranger_2": "hunters_mark_passive",
    "sk_ranger_3": "colossus_slayer",
    "sk_ranger_4": "multiattack_volley",
    "sk_rogue_1": "sneak_attack",
    "sk_rogue_2": "cunning_action",
    "sk_rogue_3": "uncanny_dodge",
    "sk_rogue_4": "assassinate"
}

SKILL_CANONICAL_TO_UI = {v: k for k, v in SKILL_UI_TO_CANONICAL.items()}

SKILL_SYNONYMS_GROUPS = [
    {"sk_warrior_1", "second_wind", "retomar o fôlego", "retomar o folego"},
    {"sk_warrior_2", "action_surge", "surto de ação", "surto de acao"},
    {"sk_warrior_3", "champion_focus", "foco do campeão", "foco do campeao"},
    {"sk_warrior_4", "extra_attack_fighter", "ataque extra (guerreiro)"},
    {"sk_cleric_1", "disciple_of_life", "discípulo da vida", "discipulo da vida"},
    {"sk_cleric_2", "channel_divinity_preserve_life", "preservar a vida", "canalizar divindade: preservar a vida", "canalizar divindade"},
    {"sk_cleric_3", "destroy_undead", "spiritual_weapon", "destruir mortos-vivos", "destruir mortos vivos"},
    {"sk_cleric_4", "divine_strike", "golpe divino"},
    {"sk_paladin_1", "lay_on_hands", "cura pelas mãos", "cura pelas maos"},
    {"sk_paladin_2", "divine_smite", "divine_smite_passive", "destruição divina", "destruicao divina"},
    {"sk_paladin_3", "aura_of_protection", "sacred_oath_devotion", "aura de proteção", "aura de protecao", "juramento de devoção: arma sagrada"},
    {"sk_paladin_4", "improved_divine_smite", "extra_attack_paladin", "destruição divina aprimorada"},
    {"sk_mage_1", "arcane_recovery", "recuperação arcana", "recuperacao arcana"},
    {"sk_mage_2", "sculpt_spells", "esculpir magias"},
    {"sk_mage_3", "potent_cantrip", "potent_spellcasting", "truque potente"},
    {"sk_mage_4", "empowered_evocation", "arcane_overload", "sobrecarga arcana", "evocação potencializada"},
    {"sk_ranger_1", "favored_enemy", "inimigo favorito"},
    {"sk_ranger_2", "hunters_mark_passive", "archery_style", "marca do caçador", "estilo de luta: arquearia"},
    {"sk_ranger_3", "colossus_slayer", "assassino de colossos"},
    {"sk_ranger_4", "multiattack_volley", "extra_attack_ranger", "saraivada"},
    {"sk_rogue_1", "sneak_attack", "ataque furtivo"},
    {"sk_rogue_2", "cunning_action", "ação astuta", "acao astuta", "ação ardilosa", "acao ardilosa"},
    {"sk_rogue_3", "uncanny_dodge", "esquiva sobrenatural"},
    {"sk_rogue_4", "assassinate", "assassinar"}
]

def normalize_skill_id(skill_ref: str) -> str:
    """Converte um ID de UI (sk_*), nome em português ou alias para o ID canônico."""
    if not skill_ref:
        return ""
    s_low = str(skill_ref).lower().strip()
    if s_low in SKILL_UI_TO_CANONICAL:
        return SKILL_UI_TO_CANONICAL[s_low]
    if s_low == "arma espiritual" or s_low == "spiritual_weapon":
        return "spiritual_weapon"
    for grp in SKILL_SYNONYMS_GROUPS:
        if s_low in grp:
            for item in grp:
                if item in SKILL_CANONICAL_TO_UI:
                    return item
    return s_low

def expand_unlocked_skills(skills_list: list) -> set:
    """Expande uma lista de habilidades desbloqueadas com todos os seus aliases (sk_*, canônicos e sinônimos)."""
    expanded = set()
    if not skills_list:
        return expanded
    for s in skills_list:
        s_low = str(s).lower().strip()
        expanded.add(s_low)
        if s_low in SKILL_UI_TO_CANONICAL:
            expanded.add(SKILL_UI_TO_CANONICAL[s_low])
        if s_low in SKILL_CANONICAL_TO_UI:
            expanded.add(SKILL_CANONICAL_TO_UI[s_low])
        for grp in SKILL_SYNONYMS_GROUPS:
            if s_low in grp:
                expanded.update(grp)
    return expanded

def sync_attributes_dict(attrs: dict) -> dict:
    """Sincroniza bidirecionalmente chaves PT (FOR..CAR) e EN (STR..CHA) preservando atualizações de Level Up."""
    if not isinstance(attrs, dict):
        return get_class_base_attributes("Guerreiro")
    pt_to_en = {"FOR": "STR", "DES": "DEX", "CON": "CON", "INT": "INT", "SAB": "WIS", "CAR": "CHA"}
    for pt_k, en_k in pt_to_en.items():
        has_pt = pt_k in attrs
        has_en = en_k in attrs
        if has_pt and has_en:
            if attrs[pt_k] != attrs[en_k]:
                # Se uma das duas foi atualizada (ex: no Level Up), preserva o valor modificado
                val = attrs[pt_k] if attrs[en_k] == 10 else (attrs[en_k] if attrs[pt_k] == 10 else max(attrs[pt_k], attrs[en_k]))
                attrs[pt_k] = val
                attrs[en_k] = val
        elif has_pt:
            attrs[en_k] = attrs[pt_k]
        elif has_en:
            attrs[pt_k] = attrs[en_k]
        else:
            attrs[pt_k] = 10
            attrs[en_k] = 10
    if "LUCK" not in attrs:
        attrs["LUCK"] = 10
    return attrs

# MATRIZ CANÔNICA DE GÊNERO DOS 42 PROTAGONISTAS (PROT-01 A PROT-42)
PROTAGONIST_GENDER_MAP = {
    "Humano": {
        "Guerreiro": "male", "Clérigo": "female", "Paladino": "male",
        "Mago": "female", "Patrulheiro": "female", "Ladino": "male"
    },
    "Anão da Colina": {
        "Guerreiro": "male", "Clérigo": "female", "Paladino": "male",
        "Mago": "male", "Patrulheiro": "female", "Ladino": "male"
    },
    "Draconato": {
        "Guerreiro": "male", "Clérigo": "female", "Paladino": "male",
        "Mago": "male", "Patrulheiro": "female", "Ladino": "male"
    },
    "Elfo da Floresta": {
        "Guerreiro": "male", "Clérigo": "female", "Paladino": "male",
        "Mago": "female", "Patrulheiro": "male", "Ladino": "female"
    },
    "Halfling": {
        "Guerreiro": "male", "Clérigo": "female", "Paladino": "male",
        "Mago": "male", "Patrulheiro": "male", "Ladino": "female"
    },
    "Meio-Orc": {
        "Guerreiro": "male", "Clérigo": "male", "Paladino": "male",
        "Mago": "male", "Patrulheiro": "male", "Ladino": "female"
    },
    "Tiefling": {
        "Guerreiro": "male", "Clérigo": "female", "Paladino": "male",
        "Mago": "male", "Patrulheiro": "female", "Ladino": "female"
    }
}

PROTAGONIST_RACE_SLUGS = {
    "Humano": "humano",
    "Anão da Colina": "anao",
    "Draconato": "draconato",
    "Elfo da Floresta": "elfo",
    "Halfling": "halfling",
    "Meio-Orc": "meio_orc",
    "Tiefling": "tiefling"
}

PROTAGONIST_CLASS_SLUGS = {
    "Guerreiro": "guerreiro",
    "Clérigo": "clerigo",
    "Paladino": "paladino",
    "Mago": "mago",
    "Patrulheiro": "patrulheiro",
    "Ladino": "ladino"
}

PROTAGONIST_RACE_ORDER = ["Humano", "Anão da Colina", "Draconato", "Elfo da Floresta", "Halfling", "Meio-Orc", "Tiefling"]
PROTAGONIST_CLASS_ORDER = ["Guerreiro", "Clérigo", "Paladino", "Mago", "Patrulheiro", "Ladino"]

def get_protagonist_gender_info(race_name: str, class_name: str) -> dict:
    """Retorna informações canônicas de gênero e caminhos de sprites para os 42 protagonistas (PROT-01 a PROT-42)."""
    gender = PROTAGONIST_GENDER_MAP.get(race_name, {}).get(class_name, "male")
    is_female = (gender == "female")
    symbol = "♀" if is_female else "♂"
    label = "Feminino" if is_female else "Masculino"
    female_class_names = {
        "Guerreiro": "Guerreira",
        "Clérigo": "Clériga",
        "Paladino": "Paladina",
        "Mago": "Maga",
        "Patrulheiro": "Patrulheira",
        "Ladino": "Ladina"
    }
    class_display = female_class_names.get(class_name, class_name) if is_female else class_name

    r_idx = PROTAGONIST_RACE_ORDER.index(race_name) if race_name in PROTAGONIST_RACE_ORDER else 0
    c_idx = PROTAGONIST_CLASS_ORDER.index(class_name) if class_name in PROTAGONIST_CLASS_ORDER else 0
    prot_id = f"PROT-{(r_idx * 6 + c_idx + 1):02d}"

    r_slug = PROTAGONIST_RACE_SLUGS.get(race_name, "humano")
    c_slug = PROTAGONIST_CLASS_SLUGS.get(class_name, "guerreiro")
    sprite_filename = f"{r_slug}_{c_slug}_{gender}.png"
    sprite_path = f"assets/sprites/heroes/{sprite_filename}"
    icon_path = f"assets/sprites/heroes/icones/{sprite_filename}"

    return {
        "prot_id": prot_id,
        "gender": gender,
        "symbol": symbol,
        "label": label,
        "gender_label": label,
        "class_display": class_display,
        "sprite_filename": sprite_filename,
        "sprite_path": sprite_path,
        "icon_path": icon_path
    }

RACAS_5E = {
    "Humano": {
        "atributos": {"Força": 1, "Destreza": 1, "Constituição": 1, "Inteligência": 1, "Sabedoria": 1, "Carisma": 1},
        "bonus": {"FOR": 1, "DES": 1, "CON": 1, "INT": 1, "SAB": 1, "CAR": 1},
        "deslocamento_m": 9.0,
        "speed": 9.0,
        "tamanho": "Médio",
        "idiomas": ["Comum", "Escolha 1"],
        "habilidades_raciais": ["Versatilidade Humana"],
        "descricao_ui": "A raça mais versátil e adaptável, capaz de preencher qualquer lacuna no grupo com facilidade e determinação."
    },
    "Halfling": {
        "atributos": {"Força": 0, "Destreza": 2, "Constituição": 0, "Inteligência": 0, "Sabedoria": 0, "Carisma": 1},
        "bonus": {"FOR": 0, "DES": 2, "CON": 0, "INT": 0, "SAB": 0, "CAR": 1},
        "deslocamento_m": 7.5,
        "speed": 7.5,
        "tamanho": "Pequeno",
        "idiomas": ["Comum", "Halfling"],
        "habilidades_raciais": ["Sorte", "Bravura", "Agilidade Halfling", "Furtividade Natural"],
        "descricao_ui": "Pequenos e furtivos, abençoados com uma sorte sobrenatural que os permite escapar de perigos quase certos."
    },
    "Draconato": {
        "atributos": {"Força": 2, "Destreza": 0, "Constituição": 0, "Inteligência": 0, "Sabedoria": 0, "Carisma": 1},
        "bonus": {"FOR": 2, "DES": 0, "CON": 0, "INT": 0, "SAB": 0, "CAR": 1},
        "deslocamento_m": 9.0,
        "speed": 9.0,
        "tamanho": "Médio",
        "idiomas": ["Comum", "Dracônico"],
        "habilidades_raciais": ["Ancestral Dracônico", "Arma de Sopro", "Resistência a Dano"],
        "descricao_ui": "Guerreiros imponentes de herança dracônica, capazes de exalar pura energia elemental para devastar seus inimigos."
    },
    "Meio-Orc": {
        "atributos": {"Força": 2, "Destreza": 0, "Constituição": 1, "Inteligência": 0, "Sabedoria": 0, "Carisma": 0},
        "bonus": {"FOR": 2, "DES": 0, "CON": 1, "INT": 0, "SAB": 0, "CAR": 0},
        "deslocamento_m": 9.0,
        "speed": 9.0,
        "tamanho": "Médio",
        "idiomas": ["Comum", "Orc"],
        "habilidades_raciais": ["Visão no Escuro", "Ameaçador", "Tolerância Infindável", "Ataques Selvagens"],
        "descricao_ui": "Brutos implacáveis forjados para a linha de frente, absorvendo ferimentos mortais e revidando com fúria devastadora."
    },
    "Tiefling": {
        "atributos": {"Força": 0, "Destreza": 0, "Constituição": 0, "Inteligência": 1, "Sabedoria": 0, "Carisma": 2},
        "bonus": {"FOR": 0, "DES": 0, "CON": 0, "INT": 1, "SAB": 0, "CAR": 2},
        "deslocamento_m": 9.0,
        "speed": 9.0,
        "tamanho": "Médio",
        "idiomas": ["Comum", "Infernal"],
        "habilidades_raciais": ["Visão no Escuro", "Resistência Infernal", "Legado Infernal"],
        "descricao_ui": "Herdeiros de uma linhagem infernal, combinando resistência sobrenatural com truques e magias arcanas inatas."
    },
    "Anão da Colina": {
        "atributos": {"Força": 0, "Destreza": 0, "Constituição": 2, "Inteligência": 0, "Sabedoria": 1, "Carisma": 0},
        "bonus": {"FOR": 0, "DES": 0, "CON": 2, "INT": 0, "SAB": 1, "CAR": 0},
        "deslocamento_m": 7.5,
        "speed": 7.5,
        "tamanho": "Médio",
        "idiomas": ["Comum", "Anão"],
        "habilidades_raciais": ["Visão no Escuro", "Resiliência Anã", "Treinamento Anão em Combate", "Tenacidade Anã"],
        "descricao_ui": "Mestres da pedra e da forja, conhecidos por sua resiliência inabalável, vigor insuperável e estoicismo diante do perigo."
    },
    "Elfo da Floresta": {
        "atributos": {"Força": 0, "Destreza": 2, "Constituição": 0, "Inteligência": 0, "Sabedoria": 1, "Carisma": 0},
        "bonus": {"FOR": 0, "DES": 2, "CON": 0, "INT": 0, "SAB": 1, "CAR": 0},
        "deslocamento_m": 10.5,
        "speed": 10.5,
        "tamanho": "Médio",
        "idiomas": ["Comum", "Élfico"],
        "habilidades_raciais": ["Visão no Escuro", "Sentidos Aguçados", "Ancestralidade Feérica", "Transe", "Treinamento Élfico com Armas", "Pés Ligeiros"],
        "descricao_ui": "Seres graciosos e antigos, dotados de sentidos sobrenaturais, reflexos impecáveis e uma conexão profunda com o mundo natural."
    }
}

# Aliases de compatibilidade para consultas canônicas
RACAS_5E["Elfo"] = RACAS_5E["Elfo da Floresta"]
RACAS_5E["Anão"] = RACAS_5E["Anão da Colina"]
RACAS_5E["Anao"] = RACAS_5E["Anão da Colina"]

def get_racial_bonus(race_name: str) -> dict:
    """
    Retorna o bônus racial estruturado de atributos padronizado para FOR, DES, CON, INT, SAB, CAR.
    Ex: get_racial_bonus('Humano') -> {'FOR': 1, 'DES': 1, 'CON': 1, 'INT': 1, 'SAB': 1, 'CAR': 1}
    """
    if not race_name:
        return {"FOR": 0, "DES": 0, "CON": 0, "INT": 0, "SAB": 0, "CAR": 0}
    r = RACAS_5E.get(race_name)
    if not r:
        r_low = race_name.lower().strip()
        for k, v in RACAS_5E.items():
            if k.lower() == r_low or r_low in k.lower() or k.lower() in r_low:
                r = v
                break
    if r and "bonus" in r:
        return r["bonus"].copy()
    return {"FOR": 0, "DES": 0, "CON": 0, "INT": 0, "SAB": 0, "CAR": 0}

def get_racial_speed(race_name: str) -> float:
    """
    Retorna o deslocamento racial oficial do D&D 5e em metros:
    - Elfo (Elfo da Floresta): 10.5m
    - Humano, Draconato, Meio-Orc, Tiefling: 9.0m
    - Anão (Anão da Colina), Halfling: 7.5m
    """
    if not race_name:
        return 9.0
    r = RACAS_5E.get(race_name)
    if not r:
        r_low = race_name.lower().strip()
        for k, v in RACAS_5E.items():
            if k.lower() == r_low or r_low in k.lower() or k.lower() in r_low:
                r = v
                break
    if r and "deslocamento_m" in r:
        return float(r["deslocamento_m"])
    return 9.0


EQUIPAMENTOS_5E = {
    "Guerreiro": {"iniciais": ["Cota de Malha", "Espada Longa", "Escudo de Carvalho", "Besta Leve", "Pacote de Aventureiro"]},
    "Ladino": {"iniciais": ["Armadura de Couro", "Rapieira de Duelo", "Adaga de Caça", "Arco Curto", "Pacote de Ladrão"]},
    "Mago": {"iniciais": ["Túnica Arcana", "Bordão de Carvalho", "Grimório de Magias", "Pacote de Estudioso"]},
    "Paladino": {"iniciais": ["Cota de Malha", "Espada Longa", "Escudo de Carvalho", "Símbolo Sagrado", "Pacote de Explorador"]},
    "Clérigo": {"iniciais": ["Peitoral de Aço", "Maça Flangeada", "Escudo de Carvalho", "Símbolo Sagrado", "Pacote de Sacerdote"]},
    "Patrulheiro": {"iniciais": ["Armadura de Couro", "Arco Longo de Teixo", "Espada Curta", "Pacote de Explorador"]}
}

CLASSES = {
    "Guerreiro": {
        "pv_base": 10,
        "dado_vida": 10,
        "proficiencias_resistencia": ["Força", "Constituição"],
        "proficiencias_pericias_qtd": 2,
        "pericias_opcoes": ["Acrobacia", "Adestrar Animais", "Atletismo", "História", "Intimidação", "Intuição", "Percepção", "Sobrevivência"],
        "proficiencias_equipamento": ["Armas simples", "Armas marciais"],
        "proficiencias_armaduras": ["Todas as armaduras", "Escudos"],
        "habilidades_nv1": ["Estilo de Luta", "Retomar o Fôlego"],
        "descricao_ui": "Mestres absolutos do combate marcial, treinados em todas as armas e armaduras para dominar o campo de batalha com pura excelência física."
    },
    "Clérigo": {
        "pv_base": 8,
        "dado_vida": 8,
        "proficiencias_resistencia": ["Sabedoria", "Carisma"],
        "proficiencias_pericias_qtd": 2,
        "pericias_opcoes": ["História", "Intuição", "Medicina", "Persuasão", "Religião"],
        "proficiencias_equipamento": ["Armas simples"],
        "proficiencias_armaduras": ["Armaduras leves", "Armaduras médias", "Escudos"],
        "habilidades_nv1": ["Conjuração", "Domínio Divino"],
        "magias_iniciais": ["Truque: Chama Sagrada", "Magia: Curar Ferimentos", "Magia: Raio Guiador", "Magia: Escudo da Fé"],
        "descricao_ui": "Sacerdotes devotos que empunham o poder dos deuses, combinando magias milagrosas de suporte com formidável proteção divina."
    },
    "Paladino": {
        "pv_base": 10,
        "dado_vida": 10,
        "proficiencias_resistencia": ["Sabedoria", "Carisma"],
        "proficiencias_pericias_qtd": 2,
        "pericias_opcoes": ["Atletismo", "Intimidação", "Intuição", "Medicina", "Persuasão", "Religião"],
        "proficiencias_equipamento": ["Todas as armaduras", "Escudos", "Armas simples", "Armas marciais"],
        "proficiencias_armaduras": ["Todas as armaduras", "Escudos"],
        "habilidades_nv1": ["Sentido Divino", "Cura pelas Mãos"],
        "magias_iniciais": ["Magia: Proteção contra o Mal e Bem", "Magia: Duelo Compelido"],
        "descricao_ui": "Guerreiros sagrados unidos por um juramento divino, misturando combate corpo a corpo brutal com magia curativa e proteção celestial."
    },
    "Mago": {
        "pv_base": 6,
        "dado_vida": 6,
        "proficiencias_resistencia": ["Inteligência", "Sabedoria"],
        "proficiencias_pericias_qtd": 2,
        "pericias_opcoes": ["Arcanismo", "História", "Intuição", "Investigação", "Medicina", "Religião"],
        "proficiencias_equipamento": ["Adagas", "Dardos", "Fundas", "Bordões", "Bestas leves"],
        "proficiencias_armaduras": ["Nenhuma"],
        "habilidades_nv1": ["Conjuração", "Recuperação Arcana"],
        "magias_iniciais": ["Truque: Raio de Fogo", "Truque: Mãos Mágicas", "Magia: Mísseis Mágicos", "Magia: Armadura Arcana", "Magia: Escudo Arcano"],
        "descricao_ui": "Estudiosos arcanos que manipulam a malha da realidade, utilizando poderosos grimórios para conjurar magias devastadoras."
    },
    "Patrulheiro": {
        "pv_base": 10,
        "dado_vida": 10,
        "proficiencias_resistencia": ["Força", "Destreza"],
        "proficiencias_pericias_qtd": 3,
        "pericias_opcoes": ["Adestrar Animais", "Atletismo", "Furtividade", "Intuição", "Investigação", "Natureza", "Percepção", "Sobrevivência"],
        "proficiencias_equipamento": ["Armas simples", "Armas marciais"],
        "proficiencias_armaduras": ["Armaduras leves", "Armaduras médias", "Escudos"],
        "habilidades_nv1": ["Marca do Caçador", "Passo Leve"],
        "descricao_ui": "Mestres da arquearia e rastreamento. Marcando seus alvos para ataques letais, eles ditam o ritmo do combate à distância."
    },
    "Ladino": {
        "pv_base": 8,
        "dado_vida": 8,
        "proficiencias_resistencia": ["Destreza", "Inteligência"],
        "proficiencias_pericias_qtd": 4,
        "pericias_opcoes": ["Acrobacia", "Atletismo", "Enganação", "Furtividade", "Intimidação", "Intuição", "Investigação", "Percepção", "Persuasão", "Prestidigitação"],
        "proficiencias_equipamento": ["Armas simples", "Bestas de mão", "Espadas longas", "Rapieiras", "Espadas curtas"],
        "proficiencias_armaduras": ["Armaduras leves"],
        "habilidades_nv1": ["Especialização", "Ataque Furtivo", "Gíria de Ladrão"],
        "descricao_ui": "Especialistas em furtividade e precisão cirúrgica, atacando onde o inimigo é mais vulnerável."
    }
}

ANTECEDENTES_5E = {
    "Herói": {
        "descricao_ui": "Você vem da lama e da pobreza. Não é um lorde ou guerreiro treinado, mas quando a tragédia bateu à porta, você ergueu sua ferramenta de trabalho como arma. O povo confia em você, mas a nobreza o despreza.",
        "proficiencias": ["Lidar com Animais", "Sobrevivência"],
        "equipamento": ["Ferramenta de artesão", "Pá velha", "Roupas rasgadas", "Bolsa com 10 po"],
        "trunfo_narrativo": "Abrigo Rústico: Camponeses e plebeus oferecerão comida e um lugar seguro para dormir, desde que você não traga perigo direto para suas famílias."
    },
    "Criminoso": {
        "descricao_ui": "Você sobreviveu nas sarjetas quebrando a lei. Conhece becos escuros, informantes e o gosto do sangue por algumas moedas. A moralidade é um luxo que você nunca pôde pagar.",
        "proficiencias": ["Enganação", "Furtividade"],
        "equipamento": ["Pé de cabra", "Roupas escuras com capuz", "Ferramentas de ladrão", "Bolsa com 15 po"],
        "trunfo_narrativo": "Contato Criminal: Você possui um informante confiável no submundo local que pode repassar mensagens ou contrabandear itens menores."
    },
    "Soldado": {
        "descricao_ui": "Você marchou em batalhas esquecidas e viu amigos morrerem na lama. A disciplina militar e o trauma da guerra estão marcados na sua postura e nas suas cicatrizes.",
        "proficiencias": ["Atletismo", "Intimidação"],
        "equipamento": ["Insígnia de patente quebrada", "Dado de osso (jogo)", "Roupas comuns", "Bolsa com 10 po"],
        "trunfo_narrativo": "Respeito Militar: Guardas e milícias tendem a tratá-lo com camaradagem básica e podem fechar os olhos para infrações menores, reconhecendo sua patente."
    },
    "Acólito": {
        "descricao_ui": "Você passou a vida em templos isolados, estudando dogmas e ritos sombrios. Sua fé não é brilhante e milagrosa, mas uma busca desesperada por luz em um mundo apodrecido.",
        "proficiencias": ["Intuição", "Religião"],
        "equipamento": ["Símbolo sagrado manchado", "Livro de orações desgastado", "Vestes litúrgicas", "Bolsa com 15 po"],
        "trunfo_narrativo": "Abrigo da Fé: Você e seus aliados podem receber cura básica (não-mágica) e estadia gratuita em templos ou santuários da sua ordem."
    },
    "Sábio": {
        "descricao_ui": "Enquanto outros lutavam com espadas, você devorava pergaminhos empoeirados. Você busca verdades perigosas e segredos arcanos que a maioria prefere esquecer.",
        "proficiencias": ["Arcanismo", "História"],
        "equipamento": ["Tinteiro e pena", "Faca pequena para pergaminhos", "Carta de um colega morto", "Bolsa com 10 po"],
        "trunfo_narrativo": "Pesquisador Obsessivo: Se você não sabe uma informação histórica ou arcana, você geralmente sabe onde ou com quem encontrar a resposta."
    },
    "Nobre": {
        "descricao_ui": "O sangue azul corre em suas veias. Você foi criado com riqueza e privilégios, mas a queda da sua Casa ou uma desgraça pessoal o jogou na mesma lama que os plebeus.",
        "proficiencias": ["História", "Persuasão"],
        "equipamento": ["Anel de sinete da família", "Pergaminho de linhagem", "Roupas finas e sujas", "Bolsa com 25 po"],
        "trunfo_narrativo": "Posição de Privilégio: Você consegue audiências com nobres, burocratas e mercadores de alto escalão usando seu nome, mesmo que esteja em desgraça."
    }
}

TENDENCIAS_5E = {
    "Leal e Bom": {"descricao_ui": "Faz o que é esperado pela sociedade e pelas leis visando sempre o bem comum e a proteção dos mais fracos."},
    "Neutro e Bom": {"descricao_ui": "Faz o melhor que pode para ajudar os outros, de acordo com as necessidades do momento, sem apego excessivo a regras."},
    "Caótico e Bom": {"descricao_ui": "Age de acordo com a própria consciência, com pouca consideração por expectativas da sociedade, focando no bem maior."},
    "Leal e Neutro": {"descricao_ui": "Acredita na lei, na ordem, em tradições e em um código de conduta pessoal absoluto acima do moralismo de bem ou mal."},
    "Neutro": {"descricao_ui": "Prefere manter-se distante de questões morais, não se sentindo impelido a tomar um lado sem motivo ou lucro justificável."},
    "Caótico e Neutro": {"descricao_ui": "Segue seus caprichos, valorizando a própria liberdade acima de tudo, não se importando em proteger ou ferir os outros."},
    "Leal e Mau": {"descricao_ui": "Tira metodicamente o que quer, dentro dos limites do seu código de conduta, ignorando danos colaterais ou crueldade."},
    "Neutro e Mau": {"descricao_ui": "É focado apenas em si mesmo e fará qualquer coisa para conseguir o que quer sem compaixão ou arrependimentos."},
    "Caótico e Mau": {"descricao_ui": "Sua motivação vem da ganância arbitrária, ódio ou puro desejo de destruição desprovido de qualquer código."}
}

class CharacterCalculator:
    """Calcula a ficha derivada sempre que Raça/Classe/Atributos mudarem."""

    @staticmethod
    def calculate_derived_stats(base_attrs: dict, race_name: str = None, class_name: str = None, background_name: str = "") -> dict:
        """
        Retorna um dicionário com os status finais processados:
        - attributes finais (com bônus racial em PT e EN sincronizados)
        - hp_max
        - ac (Classe de Armadura)
        - initiative
        - speed
        - equipment (lista com Armadura, Arma, Item Único Racial e extras)
        - abilities (lista)
        - prot_id, gender, gender_symbol, gender_label, class_display
        - sprite_filename, sprite_path, icon_path
        Suporta chamada com (char_data: dict) ou (base_attrs, race_name, class_name, background_name).
        """
        is_char_dict_call = False
        char_ref = None
        if race_name is None and class_name is None and isinstance(base_attrs, dict) and (
            "race" in base_attrs or "class" in base_attrs or "attributes" in base_attrs
        ):
            is_char_dict_call = True
            char_ref = base_attrs
            race_name = char_ref.get("race", "Humano")
            class_name = char_ref.get("class", "Guerreiro")
            background_name = char_ref.get("background", "")
            raw_attrs = char_ref.get("attributes", {})
        else:
            raw_attrs = base_attrs if isinstance(base_attrs, dict) else {}
            race_name = race_name or "Humano"
            class_name = class_name or "Guerreiro"

        # Sincroniza chaves PT e EN caso uma delas tenha sido atualizada
        synced_input = sync_attributes_dict(raw_attrs.copy()) if raw_attrs else {}
        six_pt = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]

        if (not raw_attrs or
                raw_attrs.get("use_class_array") or
                all(synced_input.get(k, 10) == 10 for k in six_pt)):
            final_attrs = get_class_base_attributes(class_name)
            apply_racial = True
        else:
            final_attrs = synced_input
            # Se for chamada direta em char_data já criado (ex: após Level Up), não soma bônus racial duplicado
            apply_racial = not (is_char_dict_call and char_ref.get("_racial_applied", False))
            if is_char_dict_call and char_ref.get("level", 1) > 1:
                apply_racial = False

        speed = "9m"
        traits = []

        if race_name in RACAS_5E:
            r5 = RACAS_5E[race_name]
            speed = f"{r5.get('deslocamento_m', 9.0)}m"
            traits = r5.get("habilidades_raciais", [])
            if apply_racial:
                if "bonus" in r5:
                    pt_to_en = {"FOR": "STR", "DES": "DEX", "CON": "CON", "INT": "INT", "SAB": "WIS", "CAR": "CHA"}
                    for pt_k, b_val in r5["bonus"].items():
                        en_k = pt_to_en.get(pt_k, pt_k)
                        val = final_attrs.get(pt_k, final_attrs.get(en_k, 10)) + b_val
                        final_attrs[pt_k] = val
                        final_attrs[en_k] = val
                else:
                    map_raca = {
                        "Força": ("FOR", "STR"),
                        "Destreza": ("DES", "DEX"),
                        "Constituição": ("CON", "CON"),
                        "Inteligência": ("INT", "INT"),
                        "Sabedoria": ("SAB", "WIS"),
                        "Carisma": ("CAR", "CHA")
                    }
                    for pt_full, (pt_short, en_short) in map_raca.items():
                        bonus = r5.get("atributos", {}).get(pt_full, 0)
                        val = final_attrs.get(pt_short, final_attrs.get(en_short, 10)) + bonus
                        final_attrs[pt_short] = val
                        final_attrs[en_short] = val


        sync_attributes_dict(final_attrs)

        dex_mod = get_modifier(final_attrs.get("DES", 10))
        con_mod = get_modifier(final_attrs.get("CON", 10))

        class_data = CLASSES.get(class_name, {})
        hp_base = class_data.get("pv_base", class_data.get("hp_base", 8))
        class_abilities = class_data.get("habilidades_nv1", class_data.get("abilities", [])).copy()
        class_abilities.extend(class_data.get("magias_iniciais", []))

        hp_max = hp_base + con_mod
        # Tenacidade Anã (+1 PV por nível)
        if race_name == "Anão da Colina":
            hp_max += 1

        # Equipamentos Iniciais da Classe + Item Único Racial na 3ª posição (índice 2)
        base_eq = []
        if class_name in EQUIPAMENTOS_5E:
            base_eq = EQUIPAMENTOS_5E[class_name].get("iniciais", []).copy()
        else:
            base_eq = ["Roupas Comuns", "Adaga de Caça"]

        racial_item = ITENS_UNICOS_RACIAIS.get(race_name, {
            "id": "i_racial_human_signet",
            "name": "Sinete da Coroa Partida"
        })
        racial_item_name = racial_item["name"]

        equipped_armor = base_eq[0] if len(base_eq) > 0 else "Roupas Comuns"
        equipped_weapon = base_eq[1] if len(base_eq) > 1 else "Adaga de Caça"

        equipment = [equipped_armor, equipped_weapon, racial_item_name]
        if len(base_eq) > 2:
            equipment.extend(base_eq[2:])

        # Cálculo estrito de CA usando ARMADURAS_5E
        ac = 10 + dex_mod
        shield_bonus = 0
        has_shield = False

        for item in equipment:
            item_lower = item.lower()
            if "escudo" in item_lower:
                shield_bonus = max(shield_bonus, ARMADURAS_5E.get("escudo", {"ca_bonus": 2})["ca_bonus"])
                has_shield = True
            elif item_lower in ARMADURAS_5E:
                armadura = ARMADURAS_5E[item_lower]
                base = armadura["ca_base"]
                if armadura["soma_des"]:
                    limit = armadura["limite_des"]
                    if limit is not None:
                        base += min(limit, dex_mod)
                    else:
                        base += dex_mod
                ac = base

        ac += shield_bonus

        # Aplicação de Bônus Mecânicos do Item Único Racial
        hp_max += racial_item.get("hp_max_bonus", 0)
        ac += racial_item.get("ac_bonus", 0)
        initiative = dex_mod + racial_item.get("initiative_bonus", 0)
        gold = 15 + racial_item.get("gold_bonus", 0)
        if racial_item.get("luck_bonus") and apply_racial:
            final_attrs["LUCK"] = final_attrs.get("LUCK", 10) + racial_item["luck_bonus"]

        abilities = traits + class_abilities
        proficiencies = class_data.get("proficiencias_equipamento", []) + class_data.get("proficiencias_armaduras", [])

        qtd_pericias = class_data.get("proficiencias_pericias_qtd", 0)
        opcoes_pericias = class_data.get("pericias_opcoes", [])
        if qtd_pericias > 0 and opcoes_pericias:
            proficiencies.extend(opcoes_pericias[:qtd_pericias])

        if background_name in ANTECEDENTES_5E:
            bg_data = ANTECEDENTES_5E[background_name]
            equipment.extend(bg_data.get("equipamento", bg_data.get("equipamento_extra", [])))
            if "trunfo_narrativo" in bg_data:
                abilities.append(bg_data["trunfo_narrativo"])
            proficiencies.extend(bg_data.get("proficiencias", []))

        gender_info = get_protagonist_gender_info(race_name, class_name)

        # Inicialização oficial 5e de unlocked_skills no Nível 1 por Classe
        class_initial_skills_map = {
            "Guerreiro": ["second_wind", "sk_warrior_1"],
            "Clérigo": ["disciple_of_life", "sk_cleric_1"],
            "Paladino": ["lay_on_hands", "sk_paladin_1"],
            "Mago": ["arcane_recovery", "sk_mage_1"],
            "Patrulheiro": ["favored_enemy", "sk_ranger_1"],
            "Ladino": ["sneak_attack", "sk_rogue_1"],
        }
        initial_skills = list(class_initial_skills_map.get(class_name, []))

        existing_unlocked = []
        if is_char_dict_call and isinstance(char_ref, dict) and "unlocked_skills" in char_ref and char_ref["unlocked_skills"]:
            existing_unlocked = list(char_ref.get("unlocked_skills") or [])
        elif isinstance(base_attrs, dict) and "unlocked_skills" in base_attrs and base_attrs["unlocked_skills"]:
            existing_unlocked = list(base_attrs.get("unlocked_skills") or [])

        unlocked_skills = list(existing_unlocked)
        for sk in initial_skills:
            if sk not in unlocked_skills:
                unlocked_skills.append(sk)

        result = {
            "attributes": final_attrs,
            "hp_max": max(1, hp_max),
            "ac": ac,
            "ca": ac,
            "initiative": initiative,
            "speed": speed,
            "speed_m": float(str(speed).replace("m", "")),
            "equipment": equipment,
            "equipped_armor": equipped_armor,
            "equipped_weapon": equipped_weapon,
            "equipped_accessory": racial_item_name,
            "has_shield": has_shield,
            "abilities": abilities,
            "proficiencies": proficiencies,
            "unlocked_skills": unlocked_skills,
            "level": 1,
            "xp": 0,
            "xp_to_next_level": 300,
            "proficiency_bonus": 2,
            "gold": gold,
            "has_pending_level_up": False,
            "prot_id": gender_info["prot_id"],
            "gender": gender_info["gender"],
            "gender_symbol": gender_info["symbol"],
            "gender_label": gender_info["label"],
            "class_display": gender_info["class_display"],
            "sprite_filename": gender_info["sprite_filename"],
            "sprite_path": gender_info["sprite_path"],
            "icon_path": gender_info["icon_path"],
            "_racial_applied": True
        }

        if is_char_dict_call and isinstance(char_ref, dict):
            char_ref["attributes"] = final_attrs
            char_ref["unlocked_skills"] = unlocked_skills
            for k in ["prot_id", "gender", "gender_symbol", "gender_label", "class_display", "sprite_filename", "sprite_path", "icon_path", "_racial_applied"]:
                char_ref[k] = result[k]
            for k, v in result.items():
                if k not in char_ref:
                    char_ref[k] = v
            char_ref["ca"] = char_ref.get("ac", ac)
            char_ref["ac"] = char_ref["ca"]
            return char_ref

        return result

    @staticmethod
    def apply_level_up(pc: dict) -> dict:
        """
        Aplica a progressão de Nível oficial do D&D 5e:
        - Aumento de Nível
        - Rolagem/Média fixa de PV baseado no Dado de Vida da classe + CON_mod (mínimo 1)
        - Atualização do Bônus de Proficiência (+2 níveis 1-4, +3 nível 5+)
        - Expansão de Spell Slots para conjuradores
        - Atualização do marco de XP para o próximo nível
        """
        XP_TABLE_5E = {
            1: 0,
            2: 300,
            3: 900,
            4: 2700,
            5: 6500,
            6: 14000,
            7: 23000,
            8: 34000
        }
        
        cur_level = pc.get("level", 1)
        next_level = cur_level + 1
        class_name = pc.get("class", "Guerreiro")
        class_data = CLASSES.get(class_name, {})
        dado_vida = class_data.get("dado_vida", 8)
        
        con_val = pc.get("attributes", {}).get("CON", 10)
        con_mod = get_modifier(con_val)
        base_pv_gain = (dado_vida // 2) + 1
        pv_gain = max(1, base_pv_gain + con_mod)
        
        pc["level"] = next_level
        pc["hp_max"] = pc.get("hp_max", 10) + pv_gain
        pc["hp_current"] = min(pc["hp_max"], pc.get("hp_current", 10) + pv_gain)
        
        prof_bonus = 2 if next_level < 5 else 3
        pc["proficiency_bonus"] = prof_bonus
        
        pc["xp_to_next_level"] = XP_TABLE_5E.get(next_level + 1, int(pc.get("xp_to_next_level", 300) * 2.2))
        pc["has_pending_level_up"] = pc.get("xp", 0) >= pc["xp_to_next_level"]
        
        slots_unlocked = {}
        if "spell_slots" in pc or class_name in ["Mago", "Clérigo", "Paladino", "Bruxo"]:
            slots = pc.setdefault("spell_slots", {"1": 2})
            if class_name in ["Mago", "Clérigo"]:
                if next_level == 2:
                    slots["1"] = max(slots.get("1", 0), 3)
                    slots_unlocked["1"] = 3
                elif next_level == 3:
                    slots["1"] = max(slots.get("1", 0), 4)
                    slots["2"] = max(slots.get("2", 0), 2)
                    slots_unlocked["2"] = 2
                elif next_level == 4:
                    slots["2"] = max(slots.get("2", 0), 3)
                    slots_unlocked["2"] = 3
                elif next_level >= 5:
                    slots["3"] = max(slots.get("3", 0), 2)
                    slots_unlocked["3"] = 2
            elif class_name == "Paladino":
                if next_level == 2:
                    slots["1"] = max(slots.get("1", 0), 2)
                    slots_unlocked["1"] = 2
                elif next_level == 3:
                    slots["1"] = max(slots.get("1", 0), 3)
                    slots_unlocked["1"] = 3
                elif next_level >= 5:
                    slots["2"] = max(slots.get("2", 0), 2)
                    slots_unlocked["2"] = 2
                    
        return {
            "new_level": next_level,
            "hp_gained": pv_gain,
            "hp_max": pc["hp_max"],
            "proficiency_bonus": prof_bonus,
            "slots_unlocked": slots_unlocked
        }

    @staticmethod
    def calculate_monster_loot(bestiary_id: str, bestiary_data: dict = None) -> dict:
        """
        Calcula o loot de ouro e possíveis itens concedidos pelo monstro.
        """
        import random
        if not bestiary_data:
            bestiary_data = {}
        cr_str = str(bestiary_data.get("cr", "1/4"))
        
        if cr_str in ["0", "1/8", "1/4"]:
            gold = random.randint(2, 8)
        elif cr_str in ["1/2", "1", "2"]:
            gold = random.randint(8, 25)
        elif cr_str in ["3", "4", "5"]:
            gold = random.randint(25, 75)
        elif cr_str in ["6", "7", "8", "9", "10"]:
            gold = random.randint(80, 200)
        else:
            gold = random.randint(200, 500)
            
        drop_item = None
        roll_drop = random.random()
        if roll_drop < 0.20:
            drop_item = "i_potion_healing"
        elif roll_drop < 0.35:
            drop_item = "i_rations"
            
        return {
            "gold": gold,
            "drop_item": drop_item
        }

BESTIARIO_5E = {
    # Criaturas Básicas e Lacaios
    "lacaio goblin": {
        "name": "Goblin",
        "ataques": [{"nome": "Cimitarra", "bonus_acerto": 4, "dano": "1d6+2"}],
        "categoria": "Lacaio", "tamanho": 1, "ca": 15, "pv_max": 7, "deslocamento_m": 9,
        "mods": {"FOR": -1, "DES": 2, "CON": 0, "INT": 0, "SAB": -1, "CAR": -1},
        "cr": "1/4", "xp": 50,
        "acoes": ["Cimitarra (+4, 1d6+2 cort)", "Arco Curto (+4, 1d6+2 perf)"],
        "regras_especiais": ["Fuga Ágil: Pode Desengajar como Ação Bônus."],
        "descricao": "Pequenos saqueadores cruéis que infestam cavernas úmidas e florestas esquecidas. Atacam em bandos desordenados, disparando flechas enferrujadas e cortando calcanhares antes de fugirem rindo pelas sombras.",
        "pontos_fortes": ["Fuga Ágil (Desengajar e Esconder como Ação Bônus)", "Alta mobilidade em terrenos fechados", "Ataques de emboscada à distância"],
        "fraquezas": ["Baixíssima vida total (7 PV)", "Moral frágil quando isolados do bando", "Vulneráveis a dano em área"]
    },
    "lacaio esqueleto": {
        "name": "Esqueleto",
        "ataques": [{"nome": "Arco Curto", "bonus_acerto": 4, "dano": "1d6+2"}, {"nome": "Espada Curta", "bonus_acerto": 4, "dano": "1d6+2"}],
        "categoria": "Lacaio", "tamanho": 1, "ca": 13, "pv_max": 13, "deslocamento_m": 9,
        "mods": {"FOR": 0, "DES": 2, "CON": 2, "INT": -2, "SAB": -1, "CAR": -3},
        "cr": "1/4", "xp": 50,
        "acoes": ["Espada Curta (+4, 1d6+2 perf)", "Arco Curto (+4, 1d6+2 perf)"],
        "regras_especiais": ["Vulnerável: Concussão", "Imune: Veneno/Envenenado"],
        "descricao": "Restos ressecados de guerreiros caídos, reanimados por profana magia necromântica. Seus ossos estalam enquanto empunham arcos e lâminas velhas com precisão impassível e incansável.",
        "pontos_fortes": ["Imunidade completa a veneno e envenenamento", "Precisão constante com arco e espada curta", "Imune a fadiga, medo e sangramento"],
        "fraquezas": ["Vulnerabilidade severa a dano de Concussão (martelos e maças estilhaçam sua estrutura)", "Ausência de criatividade tática"]
    },
    "lacaio zumbi": {
        "name": "Zumbi",
        "ataques": [{"nome": "Pancada", "bonus_acerto": 3, "dano": "1d6+1"}],
        "categoria": "Lacaio", "tamanho": 1, "ca": 8, "pv_max": 22, "deslocamento_m": 6,
        "mods": {"FOR": 1, "DES": -2, "CON": 3, "INT": -4, "SAB": -2, "CAR": -3},
        "cr": "1/4", "xp": 50,
        "acoes": ["Pancada (+3, 1d6+1 conc)"],
        "regras_especiais": ["Vontade de Ferro: Na primeira vez que cair a 0 PV, cai para 1 PV (ignora se for dano Radiante ou Crítico)."],
        "descricao": "Cadáveres putrefatos que avançam arrastando os pés e exalando o fedor pútrido da sepultura. Movidos por uma fome cega de carne viva, ignoram mutilações graves com tenacidade sobrenatural.",
        "pontos_fortes": ["Vontade de Ferro (resiste à morte na primeira queda a 0 PV)", "Boa reserva de vida para um lacaio (22 PV)", "Imunidade a veneno"],
        "fraquezas": ["Deslocamento reduzido (6m)", "Péssima Classe de Armadura (CA 8)", "Dano Radiante ou acertos críticos anulam sua resistência à morte"]
    },
    "lacaio orc": {
        "name": "Orc",
        "ataques": [{"nome": "Machado Grande", "bonus_acerto": 5, "dano": "1d12+3"}, {"nome": "Azagaia", "bonus_acerto": 5, "dano": "1d6+3"}],
        "categoria": "Lacaio", "tamanho": 1, "ca": 13, "pv_max": 15, "deslocamento_m": 9,
        "mods": {"FOR": 3, "DES": 1, "CON": 3, "INT": -2, "SAB": 0, "CAR": 0},
        "cr": "1/2", "xp": 100,
        "acoes": ["Machado Grande (+5, 1d12+3 cort)", "Azagaia (+5, 1d6+3 perf)"],
        "regras_especiais": ["Agressivo: Pode usar Ação Bônus para se mover 9m em direção ao inimigo."],
        "descricao": "Brutais guerreiros tribais que veneram o derramamento de sangue e a pura ferocidade física. Avançam berrando urros ensurdecedores, brandindo machados pesados capazes de partir escudos ao meio.",
        "pontos_fortes": ["Investida Agressiva como ação bônus", "Dano letal corpo a corpo (1d12+3)", "Elevada força e vigor físico"],
        "fraquezas": ["Baixa sabedoria e inteligência", "Suscetíveis a controle mental, ilusões e desorientação", "Comportamento previsível e impulsivo"]
    },
    "sub-chefe manticora": {
        "name": "Manticora",
        "ataques": [{"nome": "Mordida", "bonus_acerto": 5, "dano": "1d8+3"}, {"nome": "Espinho na Cauda", "bonus_acerto": 5, "dano": "1d8+3"}],
        "categoria": "Sub-Chefe", "tamanho": 1, "ca": 14, "pv_max": 68, "deslocamento_m": 9, "voo_m": 15,
        "mods": {"FOR": 3, "DES": 3, "CON": 3, "INT": -2, "SAB": 1, "CAR": -1},
        "cr": "3", "xp": 700,
        "acoes": ["Ataques Múltiplos: 1 Mordida e 2 Garras, OU 3 Espinhos", "Mordida (+5, 1d8+3 perf)", "Garra (+5, 1d6+3 cort)", "Espinho (+5, 1d8+3 perf, 30/60m)"],
        "descricao": "Uma quimera hedionda com corpo leonino musculoso, asas coriáceas de morcego e cauda repleta de puas perfurantes. Seu rosto quase humanoide ostenta fileiras de dentes afiados ávidos por carne fresca.",
        "pontos_fortes": ["Voo rápido e manobrável (15m)", "Saraivada de espinhos venenosos de longo alcance", "Ataques múltiplos em investidas aéreas"],
        "fraquezas": ["Mobilidade terrestre moderada", "Sem resistências a magias elementais", "Perde sua maior vantagem caso tenha as asas incapacitadas"]
    },
    "sub-chefe cria vampiro": {
        "name": "Cria de Vampiro",
        "ataques": [{"nome": "Mordida", "bonus_acerto": 6, "dano": "1d6+3"}, {"nome": "Garras", "bonus_acerto": 6, "dano": "2d4+3"}],
        "categoria": "Sub-Chefe", "tamanho": 1, "ca": 15, "pv_max": 82, "deslocamento_m": 9,
        "mods": {"FOR": 3, "DES": 3, "CON": 3, "INT": 0, "SAB": 0, "CAR": 1},
        "cr": "5", "xp": 1800,
        "acoes": ["Ataques Múltiplos: 2 ataques", "Garras (+6, 2d4+3 cort)", "Mordida Drenante (+6, 1d6+3 perf + 2d6 necrótico. O vampiro recupera PV igual ao dano necrótico)."],
        "regras_especiais": ["Resistência a ataques não mágicos."],
        "descricao": "Carniçais aristocráticos gerados pela maldição do sangue de um vampiro ancião. Escalam tetos e paredes na penumbra, lançando-se com unhas de ferro sobre as jugulares de quem ousa desbravar a noite.",
        "pontos_fortes": ["Mordida drenante que regenera seus próprios PV", "Resistência a armas mundanas", "Ataques múltiplos velozes e sentidos aguçados"],
        "fraquezas": ["Hipersensibilidade destrutiva à luz solar", "Extremamente vulnerável a dano Radiante e água benta", "Incapaz de curar após sofrer feitiços solares"]
    },
    "sub-chefe aparicao": {
        "name": "Aparição",
        "ataques": [{"nome": "Dreno de Vida", "bonus_acerto": 6, "dano": "4d8+3"}],
        "categoria": "Sub-Chefe", "tamanho": 2, "ca": 13, "pv_max": 67, "deslocamento_m": 0, "voo_m": 18,
        "mods": {"FOR": -2, "DES": 3, "CON": 3, "INT": 1, "SAB": 2, "CAR": 2},
        "cr": "5", "xp": 1800,
        "acoes": ["Drenar Vida (+6, 4d8+3 necrótico)."],
        "regras_especiais": ["Incorpóreo: Atravessa paredes.", "Imune a necrótico/veneno. Resistente a fogo/frio/trovejante."],
        "descricao": "Uma silhueta espectral envolta em farrapos sombrios flutuantes, emanando um frio que congela o ar ao redor. Seu toque gélido suga a essência vital, reduzindo heróis a carcaças murchas.",
        "pontos_fortes": ["Incorpóreo (atravessa paredes e terrenos sólidos)", "Dreno de vida massivo (4d8+3 necrótico)", "Resistências abundantes e imunidade a veneno e paralisia"],
        "fraquezas": ["Fraqueza à luz solar", "Sensível a dano Radiante e armas de prata abençoadas", "Incapaz de manipular fisicamente o ambiente"]
    },
    "sub-chefe quimera": {
        "name": "Quimera",
        "ataques": [{"nome": "Mordida", "bonus_acerto": 7, "dano": "2d6+4"}, {"nome": "Chifres", "bonus_acerto": 7, "dano": "1d12+4"}],
        "categoria": "Sub-Chefe", "tamanho": 2, "ca": 14, "pv_max": 114, "deslocamento_m": 9, "voo_m": 18,
        "mods": {"FOR": 4, "DES": 0, "CON": 4, "INT": -4, "SAB": 2, "CAR": 0},
        "cr": "4", "xp": 1100,
        "acoes": ["Ataques Múltiplos: Mordida, Chifres e Garras", "Mordida (+6, 2d6+4 perf)", "Chifres (+6, 1d12+4 conc)", "Sopro de Fogo (1 Uso por Combate: Cone 4,5m, TR DES CD 15, 7d8 fogo)"],
        "descricao": "Uma abominação profana que reúne as cabeças de um leão sanguinário, um bode furioso e um dragão vermelho sobre um torso leonino com asas de réptil. Destrói tropas inteiras com baforadas abrasadoras.",
        "pontos_fortes": ["Sopro de fogo mortal em cone (7d8 fogo)", "Três cabeças atacando simultaneamente com garras, dentes e chifres", "Voo intimidante e vida sólida (114 PV)"],
        "fraquezas": ["Vontades descoordenadas entre as cabeças se atordoada", "Sem resistências elementais a frio ou ácido", "Grande porte fácil de focar à distância"]
    },
    "Hidra": {
        "name": "Hidra",
        "ataques": [{"nome": "Mordida", "bonus_acerto": 8, "dano": "1d10+5"}],
        "categoria": "Chefe", "tamanho": 1, "ca": 15, "pv_max": 172, "deslocamento_m": 9,
        "mods": {"FOR": 5, "DES": 1, "CON": 5, "INT": -4, "SAB": 0, "CAR": -2},
        "cr": "8", "xp": 3900,
        "acoes": ["Mordida (+8, 1d10+5 perf)"],
        "regras_especiais": ["Fúria das Cabeças: Faz 3 ataques por turno. Se estiver com menos de 50% dos PV, passa a fazer 5 ataques por turno."],
        "descricao": "Um leviatã serpentino anfíbio das profundezas dos pântanos negros. Cada cabeça reage com reflexos predatórios instantâneos, tornando quase suicida qualquer combate corpo a corpo desprotegido.",
        "pontos_fortes": ["Fúria das Cabeças (até 5 ataques por turno ao ficar ferida)", "Reserva gigantesca de vida (172 PV)", "Múltiplas reações de oportunidade"],
        "fraquezas": ["Dano de fogo cauteriza suas carnes e impede regenerações", "Alcance estritamente corpo a corpo", "Reflexos mentais nulos contra controle de área"]
    },
    "Aboleth": {
        "name": "Aboleth",
        "ataques": [{"nome": "Tentáculo", "bonus_acerto": 9, "dano": "2d6+5"}],
        "categoria": "Chefe Supremo", "tamanho": 1, "ca": 17, "pv_max": 135, "deslocamento_m": 3, "natacao_m": 12,
        "mods": {"FOR": 5, "DES": -1, "CON": 2, "INT": 4, "SAB": 2, "CAR": 4},
        "cr": "10", "xp": 5900,
        "acoes": ["Ataques Múltiplos: 3 Tentáculos", "Tentáculo (+9, 2d6+5 conc. Alvo fica Envenenado por 1 turno).", "Escravizar (1 Uso por Combate): TR SAB CD 14 ou enfeitiçado."],
        "regras_especiais": ["Nuvem de Muco: Inimigos corpo a corpo sofrem 1d6 ácido ao atacá-lo."],
        "descricao": "Uma criatura primeva que rasteja pelos abismos aquáticos desde antes da ascensão dos mortais. Usa tentáculos cobertos por muco cáustico e poderes psíquicos para dobrar a mente de heróis à sua vontade.",
        "pontos_fortes": ["Domínio psíquico capaz de escravizar mentes mortais", "Nuvem de muco corrosivo contra atacantes adjacentes", "Excelente mobilidade e letalidade debaixo d'água"],
        "fraquezas": ["Movimentação terrestre lenta e arrastada (3m)", "Dependente de umidade constante para sobreviver", "Vulnerável a ataques elétricos concentrados"]
    },
    "Vampiro": {
        "name": "Vampiro",
        "ataques": [{"nome": "Ataque Desarmado", "bonus_acerto": 9, "dano": "1d8+4"}, {"nome": "Mordida", "bonus_acerto": 9, "dano": "1d6+4"}],
        "categoria": "Chefe Supremo", "tamanho": 1, "ca": 16, "pv_max": 144, "deslocamento_m": 9,
        "mods": {"FOR": 4, "DES": 4, "CON": 4, "INT": 3, "SAB": 2, "CAR": 4},
        "cr": "13", "xp": 10000,
        "acoes": ["Charme: TR SAB CD 17.", "Ataques Múltiplos: 2 Ataques Desarmados (+9, 1d8+4 conc).", "Mordida Drenante (+9, 1d6+4 perf + 3d6 necrótico. O vampiro recupera PV igual ao dano necrótico)."],
        "regras_especiais": ["Resistência Lendária (3 Usos por Combate): Passa num TR falho."],
        "descricao": "O senhor soberano da noite e das trevas. Elegante, imortal e despido de compaixão, comanda névoas e alcateias de lobos, regenerando-se instantaneamente a cada gota de sangue derramada.",
        "pontos_fortes": ["Resistência Lendária e regeneração contínua de ferimentos", "Charme hipnótico capaz de paralisar vontades fortes", "Alta mobilidade e dreno de vida voraz"],
        "fraquezas": ["Destruição fulminante sob luz solar real", "Dano Radiante e água benta suprimem sua regeneração", "Paralisado se transpassado por estaca de madeira no coração"]
    },
    "Lich": {
        "name": "Lich",
        "ataques": [{"nome": "Toque Paralisante", "bonus_acerto": 12, "dano": "3d6"}],
        "categoria": "Chefe Supremo", "tamanho": 1, "ca": 17, "pv_max": 135, "deslocamento_m": 9,
        "mods": {"FOR": 0, "DES": 3, "CON": 3, "INT": 5, "SAB": 2, "CAR": 3},
        "cr": "21", "xp": 33000,
        "acoes": ["Toque Paralisante (+12, 3d6 frio. TR CON CD 18 ou paralisa por 1 turno).", "Bola de Fogo (TR DES CD 18, 8d6 fogo)", "Palavra da Morte (1 Uso por Combate: Alvo com menos de 100 PV morre)."],
        "regras_especiais": ["Resistência Lendária (3 Usos por Combate)", "Imune a ataques não mágicos."],
        "descricao": "Um arquimago cadavérico que trocou sua mortalidade por conhecimento proibido eterno, encerrando sua alma em um filactério oculto. Seus olhos vazios queimam com brasas arcanas fulminantes.",
        "pontos_fortes": ["Magias arcanas apocalípticas (incluindo Palavra da Morte)", "Toque paralisante letal e Resistência Lendária", "Imunidade a armas não mágicas, veneno e paralisia"],
        "fraquezas": ["Sua alma permanece atada a um filactério vulnerável", "Físico relativamente frágil em combate direto prolongado", "Suscetível a magias de dispersão e campos de silêncio"]
    },
    "Sombra": {
        "name": "Sombra",
        "ataques": [{"nome": "Drenar Força", "bonus_acerto": 4, "dano": "2d6+2"}],
        "categoria": "Lacaio", "tamanho": 1, "ca": 12, "pv_max": 16, "deslocamento_m": 12,
        "mods": {"FOR": -2, "DES": 2, "CON": 1, "INT": -2, "SAB": 0, "CAR": -1},
        "cr": "1/2", "xp": 100,
        "acoes": ["Drenar Força (+4, 2d6+2 necrótico)."],
        "regras_especiais": ["Dreno de Atributo: Alvo perde 1d4 de Força (morre se chegar a 0).", "Furtividade Sombria: Esconder-se como Ação Bônus na penumbra.", "Desvantagem sob luz solar.", "Imune a necrótico/veneno. Resistente a não mágicos."],
        "descricao": "Contornos fantasmagóricos bidimensionais que rastejam pelas pedras das masmorras. Cada toque de seus dedos etéreos rouba a própria musculatura e vitalidade de guerreiros incautos.",
        "pontos_fortes": ["Dreno direto do atributo de Força do alvo", "Furtividade excepcional na escuridão", "Resistências abundantes a ataques físicos mundanos"],
        "fraquezas": ["Desvantagem direta e fraqueza sob luz solar", "Vulnerabilidade crítica a dano Radiante", "Vida baixa quando atingida por magia pura"]
    },
    "Kobold": {
        "name": "Kobold",
        "ataques": [{"nome": "Adaga", "bonus_acerto": 4, "dano": "1d4+2"}, {"nome": "Funda", "bonus_acerto": 4, "dano": "1d4+2"}],
        "categoria": "Lacaio", "tamanho": 1, "ca": 12, "pv_max": 5, "deslocamento_m": 9,
        "mods": {"FOR": -2, "DES": 2, "CON": -1, "INT": -1, "SAB": -2, "CAR": -1},
        "cr": "1/8", "xp": 25,
        "acoes": ["Adaga (+4, 1d4+2 perf)", "Funda (+4, 1d4+2 conc)"],
        "regras_especiais": ["Táticas de Matilha: Vantagem no ataque se houver um aliado a 1,5m do alvo."],
        "descricao": "Pequenos humanoides draconianos covardes e matreiros que se escondem nas frestas de minas profundas. Compensam sua fragilidade com emboscadas covardes e táticas de enxame.",
        "pontos_fortes": ["Táticas de Matilha (vantagem em ataques quando lutam em bando)", "Ataques de fustigamento com fundas e adagas", "Habilidade natural em túneis apertados"],
        "fraquezas": ["Sensibilidade visual à luz do sol", "Reserva de vida minúscula (5 PV)", "Desmoronam em pânico se isolados"]
    },
    "Rakshasa": {
        "name": "Rakshasa",
        "ataques": [{"nome": "Garras", "bonus_acerto": 7, "dano": "2d6+2"}],
        "categoria": "Subchefe", "tamanho": 1, "ca": 16, "pv_max": 110, "deslocamento_m": 12,
        "mods": {"FOR": 2, "DES": 3, "CON": 4, "INT": 1, "SAB": 3, "CAR": 5},
        "cr": "13", "xp": 10000,
        "acoes": ["Ataques Múltiplos: 2 Garras", "Garra (+7, 2d6+2 cort). Alvo amaldiçoado não recupera PV em descansos."],
        "regras_especiais": ["Imunidade Mágica: Imune a magias de 6º nível ou inferior.", "Vulnerável a perfurante mágico de criaturas Boas.", "Imune a ataques não mágicos."],
        "descricao": "Demônios refinados trajados em veludo e joias, ostentando cabeça de tigre e mãos invertidas. Manipulam reis e arruínam impérios inteiros pelas sombras através do engano e de garras amaldiçoadas.",
        "pontos_fortes": ["Imunidade mágica completa contra feitiços de 6º círculo ou menor", "Garras que amaldiçoam o descanso do herói", "Imunidade a armas não mágicas"],
        "fraquezas": ["Vulnerabilidade fatal a perfuração mágica de criaturas de alinhamento Bom", "Dependência do fator surpresa", "Orgulho desmedido"]
    },
    "Gigante do Fogo": {
        "name": "Gigante do Fogo",
        "ataques": [{"nome": "Espada Grande", "bonus_acerto": 11, "dano": "6d6+7"}, {"nome": "Rocha", "bonus_acerto": 11, "dano": "4d10+7"}],
        "categoria": "Subchefe", "tamanho": 2, "ca": 18, "pv_max": 162, "deslocamento_m": 9,
        "mods": {"FOR": 7, "DES": -1, "CON": 6, "INT": 0, "SAB": 2, "CAR": 1},
        "cr": "9", "xp": 5000,
        "acoes": ["Ataques Múltiplos: 2 ataques com Espadão", "Espadão (+11, 6d6+7 cort)", "Arremessar Rocha (+11, 4d10+7 conc, 18/72m)"],
        "regras_especiais": ["Imune a Fogo."],
        "descricao": "Ferreiros colossais encouraçados com placas de ferro forjado nas forjas vulcânicas do submundo. Empunham espadas monumentais com maestria militar calculada e impiedosa.",
        "pontos_fortes": ["Imunidade absoluta a dano de fogo", "Espadão brutal com dano devastador (6d6+7)", "Arremesso de rochas ciclópicas a distância"],
        "fraquezas": ["Vulnerabilidade pronunciada a ataques e magias de Gelo e Frio", "Baixa destreza e pouca agilidade contra testes de reflexo", "Alvo descomunal"]
    },
    "Kraken": {
        "name": "Kraken",
        "ataques": [{"nome": "Tentáculo", "bonus_acerto": 17, "dano": "3d6+10"}, {"nome": "Mordida", "bonus_acerto": 17, "dano": "3d8+10"}],
        "categoria": "Chefe Supremo", "tamanho": 3, "ca": 18, "pv_max": 472, "deslocamento_m": 6, "natacao_m": 18,
        "mods": {"FOR": 10, "DES": 0, "CON": 6, "INT": 6, "SAB": 4, "CAR": 5},
        "cr": "23", "xp": 32500,
        "acoes": ["Ataques Múltiplos: 3 Tentáculos (1 pode ser Mordida/Engolir).", "Tempestade de Raios"],
        "descricao": "O terror inominável que repousa nas fossas abissais do oceano. Desperta para arrastar frotas mercantes e fortalezas costeiras para o fundo do mar em meio a trovões titânicos.",
        "pontos_fortes": ["Força descomunal com múltiplos tentáculos esmagadores", "Convocar tempestades de raios elétricos", "Vida massiva (472 PV) e imunidades a condições"],
        "fraquezas": ["Incapaz de manter combate fora de águas profundas", "Silhueta imensa fácil de concentrar fogo e feitiços de longo alcance"]
    },
    # Criaturas Expandidas (Bestiário de Campanha & Side Quests)
    "m_dire_wolf": {
        "name": "Lobo Atroz",
        "ataques": [{"nome": "Mordida", "bonus_acerto": 5, "dano": "2d6+3"}],
        "categoria": "Fera", "tamanho": 2, "ca": 14, "pv_max": 37, "deslocamento_m": 15,
        "mods": {"FOR": 3, "DES": 2, "CON": 2, "INT": -4, "SAB": 1, "CAR": -2},
        "cr": "1", "xp": 200,
        "acoes": ["Mordida (+5, 2d6+3 perf. TR FOR CD 13 ou cai no chão)."],
        "descricao": "Predadores monstruosos maiores que corcéis de guerra, com presas que trituram osso como galhos secos. Suas pegadas congelam na neve enquanto caçam em matilhas implacáveis.",
        "pontos_fortes": ["Táticas de Matilha (vantagem em ataque quando luta ao lado de aliados)", "Capacidade de derrubar o alvo com sua mordida", "Excelente faro e audição"],
        "fraquezas": ["Ausência total de ataques à distância", "Vulnerável a fogo e controle de multidões", "Depende de espaço livre para avançar"]
    },
    "m_bandit": {
        "name": "Bandido",
        "ataques": [{"nome": "Cimitarra", "bonus_acerto": 3, "dano": "1d6+1"}],
        "categoria": "Humanoide", "tamanho": 1, "ca": 12, "pv_max": 11, "deslocamento_m": 9,
        "mods": {"FOR": 0, "DES": 1, "CON": 1, "INT": 0, "SAB": 0, "CAR": 0},
        "cr": "1/8", "xp": 25,
        "acoes": ["Cimitarra (+3, 1d6+1 cort)", "Besta Leve (+3, 1d8 perf)"],
        "descricao": "Mercenários desertores e foras da lei embrutecidos pela fome e pela miséria das guerras. Atacam caravanas em encruzilhadas desertas, cortando bolsas e gargantas sem piedade.",
        "pontos_fortes": ["Ataques rápidos e emboscadas em grupo", "Versatilidade entre armas brancas e bestas leves", "Conhecimento das rotas e esconderijos locais"],
        "fraquezas": ["Proteção leve (CA 12, 11 PV)", "Falta de disciplina sob pressão de magia pura", "Fugirão se seus líderes caírem rapidamente"]
    },
    "m_veteran": {
        "name": "Veterano",
        "ataques": [{"nome": "Espada Longa", "bonus_acerto": 5, "dano": "1d8+3"}],
        "categoria": "Humanoide", "tamanho": 1, "ca": 17, "pv_max": 58, "deslocamento_m": 9,
        "mods": {"FOR": 3, "DES": 1, "CON": 2, "INT": 0, "SAB": 0, "CAR": 0},
        "cr": "3", "xp": 700,
        "acoes": ["Ataques Múltiplos: 2 com Espada Longa e 1 com Espada Curta", "Espada Longa (+5, 1d8+3 cort)"],
        "descricao": "Guerreiros calejados por campanhas brutais em terra arrasada. Portam armadura de placas completa e empunham lâminas gastas com a precisão mecânica e fria de quem já enterrou centenas de homens.",
        "pontos_fortes": ["Alta Classe de Armadura (CA 17)", "Ataques múltiplos contundentes por turno", "Disciplina militar inabalável"],
        "fraquezas": ["Mobilidade reduzida pelo peso do aço", "Vulnerável a magias de calor no metal e dano elétrico", "Reflexos limitados contra testes de destreza"]
    },
    "m_ochre_jelly": {
        "name": "Geleia Ocre",
        "ataques": [{"nome": "Pseudópode", "bonus_acerto": 4, "dano": "2d6+2"}],
        "categoria": "Gosma", "tamanho": 2, "ca": 8, "pv_max": 45, "deslocamento_m": 3,
        "mods": {"FOR": 2, "DES": -2, "CON": 2, "INT": -5, "SAB": -2, "CAR": -5},
        "cr": "2", "xp": 450,
        "acoes": ["Pseudópode (+4, 2d6+2 conc + 1d6 ácido)"],
        "descricao": "Uma massa protoplasmática viscosa e amarelada que escorre silenciosamente pelos tetos e frestas de masmorras. Dissolve tecidos vivos e armaduras metálicas com ácido avassalador.",
        "pontos_fortes": ["Dano ácido corrosivo contínuo", "Divide-se em duas criaturas menores ao sofrer dano cortante ou elétrico", "Imunidade a ácido, paralisia e cegueira"],
        "fraquezas": ["Vulnerável a dano de fogo e frio", "Deslocamento extremamente lento (3m)", "Comportamento cego puramente instintivo"]
    },
    "m_giant_spider": {
        "name": "Aranha Gigante",
        "ataques": [{"nome": "Mordida", "bonus_acerto": 5, "dano": "1d8+3"}],
        "categoria": "Fera", "tamanho": 2, "ca": 14, "pv_max": 26, "deslocamento_m": 9,
        "mods": {"FOR": 2, "DES": 3, "CON": 1, "INT": -4, "SAB": 0, "CAR": -3},
        "cr": "1", "xp": 200,
        "acoes": ["Mordida (+5, 1d8+3 perf + 2d8 veneno)", "Disparar Teia (TR DES CD 12 ou fica impedido)"],
        "descricao": "Monstruosidades aracnídeas de oito patas peludas e olhos negros como azeviche. Constroem labirintos pegajosos em copas de árvores ou criptas esquecidas para capturar presas vivas.",
        "pontos_fortes": ["Teia paralisante de médio alcance", "Veneno potente na mordida que pode incapacitar a vítima", "Escalada perfeita em qualquer ângulo"],
        "fraquezas": ["Suas teias queimam instantaneamente ao contato com fogo", "Baixa blindagem corporal", "Vulnerável a concussão contundente direta"]
    },
    "m_ogre": {
        "name": "Ogro",
        "ataques": [{"nome": "Clava Grande", "bonus_acerto": 6, "dano": "2d8+4"}],
        "categoria": "Gigante", "tamanho": 2, "ca": 11, "pv_max": 59, "deslocamento_m": 12,
        "mods": {"FOR": 4, "DES": -1, "CON": 3, "INT": -3, "SAB": -2, "CAR": -2},
        "cr": "2", "xp": 450,
        "acoes": ["Clava Grande (+6, 2d8+4 conc)", "Azagaia (+6, 2d6+4 perf)"],
        "descricao": "Gigantescos trogloditas desajeitados, com dentes podres e barrigas inchadas de glutonaria. Brandem clavas feitas com troncos inteiros que esmagam cavaleiros e cavalos com igual facilidade.",
        "pontos_fortes": ["Dano brutal em acertos de clava grande (2d8+4)", "Grande quantidade de vida para seu nível (59 PV)", "Amplo alcance corporal"],
        "fraquezas": ["Classe de Armadura deplorável (CA 11)", "Extremamente tolo e vulnerável a ilusões e controle mental", "Facilmente mantido à distância por conjuradores"]
    },
    "m_ogre_brute": {
        "name": "Ogro Brutal",
        "ataques": [{"nome": "Machado Gigante", "bonus_acerto": 7, "dano": "3d8+5"}],
        "categoria": "Gigante", "tamanho": 2, "ca": 12, "pv_max": 80, "deslocamento_m": 12,
        "mods": {"FOR": 5, "DES": -1, "CON": 4, "INT": -3, "SAB": -1, "CAR": -2},
        "cr": "4", "xp": 1100,
        "acoes": ["Machado Gigante (+7, 3d8+5 cort)"],
        "descricao": "Um colosso entre os ogros, fortalecido por anos de matança contínua. Veste carcaças e placas enferrujadas e maneja um machado de carniceiro capaz de abrir fendas no chão.",
        "pontos_fortes": ["Ataques devastadores de alto dano físico (3d8+5)", "Reserva de vida massiva (80 PV)", "Fúria intimidante que quebra defesas"],
        "fraquezas": ["Baixa defesa contra ataques à distância", "Lentidão tática de raciocínio", "Previsível em combate"]
    },
    "m_animated_armor": {
        "name": "Armadura Animada",
        "ataques": [{"nome": "Pancada", "bonus_acerto": 4, "dano": "1d6+2"}],
        "categoria": "Constructo", "tamanho": 1, "ca": 18, "pv_max": 33, "deslocamento_m": 8,
        "mods": {"FOR": 2, "DES": 0, "CON": 1, "INT": -5, "SAB": -4, "CAR": -5},
        "cr": "1", "xp": 200,
        "acoes": ["Ataques Múltiplos: 2 Pancadas (+4, 1d6+2 conc)"],
        "descricao": "Uma armadura de placas desprovida de carne, animada por encantamentos de sentinela secular. Seus passos de ferro ecoam pesadamente enquanto avança incansável sobre invasores.",
        "pontos_fortes": ["Altíssima Classe de Armadura de placas (CA 18)", "Imunidades totais a veneno, sangramento, medo e cansaço", "Não necessita respirar nem dormir"],
        "fraquezas": ["Vulnerável a ataques e feitiços de choque elétrico", "Cega além de sua percepção às cegas", "Desativada em zonas de antimagia absoluta"]
    },
    "m_mimic": {
        "name": "Mímico",
        "ataques": [{"nome": "Pseudópode", "bonus_acerto": 5, "dano": "1d8+3"}],
        "categoria": "Monstruosidade", "tamanho": 1, "ca": 12, "pv_max": 58, "deslocamento_m": 5,
        "mods": {"FOR": 3, "DES": 1, "CON": 2, "INT": -3, "SAB": 1, "CAR": -1},
        "cr": "2", "xp": 450,
        "acoes": ["Pseudópode (+5, 1d8+3 conc + aderência)", "Mordida (+5, 1d8+3 perf + 1d8 ácido)"],
        "descricao": "Predadores metamorfos que assumem a textura perfeita de baús de madeira, portas talhadas ou estátuas antigas. Esperam o toque ganancioso de aventureiros para abrirem bocas cheias de dentes afiados.",
        "pontos_fortes": ["Camuflagem ilusória perfeita quando imóvel", "Aderência viscosa que prende armas e membros", "Ataque surpresa altamente letal"],
        "fraquezas": ["Baixa mobilidade quando revelado (5m)", "Vulnerável a feitiços e ataques à distância", "Ausência de defesas elementais especiais"]
    },
    "m_gargoyle": {
        "name": "Gárgula",
        "ataques": [{"nome": "Garras", "bonus_acerto": 4, "dano": "1d6+2"}],
        "categoria": "Elemental", "tamanho": 1, "ca": 15, "pv_max": 52, "deslocamento_m": 9, "voo_m": 18,
        "mods": {"FOR": 2, "DES": 0, "CON": 3, "INT": -2, "SAB": 0, "CAR": -2},
        "cr": "2", "xp": 450,
        "acoes": ["Ataques Múltiplos: 1 Mordida e 1 Garra", "Garras (+4, 1d6+2 cort)", "Mordida (+4, 1d6+2 perf)"],
        "descricao": "Monstros alados esculpidos em pedra maciça, guardando parapeitos e campanários de catedrais amaldiçoadas. Despertam com um silvo aterrorizante para mergulhar sobre intrusos.",
        "pontos_fortes": ["Resistência a dano físico cortante e perfurante não mágico", "Voo rápido e ágil (18m)", "Camuflagem perfeita quando posada em construções de pedra"],
        "fraquezas": ["Vulnerável a dano de Concussão pesada (marretas e martelos quebram a rocha)", "Sensível a feitiços de estilhaçamento e tremor sísmico"]
    },
    "m_supreme_dragon": {
        "name": "Dragão Supremo",
        "ataques": [{"nome": "Mordida", "bonus_acerto": 14, "dano": "2d10+8"}, {"nome": "Sopro de Cinzas", "bonus_acerto": 15, "dano": "8d8"}],
        "categoria": "Chefe Supremo", "tamanho": 3, "ca": 22, "pv_max": 300, "deslocamento_m": 12, "voo_m": 24,
        "mods": {"FOR": 8, "DES": 0, "CON": 7, "INT": 4, "SAB": 3, "CAR": 5},
        "cr": "24", "xp": 62000,
        "acoes": ["Sopro do Fim do Mundo (Cone mortal)", "Mordida Devastadora (+14, 2d10+8 perf)", "Garras Titânicas (+14, 2d6+8 cort)"],
        "regras_especiais": ["Armadura Absoluta: 99% de redução de dano sem o Orbe Quebra-Chamas.", "Ciclo do Tempo: O senhor do Loop Temporal."],
        "descricao": "O Tirano das Cinzas. Uma força cataclísmica encarnada em escamas de obsidiana impenetráveis e magma puro. Seu sopro incinera eras e sua vontade aprisiona o próprio fluxo do tempo no reino.",
        "pontos_fortes": ["Sopro cósmico de devastação total", "Carapaça primordial quase imune a dano sem o artefato sagrado", "Ataques múltiplos ciclópicos"],
        "fraquezas": ["Sua armadura se racha para CA 14 e 100 PV sob a ressonância do Orbe Quebra-Chamas", "Intervalo tático de recarga após iniciar o sopro supremo"]
    }
}

# Aliases de compatibilidade para buscas diretas por IDs canônicos m_* e nomes simplificados
_ALIASES_BESTIARIO = {
    "m_goblin": "lacaio goblin",
    "goblin": "lacaio goblin",
    "m_skeleton": "lacaio esqueleto",
    "skeleton": "lacaio esqueleto",
    "esqueleto": "lacaio esqueleto",
    "m_zombie": "lacaio zumbi",
    "m_zombie_fast": "lacaio zumbi",
    "zombie": "lacaio zumbi",
    "zumbi": "lacaio zumbi",
    "m_orc": "lacaio orc",
    "orc": "lacaio orc",
    "m_manticore": "sub-chefe manticora",
    "manticore": "sub-chefe manticora",
    "manticora": "sub-chefe manticora",
    "m_vampire_spawn": "sub-chefe cria vampiro",
    "cria de vampiro": "sub-chefe cria vampiro",
    "m_wraith": "sub-chefe aparicao",
    "wraith": "sub-chefe aparicao",
    "aparicao": "sub-chefe aparicao",
    "aparição": "sub-chefe aparicao",
    "m_chimera": "sub-chefe quimera",
    "chimera": "sub-chefe quimera",
    "quimera": "sub-chefe quimera",
    "hidra": "Hidra",
    "aboleth": "Aboleth",
    "vampiro": "Vampiro",
    "m_lich": "Lich",
    "lich": "Lich",
    "m_shadow": "Sombra",
    "sombra": "Sombra",
    "m_kobold": "Kobold",
    "kobold": "Kobold",
    "m_rakshasa": "Rakshasa",
    "rakshasa": "Rakshasa",
    "m_fire_giant": "Gigante do Fogo",
    "gigante do fogo": "Gigante do Fogo",
    "kraken": "Kraken",
    "lobo atroz": "m_dire_wolf",
    "bandido": "m_bandit",
    "veterano": "m_veteran",
    "geleia ocre": "m_ochre_jelly",
    "aranha gigante": "m_giant_spider",
    "ogro": "m_ogre",
    "ogro brutal": "m_ogre_brute",
    "armadura animada": "m_animated_armor",
    "mimico": "m_mimic",
    "mímico": "m_mimic",
    "gargula": "m_gargoyle",
    "gárgula": "m_gargoyle",
    "dragao supremo": "m_supreme_dragon",
    "dragão supremo": "m_supreme_dragon"
}

for _alias, _target in _ALIASES_BESTIARIO.items():
    if _target in BESTIARIO_5E and _alias not in BESTIARIO_5E:
        BESTIARIO_5E[_alias] = BESTIARIO_5E[_target]


def get_monster_bestiary_entry(monster_id: str) -> dict:
    """
    Retorna os dados enriquecidos de uma criatura para o Bestiário:
    - id
    - nome
    - descricao (texto evocativo Dark Fantasy)
    - pontos_fortes (lista de forças)
    - fraquezas (lista de fraquezas)
    - ca, pv_max, xp, ataques, acoes, regras_especiais
    """
    if not monster_id:
        return {}

    m_low = str(monster_id).lower().strip()
    
    # 1. Busca direta no BESTIARIO_5E
    if m_low in BESTIARIO_5E:
        entry = BESTIARIO_5E[m_low].copy()
        entry["id"] = monster_id
        entry["nome"] = entry.get("name", m_low.title())
        return entry

    # 2. Busca por alias ou chave parcial
    for k, v in BESTIARIO_5E.items():
        if k.lower() == m_low or k.lower().replace("m_", "") == m_low.replace("m_", ""):
            entry = v.copy()
            entry["id"] = monster_id
            entry["nome"] = entry.get("name", k.title())
            return entry

    # 3. Fallback genérico Dark Fantasy
    return {
        "id": monster_id,
        "nome": str(monster_id).replace("m_", "").replace("_", " ").title(),
        "ca": 12,
        "pv_max": 20,
        "xp": 50,
        "descricao": "Uma abominação das terras sombrias que espreita nas sombras do reino, pronta para emboscar os incautos.",
        "pontos_fortes": ["Sentidos aguçados na penumbra", "Instinto predatório cruel"],
        "fraquezas": ["Vulnerável a magia radiante e ataques concentrados"],
        "ataques": [{"nome": "Pancada", "bonus_acerto": 3, "dano": "1d6+1"}]
    }


ARMAS_5E = {
    "espada longa": {"dano": "1d8", "atributo": "FOR", "propriedades": ["versatil"]},
    "espada longa de aço forjado +1": {"dano": "1d8+1", "atributo": "FOR", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["versatil", "magica"]},
    "espada longa rúnica": {"dano": "1d8+1", "atributo": "FOR", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["versatil", "magica"]},
    "espada curta": {"dano": "1d6", "atributo": "DES", "propriedades": ["acuidade", "leve"]},
    "montante": {"dano": "2d6", "atributo": "FOR", "propriedades": ["pesada", "duas_maos"]},
    "espada grande": {"dano": "2d6", "atributo": "FOR", "propriedades": ["pesada", "duas_maos"]},
    "machado de guerra": {"dano": "1d12", "atributo": "FOR", "propriedades": ["pesada", "duas_maos"]},
    "montante de adamante das cinzas +1": {"dano": "2d6+1", "atributo": "FOR", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["pesada", "duas_maos", "magica"]},
    "espada grande flamejante": {"dano": "2d6+1", "atributo": "FOR", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["pesada", "duas_maos", "magica"]},
    "rapieira": {"dano": "1d8", "atributo": "DES", "propriedades": ["acuidade"]},
    "rapieira de duelo": {"dano": "1d8", "atributo": "DES", "propriedades": ["acuidade"]},
    "adaga": {"dano": "1d4", "atributo": "DES", "propriedades": ["acuidade", "leve", "arremesso"]},
    "adaga de caça": {"dano": "1d4", "atributo": "DES", "propriedades": ["acuidade", "leve", "arremesso"]},
    "adaga de mithral serrilhada +1": {"dano": "1d4+1", "atributo": "DES", "bonus_hit": 1, "bonus_damage": 1, "crit_threshold": 19, "propriedades": ["acuidade", "leve", "arremesso", "magica"]},
    "adaga de mithral": {"dano": "1d4+1", "atributo": "DES", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["acuidade", "leve", "arremesso", "magica"]},
    "maça": {"dano": "1d6", "atributo": "FOR", "propriedades": ["simples"]},
    "maça flangeada": {"dano": "1d6", "atributo": "FOR", "propriedades": ["simples"]},
    "martelo de guerra": {"dano": "1d8", "atributo": "FOR", "propriedades": ["versatil"]},
    "martelo abençoado do alvorecer +1": {"dano": "1d8+1", "atributo": "FOR", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["versatil", "magica"]},
    "maça abençoada": {"dano": "1d6+1", "atributo": "FOR", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["simples", "magica"]},
    "arco curto": {"dano": "1d6", "atributo": "DES", "propriedades": ["distancia", "duas_maos"]},
    "arco longo": {"dano": "1d8", "atributo": "DES", "propriedades": ["distancia", "pesada", "duas_maos"]},
    "arco longo de teixo": {"dano": "1d8", "atributo": "DES", "propriedades": ["distancia", "pesada", "duas_maos"]},
    "arco élfico de madeira-cinza +1": {"dano": "1d8+1", "atributo": "DES", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["distancia", "pesada", "duas_maos", "magica"]},
    "arco curto élfico": {"dano": "1d6+1", "atributo": "DES", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["distancia", "duas_maos", "magica"]},
    "besta leve": {"dano": "1d8", "atributo": "DES", "propriedades": ["distancia", "recarga", "duas_maos"]},
    "besta de mão": {"dano": "1d6", "atributo": "DES", "propriedades": ["distancia", "recarga", "leve"]},
    "besta mecânica reforçada +1": {"dano": "1d8+1", "atributo": "DES", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["distancia", "recarga", "duas_maos", "magica"]},
    "varinha de freixo": {"dano": "1d4", "atributo": "INT", "propriedades": ["foco", "leve"]},
    "bordão": {"dano": "1d6", "atributo": "FOR", "propriedades": ["versatil", "foco"]},
    "bordão de carvalho": {"dano": "1d6", "atributo": "FOR", "propriedades": ["versatil", "foco"]},
    "cajado arcano do vácuo +1": {"dano": "1d6+1", "atributo": "INT", "bonus_hit": 1, "bonus_damage": 1, "propriedades": ["versatil", "foco", "magica"]}
}

ARMADURAS_5E = {
    "cota de malha": {"ca_base": 16, "soma_des": False, "limite_des": None, "ca_bonus": 0},
    "armadura de couro": {"ca_base": 11, "soma_des": True, "limite_des": None, "ca_bonus": 0},
    "túnica arcana": {"ca_base": 11, "soma_des": True, "limite_des": None, "ca_bonus": 0},
    "brunea": {"ca_base": 14, "soma_des": True, "limite_des": 2, "ca_bonus": 0},
    "peitoral de aço": {"ca_base": 14, "soma_des": True, "limite_des": 2, "ca_bonus": 0},
    "escudo": {"ca_base": 0, "soma_des": False, "limite_des": None, "ca_bonus": 2},
    "escudo de carvalho": {"ca_base": 0, "soma_des": False, "limite_des": None, "ca_bonus": 2}
}

MAGIAS_5E = {
    "bola de fogo": {"dano": "8d6", "save_tipo": "DES", "alvos_max": 4, "alcance": "longo_alcance"},
    "míssil mágico": {"dano": "3d4", "save_tipo": "NENHUM", "alvos_max": 3, "alcance": "longo_alcance"},
    "raio de gelo": {"dano": "1d8", "save_tipo": "NENHUM", "alvos_max": 1, "alcance": "longo_alcance"},
    "onda trovejante": {"dano": "2d8", "save_tipo": "CON", "alvos_max": 3, "alcance": "curto_alcance"},
    "toque chocante": {"dano": "1d8", "save_tipo": "NENHUM", "alvos_max": 1, "alcance": "corpo_a_corpo"},
    "curar ferimentos": {"cura": "1d8", "save_tipo": "NENHUM", "alvos_max": 1, "alcance": "corpo_a_corpo"},
    "palavra curativa": {"cura": "1d4", "save_tipo": "NENHUM", "alvos_max": 1, "alcance": "curto_alcance"}
}

import json
import os

def load_character_creation_jsons():
    # Carrega Raças
    try:
        with open('data/races.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            mapping = {
                "race_human": "Humano",
                "race_halfling": "Halfling",
                "race_dragonborn": "Draconato",
                "race_half_orc": "Meio-Orc",
                "race_tiefling": "Tiefling",
                "race_hill_dwarf": "Anão da Colina",
                "race_wood_elf": "Elfo da Floresta"
            }
            for key, val in data.items():
                if key in mapping and mapping[key] in RACAS_5E:
                    raca_info = RACAS_5E[mapping[key]]
                    if val.get("description_pt"):
                        raca_info["descricao_ui"] = val.get("description_pt", "")
                    if "stat_bonuses" in val:
                        raca_info["stat_bonuses"] = val["stat_bonuses"]
                        pt_map = {"Força": "FOR", "Destreza": "DES", "Constituição": "CON", "Inteligência": "INT", "Sabedoria": "SAB", "Carisma": "CAR"}
                        bonus_dict = {"FOR": 0, "DES": 0, "CON": 0, "INT": 0, "SAB": 0, "CAR": 0}
                        for full_k, v in val["stat_bonuses"].items():
                            if full_k in pt_map:
                                bonus_dict[pt_map[full_k]] = v
                        raca_info["bonus"] = bonus_dict
                    if "speed" in val:
                        raca_info["speed"] = val["speed"]
                        raca_info["deslocamento_m"] = float(val["speed"])
                    if "size" in val:
                        raca_info["size"] = val["size"]
            # Sincroniza aliases canônicos
            RACAS_5E["Elfo"] = RACAS_5E["Elfo da Floresta"]
            RACAS_5E["Anão"] = RACAS_5E["Anão da Colina"]
            RACAS_5E["Anao"] = RACAS_5E["Anão da Colina"]
    except Exception:
        pass

    # Carrega Classes
    try:
        with open('data/classes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            mapping = {
                "class_fighter": "Guerreiro",
                "class_cleric": "Clérigo",
                "class_paladin": "Paladino",
                "class_wizard": "Mago",
                "class_ranger": "Patrulheiro",
                "class_rogue": "Ladino"
            }
            for key, val in data.items():
                if key in mapping and mapping[key] in CLASSES:
                    classe_info = CLASSES[mapping[key]]
                    if val.get("description_pt"):
                        classe_info["descricao_ui"] = val.get("description_pt", "")
                    if "hit_dice" in val:
                        classe_info["hit_dice"] = val["hit_dice"]
    except Exception:
        pass

    # Carrega Antecedentes
    try:
        with open('data/backgrounds.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            mapping = {
                "bg_hero": "Herói",
                "bg_criminal": "Criminoso",
                "bg_soldier": "Soldado",
                "bg_acolyte": "Acólito",
                "bg_sage": "Sábio",
                "bg_noble": "Nobre"
            }
            for key, val in data.items():
                if key in mapping and mapping[key] in ANTECEDENTES_5E:
                    if val.get("description_pt"):
                        ANTECEDENTES_5E[mapping[key]]["descricao_ui"] = val.get("description_pt", "")
    except Exception:
        pass

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
                    if val.get("description_pt"):
                        TENDENCIAS_5E[mapping[key]]["descricao_ui"] = val.get("description_pt", "")
    except Exception:
        pass

MANUAL_DO_JOGADOR_5E = {}

def get_manual_do_jogador(secao: str = None) -> dict:
    """Retorna os dados estruturados do Manual do Jogador D&D 5e (SRD)."""
    global MANUAL_DO_JOGADOR_5E
    if not MANUAL_DO_JOGADOR_5E:
        try:
            with open("data/manual_do_jogador.json", "r", encoding="utf-8") as f:
                MANUAL_DO_JOGADOR_5E = json.load(f)
        except Exception:
            try:
                with open("data/player_handbook.json", "r", encoding="utf-8") as f:
                    MANUAL_DO_JOGADOR_5E = json.load(f)
            except Exception:
                MANUAL_DO_JOGADOR_5E = {}
    if secao:
        return MANUAL_DO_JOGADOR_5E.get("secoes", {}).get(secao, {})
    return MANUAL_DO_JOGADOR_5E

get_player_handbook = get_manual_do_jogador
get_player_handbook_entry = get_manual_do_jogador

load_character_creation_jsons()
get_manual_do_jogador()

