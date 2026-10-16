import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()
pygame.font.init()
pygame.display.set_mode((1280, 720))

from ui.scene_renderer import get_act_and_chapter_title, SceneRenderer, BeatTransitionScene
from core.game_engine import SessionManager
from ai_master.ai_client import AIGameMaster

class MockAI(AIGameMaster):
    def parse_player_intent(self, text, state):
        if any(w in text.lower() for w in ["avancar", "avançar", "sair", "viajar"]):
            return {"tipo_acao": "AVANCAR_HISTORIA", "recurso_utilizado": None, "alvo": [], "intencao_cena": "avançar"}
        return {"tipo_acao": "INTERAGIR_AMBIENTE", "recurso_utilizado": None, "alvo": [], "intencao_cena": "observar"}

    def generate_narrative_from_math(self, log, intent):
        return "Narrativa de transição mock."

def test_act_and_chapter_title_format():
    """Valida o formato canônico 'Ato I: Capítulo II' solicitado pelo usuário."""
    assert get_act_and_chapter_title(1)[0] == "Ato I: Capítulo I"
    assert get_act_and_chapter_title(2)[0] == "Ato I: Capítulo II"
    assert get_act_and_chapter_title(5)[0] == "Ato I: Capítulo V"
    assert get_act_and_chapter_title(6)[0] == "Ato II: Capítulo VI"
    assert get_act_and_chapter_title(10)[0] == "Ato II: Capítulo X"
    assert get_act_and_chapter_title(11)[0] == "Ato III: Capítulo XI"
    assert get_act_and_chapter_title(14)[0] == "Ato III: Capítulo XIV"
    assert get_act_and_chapter_title(15)[0] == "Ato III: O Clímax Final"

def test_monster_dimensions_hierarchy():
    """
    Valida que a hierarquia visual é estrita:
    Dragão Supremo > Gigante de Fogo > Ogros/Quimeras > Lobos Atrozes > Lich > Médios > Goblins.
    """
    dim_dragao = SceneRenderer._resolve_monster_dimensions("Tirano", "m_supreme_dragon")
    dim_gigante = SceneRenderer._resolve_monster_dimensions("Gigante", "m_fire_giant")
    dim_ogro = SceneRenderer._resolve_monster_dimensions("Ogro", "m_ogre")
    dim_lobo = SceneRenderer._resolve_monster_dimensions("Lobo", "m_dire_wolf")
    dim_lich = SceneRenderer._resolve_monster_dimensions("Lich", "m_lich")
    dim_medio = SceneRenderer._resolve_monster_dimensions("Bandido", "m_bandit")
    dim_goblin = SceneRenderer._resolve_monster_dimensions("Goblin", "m_goblin")
    
    # Dragão Supremo é indiscutivelmente o maior
    assert dim_dragao[0] > dim_gigante[0] and dim_dragao[1] > dim_gigante[1]
    # Gigante maior que Ogro
    assert dim_gigante[1] > dim_ogro[1]
    # Ogro maior que Lobo
    assert dim_ogro[1] > dim_lobo[1]
    # Médio maior que Goblin
    assert dim_medio[1] > dim_goblin[1]
    # Goblin é o menor
    assert dim_goblin[0] <= 70 and dim_goblin[1] <= 90

def test_beat_transition_scene_lifecycle():
    """Valida ciclo de vida, pré-alocação e resposta a eventos da BeatTransitionScene."""
    scene = BeatTransitionScene(1280, 720)
    assert not scene.is_active
    
    # Inicia transição para o Beat 2 (Planície dos Uivos)
    scene.start_transition(
        beat_num=2,
        beat_name="Planície dos Uivos",
        description="Uma planície vasta e varrida pelo vento, com grama alta escondendo perigos.",
        bg_image="dirt_road_plains_bg.jpg"
    )
    
    assert scene.is_active
    assert scene.current_beat == 2
    assert scene.beat_name == "Planície dos Uivos"
    assert len(scene.desc_lines) > 0
    
    # Evento de tecla neutra (não avança)
    dummy_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
    assert not scene.handle_event(dummy_event)
    assert scene.is_active
    
    # Evento de ENTER: 1º completa o typewriter (se em andamento), 2º avança/fecha a cena
    enter_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    res_first = scene.handle_event(enter_event)
    if scene.is_active:
        assert scene.handle_event(enter_event)
    else:
        assert res_first
    assert not scene.is_active

def test_engine_avancar_historia_dispatches_beat_transition():
    """Valida que o comando de avançar história despacha o evento de transição na ui_queue."""
    session = SessionManager(MockAI())
    session.game_state["player_character"] = {
        "name": "Thorin",
        "class": "Guerreiro",
        "race": "Anão",
        "hp_max": 25,
        "hp_current": 25
    }
    session.story.current_beat = 1 # Taverna
    session.game_mode = "EXPLORACAO"
    
    # Processa avanço de história
    session._async_turn_processor("sair da taverna e avancar na estrada", [], [])
    
    # O beat avançou para 2
    assert session.story.current_beat == 2
    
    # Coleta mensagens na fila da UI procurando beat_transition
    transition_msg = None
    while not session.ui_queue.empty():
        msg = session.ui_queue.get()
        if msg.get("type") == "beat_transition":
            transition_msg = msg
            break
            
    assert transition_msg is not None, "Evento 'beat_transition' não foi emitido!"
    assert transition_msg["beat"] == 2
    assert transition_msg["name"] == "Planície dos Uivos"
    assert "dirt_road_plains" in transition_msg["bg_image"]

def test_allies_adventuring_solo_until_climax():
    """
    Valida a regra solicitada pelo usuário:
    O jogador se aventura SOZINHO nos beats normais, e os aliados
    reunidos durante a jornada só entram no combate contra o dragão no Beat 15.
    """
    session = SessionManager(MockAI())
    pc = {
        "name": "Valeros",
        "class": "Guerreiro",
        "race": "Humano",
        "hp_max": 25,
        "hp_current": 25
    }
    session.game_state["player_character"] = pc
    session.game_mode = "EXPLORACAO"
    
    # Desbloqueia alguns aliados na campanha
    session.story.unlock_ally("cleric")
    session.story.unlock_ally("wizard")
    
    # Avança para Beat 4 (combate normal)
    session.story.current_beat = 3
    session._async_turn_processor("avancar para acampamento", [], [])
    
    assert session.story.current_beat == 4
    # No Beat 4, os aliados NÃO devem estar em active_combat_targets (apenas inimigos)
    allies_in_combat = [t for t in session.active_combat_targets.values() if t.get("faction") == "ally"]
    assert len(allies_in_combat) == 0, "Aliados não devem entrar em combate antes do Beat 15!"
    
    # Agora simula avanço até Beat 15 (Clímax do Dragão)
    session.active_combat_targets.clear()
    session.story.current_beat = 14
    session.game_mode = "EXPLORACAO"
    session._async_turn_processor("avancar para covil do dragao", [], [])
    
    assert session.story.current_beat == 15
    # No Beat 15, TODOS os aliados entram em campo contra o Dragão!
    climax_allies = [t for t in session.active_combat_targets.values() if t.get("faction") == "ally"]
    assert len(climax_allies) >= 2, "Aliados deveriam entrar em combate contra o Dragão no Clímax!"
