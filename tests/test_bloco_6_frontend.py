import os
import pytest
import pygame

# Inicialização sem display para ambiente de testes headless
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.font.init()
pygame.display.set_mode((1280, 720))

def _get_screen():
    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode((1280, 720))
    return screen


def test_legacy_renderer_file_removed():
    """Valida que o arquivo legado não utilizado ui/renderer.py foi removido."""
    legacy_file = os.path.join("ui", "renderer.py")
    assert not os.path.exists(legacy_file), "O arquivo legado ui/renderer.py deve ser excluído!"


def test_asset_manager_clear_cache():
    """Valida que clear_cache limpa os caches de imagem e escalonamento sem quebrar fontes."""
    from ui.asset_manager import AssetManager

    # Simula inserções no cache
    dummy_surf = pygame.Surface((10, 10))
    AssetManager._image_cache["test_dummy"] = dummy_surf
    AssetManager._scaled_cache[("test_dummy", (20, 20))] = dummy_surf

    # Garante que uma fonte existe no cache
    _ = AssetManager.get_font(18)
    assert len(AssetManager._fonts) > 0

    # Limpa com keep_fonts=True (padrão)
    AssetManager.clear_cache(keep_fonts=True)
    assert len(AssetManager._image_cache) == 0
    assert len(AssetManager._scaled_cache) == 0
    assert len(AssetManager._fonts) > 0

    # Limpa com keep_fonts=False
    AssetManager.clear_cache(keep_fonts=False)
    assert len(AssetManager._fonts) == 0


def test_hud_components_surface_caching():
    """Valida que draw_ui_panel e draw_ui_button utilizam cache de superfície."""
    from ui.hud_components import (
        draw_ui_panel, draw_ui_button, _PANEL_SURF_CACHE, _BUTTON_BG_CACHE, clear_hud_cache
    )
    from ui.asset_manager import AssetManager

    clear_hud_cache()
    screen = _get_screen()
    font = AssetManager.get_font(16)
    rect = pygame.Rect(10, 10, 150, 40)

    # Primeira chamada: preenche cache
    draw_ui_panel(screen, rect)
    assert (150, 40) in _PANEL_SURF_CACHE
    panel_surf_1 = _PANEL_SURF_CACHE[(150, 40)]

    # Segunda chamada: deve reutilizar a mesma Surface
    draw_ui_panel(screen, rect)
    assert _PANEL_SURF_CACHE[(150, 40)] is panel_surf_1

    # Botão: primeira chamada
    draw_ui_button(screen, rect, "Ataque", font, is_hover=False, is_ready=True)
    btn_key = (150, 40, False, True)
    assert btn_key in _BUTTON_BG_CACHE
    btn_surf_1 = _BUTTON_BG_CACHE[btn_key]

    # Segunda chamada: reutiliza a mesma Surface
    draw_ui_button(screen, rect, "Ataque", font, is_hover=False, is_ready=True)
    assert _BUTTON_BG_CACHE[btn_key] is btn_surf_1


def test_text_input_bar_and_chat_box_optimization():
    """Valida que ChatBox / TextInputBar cria a superfície uma única vez no init."""
    from ui.hud_components import ChatBox, TextInputBar

    assert TextInputBar is ChatBox

    chat = TextInputBar(0, 0, 300, 40)
    assert hasattr(chat, "_bg_surface")
    assert chat._bg_surface is not None
    initial_surf = chat._bg_surface

    screen = _get_screen()
    chat.draw(screen)
    assert chat._bg_surface is initial_surf


def test_loading_dice_animation_optimization():
    """Valida que LoadingDiceAnimation pré-aloca poly_surface no init."""
    from ui.hud_components import LoadingDiceAnimation

    anim = LoadingDiceAnimation()
    assert hasattr(anim, "poly_surface")
    assert isinstance(anim.poly_surface, pygame.Surface)
    poly_surf = anim.poly_surface

    screen = _get_screen()
    anim.draw(screen, 100, 100)
    assert anim.poly_surface is poly_surf


def test_generic_selection_panels_dry():
    """Valida a classe genérica e subclasses mantendo total compatibilidade."""
    from ui.menu_components import (
        GenericSelectionPanel,
        RaceSelectionPanel,
        ClassSelectionPanel,
        BackgroundSelectionPanel,
        AlignmentSelectionPanel,
    )
    from core.dnd_rules import RACAS_5E, CLASSES, ANTECEDENTES_5E, TENDENCIAS_5E

    races = list(RACAS_5E.keys())
    race_panel = RaceSelectionPanel(races)
    assert issubclass(RaceSelectionPanel, GenericSelectionPanel)
    assert race_panel.items == races
    assert race_panel.racas_data == RACAS_5E
    assert len(race_panel.rects) == len(races)

    classes = list(CLASSES.keys())
    class_panel = ClassSelectionPanel(classes)
    assert issubclass(ClassSelectionPanel, GenericSelectionPanel)
    assert class_panel.items == classes
    assert class_panel.class_data == CLASSES

    bgs = list(ANTECEDENTES_5E.keys())
    bg_panel = BackgroundSelectionPanel(bgs)
    assert issubclass(BackgroundSelectionPanel, GenericSelectionPanel)
    assert bg_panel.items == bgs
    assert bg_panel.bg_data == ANTECEDENTES_5E

    aligns = list(TENDENCIAS_5E.keys())
    align_panel = AlignmentSelectionPanel(aligns)
    assert issubclass(AlignmentSelectionPanel, GenericSelectionPanel)
    assert align_panel.items == aligns
    assert align_panel.al_data == TENDENCIAS_5E

    # Teste de render e hover sem erro
    screen = _get_screen()
    race_panel.is_visible = True
    race_panel.hover_item = races[0]
    race_panel.draw(screen)

    # Teste de evento
    mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": race_panel.rects[0][0].center})
    selected = race_panel.handle_event(mock_event)
    assert selected == races[0]


def test_scene_renderer_shadow_cache_and_chat_optimization():
    """Valida o cache de sombras, cache do painel lateral e pré-cálculo de mensagens com limite de 40."""
    from ui.scene_renderer import SceneRenderer

    renderer = SceneRenderer(1280, 720)
    screen = _get_screen()

    # Valida shadow cache em draw_board_token
    token_surf = pygame.Surface((64, 64))
    assert 64 not in renderer._shadow_cache
    renderer.draw_board_token(screen, token_surf, 100, 100, 64)
    assert 64 in renderer._shadow_cache
    cached_shadow = renderer._shadow_cache[64]
    renderer.draw_board_token(screen, token_surf, 100, 100, 64)
    assert renderer._shadow_cache[64] is cached_shadow

    # Valida adição de mensagens pré-formatadas
    renderer.add_combat_log("O guerreiro desferiu um golpe devastador!")
    assert len(renderer.chat_history) == 1
    assert len(renderer._formatted_messages) == 1
    msg_formatted = renderer._formatted_messages[0]
    assert "lines" in msg_formatted
    assert "h" in msg_formatted
    assert msg_formatted["h"] > 0
    assert len(msg_formatted["lines"]) >= 1

    # Valida limite estrito de 40 mensagens
    for i in range(50):
        renderer.add_combat_log(f"Mensagem de combate número {i}")

    assert len(renderer.chat_history) == 40
    assert len(renderer._formatted_messages) == 40
    assert renderer.chat_history[-1]["text"] == "Mensagem de combate número 49"

    # Valida draw_side_dialog_panel com reutilização de superfícies
    renderer.draw_side_dialog_panel(screen, {"text": "Narrador falando algo crucial", "type": "narrative", "npc_falando": "Mestre"})
    assert len(renderer.chat_history) == 40
    panel_w = int(1280 * 0.40)
    assert len(renderer._panel_bg_cache) >= 1
    bg_key = [k for k in renderer._panel_bg_cache.keys() if k[0] == panel_w][0]
    cached_bg = renderer._panel_bg_cache[bg_key]

    # Próximo frame deve reutilizar a mesma Surface de fundo do painel
    renderer.draw_side_dialog_panel(screen, None)
    assert renderer._panel_bg_cache[bg_key] is cached_bg


def test_beat_transition_scene_epic_act_interludes():
    """Valida o sistema aprimorado de Interlúdios de Ato Épicos (Beats 1, 6, 11 e 15)."""
    from ui.scene_renderer import BeatTransitionScene, ACT_INTERLUDES

    scene = BeatTransitionScene(1280, 720)
    screen = _get_screen()

    # 1. Verifica superfícies pré-alocadas no __init__ (Zero Garbage por frame)
    assert hasattr(scene, "overlay_surf")
    assert hasattr(scene, "overlay_interlude_surf")
    assert hasattr(scene, "card_surf")
    assert hasattr(scene, "card_interlude_surf")
    assert scene.card_interlude_w > scene.card_w
    assert scene.card_interlude_h > scene.card_h

    long_lore = (
        "Uma lenda ancestral diz que nas profundezas da montanha, o calor ardente consome os fracos.\n"
        "As chamas nunca cessam e o céu se tingiu de vermelho sangue sobre as planícies.\n"
        "Guerreiros marcharam para o abismo e poucos retornaram para contar o que viram.\n"
        "O aço das espadas foi forjado no coração do vulcão primordial.\n"
        "Agora, a hora final se aproxima e o destino de todos repousa sobre seus ombros.\n"
        "Prepare-se para o maior confronto de sua vida diante do trono de cinzas."
    )

    # 2. Beat 1: Detectado automaticamente como Interlúdio de Ato (Ato I)
    scene.start_transition(1, "Taverna do Dragão", long_lore, "tavern_bg.jpg")
    assert scene.is_act_interlude is True
    assert scene.interlude_info["act_title"] == "Ato I"
    assert scene.interlude_info["subtitle"] == "As Sombras se Alastram"
    assert 4 < len(scene.desc_lines) <= 8 # Interlúdio suporta mais linhas (até 8)

    scene.draw(screen)
    assert scene.is_active

    # 3. Beat 2: Transição padrão de capítulo (não é interlúdio)
    scene.start_transition(2, "Planície dos Uivos", long_lore, "plains_bg.jpg")
    assert scene.is_act_interlude is False
    assert len(scene.desc_lines) <= 4 # Transição padrão limita a 4 linhas

    scene.draw(screen)
    assert scene.is_active

    # 4. Beats 6, 11 e 15: Devem ser detectados como Interlúdios de Ato
    for b in [6, 11, 15]:
        scene.start_transition(b, f"Local do Beat {b}", "Descrição rápida", "bg.jpg")
        assert scene.is_act_interlude is True
        assert b in ACT_INTERLUDES
        scene.draw(screen)

    # 5. Parâmetro explícito is_act_interlude=True em beat normal
    scene.start_transition(3, "Floresta Misteriosa", "Texto", "bg.jpg", is_act_interlude=True)
    assert scene.is_act_interlude is True

