import pygame
import os
import re
import unicodedata


# =============================================================================
# Normalização de chaves (o backend envia IDs crus; os arquivos usam slugs PT)
# =============================================================================

def _fix_mojibake(text: str) -> str:
    """Repara UTF-8 que foi lido como Latin-1/CP1252 ('ClÃ©rigo' -> 'Clérigo')."""
    if "Ã" not in text and "Â" not in text:
        return text
    for enc in ("cp1252", "latin-1"):
        try:
            return text.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return text


def _slug(text) -> str:
    """'Anão da Colina' -> 'anao_da_colina' | 'Meio-Orc' -> 'meio_orc'."""
    if not text:
        return ""
    text = _fix_mojibake(str(text))
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "_", text.lower())
    return text.strip("_")


# Raça (PT, EN ou ID de dados) -> prefixo usado nos arquivos de heroes/
RACE_SLUGS = {
    "humano": "humano", "human": "humano",
    "anao": "anao", "anao_da_colina": "anao", "dwarf": "anao", "hill_dwarf": "anao",
    "elfo": "elfo", "elfo_da_floresta": "elfo", "elf": "elfo", "wood_elf": "elfo",
    "meio_orc": "meio_orc", "half_orc": "meio_orc",
    "draconato": "draconato", "dragonborn": "draconato",
    "halfling": "halfling",
    "tiefling": "tiefling",
}

# Classe (PT, EN ou ID de dados) -> slug usado nos arquivos de heroes/
CLASS_SLUGS = {
    "guerreiro": "guerreiro", "fighter": "guerreiro",
    "cavaleiro": "cavaleiro", "knight": "cavaleiro",
    "clerigo": "clerigo", "cleric": "clerigo",
    "paladino": "paladino", "paladin": "paladino",
    "mago": "mago", "wizard": "mago", "mage": "mago",
    "patrulheiro": "patrulheiro", "ranger": "patrulheiro",
    "ladino": "ladino", "rogue": "ladino",
    "bruxo": "bruxo", "warlock": "bruxo",
    "feiticeiro": "feiticeiro", "sorcerer": "feiticeiro",
}

# Quando o arquivo exato não existe, tenta estes slugs equivalentes (mesma raça/classe).
CLASS_FILE_ALIASES = {
    "guerreiro": ["guerreiro", "cavaleiro"],
    "cavaleiro": ["cavaleiro", "guerreiro"],
    "ladino": ["ladino", "rogue"],
    "rogue": ["ladino", "rogue"],
}

GENDER_SLUGS = {
    "m": "male", "male": "male", "masculino": "male", "homem": "male",
    "f": "female", "female": "female", "feminino": "female", "mulher": "female",
}

# Manifesto Canônico dos 42 Sprites e Ícones de Protagonistas (7 Raças x 6 Classes)
# Conforme especificado na Seção 9 de docs/prompts_protagonistas_racas_classes.md
PROTAGONIST_SPRITE_MANIFEST = {
    # 1. Humano (male)
    ("humano", "guerreiro"): {"sprite": "humano_guerreiro_male.png", "icon": "humano_guerreiro_male.jpg", "gender": "male"},
    ("humano", "clerigo"): {"sprite": "humano_clerigo_male.png", "icon": "humano_clerigo_male.jpg", "gender": "male"},
    ("humano", "mago"): {"sprite": "humano_mago_male.png", "icon": "humano_mago_male.jpg", "gender": "male"},
    ("humano", "paladino"): {"sprite": "humano_paladino_male.png", "icon": "humano_paladino_male.jpg", "gender": "male"},
    ("humano", "patrulheiro"): {"sprite": "humano_patrulheiro_male.png", "icon": "humano_patrulheiro_male.jpg", "gender": "male"},
    ("humano", "ladino"): {"sprite": "humano_ladino_male.png", "icon": "humano_ladino_male.jpg", "gender": "male"},
    # 2. Anão da Colina (male)
    ("anao", "guerreiro"): {"sprite": "anao_guerreiro_male.png", "icon": "anao_guerreiro_male.jpg", "gender": "male"},
    ("anao", "clerigo"): {"sprite": "anao_clerigo_male.png", "icon": "anao_clerigo_male.jpg", "gender": "male"},
    ("anao", "mago"): {"sprite": "anao_mago_male.png", "icon": "anao_mago_male.jpg", "gender": "male"},
    ("anao", "paladino"): {"sprite": "anao_paladino_male.png", "icon": "anao_paladino_male.jpg", "gender": "male"},
    ("anao", "patrulheiro"): {"sprite": "anao_patrulheiro_male.png", "icon": "anao_patrulheiro_male.jpg", "gender": "male"},
    ("anao", "ladino"): {"sprite": "anao_ladino_male.png", "icon": "anao_ladino_male.jpg", "gender": "male"},
    # 3. Elfo da Floresta (female)
    ("elfo", "guerreiro"): {"sprite": "elfo_guerreiro_female.png", "icon": "elfo_guerreiro_female.jpg", "gender": "female"},
    ("elfo", "clerigo"): {"sprite": "elfo_clerigo_female.png", "icon": "elfo_clerigo_female.jpg", "gender": "female"},
    ("elfo", "mago"): {"sprite": "elfo_mago_female.png", "icon": "elfo_mago_female.jpg", "gender": "female"},
    ("elfo", "paladino"): {"sprite": "elfo_paladino_female.png", "icon": "elfo_paladino_female.jpg", "gender": "female"},
    ("elfo", "patrulheiro"): {"sprite": "elfo_patrulheiro_female.png", "icon": "elfo_patrulheiro_female.jpg", "gender": "female"},
    ("elfo", "ladino"): {"sprite": "elfo_ladino_female.png", "icon": "elfo_ladino_female.jpg", "gender": "female"},
    # 4. Meio-Orc (male)
    ("meio_orc", "guerreiro"): {"sprite": "meio_orc_guerreiro_male.png", "icon": "meio_orc_guerreiro_male.jpg", "gender": "male"},
    ("meio_orc", "clerigo"): {"sprite": "meio_orc_clerigo_male.png", "icon": "meio_orc_clerigo_male.jpg", "gender": "male"},
    ("meio_orc", "mago"): {"sprite": "meio_orc_mago_male.png", "icon": "meio_orc_mago_male.jpg", "gender": "male"},
    ("meio_orc", "paladino"): {"sprite": "meio_orc_paladino_male.png", "icon": "meio_orc_paladino_male.jpg", "gender": "male"},
    ("meio_orc", "patrulheiro"): {"sprite": "meio_orc_patrulheiro_male.png", "icon": "meio_orc_patrulheiro_male.jpg", "gender": "male"},
    ("meio_orc", "ladino"): {"sprite": "meio_orc_ladino_male.png", "icon": "meio_orc_ladino_male.jpg", "gender": "male"},
    # 5. Draconato (male)
    ("draconato", "guerreiro"): {"sprite": "draconato_guerreiro_male.png", "icon": "draconato_guerreiro_male.jpg", "gender": "male"},
    ("draconato", "clerigo"): {"sprite": "draconato_clerigo_male.png", "icon": "draconato_clerigo_male.jpg", "gender": "male"},
    ("draconato", "mago"): {"sprite": "draconato_mago_male.png", "icon": "draconato_mago_male.jpg", "gender": "male"},
    ("draconato", "paladino"): {"sprite": "draconato_paladino_male.png", "icon": "draconato_paladino_male.jpg", "gender": "male"},
    ("draconato", "patrulheiro"): {"sprite": "draconato_patrulheiro_male.png", "icon": "draconato_patrulheiro_male.jpg", "gender": "male"},
    ("draconato", "ladino"): {"sprite": "draconato_ladino_male.png", "icon": "draconato_ladino_male.jpg", "gender": "male"},
    # 6. Halfling (male)
    ("halfling", "guerreiro"): {"sprite": "halfling_guerreiro_male.png", "icon": "halfling_guerreiro_male.jpg", "gender": "male"},
    ("halfling", "clerigo"): {"sprite": "halfling_clerigo_male.png", "icon": "halfling_clerigo_male.jpg", "gender": "male"},
    ("halfling", "mago"): {"sprite": "halfling_mago_male.png", "icon": "halfling_mago_male.jpg", "gender": "male"},
    ("halfling", "paladino"): {"sprite": "halfling_paladino_male.png", "icon": "halfling_paladino_male.jpg", "gender": "male"},
    ("halfling", "patrulheiro"): {"sprite": "halfling_patrulheiro_male.png", "icon": "halfling_patrulheiro_male.jpg", "gender": "male"},
    ("halfling", "ladino"): {"sprite": "halfling_ladino_male.png", "icon": "halfling_ladino_male.jpg", "gender": "male"},
    # 7. Tiefling (male)
    ("tiefling", "guerreiro"): {"sprite": "tiefling_guerreiro_male.png", "icon": "tiefling_guerreiro_male.jpg", "gender": "male"},
    ("tiefling", "clerigo"): {"sprite": "tiefling_clerigo_male.png", "icon": "tiefling_clerigo_male.jpg", "gender": "male"},
    ("tiefling", "mago"): {"sprite": "tiefling_mago_male.png", "icon": "tiefling_mago_male.jpg", "gender": "male"},
    ("tiefling", "paladino"): {"sprite": "tiefling_paladino_male.png", "icon": "tiefling_paladino_male.jpg", "gender": "male"},
    ("tiefling", "patrulheiro"): {"sprite": "tiefling_patrulheiro_male.png", "icon": "tiefling_patrulheiro_male.jpg", "gender": "male"},
    ("tiefling", "ladino"): {"sprite": "tiefling_ladino_male.png", "icon": "tiefling_ladino_male.jpg", "gender": "male"},
}

# Fallback Visual Canônico para os 42 Heróis Aliados já existentes em assets/sprites/heroes/
# (Usado enquanto os arquivos {raca}_{classe}_{genero}.png dos protagonistas ainda não foram gerados em disco)
ALLY_HERO_FALLBACK_BY_RACE_CLASS = {
    ("humano", "guerreiro"): "Sir Alistair Valerius",
    ("humano", "clerigo"): "Padre Lucien",
    ("humano", "paladino"): "Lorde Barent de Oakhaven",
    ("humano", "mago"): "Arquimago Vane",
    ("humano", "patrulheiro"): "Garrick Rastreador-de-Pegadas",
    ("humano", "ladino"): "Corbin Mãos-de-Sombra",
    ("anao", "guerreiro"): "Brakus Barba-de-Ferro",
    ("anao", "clerigo"): "Kargan Forja-Divina",
    ("anao", "paladino"): "Thalgrim Escudo-da-Montanha",
    ("anao", "mago"): "Orin Forjador-de-Runas",
    ("anao", "patrulheiro"): "Durnik Olho-de-Rapina",
    ("anao", "ladino"): "Morgran Dedos-de-Ouro",
    ("draconato", "guerreiro"): "General Vrakhas",
    ("draconato", "clerigo"): "Sacerdote Baham-Raza",
    ("draconato", "paladino"): "Balthazar Escama-Dourada",
    ("draconato", "mago"): "Ignisrax, o Piromante do Fogo Dracônico",
    ("draconato", "patrulheiro"): "Kresh Veneno-Silencioso",
    ("draconato", "ladino"): "Zyrak Escama-de-Sombra",
    ("elfo", "guerreiro"): "Dama Aeloria Vento-Cortante",
    ("elfo", "clerigo"): "Sacerdotisa Faen",
    ("elfo", "paladino"): "Sylphira Lâmina-do-Amanhecer",
    ("elfo", "mago"): "Arquimaga Caelynn",
    ("elfo", "patrulheiro"): "Sylas Rastreadora-da-Lua",
    ("elfo", "ladino"): "Kaelen Passo-de-Névoa",
    ("halfling", "guerreiro"): "Tobias Bravo-Coração",
    ("halfling", "clerigo"): "Milo Concha-de-Ouro",
    ("halfling", "paladino"): "Sir Pip, o Campeão Valente dos Indefesos",
    ("halfling", "mago"): "Wilkin Faísca-Rápida",
    ("halfling", "patrulheiro"): "Caelen Olho-de-Lebre",
    ("halfling", "ladino"): "Finn Pés-Leves",
    ("meio_orc", "guerreiro"): "Thorgar Quebrador-de-Ossos",
    ("meio_orc", "clerigo"): "Gromph Clamor-do-Trovão",
    ("meio_orc", "paladino"): "Varek o Redentor",
    ("meio_orc", "mago"): "Morgok Sangue-Feiticeiro",
    ("meio_orc", "patrulheiro"): "Kallor Dente-de-Lobo",
    ("meio_orc", "ladino"): "Zulgor Mão-de-Ferro",
    ("tiefling", "guerreiro"): "Malakor Chifre-Partido",
    ("tiefling", "clerigo"): "Irmão Damian, o Inquisidor do Crepúsculo Abissal",
    ("tiefling", "paladino"): "Valravn o Purificado",
    ("tiefling", "mago"): "Azaroth o Necro-Arcanista",
    ("tiefling", "patrulheiro"): "Kallisto Sombra-da-Penumbra",
    ("tiefling", "ladino"): "Balthazar Pé-de-Cabra",
}

# Manifesto Canônico dos 24 Ícones de Habilidades de Classe (6 Classes x 4 Tiers)
# Conforme especificado em docs/prompts_skills_art_direction.md e data/class_skills.json
SKILL_ICON_MANIFEST = {
    # Guerreiro (Fighter)
    "sk_warrior_1": "skill_fighter_1_retomar_folego.png",
    "second_wind": "skill_fighter_1_retomar_folego.png",
    "sk_warrior_2": "skill_fighter_2_surto_acao.png",
    "action_surge": "skill_fighter_2_surto_acao.png",
    "sk_warrior_3": "skill_fighter_3_foco_campeao.png",
    "champion_focus": "skill_fighter_3_foco_campeao.png",
    "sk_warrior_5": "skill_fighter_5_ataque_extra.png",
    "extra_attack_fighter": "skill_fighter_5_ataque_extra.png",
    # Clérigo (Cleric)
    "sk_cleric_1": "skill_cleric_1_discipulo_vida.png",
    "disciple_of_life": "skill_cleric_1_discipulo_vida.png",
    "sk_cleric_2": "skill_cleric_2_preservar_vida.png",
    "channel_divinity_preserve_life": "skill_cleric_2_preservar_vida.png",
    "sk_cleric_3": "skill_cleric_3_arma_espiritual.png",
    "spiritual_weapon": "skill_cleric_3_arma_espiritual.png",
    "sk_cleric_5": "skill_cleric_5_destruir_mortos_vivos.png",
    "destroy_undead": "skill_cleric_5_destruir_mortos_vivos.png",
    # Mago (Wizard)
    "sk_wizard_1": "skill_wizard_1_recuperacao_arcana.png",
    "arcane_recovery": "skill_wizard_1_recuperacao_arcana.png",
    "sk_wizard_2": "skill_wizard_2_evocacao_potente.png",
    "sculpt_spells": "skill_wizard_2_evocacao_potente.png",
    "sk_wizard_3": "skill_wizard_3_escudo_arcano.png",
    "potent_cantrip": "skill_wizard_3_escudo_arcano.png",
    "sk_wizard_5": "skill_wizard_5_mestre_elementos.png",
    "arcane_overload": "skill_wizard_5_mestre_elementos.png",
    # Paladino (Paladin)
    "sk_paladin_1": "skill_paladin_1_cura_pelas_maos.png",
    "lay_on_hands": "skill_paladin_1_cura_pelas_maos.png",
    "sk_paladin_2": "skill_paladin_2_destruicao_divina.png",
    "divine_smite": "skill_paladin_2_destruicao_divina.png",
    "sk_paladin_3": "skill_paladin_3_aura_protecao.png",
    "sacred_oath_devotion": "skill_paladin_3_aura_protecao.png",
    "sk_paladin_5": "skill_paladin_5_ataque_extra_sagrado.png",
    "extra_attack_paladin": "skill_paladin_5_ataque_extra_sagrado.png",
    # Patrulheiro (Ranger)
    "sk_ranger_1": "skill_ranger_1_marca_cacador.png",
    "favored_enemy": "skill_ranger_1_marca_cacador.png",
    "sk_ranger_2": "skill_ranger_2_estilo_arquearia.png",
    "archery_style": "skill_ranger_2_estilo_arquearia.png",
    "sk_ranger_3": "skill_ranger_3_matador_colossos.png",
    "colossus_slayer": "skill_ranger_3_matador_colossos.png",
    "sk_ranger_5": "skill_ranger_5_rajada_flechas.png",
    "extra_attack_ranger": "skill_ranger_5_rajada_flechas.png",
    # Ladino (Rogue)
    "sk_rogue_1": "skill_rogue_1_ataque_furtivo.png",
    "sneak_attack": "skill_rogue_1_ataque_furtivo.png",
    "sk_rogue_2": "skill_rogue_2_acao_ardilosa.png",
    "cunning_action": "skill_rogue_2_acao_ardilosa.png",
    "sk_rogue_3": "skill_rogue_3_emboscada_mortal.png",
    "assassinate": "skill_rogue_3_emboscada_mortal.png",
    "sk_rogue_5": "skill_rogue_5_esquiva_sobrenatural.png",
    "uncanny_dodge": "skill_rogue_5_esquiva_sobrenatural.png",
}

# IDs legados (campanha antiga / BESTIARIO_5E em PT) -> nome do arquivo em enemies/
ENEMY_ALIASES = {
    "boss_final": "supreme_dragon",
    "tirano_das_cinzas": "supreme_dragon",
    "esqueleto": "skeleton",
    "zumbi": "zombie",
    "manticora": "manticore",
    "cria_vampiro": "vampire_spawn",
    "vampiro": "vampire_spawn",
    "aparicao": "wraith",
    "quimera": "chimera",
    "sombra": "shadow",
    "gigante_do_fogo": "fire_giant",
    "aranha_gigante": "giant_spider",
    "armadura_animada": "animated_armor",
    "lobo_atroz": "dire_wolf",
    "gargula": "gargoyle",
    "bandido": "bandit",
    "ogro": "ogre",
    "mimico": "mimic",
    "geleia_ocre": "ochre_jelly",
}

# Prefixos de categoria do bestiário legado ('lacaio goblin', 'sub-chefe quimera')
ENEMY_CATEGORY_PREFIXES = ("lacaio_", "sub_chefe_", "subchefe_", "chefe_", "elite_")

COLOR_MISSING_ENEMY = (255, 0, 255)   # Magenta
COLOR_MISSING_HERO = (0, 255, 255)    # Ciano


def _resolve_slug(raw, table: dict, strip_prefix: str) -> str:
    key = _slug(raw)
    if key.startswith(strip_prefix):
        key = key[len(strip_prefix):]
    if key in table:
        return table[key]
    # 'anao_xpto' -> 'anao' (prefixo mais longo vence: 'meio_orc' antes de 'meio')
    for known in sorted(table.keys(), key=len, reverse=True):
        if key.startswith(known + "_"):
            return table[known]
    return ""


class AssetManager:
    """Gerenciador estático de texturas, fontes e imagens do jogo.

    Toda Surface carregada do disco fica em `_image_cache` (chave = caminho do arquivo
    ou chave lógica). Nenhuma imagem é lida do disco duas vezes.
    """

    BASE_ENEMIES = os.path.normpath("assets/sprites/enemies")
    BASE_HEROES = os.path.normpath("assets/sprites/heroes")
    BASE_PERSONAGENS = os.path.normpath("assets/sprites/personagens")
    BASE_ICONS = [
        os.path.normpath("assets/sprites/personagens/retratos"),
        os.path.normpath("assets/sprites/personagens/icones"),
        os.path.normpath("assets/sprites/personagens"),
        os.path.normpath("assets/sprites/heroes/icones"),
        os.path.normpath("assets/sprites/heroes"),
        os.path.normpath("assets/sprites/icones")
    ]
    BASE_SKILLS = os.path.normpath("assets/ui/skills")
    
    _PRIMARY_FONT = os.path.normpath("assets/fonts/Retro Gaming.ttf")
    _FALLBACK_FONT = os.path.normpath("assets/fonts/pixel_font.ttf")
    FONT_PATH = _PRIMARY_FONT if os.path.exists(_PRIMARY_FONT) else _FALLBACK_FONT

    _image_cache = {}
    _cache = _image_cache          # Alias legado (hud_components usa AssetManager._cache)
    _scaled_cache = {}
    _fonts = {}

    # ------------------------------------------------------------------ FONTES
    @classmethod
    def get_font(cls, size: int, bold: bool = False, italic: bool = False) -> pygame.font.Font:
        if not pygame.font.get_init():
            pygame.font.init()
            cls._fonts.clear()

        key = (size, bold, italic)
        if key in cls._fonts:
            try:
                cls._fonts[key].get_height()
                return cls._fonts[key]
            except (pygame.error, Exception):
                cls._fonts.clear()

        try:
            font = pygame.font.Font(cls.FONT_PATH, size)
        except (FileNotFoundError, OSError, pygame.error):
            fallback = os.path.normpath("assets/fonts/pixel_font.ttf")
            if os.path.exists(fallback) and cls.FONT_PATH != fallback:
                try:
                    font = pygame.font.Font(fallback, size)
                except Exception:
                    font = pygame.font.SysFont("Arial", size)
            else:
                font = pygame.font.SysFont("Arial", size)
        if bold:
            try:
                font.set_bold(True)
            except Exception:
                pass
        if italic:
            try:
                font.set_italic(True)
            except Exception:
                pass
        cls._fonts[key] = font
        return font

    # -------------------------------------------------------- NÚCLEO DE CACHE
    @classmethod
    def _load_file(cls, filepath: str, alpha: bool = True):
        """Carrega uma imagem UMA única vez. Retorna None se o arquivo não existir."""
        if filepath in cls._image_cache:
            return cls._image_cache[filepath]
        if not os.path.exists(filepath):
            return None
        try:
            raw = pygame.image.load(filepath)
            try:
                surf = raw.convert_alpha() if alpha else raw.convert()
            except pygame.error:
                surf = raw  # Display ainda não inicializado
        except pygame.error as e:
            print(f"[ERRO UI] Falha ao decodificar '{filepath}': {e}")
            return None
        cls._image_cache[filepath] = surf
        return surf

    @classmethod
    def _placeholder(cls, color: tuple, size: tuple = (64, 64)) -> pygame.Surface:
        key = ("__placeholder__", color, size)
        if key not in cls._image_cache:
            surf = pygame.Surface(size)
            surf.fill(color)
            cls._image_cache[key] = surf
        return cls._image_cache[key]

    @classmethod
    def progressive_downscale(cls, surface: pygame.Surface, target_size: tuple) -> pygame.Surface:
        """Reduz a resolução progressivamente em potências de 2 antes do smoothscale final.
        Evita o efeito borrado e serrilhado em imagens de alta resolução (ex: 2048x2048 -> 100x100).
        Utiliza cache de textura para garantir zero overhead por frame a 60 FPS."""
        if surface is None:
            return surface
        target_w, target_h = int(target_size[0]), int(target_size[1])
        if target_w <= 0 or target_h <= 0:
            return surface
        cur_w, cur_h = surface.get_size()
        if (cur_w, cur_h) == (target_w, target_h):
            return surface

        key = (id(surface), (target_w, target_h), "progressive")
        cached = cls._scaled_cache.get(key)
        if cached is not None:
            return cached

        cur_surf = surface
        # Reduz em passos graduais de 50% enquanto a dimensão atual for pelo menos o dobro da meta
        while cur_w // 2 >= target_w and cur_h // 2 >= target_h:
            cur_w //= 2
            cur_h //= 2
            try:
                cur_surf = pygame.transform.smoothscale(cur_surf, (cur_w, cur_h))
            except (ValueError, pygame.error):
                cur_surf = pygame.transform.scale(cur_surf, (cur_w, cur_h))

        # Redimensionamento final para o tamanho exato solicitado
        if (cur_w, cur_h) != (target_w, target_h):
            try:
                cur_surf = pygame.transform.smoothscale(cur_surf, (target_w, target_h))
            except (ValueError, pygame.error):
                cur_surf = pygame.transform.scale(cur_surf, (target_w, target_h))

        cls._scaled_cache[key] = cur_surf
        return cur_surf

    @classmethod
    def get_scaled(cls, surface: pygame.Surface, size: tuple, smooth: bool = False) -> pygame.Surface:
        """Redimensiona com cache. Evita `smoothscale` a cada frame (queda de FPS)."""
        size = (int(size[0]), int(size[1]))
        if surface.get_size() == size:
            return surface
        key = (id(surface), size, smooth)
        cached = cls._scaled_cache.get(key)
        if cached is None:
            # Para downscales significativos com smooth=True, usa downscale progressivo
            if smooth and surface.get_width() > size[0] * 1.5:
                cached = cls.progressive_downscale(surface, size)
            else:
                fn = pygame.transform.smoothscale if smooth else pygame.transform.scale
                try:
                    cached = fn(surface, size)
                except ValueError:  # smoothscale exige 24/32 bits
                    cached = pygame.transform.scale(surface, size)
            cls._scaled_cache[key] = cached
        return cached

    # ---------------------------------------------------------------- INIMIGOS
    @classmethod
    def resolve_enemy_filename(cls, enemy_id: str) -> str:
        """'m_goblin' -> 'goblin.png' | 'goblin' -> 'goblin.png'."""
        name = _slug(enemy_id)
        if name.startswith("m_"):
            name = name[2:]
        if name.endswith("_png"):
            name = name[:-4]
        for prefix in ENEMY_CATEGORY_PREFIXES:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        name = ENEMY_ALIASES.get(name, name)
        return f"{name}.png"

    @classmethod
    def get_enemy_sprite(cls, enemy_id: str) -> pygame.Surface:
        """Carrega assets/sprites/enemies/{id_sem_m_}.png. Falha -> quadrado Magenta."""
        filename = cls.resolve_enemy_filename(enemy_id or "")
        filepath = os.path.join(cls.BASE_ENEMIES, filename)
        surf = cls._load_file(filepath)
        if surf is not None:
            return surf

        miss_key = ("__missing_enemy__", filepath)
        if miss_key not in cls._image_cache:
            print(f"[ERRO UI] Sprite de inimigo ausente: '{filepath}' (id='{enemy_id}'). Usando Magenta.")
            cls._image_cache[miss_key] = cls._placeholder(COLOR_MISSING_ENEMY)
        return cls._image_cache[miss_key]

    # ------------------------------------------------------------------ HERÓIS
    @classmethod
    def resolve_hero_candidates(cls, race: str, char_class: str, gender: str = None) -> list:
        """Lista ordenada de caminhos possíveis para {race}_{class}_{gender}.png."""
        race_slug = _resolve_slug(race, RACE_SLUGS, "race_")
        class_slug = _resolve_slug(char_class, CLASS_SLUGS, "class_")
        if not race_slug or not class_slug:
            return []

        canonical_class = "guerreiro" if class_slug == "cavaleiro" else class_slug
        manifest_entry = PROTAGONIST_SPRITE_MANIFEST.get((race_slug, canonical_class))

        g = GENDER_SLUGS.get(_slug(gender), None)
        if not g and manifest_entry:
            g = manifest_entry["gender"]
        genders = [g, "female" if g == "male" else "male"] if g else ["male", "female"]

        names = []
        if manifest_entry and manifest_entry["sprite"] not in names:
            names.append(manifest_entry["sprite"])

        for cls_name in CLASS_FILE_ALIASES.get(class_slug, [class_slug]):
            for gen in genders:
                cand = f"{race_slug}_{cls_name}_{gen}.png"
                if cand not in names:
                    names.append(cand)
            cand_no_gen = f"{race_slug}_{cls_name}.png"
            if cand_no_gen not in names:
                names.append(cand_no_gen)

        return names

    @classmethod
    def get_hero_icon(cls, race: str, char_class: str, gender: str = None, size: tuple = (128, 128)) -> pygame.Surface:
        target_size = size or (128, 128)
        logical_key = ("__hero_icon__", _slug(race), _slug(char_class), _slug(gender), target_size)
        if logical_key in cls._image_cache:
            return cls._image_cache[logical_key]

        race_slug = _resolve_slug(race, RACE_SLUGS, "race_")
        class_slug = _resolve_slug(char_class, CLASS_SLUGS, "class_")
        canonical_class = "guerreiro" if class_slug == "cavaleiro" else class_slug

        names = []
        manifest_entry = PROTAGONIST_SPRITE_MANIFEST.get((race_slug, canonical_class))
        if manifest_entry:
            names.append(manifest_entry["icon"])
            names.append(manifest_entry["sprite"])
        for n in cls.resolve_hero_candidates(race, char_class, gender):
            stem, _ = os.path.splitext(n)
            for ext in (".jpg", ".png"):
                if stem + ext not in names:
                    names.append(stem + ext)

        candidates = [os.path.join(d, n) for d in cls.BASE_ICONS for n in names]
        surf = None
        for path in candidates:
            surf = cls._load_file(path)
            if surf is not None:
                break

        # Fallback para o ícone real do aliado da mesma Raça + Classe se o protagonista ainda não foi gerado
        if surf is None and race_slug and canonical_class:
            ally_stem = ALLY_HERO_FALLBACK_BY_RACE_CLASS.get((race_slug, canonical_class))
            if ally_stem:
                for d in cls.BASE_ICONS:
                    for ext in (".jpg", ".png", ".jpeg"):
                        surf = cls._load_file(os.path.join(d, ally_stem + ext), alpha=(ext == ".png"))
                        if surf is not None:
                            break
                    if surf is not None:
                        break

        if surf is None:
            print(f"[ERRO UI] Ícone de herói ausente: raça='{race}' classe='{char_class}' "
                  f"gênero='{gender}'. Usando Ciano.")
            surf = cls._placeholder(COLOR_MISSING_HERO)

        if target_size:
            surf = cls.progressive_downscale(surf, target_size)

        cls._image_cache[logical_key] = surf
        return surf

    @classmethod
    def get_hero_sprite(cls, race: str, char_class: str, gender: str = None) -> pygame.Surface:
        """Herói/aliado: assets/sprites/heroes/{race}_{class}_{gender}.png. Falha -> Ciano."""
        logical_key = ("__hero__", _slug(race), _slug(char_class), _slug(gender))
        if logical_key in cls._image_cache:
            return cls._image_cache[logical_key]

        names = cls.resolve_hero_candidates(race, char_class, gender)
        candidates = [os.path.join(cls.BASE_PERSONAGENS, n) for n in names] + \
                     [os.path.join(cls.BASE_HEROES, n) for n in names]
        surf = None
        for path in candidates:
            surf = cls._load_file(path)
            if surf is not None:
                break

        # Fallback para o sprite real do aliado da mesma Raça + Classe se o protagonista ainda não foi gerado
        if surf is None:
            race_slug = _resolve_slug(race, RACE_SLUGS, "race_")
            class_slug = _resolve_slug(char_class, CLASS_SLUGS, "class_")
            canonical_class = "guerreiro" if class_slug == "cavaleiro" else class_slug
            ally_stem = ALLY_HERO_FALLBACK_BY_RACE_CLASS.get((race_slug, canonical_class))
            if ally_stem:
                for ext in (".png", ".jpg", ".jpeg"):
                    surf = cls._load_file(os.path.join(cls.BASE_HEROES, ally_stem + ext), alpha=(ext == ".png"))
                    if surf is not None:
                        break

        if surf is None:
            print(f"[ERRO UI] Sprite de herói ausente: raça='{race}' classe='{char_class}' "
                  f"gênero='{gender}'. Usando Ciano.")
            surf = cls._placeholder(COLOR_MISSING_HERO)

        cls._image_cache[logical_key] = surf
        return surf

    @classmethod
    def get_character_sprite(cls, raca: str, classe: str, genero: str = None, tipo: str = "corpo",
                             allow_placeholder: bool = True) -> pygame.Surface:
        """Compatibilidade legada -> get_hero_sprite."""
        if tipo == "icone":
            return cls.get_hero_icon(raca, classe, genero)
        return cls.get_hero_sprite(raca, classe, genero)

    DEFAULT_NPC_FALLBACK = ("Humano", "Paladino", "M")

    @classmethod
    def get_npc_sprite(cls, raca: str, classe: str, genero: str, tipo: str = "corpo") -> pygame.Surface:
        if tipo == "icone":
            return cls.get_hero_icon(raca, classe, genero)
        return cls.get_hero_sprite(raca, classe, genero)

    @classmethod
    def get_entity_sprite(cls, entity, kind: str = "corpo", size: tuple = None) -> pygame.Surface:
        """Roteador universal: dict com sprite_key/portrait_key ou race+class -> herói/aliado; ID 'm_*'/string -> inimigo."""
        surf = None
        if isinstance(entity, dict):
            # 1. Tenta sprite_key / portrait_key explícito (aliados nomeados e NPCs especiais)
            direct_key = (entity.get("portrait_key") or entity.get("sprite_key")) if kind == "icone" else (entity.get("sprite_key") or entity.get("portrait_key"))
            if direct_key:
                direct_key_str = str(direct_key).strip()
                base_dirs = cls.BASE_ICONS if kind == "icone" else [cls.BASE_HEROES]
                for bdir in base_dirs:
                    for ext in ("", ".png", ".jpg", ".jpeg"):
                        cand_path = os.path.join(bdir, direct_key_str + ext)
                        surf = cls._load_file(cand_path, alpha=not cand_path.lower().endswith((".jpg", ".jpeg")))
                        if surf is not None:
                            break
                    if surf is not None:
                        break

            # 2. Tenta por race + class (protagonistas ou aliados sem sprite_key direto)
            if surf is None and entity.get("race") and entity.get("class"):
                if kind == "icone":
                    surf = cls.get_hero_icon(entity["race"], entity["class"],
                                             entity.get("gender") or entity.get("genero"))
                else:
                    surf = cls.get_hero_sprite(entity["race"], entity["class"],
                                               entity.get("gender") or entity.get("genero"))

            # 3. Fallback para inimigo por id/tipo_bestiario
            if surf is None:
                enemy_id = entity.get("id") or entity.get("tipo_bestiario") or entity.get("name") or ""
                surf = cls.get_enemy_sprite(str(enemy_id))
        else:
            surf = cls.get_enemy_sprite(str(entity))

        if size is not None and surf is not None:
            return cls.get_scaled(surf, size)
        return surf

    # ------------------------------------------------------- ÍCONES DE SKILLS
    @classmethod
    def get_skill_icon(cls, skill_id_or_dict, size: tuple = (36, 36)):
        """Busca o ícone quadrado de habilidade em assets/ui/skills/.
        Retorna a Surface escalonada se o arquivo existir em disco, ou None para usar o fallback procedural."""
        candidates = []
        if isinstance(skill_id_or_dict, dict):
            for k in ("icon_file", "id", "canonical_id"):
                val = skill_id_or_dict.get(k)
                if val:
                    candidates.append(str(val))
        elif skill_id_or_dict:
            candidates.append(str(skill_id_or_dict))

        for key in candidates:
            fname = SKILL_ICON_MANIFEST.get(key, key)
            if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                fname = f"{fname}.png"
            filepath = os.path.join(cls.BASE_SKILLS, fname)
            surf = cls._load_file(filepath)
            if surf is not None:
                return cls.get_scaled(surf, size) if size else surf
        return None

    # --------------------------------------------------------------- RETRATOS
    @classmethod
    def get_portrait_sprite(cls, name: str, size: tuple = (100, 100)) -> pygame.Surface:
        """Retrato com downscale progressivo para a caixa de diálogo (suporta Menestrel/DM, Heróis, Aliados e Inimigos)."""
        if not name:
            return cls.progressive_downscale(cls._placeholder(COLOR_MISSING_ENEMY), size)

        clean_name = str(name).strip()
        chave = re.sub(r"_(\d+|[0-9a-f]{4})$", "", _slug(clean_name))

        cache_key = ("__portrait__", chave, size)
        if cache_key in cls._image_cache:
            return cls._image_cache[cache_key]

        # 1. Aliases especiais (Taverneiro, Menestrel, Mestre, DM, Maelor)
        if chave == "taverneiro" or "taverneiro" in chave:
            for icon_dir in cls.BASE_ICONS:
                for candidate in ("taverneiro.jpg", "taverneiro.png", "taverneiro.jpeg"):
                    path = os.path.join(icon_dir, candidate)
                    surf = cls._load_file(path)
                    if surf is not None:
                        res = cls.progressive_downscale(surf, size)
                        cls._image_cache[cache_key] = res
                        return res

        if chave in ("menestrel", "mestre", "dm", "dungeon_master", "minstrel", "maelor", "maelor_das_cordas_de_cinza"):
            for icon_dir in cls.BASE_ICONS:
                for candidate in ("menestrel.jpg", "mestre.jpg", "minstrel.jpg", "Maelor das Cordas de Cinza.jpg", "menestrel.png"):
                    path = os.path.join(icon_dir, candidate)
                    surf = cls._load_file(path)
                    if surf is not None:
                        res = cls.progressive_downscale(surf, size)
                        cls._image_cache[cache_key] = res
                        return res

        # 2. Busca em ícones de heróis / NPCs (assets/sprites/heroes/icones/)
        for icon_dir in cls.BASE_ICONS:
            if not os.path.isdir(icon_dir):
                continue
            # Tentativa direta com extensões comuns
            for ext in (".jpg", ".png", ".jpeg"):
                for probe in (clean_name + ext, chave + ext):
                    probe_path = os.path.join(icon_dir, probe)
                    surf = cls._load_file(probe_path)
                    if surf is not None:
                        res = cls.progressive_downscale(surf, size)
                        cls._image_cache[cache_key] = res
                        return res

            # Busca por prefixo ou correspondência insensível a maiúsculas
            for fname in os.listdir(icon_dir):
                f_base, _ = os.path.splitext(fname)
                if _slug(f_base) == chave or _slug(f_base).startswith(chave) or chave.startswith(_slug(f_base)):
                    surf = cls._load_file(os.path.join(icon_dir, fname))
                    if surf is not None:
                        res = cls.progressive_downscale(surf, size)
                        cls._image_cache[cache_key] = res
                        return res

        # 3. Busca em sprites de corpo de personagens e heróis
        for body_dir in (cls.BASE_PERSONAGENS, cls.BASE_HEROES):
            if os.path.isdir(body_dir):
                for ext in (".png", ".jpg"):
                    probe_path = os.path.join(body_dir, clean_name + ext)
                    surf = cls._load_file(probe_path)
                    if surf is not None:
                        res = cls.progressive_downscale(surf, size)
                        cls._image_cache[cache_key] = res
                        return res

        # 4. Busca na pasta de inimigos (assets/sprites/enemies/)
        enemy_filename = cls.resolve_enemy_filename(chave)
        enemy_path = os.path.join(cls.BASE_ENEMIES, enemy_filename)
        surf = cls._load_file(enemy_path)
        if surf is not None:
            res = cls.progressive_downscale(surf, size)
            cls._image_cache[cache_key] = res
            return res

        # 5. Fallback se não encontrar
        print(f"[AVISO UI] Retrato não encontrado para '{name}' (chave='{chave}'). Usando Magenta.")
        placeholder = cls.progressive_downscale(cls._placeholder(COLOR_MISSING_ENEMY), size)
        cls._image_cache[cache_key] = placeholder
        return placeholder

    # ----------------------------------------------------------------- CENÁRIOS
    @classmethod
    def load_backgrounds(cls):
        pass  # Desativado no Bloco 38, carregamento on-demand por filepath

    @classmethod
    def load_enemies(cls):
        pass  # Compatibilidade legada, carregamento on-demand por sprite

    @classmethod
    def load_character_sprites(cls):
        pass  # Compatibilidade legada, carregamento on-demand por sprite

    @classmethod
    def get_background(cls, bg_image_filename: str) -> pygame.Surface:
        """Bloco 38: Carrega exatamente a bg_image solicitada do beat."""
        if not bg_image_filename:
            bg_image_filename = "default_bg.jpg"

        filepath = os.path.join(os.path.normpath("assets/backgrounds/Fases"), bg_image_filename)
        cache_key = ("__bg__", filepath)
        if cache_key in cls._image_cache:
            return cls._image_cache[cache_key]

        raw = cls._load_file(filepath, alpha=False)
        if raw is not None:
            surf = pygame.transform.scale(raw, (1280, 720))
        else:
            print(f"[ERRO UI] Cenário ausente: '{filepath}'. Usando placeholder.")
            surf = cls._placeholder(COLOR_MISSING_ENEMY, (1280, 720))
        cls._image_cache[cache_key] = surf
        return surf

    @classmethod
    def get_narrative_backgrounds(cls) -> list:
        return []

    # ------------------------------------------------------------------ LEGADO
    @classmethod
    def get_image(cls, category: str, name: str, fallback_name: str = None) -> pygame.Surface:
        """Compatibilidade legado minimizada."""
        key = f"{category}_{name}"
        if key in cls._image_cache:
            return cls._image_cache[key]

        path_map = {
            "background": "assets/backgrounds",
            "monster": "assets/sprites/enemies",
            "player": "assets/sprites/heroes",
            "ui": "assets/ui",
            "sprite": "assets/sprites"
        }
        base_dir = path_map.get(category, "assets")
        extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']

        # Suporte a aliases para texturas de UI
        aliases = []
        if category == "ui":
            ui_slug = _slug(name)
            UI_ALIASES = {
                "open_book": ["open_book", "grimorio_aberto", "Grimório Aberto"],
                "grimorio_aberto": ["open_book", "grimorio_aberto", "Grimório Aberto"],
                "grimorio": ["open_book", "grimorio_aberto", "Grimório Aberto"],
                "backpack_bg": ["backpack_bg", "mochila_aventureiro", "Mochila do Aventureiro"],
                "backpack": ["backpack_bg", "mochila_aventureiro", "Mochila do Aventureiro"],
                "mochila_aventureiro": ["backpack_bg", "mochila_aventureiro", "Mochila do Aventureiro"],
                "mochila": ["backpack_bg", "mochila_aventureiro", "Mochila do Aventureiro"],
            }
            aliases = UI_ALIASES.get(ui_slug, [])

        targets = [name] + [a for a in aliases if a != name]
        if fallback_name and fallback_name not in targets:
            targets.append(fallback_name)

        for target_name in targets:
            if not target_name:
                continue
            for ext in extensions:
                filepath = os.path.normpath(os.path.join(base_dir, f"{target_name}{ext}"))
                use_alpha = not (ext.lower() in ['.jpg', '.jpeg'] or category == "background")
                surf = cls._load_file(filepath, alpha=use_alpha)
                if surf is not None:
                    cls._image_cache[key] = surf
                    return surf

        # Em UI, se não houver arquivo físico, retornar None para permitir fallback procedural sem artefato magenta
        if category == "ui":
            return None

        placeholder = cls._placeholder(COLOR_MISSING_ENEMY)
        cls._image_cache[key] = placeholder
        return placeholder

    # -------------------------------------------------------- LIMPEZA DE MEMÓRIA
    @classmethod
    def clear_cache(cls, keep_fonts: bool = True):
        """Limpa o cache de texturas e imagens escalonadas para evitar vazamento de memória."""
        cls._image_cache.clear()
        cls._scaled_cache.clear()
        if not keep_fonts:
            cls._fonts.clear()

