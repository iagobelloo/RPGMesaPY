"""
Módulo Principal do VTT (Front-End Pygame) - RPGMesaPY.
Orquestra a Interface Gráfica, capturando cliques e delegando ao SessionManager.

Desenvolvido por Inteligência Artificial (Google Antigravity / Gemini)
sob direção criativa e comando de Iago Bello (@iagobelloo).
"""
import os
import sys
import queue
import re
import threading
import pygame

# Importação dos Módulos do Backend (Regras e IA)
from core.game_engine import SessionManager, CharacterBuilder
from core.dnd_rules import RACAS_5E, CLASSES, ANTECEDENTES_5E, TENDENCIAS_5E, BESTIARIO_5E
from core.audio_manager import AudioManager
from ai_master.ai_client import AIGameMaster

# Importação dos Componentes Visuais (HUD, Menus e Assets)
from ui.asset_manager import AssetManager
from ui.hud_components import (
    COLOR_BG,
    MainMenuPanel,
    GrimoireModal,
    BackpackModal,
    ChatBox,
    LoadingDiceAnimation,
    QuickActionBar,
    PlayerManualModal,
)
from ui.widgets import MainMenuWidget, InGameHUD, CONSUMED, BarMode
from ui.menu_components import (
    CharacterCreationPanel,
    PauseMenuPanel,
    JournalModal,
    SaveSelectionPanel,
)
from ui.scene_renderer import SceneRenderer, BeatTransitionScene

# Resolução base
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60


def main():
    """Função de inicialização e Loop Gráfico Principal."""

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Crônicas da Taverna - D&D 5e VTT")

    # Carregamento Dinâmico Inquebrável de Assets (Requer Display inicializado para .convert())
    AssetManager.load_backgrounds()
    clock = pygame.time.Clock()

    audio = AudioManager.get_instance()
    audio.play_bgm("main_theme")

    print("[SYSTEM] Conectando ao AI Game Master...")
    ai_master = AIGameMaster()
    session = SessionManager(ai_master)

    # --- Instanciação dos Modais e Telas (UI) ---
    menu_width, menu_height = 400, 350
    menu_x = (WINDOW_WIDTH - menu_width) // 2
    menu_y = (WINDOW_HEIGHT - menu_height) // 2

    bg_menu = AssetManager.get_background("tavern_bg.jpg")
    main_menu = MainMenuWidget(background=bg_menu)
    hud = InGameHUD()

    save_selection_panel = SaveSelectionPanel(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    creation_menu = CharacterCreationPanel(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    pause_menu = PauseMenuPanel(menu_x, menu_y, 400, 350)
    journal_modal = JournalModal(menu_x - 100, menu_y - 100, 600, 500)
    journal_modal.game_state_ref = session.game_state

    grimoire = GrimoireModal((WINDOW_WIDTH - 800) // 2, (WINDOW_HEIGHT - 600) // 2, 800, 600)
    grimoire.game_state_ref = session.game_state
    grimoire.session_ref = session
    grimoire.is_visible = False
    grimoire.active_tab = "habilidades"

    backpack = BackpackModal((WINDOW_WIDTH - 840) // 2, (WINDOW_HEIGHT - 560) // 2, 840, 560)
    backpack.game_state_ref = session.game_state
    backpack.is_visible = False

    player_manual = PlayerManualModal((WINDOW_WIDTH - 840) // 2, (WINDOW_HEIGHT - 560) // 2, 840, 560)
    player_manual.is_visible = False

    dice_anim = LoadingDiceAnimation()

    scene_renderer = SceneRenderer(WINDOW_WIDTH, WINDOW_HEIGHT)
    beat_transition_scene = BeatTransitionScene(WINDOW_WIDTH, WINDOW_HEIGHT)

    # --- Máquina de Estados ---
    current_state = "MAIN_MENU"
    main_menu.is_visible = True

    # --- Variáveis In-Game ---
    player_chat_input = ""
    is_ai_thinking = False
    current_bubble_message = None
    last_hitboxes = {}
    # --- Overlays translúcidos pré-alocados (Zero Garbage por frame / 60 FPS) ---
    overlay_pause = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay_pause.fill((0, 0, 0, 150))
    overlay_grimoire = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay_grimoire.fill((0, 0, 0, 180))
    running = True
    dt = 0.016

    while running:
        # --- CAPTURA DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Atalho Global F1 ou H para alternar o Manual do Jogador
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_F1, pygame.K_h):
                is_typing = (current_state == "CHARACTER_CREATION" and getattr(creation_menu, "active_input", False))
                if not is_typing:
                    player_manual.is_visible = not player_manual.is_visible
                    continue

            # Se o Manual do Jogador estiver aberto, consome os eventos prioritariamente
            if player_manual.is_visible:
                m_act = player_manual.handle_event(event)
                if m_act == "close":
                    player_manual.is_visible = False
                continue

            # Delegação de Estado: MAIN MENU
            if current_state == "MAIN_MENU":
                action = main_menu.handle_event(event)
                if action == "action_quit":
                    running = False
                elif action == "action_player_manual":
                    player_manual.is_visible = True
                elif action == "action_new_game":
                    session = SessionManager(ai_master)
                    # Determina o primeiro slot vazio como padrão para o novo herói (1, 2 ou 3)
                    first_empty_slot = 1
                    for s in [1, 2, 3]:
                        meta = SessionManager.get_slot_metadata(s)
                        if meta.get("is_empty"):
                            first_empty_slot = s
                            break
                    session.current_save_slot = first_empty_slot

                    journal_modal.game_state_ref = session.game_state
                    grimoire.game_state_ref = session.game_state
                    grimoire.session_ref = session
                    backpack.game_state_ref = session.game_state
                    current_bubble_message = None
                    last_hitboxes = {}
                    creation_menu.reset()
                    main_menu.is_visible = False
                    creation_menu.is_visible = True
                    current_state = "CHARACTER_CREATION"
                elif action == "action_load_game" or (event.type == pygame.MOUSEBUTTONDOWN and main_menu.btn_load_game.collidepoint(event.pos)):
                    save_selection_panel.mode = "load"
                    save_selection_panel.refresh_slots()
                    main_menu.is_visible = False
                    save_selection_panel.is_visible = True
                    current_state = "SAVE_SELECTION"

            # Delegação de Estado: SAVE SELECTION (3 SLOTS)
            elif current_state == "SAVE_SELECTION":
                save_action = save_selection_panel.handle_event(event)
                if save_action in ("back_to_menu", "back_to_game"):
                    save_selection_panel.is_visible = False
                    if getattr(save_selection_panel, "mode", "load") == "save" and session.game_state.get("player_character"):
                        pause_menu.is_visible = True
                        current_state = "PAUSE_MENU"
                    else:
                        main_menu.is_visible = True
                        current_state = "MAIN_MENU"
                elif isinstance(save_action, tuple):
                    cmd, slot_num = save_action
                    if cmd == "load_slot":
                        if session.load_game(slot_num):
                            print(f"[Sistema] Jogo Carregado com Sucesso do Slot {slot_num}!")
                            journal_modal.game_state_ref = session.game_state
                            grimoire.game_state_ref = session.game_state
                            grimoire.session_ref = session
                            backpack.game_state_ref = session.game_state
                            save_selection_panel.is_visible = False
                            current_state = "IN_GAME"
                            session._push_event("system_event", {"text": f"O Mestre retoma as crônicas do Registro {slot_num}..."})
                        else:
                            print(f"[Sistema] Nenhum save encontrado no Slot {slot_num}.")
                    elif cmd in ("save_slot", "new_game_slot"):
                        if getattr(save_selection_panel, "mode", "load") == "load" or cmd == "new_game_slot" or not session.game_state.get("player_character"):
                            session = SessionManager(ai_master)
                            session.current_save_slot = slot_num
                            journal_modal.game_state_ref = session.game_state
                            grimoire.game_state_ref = session.game_state
                            grimoire.session_ref = session
                            backpack.game_state_ref = session.game_state
                            current_bubble_message = None
                            last_hitboxes = {}
                            creation_menu.reset()
                            save_selection_panel.is_visible = False
                            creation_menu.is_visible = True
                            current_state = "CHARACTER_CREATION"
                        else:
                            session.save_game(slot=slot_num)
                            session.current_save_slot = slot_num
                            session._push_event("system_event", {"text": f"Jogo gravado com sucesso no Pergaminho {slot_num}!"})
                            save_selection_panel.refresh_slots()
                            save_selection_panel.is_visible = False
                            current_state = "IN_GAME"
                    elif cmd == "delete_slot":
                        SessionManager.delete_save_slot(slot_num)
                        save_selection_panel.refresh_slots()

            # Delegação de Estado: CHARACTER CREATION
            elif current_state == "CHARACTER_CREATION":
                char_data = creation_menu.handle_event(event)

                if char_data:
                    if char_data.get("action") == "cancel":
                        creation_menu.is_visible = False
                        main_menu.is_visible = True
                        current_state = "MAIN_MENU"
                    elif char_data.get("action") == "start":
                        final_char = char_data["char"]
                        session.game_state["player_character"] = final_char

                        creation_menu.is_visible = False
                        is_ai_thinking = False

                        # Carregamento do Prólogo Personalizado
                        try:
                            prologue_text = ai_master.get_personalized_prologue(final_char)
                        except Exception as e:
                            print(f"Erro ao carregar o prólogo personalizado: {e}")
                            prologue_text = f"Você é {final_char.get('name', 'o herói')}, um {final_char.get('race', 'Humano')} {final_char.get('class', 'Guerreiro')}. Sua lenda começa agora nas terras sombrias do reino!"
                        session.game_state["prologue"] = prologue_text
                        session.game_state["recent_history"].append(f"Prólogo: {prologue_text}")

                        # Inicia a transição de capítulo com o prólogo do personagem na tela
                        beat_data = session.story.campaign_data.get("1", {})
                        beat_transition_scene.start_transition(
                            beat_num=1,
                            beat_name=beat_data.get("name", "Taverna do Dragão Acordado"),
                            description=prologue_text,
                            bg_image=beat_data.get("bg_image", "tavern_bg.jpg")
                        )
                        current_state = "BEAT_TRANSITION"

                        # Diálogo acolhedor do taverneiro/menestrel para quando o chat abrir limpo
                        tavern_greeting = (
                            "O taverneiro limpa uma caneca de madeira com um pano encardido e o menestrel dedilha seu alaúde ao canto da lareira: "
                            f"'Saudações, {final_char.get('name', 'forasteiro')}! Que os deuses guardem seus passos. O que traz um {final_char.get('race', 'aventureiro')} "
                            f"{final_char.get('class', '')} como você à Taverna do Dragão Acordado sob a tempestade?'"
                        )
                        current_bubble_message = {"text": tavern_greeting, "type": "narrative", "npc_falando": "Taverneiro"}

            # Delegação de Estado: IN GAME
            elif current_state == "IN_GAME":
                if backpack.is_visible:
                    bp_action = backpack.handle_event(event)
                    if bp_action == "close_backpack":
                        backpack.is_visible = False
                    elif bp_action.startswith("equip_weapon:"):
                        weapon_name = bp_action.split(":", 1)[1]
                        pc = session.game_state.get("player_character")
                        if hasattr(session, "equip_item"):
                            res = session.equip_item(weapon_name)
                            msg = res.get("message", f"Equipado: {weapon_name}") if isinstance(res, dict) else f"Equipado: {weapon_name}"
                            scene_renderer.add_combat_log(msg)
                            session._push_event("system_event", {"text": f"⚔️ {msg}"})
                        elif pc:
                            pc["equipped_weapon"] = weapon_name
                            if isinstance(pc.get("equipment"), dict):
                                pc["equipment"]["weapon"] = weapon_name
                            scene_renderer.add_combat_log(f"Arma equipada: {weapon_name}")
                            session._push_event("system_event", {"text": f"⚔️ Você empunha {weapon_name} como arma principal!"})
                    elif bp_action.startswith("use_item:"):
                        backpack.is_visible = False
                        current_bubble_message = None
                        is_ai_thinking = True
                        current_state = "AGUARDANDO_IA"
                        bgs = AssetManager.get_narrative_backgrounds()
                        lista_bestiario = list(BESTIARIO_5E.keys())
                        session.process_action_async(bp_action, bgs, lista_bestiario)

                elif grimoire.is_visible:
                    grimoire_action = grimoire.handle_event(event)
                    if grimoire_action == "close_grimoire":
                        grimoire.is_visible = False
                    elif grimoire_action == "open_backpack":
                        grimoire.is_visible = False
                        backpack.is_visible = True
                    elif grimoire_action == "open_level_up_modal":
                        pass
                    elif grimoire_action.startswith("cast_spell:") or grimoire_action.startswith("use_skill:") or grimoire_action == "level_up" or grimoire_action.startswith("travel_side_quest:") or grimoire_action.startswith("accept_side_quest:"):
                        grimoire.is_visible = False
                        current_bubble_message = None
                        is_ai_thinking = True
                        current_state = "AGUARDANDO_IA"

                        action_to_dispatch = "subir de nivel" if grimoire_action == "level_up" else grimoire_action
                        if grimoire_action.startswith("use_skill:"):
                            skill_label = grimoire_action.split("|")[-1] if "|" in grimoire_action else grimoire_action.replace("use_skill:", "")
                            pc_name = session.game_state.get("player_character", {}).get("name", "Herói")
                            scene_renderer._add_chat_message({"text": f"⚡ Usou habilidade: {skill_label}", "type": "player", "npc_falando": pc_name})
                        bgs = AssetManager.get_narrative_backgrounds()
                        lista_bestiario = list(BESTIARIO_5E.keys())
                        session.process_action_async(action_to_dispatch, bgs, lista_bestiario)

                if not grimoire.is_visible and not backpack.is_visible:
                    # Delega eventos prioritariamente ao InGameHUD (Hotbar, Chat, Dock, Iniciativa, Card)
                    hud_action = hud.handle_event(event)
                    if hud_action == CONSUMED:
                        continue

                    if hud_action:
                        if hud_action.startswith("say:"):
                            cmd_text = hud_action[4:].strip()
                            if cmd_text and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                                pc_name = session.game_state.get("player_character", {}).get("name", "Herói")
                                hud.push_narration(pc_name, cmd_text, "player")
                                scene_renderer._add_chat_message({"text": cmd_text, "type": "player", "npc_falando": pc_name})
                                current_bubble_message = None
                                is_ai_thinking = True
                                current_state = "AGUARDANDO_IA"
                                bgs = AssetManager.get_narrative_backgrounds()
                                lista_bestiario = list(BESTIARIO_5E.keys())
                                session.process_action_async(cmd_text, bgs, lista_bestiario)

                        elif hud_action.startswith("select_target:"):
                            target_uid = hud_action.split(":", 1)[1]
                            scene_renderer.selected_target_id = target_uid

                        elif hud_action == "inventory":
                            backpack.is_visible = True
                            grimoire.is_visible = False

                        elif hud_action == "grimoire":
                            grimoire.is_visible = True
                            backpack.is_visible = False

                        elif hud_action == "system_menu":
                            current_state = "PAUSE_MENU"
                            pause_menu.is_visible = True

                        elif hud_action == "skills":
                            s_list = session.get_available_skills()
                            hud.action_bar.open_skills_flyout(s_list)

                        elif hud_action == "spells":
                            sp_list = session.get_available_spells()
                            hud.action_bar.open_spells_flyout(sp_list)

                        elif hud_action == "attack" and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            target_name = "o inimigo"
                            combat_targets = getattr(session, "active_combat_targets", {}) or {}
                            selected_id = getattr(scene_renderer, "selected_target_id", None)
                            if selected_id and selected_id in combat_targets:
                                t_data = combat_targets[selected_id]
                                target_name = (t_data.get("name") if isinstance(t_data, dict) else None) or selected_id
                            elif combat_targets:
                                living = [t for t in combat_targets.values() if isinstance(t, dict) and t.get("status") != "morto" and t.get("faction") != "ally"]
                                if living:
                                    target_name = living[0].get("name") or living[0].get("id") or "o inimigo"
                            attack_cmd = f"Atacar {target_name}"
                            pc_name = session.game_state.get("player_character", {}).get("name", "Herói")
                            hud.push_narration(pc_name, attack_cmd, "player")
                            scene_renderer._add_chat_message({"text": attack_cmd, "type": "player", "npc_falando": pc_name})
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async(attack_cmd, bgs, lista_bestiario)

                        elif hud_action == "dodge" and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            pc_name = session.game_state.get("player_character", {}).get("name", "Herói")
                            hud.push_narration(pc_name, "🛡 Assumiu postura defensiva total (Esquivar / Dodge)!", "player")
                            scene_renderer._add_chat_message({"text": "🛡 Assumiu postura defensiva total (Esquivar / Dodge). Ataques contra você terão Desvantagem!", "type": "player", "npc_falando": pc_name})
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async("Esquivar dos ataques adotando postura defensiva total (Dodge).", bgs, lista_bestiario)

                        elif hud_action == "disengage" and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            pc_name = session.game_state.get("player_character", {}).get("name", "Herói")
                            hud.push_narration(pc_name, "🏃 Recuou cautelosamente (Desengajar / Disengage)!", "player")
                            scene_renderer._add_chat_message({"text": "🏃 Recuou cautelosamente da linha de frente (Desengajar / Disengage)!", "type": "player", "npc_falando": pc_name})
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async("Recuar cautelosamente sem provocar ataques de oportunidade (Disengage).", bgs, lista_bestiario)

                        elif hud_action == "observe" and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async("Observo atentamente o cenário ao redor, procurando detalhes, pistas e perigos.", bgs, lista_bestiario)

                        elif hud_action == "talk" and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async("Aproximo-me e tento conversar com quem estiver por perto para obter informações.", bgs, lista_bestiario)

                        elif hud_action == "rest" and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async("Descansar", bgs, lista_bestiario)

                        elif hud_action == "travel" and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async("Partir para o próximo destino da jornada.", bgs, lista_bestiario)

                        elif hud_action.startswith("use_skill:") and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            skill_payload = hud_action.split("use_skill:", 1)[1].strip()
                            target_name = ""
                            selected_id = getattr(scene_renderer, "selected_target_id", None)
                            combat_targets = getattr(session, "active_combat_targets", {}) or {}
                            if selected_id and selected_id in combat_targets:
                                t_data = combat_targets[selected_id]
                                target_name = (t_data.get("name") if isinstance(t_data, dict) else None) or selected_id
                            cmd_str = f"use_skill:{skill_payload}|{target_name}" if target_name else f"use_skill:{skill_payload}"
                            display_name = skill_payload.split("|")[-1] if "|" in skill_payload else skill_payload
                            pc_name = session.game_state.get("player_character", {}).get("name", "Herói")
                            hud.push_narration(pc_name, f"⚡ Usou habilidade: {display_name}", "player")
                            scene_renderer._add_chat_message({"text": f"⚡ Usou habilidade: {display_name}", "type": "player", "npc_falando": pc_name})
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async(cmd_str, bgs, lista_bestiario)

                        elif hud_action.startswith("cast_spell:") and not is_ai_thinking and session.game_mode not in ["EPILOGO", "GAME_OVER"]:
                            spell_name = hud_action.split("cast_spell:", 1)[1].strip()
                            target_name = ""
                            selected_id = getattr(scene_renderer, "selected_target_id", None)
                            combat_targets = getattr(session, "active_combat_targets", {}) or {}
                            if selected_id and selected_id in combat_targets:
                                t_data = combat_targets[selected_id]
                                target_name = (t_data.get("name") if isinstance(t_data, dict) else None) or selected_id
                            cmd_str = f"cast_spell:{spell_name}:{target_name}" if target_name else f"cast_spell:{spell_name}"
                            pc_name = session.game_state.get("player_character", {}).get("name", "Herói")
                            hud.push_narration(pc_name, f"✨ Conjurou magia: {spell_name}", "player")
                            scene_renderer._add_chat_message({"text": f"✨ Conjurou magia: {spell_name}", "type": "player", "npc_falando": pc_name})
                            current_bubble_message = None
                            is_ai_thinking = True
                            current_state = "AGUARDANDO_IA"
                            bgs = AssetManager.get_narrative_backgrounds()
                            lista_bestiario = list(BESTIARIO_5E.keys())
                            session.process_action_async(cmd_str, bgs, lista_bestiario)

                    # Interação direta com o palco visual 2.5D (seleção de tokens de monstros e herói)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        clicked_enemy = None
                        combat_targets = getattr(session, "active_combat_targets", {}) or {}
                        for key, rect in last_hitboxes.items():
                            if rect.collidepoint(event.pos):
                                if key.startswith("enemy_") or key in combat_targets:
                                    clicked_enemy = key.replace("enemy_", "")
                                    break

                        if clicked_enemy:
                            # Apenas seleciona como alvo ativo (NUNCA dispara ataque automático)
                            scene_renderer.selected_target_id = clicked_enemy
                            t_data = combat_targets.get(clicked_enemy, {})
                            t_name = (t_data.get("name") if isinstance(t_data, dict) else None) or clicked_enemy
                            hud.action_bar.set_target(t_name)

                        elif "player" in last_hitboxes and last_hitboxes["player"].collidepoint(event.pos):
                            grimoire.is_visible = True

                    elif event.type == pygame.KEYDOWN and not hud.console.has_focus:
                        if event.key == pygame.K_ESCAPE:
                            current_state = "PAUSE_MENU"
                            pause_menu.is_visible = True
                        elif event.key == pygame.K_TAB:
                            grimoire.is_visible = not grimoire.is_visible

            # Delegação de Estado: PAUSE MENU
            elif current_state == "PAUSE_MENU":
                if journal_modal.is_visible:
                    if journal_modal.handle_event(event) == "close":
                        journal_modal.is_visible = False
                else:
                    action = pause_menu.handle_event(event)
                    if action == "resume":
                        pause_menu.is_visible = False
                        current_state = "IN_GAME"
                    elif action == "journal":
                        grimoire.active_tab = "diario"
                        grimoire.is_visible = True
                        pause_menu.is_visible = False
                        current_state = "IN_GAME"
                    elif action == "action_player_manual":
                        player_manual.is_visible = True
                    elif action == "save":
                        save_selection_panel.mode = "save"
                        save_selection_panel.refresh_slots()
                        pause_menu.is_visible = False
                        save_selection_panel.is_visible = True
                        current_state = "SAVE_SELECTION"
                    elif action == "quit":
                        pause_menu.is_visible = False
                        main_menu.is_visible = True
                        current_state = "MAIN_MENU"

            # Delegação de Estado: BEAT TRANSITION
            elif current_state == "BEAT_TRANSITION":
                if beat_transition_scene.handle_event(event):
                    current_state = "IN_GAME"
                    AssetManager.clear_cache(keep_fonts=True)
                    if current_bubble_message and not scene_renderer.chat_history:
                        scene_renderer._add_chat_message(current_bubble_message)
                        session.game_state["recent_history"].append(f"Taverneiro: {current_bubble_message['text']}")

        # --- PROCESSAMENTO DO CONTROLLER (POLLING) ---
        while session.ui_event_queue:
            ui_event = session.ui_event_queue.pop(0)
            event_type = ui_event.get("type")

            if event_type == "system_loading":
                current_bubble_message = {"text": "Rolando dados e consultando os deuses...", "type": "narrative"}
            elif event_type in ["damage", "heal", "system_event", "gain_xp", "gain_item"]:
                scene_renderer.handle_ui_event(ui_event, session.game_state)
                if event_type == "damage":
                    hud.push_narration("Combate", f"{ui_event.get('target')} sofreu {ui_event.get('amount', 0)} de dano.", "damage")
                elif event_type == "heal":
                    hud.push_narration("Cura", f"{ui_event.get('target')} recuperou {ui_event.get('amount', 0)} PV.", "narration")
                elif event_type == "gain_xp":
                    hud.push_narration("Experiência", f"+{ui_event.get('amount', 0)} XP", "system")
                elif event_type == "gain_item":
                    hud.push_narration("Item", f"+ {ui_event.get('item', '')}", "system")
            elif event_type in ["narrative", "dialogue"]:
                is_ai_thinking = False
                current_bubble_message = ui_event
                hud.push_narration(ui_event.get("npc_falando") or "Mestre", ui_event.get("text") or "", "narration")

        # --- RENDERIZAÇÃO (DRAWING) E POLLING DA FILA ---
        while True:
            try:
                msg = session.ui_queue.get_nowait()
            except queue.Empty:
                break

            is_ai_thinking = False
            if current_state == "AGUARDANDO_IA":
                current_state = "IN_GAME"

            msg_type = msg.get("type")
            # 0. Transição de Beat / Apresentação de Capítulo
            if msg_type == "beat_transition":
                beat_transition_scene.start_transition(
                    beat_num=msg.get("beat", 1),
                    beat_name=msg.get("name", ""),
                    description=msg.get("description", ""),
                    bg_image=msg.get("bg_image", "tavern_bg.jpg")
                )
                current_state = "BEAT_TRANSITION"
            # 1. Mensagem de Sistema / Combate / Rolagem de dados
            elif msg_type == "system_message":
                sys_text = msg.get("content", "")
                if sys_text:
                    scene_renderer.add_combat_log(sys_text)
                    hud.push_narration("Sistema", sys_text, "combat")
                    session.game_state["recent_history"].append(sys_text)
                    m_roll = re.search(r"d20[:\s\(]*(\d+)", sys_text, re.IGNORECASE)
                    if m_roll:
                        dice_anim.trigger_roll_result(int(m_roll.group(1)))
                    elif "CRÍTICO" in sys_text.upper() and "FALHA" not in sys_text.upper():
                        dice_anim.trigger_roll_result(20)
                    elif "FALHA CRÍTICA" in sys_text.upper():
                        dice_anim.trigger_roll_result(1)
            # 2. Mensagem narrativa explícita (type: narrative / dialogue)
            elif msg_type in ["narrative", "dialogue"]:
                content = msg.get("content", "")
                falante = msg.get("npc_falando") or "Mestre"
                if content:
                    current_bubble_message = {"text": content, "type": "narrative", "npc_falando": falante}
                    hud.push_narration(falante, content, "narration")
                    if not scene_renderer.chat_history or scene_renderer.chat_history[-1].get("text") != content:
                        scene_renderer._add_chat_message(current_bubble_message)
                        session.game_state["recent_history"].append(f"Mestre: {content}")
            # 3. Formato com chave 'narrativa'
            elif "narrativa" in msg:
                narrativa_data = msg["narrativa"]
                if isinstance(narrativa_data, dict):
                    texto = narrativa_data.get("texto", "")
                    falante = narrativa_data.get("npc_falando") or "Mestre"
                else:
                    texto = str(narrativa_data)
                    falante = msg.get("npc_falando") or "Mestre"
                if texto:
                    current_bubble_message = {"text": texto, "type": "narrative", "npc_falando": falante}
                    hud.push_narration(falante, texto, "narration")
                    if not scene_renderer.chat_history or scene_renderer.chat_history[-1].get("text") != texto:
                        scene_renderer._add_chat_message(current_bubble_message)
                        session.game_state["recent_history"].append(f"Mestre: {texto}")
            # 4. Outro formato genérico com texto
            else:
                fallback_txt = msg.get("text") or msg.get("content") or ""
                if fallback_txt:
                    scene_renderer.add_combat_log(fallback_txt)
                    hud.push_narration("Sistema", fallback_txt, "system")

        screen.fill(COLOR_BG)

        if current_state == "MAIN_MENU":
            main_menu.update(dt)
            main_menu.draw(screen)

        elif current_state == "SAVE_SELECTION":
            save_selection_panel.draw(screen)

        elif current_state == "CHARACTER_CREATION":
            creation_menu.draw(screen)

        elif current_state == "BEAT_TRANSITION":
            beat_transition_scene.draw(screen)

        elif current_state in ["IN_GAME", "PAUSE_MENU", "AGUARDANDO_IA"]:
            # Atualização e sincronização da nova HUD
            hud.update(dt)
            hud.sync(session)

            # Sincroniza alvo selecionado na Hotbar
            selected_id = getattr(scene_renderer, "selected_target_id", None)
            combat_targets = getattr(session, "active_combat_targets", {}) or {}
            if selected_id and selected_id in combat_targets:
                t_data = combat_targets[selected_id]
                t_name = (t_data.get("name") if isinstance(t_data, dict) else None) or selected_id
            elif combat_targets:
                living = [t for t in combat_targets.values() if isinstance(t, dict) and t.get("status") != "morto" and t.get("faction") != "ally"]
                t_name = living[0].get("name") or living[0].get("id") or None if living else None
            else:
                t_name = None
            hud.action_bar.set_target(t_name)

            # Renderiza o palco 2.5D sem HUD legada
            last_hitboxes = scene_renderer.draw_in_game(screen, session, current_bubble_message, render_legacy_hud=False)

            # Renderiza o HUD completo (5 blocos + tooltips no topo)
            hud.draw(screen)

            if current_state == "AGUARDANDO_IA":
                dice_anim.draw(screen, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            else:
                if dice_anim.is_showing_result():
                    dice_anim.draw(screen, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)

            if current_state == "PAUSE_MENU":
                screen.blit(overlay_pause, (0, 0))
                pause_menu.draw(screen)
                if journal_modal.is_visible:
                    journal_modal.draw(screen)

            if backpack.is_visible:
                screen.blit(overlay_grimoire, (0, 0))
                backpack.draw(screen)

            if grimoire.is_visible:
                screen.blit(overlay_grimoire, (0, 0))
                grimoire.draw(screen)

        if player_manual.is_visible:
            screen.blit(overlay_grimoire, (0, 0))
            player_manual.draw(screen)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000.0

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()