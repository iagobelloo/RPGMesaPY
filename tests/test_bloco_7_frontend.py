import os
import pygame
import pytest
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster
from ui.hud_components import GrimoireModal
from ui.scene_renderer import SceneRenderer

class MockAI(AIGameMaster):
    def parse_player_intent(self, user_input, game_state):
        return {"tipo_acao": "INTERAGIR_AMBIENTE", "alvo": [], "recurso_utilizado": None, "intencao_cena": "Nada"}

    def generate_narrative_from_math(self, sys_log, intent):
        return f"Narrativa: {sys_log}"

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1280, 720))
    yield
    pygame.quit()

def test_grimoire_initialization_and_tabs():
    modal = GrimoireModal(100, 100, 800, 600)
    modal.is_visible = True
    assert modal.active_tab in ("habilidades", "items")
    assert modal.tab_items_rect.width > 0
    assert modal.tab_spells_rect.width > 0

    # Simula clique na aba de magias
    dummy_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": modal.tab_spells_rect.center, "button": 1})
    res = modal.handle_event(dummy_event)
    assert modal.active_tab == "spells"
    assert res == ""

    # Simula clique de volta na aba de itens/status
    dummy_event_items = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": modal.tab_items_rect.center, "button": 1})
    res_i = modal.handle_event(dummy_event_items)
    assert modal.active_tab in ("items", "status")
    assert res_i == ""

def test_grimoire_consumables_and_use_button():
    modal = GrimoireModal(100, 100, 800, 600)
    modal.is_visible = True
    modal.active_tab = "items"
    screen = pygame.display.get_surface()

    mock_state = {
        "player_character": {
            "name": "Aragorn",
            "race": "Humano",
            "class": "Guerreiro",
            "level": 3,
            "hp_current": 15,
            "hp_max": 30,
            "xp": 500,
            "xp_to_next_level": 1000,
            "inventory": ["Poção de Cura", "Espada Longa"],
            "equipment": {"weapon": "Espada Longa", "armor": "Cota de Malha"}
        },
        "inventory": {"i_potion_healing": 2, "i_scroll_revive": 1}
    }
    modal.game_state_ref = mock_state

    consumables = modal._get_player_consumables()
    assert len(consumables) >= 2
    item_ids = [c["id"] for c in consumables]
    assert "i_potion_healing" in item_ids
    assert "i_scroll_revive" in item_ids

    # Desenha o modal para popular as hitboxes dos botões
    modal.draw(screen)
    assert "i_potion_healing" in modal._item_buttons
    btn_rect = modal._item_buttons["i_potion_healing"]

    # Simula clique no botão [Usar]
    click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": btn_rect.center, "button": 1})
    action = modal.handle_event(click_event)
    assert action == "use_item:i_potion_healing"

def test_grimoire_spells_and_cast_button():
    modal = GrimoireModal(100, 100, 800, 600)
    modal.is_visible = True
    modal.active_tab = "spells"
    screen = pygame.display.get_surface()

    mock_state = {
        "player_character": {
            "name": "Gandalf",
            "race": "Humano",
            "class": "Mago",
            "level": 3,
            "hp_current": 18,
            "hp_max": 20,
            "spell_slots": {"1": 3, "2": 1},
            "spells": ["s_magic_missile", "s_fireball"]
        }
    }
    modal.game_state_ref = mock_state

    spells = modal._get_player_spells()
    assert len(spells) >= 1

    modal.draw(screen)
    assert len(modal._spell_buttons) >= 1

    # Testa clique no botão de conjurar primeira magia
    spell_id = list(modal._spell_buttons.keys())[0]
    btn_rect = modal._spell_buttons[spell_id]

    click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": btn_rect.center, "button": 1})
    action = modal.handle_event(click_event)
    assert action == f"cast_spell:{spell_id}"

def test_fastpath_item_use_in_engine():
    ai = MockAI()
    session = SessionManager(ai)
    session.game_state["player_character"] = {
        "name": "Thrain",
        "hp_current": 10,
        "hp_max": 30,
        "inventory": {"i_potion_healing": 2}
    }
    session.game_state["inventory"] = {"i_potion_healing": 2}
    session.game_mode = "EXPLORACAO"

    # Executa atalho direto use_item
    session._async_turn_processor("use_item:i_potion_healing", [], [])

    # HP deve ter aumentado
    assert session.game_state["player_character"]["hp_current"] > 10
    # Quantidade deve ter diminuído para 1
    assert session.get_inventory_item_count("i_potion_healing") == 1

def test_fastpath_cast_spell_in_engine():
    ai = MockAI()
    session = SessionManager(ai)
    session.story.current_beat = 1
    session.game_state["player_character"] = {
        "name": "Elminster",
        "hp_current": 20,
        "hp_max": 20,
        "spell_slots": {"1": 3, "2": 0},
        "inventory": {}
    }
    session.active_combat_targets = {
        "m_goblin_1": {"name": "m_goblin_1", "faction": "enemy", "pv_atual": 60, "pv_max": 60, "ca": 12, "status": "vivo"}
    }
    session.game_mode = "COMBATE"

    # Conjura Mísseis Mágicos direto
    session._async_turn_processor("cast_spell:s_magic_missile", [], [])

    # Deve ter consumido slot de nível 1
    slots = session.game_state["player_character"]["spell_slots"]
    assert slots["1"] == 2
    # Goblin deve ter tomado dano
    assert session.active_combat_targets["m_goblin_1"]["pv_atual"] < 60

def test_scene_renderer_allies_party_rendering():
    renderer = SceneRenderer(1280, 720)
    screen = pygame.display.get_surface()

    ai = MockAI()
    session = SessionManager(ai)
    session.game_state["player_character"] = {
        "name": "Heroi",
        "race": "Humano",
        "class": "Guerreiro",
        "hp_current": 40,
        "hp_max": 40
    }
    # Adiciona aliados na party em combate
    session.active_combat_targets = {
        "Thorin": {"name": "Thorin", "race": "Anão", "class": "Clérigo", "faction": "ally", "pv_atual": 25, "pv_max": 30, "status": "vivo"},
        "Legolas": {"name": "Legolas", "race": "Elfo", "class": "Patrulheiro", "faction": "ally", "pv_atual": 20, "pv_max": 22, "status": "vivo"},
        "Dragão": {"name": "Dragão", "faction": "enemy", "pv_atual": 100, "pv_max": 100, "ca": 14, "tipo_bestiario": "dragao", "status": "vivo"}
    }
    session.active_visual_npcs = {
        "Thorin": "clerigo",
        "Legolas": "patrulheiro",
        "Dragão": "dragao"
    }

    hitboxes = renderer.draw_in_game(screen, session)
    # Jogador deve ter hitbox
    assert "player" in hitboxes
    # Aliados devem ter hitboxes na party
    assert "Thorin" in hitboxes or "ally_1" in hitboxes
    assert "Legolas" in hitboxes or "ally_2" in hitboxes

def test_deja_vu_background_and_cutscene_switch():
    ai = MockAI()
    session = SessionManager(ai)
    session.story.current_beat = 15
    session.game_mode = "COMBATE"
    session.game_state["player_character"] = {
        "name": "Heroi",
        "hp_current": 0,
        "hp_max": 50,
        "xp": 1000,
        "status": "morto"
    }
    session.game_state["meta"] = {"loop_count": 0, "segredo_tirano": False}
    session.active_combat_targets = {
        "m_supreme_dragon": {"name": "Tirano", "faction": "enemy", "ca": 99, "pv_max": 999, "pv_atual": 999}
    }

    # Dispara a morte no Boss (Loop 0)
    session.resolve_player_death()

    # Cenário deve mudar para a arte do Déjà Vu
    assert session.game_state.get("current_background") == "deja_vu_bg.jpg"
    # Segredo ativado e loop avançado
    assert session.game_state["meta"]["loop_count"] == 1
    assert session.game_state["meta"]["segredo_tirano"] is True

    # Mensagens de narrativa e sistema na fila
    narrativas = []
    while not session.ui_queue.empty():
        item = session.ui_queue.get()
        if "narrativa" in item:
            narrativas.append(item["narrativa"])
        elif item.get("type") == "narrative":
            narrativas.append(item.get("content"))

    # Confirma que a cutscene de morte beat_15_loop_0_death foi emitida
    assert any("Tirano das Cinzas" in str(n) or "Déjà Vu" in str(n) for n in narrativas)
