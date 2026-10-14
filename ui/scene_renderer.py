import pygame
from ui.asset_manager import AssetManager

class SceneRenderer:
    """Renderiza o estado "IN_GAME" na estética 'Knights of Pen & Paper'."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        from ui.asset_manager import AssetManager
        self.font_dmg = AssetManager.get_font(32)
        self.font_narrative = AssetManager.get_font(20)
        self.font_names = AssetManager.get_font(18)
        self.font_log = AssetManager.get_font(16)
        self.font_hud = AssetManager.get_font(14)
            
        self.font_dmg.set_bold(True)
        self.font_names.set_bold(True)
        
        self.floating_texts = []
        self.combat_log = []
        self.chat_history = []
        self._formatted_messages = []
        self._panel_bg_cache = {}
        self._shadow_cache = {}
        self._cached_panel_w = int(self.width * 0.40)
        self.last_msg_id = None
        self.scroll_y = 0
        
        from ui.hud_components import PlayerHUD
        self.player_hud = PlayerHUD(12, 12)
        self._hud_rect = pygame.Rect(12, 12, 0, 0)
        
    def add_floating_text(self, text: str, x: int, y: int, color: tuple):
        self.floating_texts.append({"text": text, "x": x, "y": y, "color": color, "timer": 60})

    def _format_chat_message(self, msg: dict, panel_w: int) -> dict:
        """Pré-calcula a quebra de linha e altura de uma mensagem no momento da inserção (Zero Garbage a 60 FPS)."""
        from ui.hud_components import get_wrapped_text_dimensions
        text_str = msg.get("text", "")
        falante = msg.get("npc_falando") or "nenhum"
        msg_type = msg.get("type", "narrative")
        
        font_to_use = self.font_narrative if msg_type == "narrative" else self.font_log
        
        has_portrait = falante.lower() != "nenhum" and msg_type == "narrative"
        if has_portrait:
            msg_w = panel_w - 120
        else:
            msg_w = panel_w - 55
            
        _, text_h, lines = get_wrapped_text_dimensions(text_str, font_to_use, msg_w)
        
        total_msg_h = text_h
        if has_portrait:
            total_msg_h = max(text_h + 30, 80)
            
        return {
            "msg": msg,
            "lines": lines,
            "h": total_msg_h,
            "has_portrait": has_portrait,
            "falante": falante,
            "font": font_to_use,
            "msg_type": msg_type,
            "msg_w": msg_w,
            "text_h": text_h
        }

    def _add_chat_message(self, msg: dict, panel_w: int = None):
        """Adiciona e pré-processa uma mensagem no histórico respeitando o limite de 40 itens."""
        if panel_w is None:
            panel_w = getattr(self, "_cached_panel_w", int(self.width * 0.40))
        self.chat_history.append(msg)
        formatted = self._format_chat_message(msg, panel_w)
        self._formatted_messages.append(formatted)
        if len(self.chat_history) > 40:
            self.chat_history.pop(0)
            self._formatted_messages.pop(0)
        
    def add_combat_log(self, text: str):
        msg = {"text": text, "npc_falando": "Sistema", "type": "combat"}
        self._add_chat_message(msg)

    def draw_top_hud(self, screen: pygame.Surface, player: dict) -> pygame.Rect:
        """Delegado ao PlayerHUD (painel retrô com layout vertical dinâmico)."""
        if not player:
            return self._hud_rect
        self._hud_rect = self.player_hud.draw(screen, player)
        return self._hud_rect

    @staticmethod
    def _resolve_npc_sprite(session, npc_id: str, tipo: str, target: dict) -> pygame.Surface:
        """Aliados -> sprite de herói (raça/classe); inimigos -> enemies/{id sem m_}.png."""
        if target and target.get("faction") == "ally":
            race, char_class, gender = target.get("race"), target.get("class"), target.get("gender")
            if not (race and char_class):
                story = getattr(session, "story", None)
                for ally in getattr(story, "allies_pool", {}).values():
                    if ally.get("name") == npc_id:
                        race, char_class = ally.get("race"), ally.get("class")
                        gender = gender or ally.get("gender")
                        break
            return AssetManager.get_hero_sprite(race, char_class, gender)
        return AssetManager.get_enemy_sprite(tipo or (target or {}).get("tipo_bestiario", ""))

    def draw_board_token(self, screen: pygame.Surface, image: pygame.Surface, x: int, y: int, size: int):
        if size not in self._shadow_cache:
            shadow_surf = pygame.Surface((size, size // 2), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surf, (0, 0, 0, 150), shadow_surf.get_rect())
            self._shadow_cache[size] = shadow_surf
        screen.blit(self._shadow_cache[size], (x, y + size - (size // 4)))
        screen.blit(image, x, y) if isinstance(y, tuple) else screen.blit(image, (x, y))

    def draw_health_bar(self, screen, cx, cy, hp_cur, hp_max, width):
        """Desenha a barra de vida centralizada num ponto horizontal (cx)."""
        pygame.draw.rect(screen, (20, 20, 20), (cx - width//2 - 2, cy - 2, width + 4, 14))
        pygame.draw.rect(screen, (60, 0, 0), (cx - width//2, cy, width, 10))
        fill_w = int((hp_cur / max(hp_max, 1)) * width)
        if fill_w > 0:
            color = (50, 200, 50) if hp_cur > (hp_max // 2) else (200, 50, 50)
            pygame.draw.rect(screen, color, (cx - width//2, cy, fill_w, 10))

    def _get_campaign(self) -> dict:
        """Lê data/campaign.json UMA vez (antes era lido do disco a cada frame)."""
        if getattr(self, "_campaign_cache", None) is None:
            import json
            try:
                with open("data/campaign.json", "r", encoding="utf-8") as f:
                    self._campaign_cache = json.load(f)
            except Exception as e:
                print(f"[ERRO UI] Falha ao ler campaign.json: {e}")
                self._campaign_cache = {}
        return self._campaign_cache

    @staticmethod
    def _resolve_monster_dimensions(npc_id: str, tipo: str, target: dict = None) -> tuple:
        """Calcula largura e altura proporcionais com base no porte da criatura em D&D 5e."""
        key = f"{npc_id} {tipo} {(target or {}).get('tipo_bestiario', '')}".lower()
        
        # Colossal / Boss Supremo (Dragão é o maior inimigo)
        if any(w in key for w in ["dragao", "dragon", "tirano", "boss_final", "supreme"]):
            return (220, 240)
        # Enorme (Gigantes de Fogo)
        elif any(w in key for w in ["gigante", "giant"]):
            return (150, 180)
        # Grande (Quimeras, Mantícoras, Ogros)
        elif any(w in key for w in ["quimera", "chimera", "manticora", "manticore", "ogro", "ogre", "troll"]):
            return (135, 150)
        # Grande Bestial (Lobo Atroz, Aranha Gigante, Geleia Ocre)
        elif any(w in key for w in ["lobo atroz", "dire wolf", "aranha", "spider", "geleia", "jelly"]):
            return (120, 130)
        # Médio/Grande Imponente (Lich, Rakshasa, Gárgula, Cria de Vampiro)
        elif any(w in key for w in ["lich", "rakshasa", "gargoyle", "gargula", "vampir"]):
            return (105, 130)
        # Pequeno (Goblins, Kobolds, Halflings, Gnomos)
        elif any(w in key for w in ["goblin", "kobold", "halfling", "gnomo"]):
            return (65, 80)
        # Médio Padrão e Robusto (Bandidos, Esqueletos, Zumbis, Veteranos, Orcs, Sombras)
        else:
            return (85, 115)

    def draw_in_game(self, screen: pygame.Surface, session: "SessionManager", current_message: dict = None):
        game_state = session.game_state
        story_obj = getattr(session, "story", None)
        beat_str = str(getattr(story_obj, "current_beat", 1))
        bg_image = game_state.get("current_background") or self._get_campaign().get(beat_str, {}).get("bg_image", "tavern_bg.jpg")
            
        bg_surf = AssetManager.get_background(bg_image)
        screen.blit(AssetManager.get_scaled(bg_surf, (self.width, self.height)), (0, 0))

        if game_state.get("player_character"):
            self.draw_top_hud(screen, game_state["player_character"])

        # Coleta Inimigos e Monstros Vivos com porte proporcional (lado direito)
        living_enemies = []
        visual_npcs = getattr(session, "active_visual_npcs", {}) or {}
        combat_targets = getattr(session, "active_combat_targets", {}) or {}
        for npc_id, tipo in visual_npcs.items():
            target = combat_targets.get(npc_id)
            if target and target.get("status") == "morto": continue
            if target and target.get("faction") == "ally": continue # Aliados ficam na linha da party
            w, h = self._resolve_monster_dimensions(npc_id, tipo, target)
            living_enemies.append({
                "id": npc_id,
                "tipo": tipo,
                "target": target,
                "w": w,
                "h": h
            })

        enemy_hitboxes = {}
        if living_enemies:
            play_area_x = int(self.width * 0.44)
            avail_w = (self.width - 40) - play_area_x
            n_enemies = len(living_enemies)
            total_w = sum(e["w"] for e in living_enemies)
            gap = max(24, (avail_w - total_w) // (n_enemies + 1)) if avail_w > total_w else 16
            
            # Ponto de apoio do solo para alinhamento dos pés
            ground_y = self.height - 220
            start_x = play_area_x + max(10, (avail_w - (total_w + gap * (n_enemies - 1))) // 2)
            cur_x = start_x
            mouse_pos = pygame.mouse.get_pos()
            is_combat = (getattr(session, "game_mode", "") == "COMBATE" or bool(getattr(session, "active_combat_targets", None)))
            
            for enemy in living_enemies:
                e_w, e_h = enemy["w"], enemy["h"]
                sprite = self._resolve_npc_sprite(session, enemy["id"], enemy["tipo"], enemy["target"])
                s_w, s_h = sprite.get_size()
                if s_h > 0 and s_w > 0:
                    draw_w = int(e_h * (s_w / s_h))
                    draw_h = e_h
                else:
                    draw_w, draw_h = e_w, e_h
                
                x_pos = cur_x
                y_pos = ground_y - draw_h
                
                screen.blit(AssetManager.get_scaled(sprite, (draw_w, draw_h)), (x_pos, y_pos))

                # Registra hitbox do inimigo para cliques de ataque
                enemy_rect = pygame.Rect(x_pos, y_pos, draw_w, draw_h)
                enemy_hitboxes[f"enemy_{enemy['id']}"] = enemy_rect
                enemy_hitboxes[enemy["id"]] = enemy_rect

                # Feedback visual de hover/mira em combate
                if is_combat and enemy_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (255, 60, 60), enemy_rect, 2, border_radius=4)
                    tip_surf = self.font_names.render("⚔ Atacar", True, (255, 215, 0))
                    cx_tip = x_pos + (draw_w // 2)
                    tip_bg = pygame.Rect(cx_tip - tip_surf.get_width() // 2 - 6, y_pos - 22, tip_surf.get_width() + 12, tip_surf.get_height() + 4)
                    pygame.draw.rect(screen, (25, 15, 15), tip_bg, border_radius=3)
                    pygame.draw.rect(screen, (255, 60, 60), tip_bg, 1, border_radius=3)
                    screen.blit(tip_surf, (tip_bg.x + 6, tip_bg.y + 2))
                
                # Health Bar dinâmica
                cx = x_pos + (draw_w // 2)
                bar_w = max(70, min(110, draw_w))
                if enemy["target"]:
                    self.draw_health_bar(screen, cx, ground_y + 10, enemy["target"].get("pv_atual", 0), enemy["target"].get("pv_max", 10), bar_w)
                    
                name_txt = self.font_names.render(enemy["id"], True, (255, 255, 255))
                screen.blit(name_txt, (cx - (name_txt.get_width() // 2), ground_y + 26))
                
                cur_x += max(e_w, draw_w) + gap


        # Linha da Party (Jogador + Aliados no Clímax Beat 15 ou ativos em combate)
        players = []
        if game_state.get("player_character"):
            players.append(game_state["player_character"])

        # Coleta aliados ativos explicitamente no combate ou no Clímax (Beat 15)
        combat_allies = [
            t for t in session.active_combat_targets.values()
            if t.get("faction") == "ally" and t.get("status") != "morto"
        ]
        extra_combat_allies = getattr(session, "combat_allies", None)
        if isinstance(extra_combat_allies, dict):
            for ally in extra_combat_allies.values():
                if isinstance(ally, dict) and ally.get("status") != "morto" and ally not in combat_allies:
                    combat_allies.append(ally)
        elif isinstance(extra_combat_allies, list):
            for ally in extra_combat_allies:
                if isinstance(ally, dict) and ally.get("status") != "morto" and ally not in combat_allies:
                    combat_allies.append(ally)

        if combat_allies:
            players.extend(combat_allies)
        elif hasattr(session, "story") and hasattr(session.story, "is_climax") and session.story.is_climax():
            unlocked = session.story.get_unlocked_allies()
            for ally in unlocked.values():
                players.append(ally)

        hitboxes = self.draw_players(screen, players)
        hitboxes.update(enemy_hitboxes)

        self.draw_side_dialog_panel(screen, current_message)

        for ft in self.floating_texts[:]:
            ft["y"] -= 1
            ft["timer"] -= 1

            if ft["timer"] <= 0:
                self.floating_texts.remove(ft)
            else:
                alpha = min(255, ft["timer"] * 5) # Fade out suave
                txt_surf = self.font_dmg.render(ft["text"], True, ft["color"])
                txt_surf.set_alpha(alpha)
                outline = self.font_dmg.render(ft["text"], True, (0, 0, 0))
                outline.set_alpha(alpha)
                screen.blit(outline, (ft["x"] - outline.get_width()//2 + 2, ft["y"] + 2))
                screen.blit(txt_surf, (ft["x"] - txt_surf.get_width()//2, ft["y"]))

        # Combat log is now handled entirely by draw_side_dialog_panel
        return hitboxes

    def handle_ui_event(self, event: dict, game_state: dict):
        event_type = event.get("type")

        if event_type in ["damage", "heal"]:
            target_name = event.get("target")
            amount = event.get("amount", 0)
            is_pc = event.get("is_pc", False)
            color = (255, 50, 50) if event_type == "damage" else (50, 255, 50)
            prefix = "-" if event_type == "damage" else "+"

            target_x, target_y = self.width // 2, self.height // 2

            if is_pc:
                players = []
                if game_state.get("player_character"): players.append(game_state["player_character"])
                spacing = self.width // (len(players) + 1)
                for i, p in enumerate(players):
                    if p.get("name") == target_name:
                        target_x = spacing * (i + 1)
                        target_y = self.height - 150
                        break
            else:
                active_entities = game_state.get("active_entities", [])
                spacing = self.width // (len(active_entities) + 1)
                for i, ent in enumerate(active_entities):
                    if ent.get("name") == target_name:
                        target_x = spacing * (i + 1)
                        target_y = self.height - 300
                        break

            self.add_floating_text(f"{prefix}{amount}", target_x, target_y, color)
            self.add_combat_log(f"{target_name} sofreu {amount} de dano." if event_type == "damage" else f"{target_name} recuperou {amount} HP.")

        elif event_type == "system_event":
            text = event.get("text", "")
            self.add_combat_log(text)

        elif event_type in ["gain_xp", "gain_item"]:
            target_name = event.get("target")
            target_x, target_y = self.width // 2, self.height - 150 # default player pos

            players = []
            if game_state.get("player_character"): players.append(game_state["player_character"])
            spacing = self.width // (len(players) + 1)
            for i, p in enumerate(players):
                if p.get("name") == target_name:
                    target_x = spacing * (i + 1)
                    target_y = self.height - 150
                    break

            if event_type == "gain_xp":
                amount = event.get("amount", 0)
                self.add_floating_text(f"+{amount} XP", target_x, target_y - 30, (255, 215, 0)) # Amarelo/Dourado
            elif event_type == "gain_item":
                item_name = event.get("item", "")
                self.add_floating_text(f"+ {item_name}", target_x, target_y - 50, (180, 100, 255)) # Roxo/Azul

    def draw_players(self, screen: pygame.Surface, players: list) -> dict:
        hitboxes = {}
        if not players: return hitboxes
        from ui.asset_manager import AssetManager

        play_area_x = int(self.width * 0.40)
        play_area_w = self.width - play_area_x
        spacing = play_area_w // (len(players) + 1)
        token_size = 104

        for i, p in enumerate(players):
            cx = play_area_x + spacing * (i + 1)
            cy = self.height - 165

            if p.get("sprite_key") or p.get("faction") == "ally":
                hero_surf = AssetManager.get_entity_sprite(p, kind="corpo", size=(token_size, token_size))
            else:
                hero_surf = AssetManager.get_hero_sprite(p.get("race"), p.get("class"),
                                                         p.get("gender") or p.get("genero"))
                hero_surf = AssetManager.get_scaled(hero_surf, (token_size, token_size))
            
            self.draw_board_token(screen, hero_surf, cx - (token_size // 2), cy - (token_size // 2), token_size)
            box_rect = pygame.Rect(cx - (token_size // 2), cy - (token_size // 2), token_size, token_size)
            if i == 0:
                hitboxes["player"] = box_rect
            else:
                hitboxes[f"ally_{i}"] = box_rect
                if p.get("name"):
                    hitboxes[p["name"]] = box_rect
            
            name_txt = self.font_names.render(p.get("name", "Unknown"), True, (255, 255, 255))
            screen.blit(name_txt, (cx - (name_txt.get_width()//2), cy + (token_size // 2) + 6))
            
            # Health Bar dinâmica para membros da party
            hp_cur = p.get("hp_current", p.get("pv_atual", 0))
            hp_max = max(1, p.get("hp_max", p.get("pv_max", 1)))
            self.draw_health_bar(screen, cx, cy + (token_size // 2) + 24, hp_cur, hp_max, 56)
            
        return hitboxes

    def draw_side_dialog_panel(self, screen: pygame.Surface, message: dict):
        from ui.asset_manager import AssetManager
        import pygame
        
        panel_w = int(self.width * 0.40)
        panel_h = 240
        panel_x = 12
        panel_y = self.height - panel_h - 85
        
        # Garante que mensagens pré-calculadas acompanhem a largura do painel
        if getattr(self, "_cached_panel_w", None) != panel_w or len(self._formatted_messages) != len(self.chat_history):
            self._cached_panel_w = panel_w
            self._formatted_messages = [
                self._format_chat_message(m, panel_w) for m in self.chat_history
            ]
        
        new_message = False
        if message:
            msg_id = id(message)
            if msg_id != getattr(self, "last_msg_id", None):
                self.last_msg_id = msg_id
                self._add_chat_message(message.copy(), panel_w)
                new_message = True
        
        # Cache de superfície de fundo (Zero Garbage por frame)
        bg_key = (panel_w, panel_h)
        if bg_key not in self._panel_bg_cache:
            bg_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            bg_surf.fill((15, 15, 15, 230))
            pygame.draw.rect(bg_surf, (180, 150, 50), (0, 0, panel_w, panel_h), 2)
            self._panel_bg_cache[bg_key] = bg_surf
        screen.blit(self._panel_bg_cache[bg_key], (panel_x, panel_y))
        
        color_narrative = (240, 230, 200)
        color_combat = (200, 200, 200)
        
        total_content_h = sum(pmsg["h"] + 15 for pmsg in self._formatted_messages)
        max_scroll = max(0, total_content_h - (panel_h - 40))
        if not hasattr(self, "scroll_y"):
            self.scroll_y = max_scroll
            
        if new_message:
            self.scroll_y = max_scroll
            
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))
        
        old_clip = screen.get_clip()
        screen.set_clip(pygame.Rect(panel_x, panel_y, panel_w, panel_h))
        
        current_y = panel_y + 20 - self.scroll_y
        
        for pmsg in self._formatted_messages:
            msg_h = pmsg["h"]
            
            if current_y + msg_h > panel_y and current_y < panel_y + panel_h:
                draw_x = panel_x + 20
                if pmsg["has_portrait"]:
                    portrait = AssetManager.get_portrait_sprite(pmsg["falante"])
                    portrait = AssetManager.get_scaled(portrait, (60, 60))
                    screen.blit(portrait, (draw_x, current_y))
                    pygame.draw.rect(screen, (180, 150, 50), (draw_x, current_y, 60, 60), 1)
                    
                    name_tag = self.font_names.render(pmsg["falante"].capitalize(), True, (180, 150, 50))
                    screen.blit(name_tag, (draw_x + 70, current_y))
                    
                    text_y = current_y + 25
                    line_h = pmsg["font"].get_linesize()
                    for line in pmsg["lines"]:
                        if text_y + pmsg["font"].get_height() > panel_y + panel_h:
                            break
                        if line:
                            txt_surf = pmsg["font"].render(line, True, color_narrative)
                            screen.blit(txt_surf, (draw_x + 70, text_y))
                        text_y += line_h
                else:
                    c = color_combat if pmsg["msg_type"] == "combat" else color_narrative
                    text_y = current_y
                    line_h = pmsg["font"].get_linesize()
                    for line in pmsg["lines"]:
                        if text_y + pmsg["font"].get_height() > panel_y + panel_h:
                            break
                        if line:
                            txt_surf = pmsg["font"].render(line, True, c)
                            screen.blit(txt_surf, (draw_x, text_y))
                        text_y += line_h
                    
            current_y += msg_h + 15
            
        screen.set_clip(old_clip)
        
        if max_scroll > 0:
            scroll_bar_h = max(20, int((panel_h / total_content_h) * panel_h))
            scroll_progress = self.scroll_y / max_scroll
            scroll_bar_y = panel_y + int(scroll_progress * (panel_h - scroll_bar_h))
            
            sb_x = panel_x + panel_w - 12
            pygame.draw.rect(screen, (40, 35, 30), (sb_x, panel_y + 2, 8, panel_h - 4), border_radius=4)
            pygame.draw.rect(screen, (180, 150, 50), (sb_x, scroll_bar_y, 8, scroll_bar_h), border_radius=4)

    def draw_bottom_dialog_box(self, screen: pygame.Surface, message: dict):
        """Compatibilidade legada para draw_side_dialog_panel."""
        return self.draw_side_dialog_panel(screen, message)


def get_act_and_chapter_title(beat_num: int) -> tuple:
    """
    Converte o número do Beat para o formato canônico:
    Ato I (Beats 1-5), Ato II (Beats 6-10), Ato III (Beats 11-15).
    Ex: Beat 2 -> ("Ato I: Capítulo II", "II")
    """
    ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", 
               "XI", "XII", "XIII", "XIV", "XV"]
    
    if beat_num <= 5:
        ato_str = "Ato I"
    elif beat_num <= 10:
        ato_str = "Ato II"
    else:
        ato_str = "Ato III"
        
    idx = max(0, min(beat_num - 1, len(ROMANOS) - 1))
    cap_romano = ROMANOS[idx]
    
    if beat_num == 15:
        return (f"{ato_str}: O Clímax Final", cap_romano)
    return (f"{ato_str}: Capítulo {cap_romano}", cap_romano)


ACT_INTERLUDES = {
    1: {
        "act_title": "Ato I",
        "subtitle": "As Sombras se Alastram",
        "tag": "Início da Jornada",
        "prompt": "[ Pressione ENTER ou Clique para Iniciar a Jornada ]"
    },
    6: {
        "act_title": "Ato II",
        "subtitle": "O Cerco de Gelo e Sangue",
        "tag": "A Grande Ruptura",
        "prompt": "[ Pressione ENTER ou Clique para Iniciar o Ato II ]"
    },
    11: {
        "act_title": "Ato III",
        "subtitle": "A Caldeira do Tirano",
        "tag": "A Marcha Final",
        "prompt": "[ Pressione ENTER ou Clique para Iniciar a Marcha Final ]"
    },
    15: {
        "act_title": "Ato III: Clímax",
        "subtitle": "O Confronto com o Tirano",
        "tag": "O Clímax Supremo",
        "prompt": "[ Pressione ENTER ou Clique para o Confronto Final ]"
    }
}


class BeatTransitionScene:
    """
    Cena de Transição e Apresentação de Capítulo / Beat (Dark Fantasy).
    Apresenta Interlúdios de Ato Épicos solenes e transições de capítulos padrão.
    Zero Garbage a 60 FPS com superfícies de vinheta e moldura pré-alocadas.
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.is_active = False
        
        from ui.asset_manager import AssetManager
        self.font_act = AssetManager.get_font(28)
        self.font_act.set_bold(True)
        self.font_title = AssetManager.get_font(36)
        self.font_title.set_bold(True)
        self.font_desc = AssetManager.get_font(18)
        self.font_prompt = AssetManager.get_font(16)
        
        # Tipografia Solene para Interlúdios de Atos Épicos
        self.font_interlude_tag = AssetManager.get_font(15, bold=True)
        self.font_interlude_act = AssetManager.get_font(34, bold=True)
        self.font_interlude_sub = AssetManager.get_font(22, italic=True)
        
        self.current_beat = 1
        self.beat_name = ""
        self.description = ""
        self.bg_image_name = "tavern_bg.jpg"
        self.desc_lines = []
        self.is_act_interlude = False
        self.interlude_info = None
        
        # Animação não-bloqueante a 60 FPS
        self.alpha = 0.0
        self.fade_speed = 12.0
        self.pulse_timer = 0.0
        
        # Cache de Superfícies de Overlay de Vinheta (Zero Garbage por frame)
        self.overlay_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.overlay_surf.fill((10, 10, 15, 185))
        
        self.overlay_interlude_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.overlay_interlude_surf.fill((8, 6, 12, 220))
        
        # 1. Card Padrão de Beat
        self.card_w = min(860, self.width - 80)
        self.card_h = min(360, self.height - 100)
        self.card_x = (self.width - self.card_w) // 2
        self.card_y = (self.height - self.card_h) // 2
        self.card_surf = pygame.Surface((self.card_w, self.card_h), pygame.SRCALPHA)
        self._render_card_base()

        # 2. Card Épico de Interlúdio de Ato (Mais solene, imponente e com moldura reforçada)
        self.card_interlude_w = min(960, self.width - 40)
        self.card_interlude_h = min(500, self.height - 60)
        self.card_interlude_x = (self.width - self.card_interlude_w) // 2
        self.card_interlude_y = (self.height - self.card_interlude_h) // 2
        self.card_interlude_surf = pygame.Surface((self.card_interlude_w, self.card_interlude_h), pygame.SRCALPHA)
        self._render_interlude_card_base()

    def _render_card_base(self):
        """Pré-renderiza o card gótico padrão com bordas de bronze e cantoneiras."""
        self.card_surf.fill((16, 14, 22, 235))
        # Borda externa dupla gótica
        pygame.draw.rect(self.card_surf, (80, 65, 40), (0, 0, self.card_w, self.card_h), 2)
        pygame.draw.rect(self.card_surf, (190, 155, 65), (6, 6, self.card_w - 12, self.card_h - 12), 1)
        # Cantoneiras ornamentais
        corner_len = 18
        c_gold = (225, 190, 85)
        # Top-left
        pygame.draw.line(self.card_surf, c_gold, (6, 6), (6 + corner_len, 6), 2)
        pygame.draw.line(self.card_surf, c_gold, (6, 6), (6, 6 + corner_len), 2)
        # Top-right
        pygame.draw.line(self.card_surf, c_gold, (self.card_w - 7, 6), (self.card_w - 7 - corner_len, 6), 2)
        pygame.draw.line(self.card_surf, c_gold, (self.card_w - 7, 6), (self.card_w - 7, 6 + corner_len), 2)
        # Bottom-left
        pygame.draw.line(self.card_surf, c_gold, (6, self.card_h - 7), (6 + corner_len, self.card_h - 7), 2)
        pygame.draw.line(self.card_surf, c_gold, (6, self.card_h - 7), (6, self.card_h - 7 - corner_len), 2)
        # Bottom-right
        pygame.draw.line(self.card_surf, c_gold, (self.card_w - 7, self.card_h - 7), (self.card_w - 7 - corner_len, self.card_h - 7), 2)
        pygame.draw.line(self.card_surf, c_gold, (self.card_w - 7, self.card_h - 7), (self.card_w - 7, self.card_h - 7 - corner_len), 2)

    def _render_interlude_card_base(self):
        """Pré-renderiza o card solene de Interlúdio de Ato com moldura reforçada e cantoneiras imperiais."""
        w, h = self.card_interlude_w, self.card_interlude_h
        self.card_interlude_surf.fill((14, 12, 19, 245))
        
        # 1. Borda externa em bronze escurecido
        pygame.draw.rect(self.card_interlude_surf, (85, 70, 42), (0, 0, w, h), 2, border_radius=6)
        
        # 2. Borda intermediária de ouro envelhecido
        pygame.draw.rect(self.card_interlude_surf, (155, 125, 55), (4, 4, w - 8, h - 8), 1, border_radius=5)
        
        # 3. Moldura interna reforçada em ouro radiante
        pygame.draw.rect(self.card_interlude_surf, (225, 185, 80), (8, 8, w - 16, h - 16), 2, border_radius=4)
        
        # 4. Filete decorativo sutil
        pygame.draw.rect(self.card_interlude_surf, (60, 48, 28), (14, 14, w - 28, h - 28), 1)
        
        # 5. Cantoneiras ornamentais reforçadas (com cantos duplos e losangos dourados)
        c_gold = (245, 210, 95)
        c_bronze = (170, 135, 55)
        corner_len = 30
        
        def draw_diamond(cx, cy, radius=4):
            pts = [(cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)]
            pygame.draw.polygon(self.card_interlude_surf, c_gold, pts)
        
        # Top-Left
        pygame.draw.line(self.card_interlude_surf, c_gold, (8, 8), (8 + corner_len, 8), 3)
        pygame.draw.line(self.card_interlude_surf, c_gold, (8, 8), (8, 8 + corner_len), 3)
        pygame.draw.line(self.card_interlude_surf, c_bronze, (14, 14), (14 + corner_len - 6, 14), 1)
        pygame.draw.line(self.card_interlude_surf, c_bronze, (14, 14), (14, 14 + corner_len - 6), 1)
        draw_diamond(8 + corner_len + 5, 8)
        draw_diamond(8, 8 + corner_len + 5)
        
        # Top-Right
        pygame.draw.line(self.card_interlude_surf, c_gold, (w - 9, 8), (w - 9 - corner_len, 8), 3)
        pygame.draw.line(self.card_interlude_surf, c_gold, (w - 9, 8), (w - 9, 8 + corner_len), 3)
        pygame.draw.line(self.card_interlude_surf, c_bronze, (w - 15, 14), (w - 15 - corner_len + 6, 14), 1)
        pygame.draw.line(self.card_interlude_surf, c_bronze, (w - 15, 14), (w - 15, 14 + corner_len - 6), 1)
        draw_diamond(w - 9 - corner_len - 5, 8)
        draw_diamond(w - 9, 8 + corner_len + 5)
        
        # Bottom-Left
        pygame.draw.line(self.card_interlude_surf, c_gold, (8, h - 9), (8 + corner_len, h - 9), 3)
        pygame.draw.line(self.card_interlude_surf, c_gold, (8, h - 9), (8, h - 9 - corner_len), 3)
        pygame.draw.line(self.card_interlude_surf, c_bronze, (14, h - 15), (14 + corner_len - 6, h - 15), 1)
        pygame.draw.line(self.card_interlude_surf, c_bronze, (14, h - 15), (14, h - 15 - corner_len + 6), 1)
        draw_diamond(8 + corner_len + 5, h - 9)
        draw_diamond(8, h - 9 - corner_len - 5)
        
        # Bottom-Right
        pygame.draw.line(self.card_interlude_surf, c_gold, (w - 9, h - 9), (w - 9 - corner_len, h - 9), 3)
        pygame.draw.line(self.card_interlude_surf, c_gold, (w - 9, h - 9), (w - 9, h - 9 - corner_len), 3)
        pygame.draw.line(self.card_interlude_surf, c_bronze, (w - 15, h - 15), (w - 15 - corner_len + 6, h - 15), 1)
        pygame.draw.line(self.card_interlude_surf, c_bronze, (w - 15, h - 15), (w - 15, h - 15 - corner_len + 6), 1)
        draw_diamond(w - 9 - corner_len - 5, h - 9)
        draw_diamond(w - 9, h - 9 - corner_len - 5)

    def start_transition(
        self,
        beat_num: int,
        beat_name: str,
        description: str,
        bg_image: str,
        is_act_interlude: bool = False
    ):
        self.is_active = True
        self.current_beat = beat_num
        self.beat_name = beat_name
        self.description = description
        self.bg_image_name = bg_image
        self.alpha = 0.0
        self.pulse_timer = 0.0
        
        # Detecta Interlúdio de Ato se is_act_interlude for True OU se beat_num estiver nos beats de interlúdio (1, 6, 11, 15)
        self.is_act_interlude = bool(is_act_interlude or (beat_num in ACT_INTERLUDES))
        self.interlude_info = ACT_INTERLUDES.get(beat_num) if self.is_act_interlude else None
        
        # Pré-calcula quebra de linhas da descrição no momento de início (Zero Garbage a 60 FPS)
        from ui.hud_components import get_wrapped_text_dimensions
        if self.is_act_interlude:
            max_text_w = self.card_interlude_w - 90
            max_lines = 8
        else:
            max_text_w = self.card_w - 80
            max_lines = 4
            
        _, _, lines = get_wrapped_text_dimensions(self.description, self.font_desc, max_text_w)
        self.desc_lines = lines[:max_lines] if lines else []

    def handle_event(self, event) -> bool:
        """Retorna True se o jogador pressionar tecla ou clicar para continuar."""
        if not self.is_active:
            return False
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
            self.is_active = False
            return True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_active = False
            return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        if not self.is_active:
            return
            
        self.pulse_timer += 0.06
        if self.alpha < 255.0:
            self.alpha = min(255.0, self.alpha + self.fade_speed)
            
        # 1. Renderiza o fundo do novo cenário
        from ui.asset_manager import AssetManager
        bg_surf = AssetManager.get_background(self.bg_image_name)
        screen.blit(AssetManager.get_scaled(bg_surf, (self.width, self.height)), (0, 0))
        
        import math
        pulse_val = int(185 + 70 * math.sin(self.pulse_timer * 3))
        cx = self.width // 2
        
        if self.is_act_interlude:
            # =========================================================================
            # INTERLÚDIO DE ATO ÉPICO (BEATS 1, 6, 11, 15 OU FORÇADO VIA PARAM)
            # =========================================================================
            screen.blit(self.overlay_interlude_surf, (0, 0))
            screen.blit(self.card_interlude_surf, (self.card_interlude_x, self.card_interlude_y))
            
            top_y = self.card_interlude_y
            info = self.interlude_info or ACT_INTERLUDES.get(self.current_beat, {
                "act_title": "ATO",
                "subtitle": "Interlúdio Solene",
                "tag": "Transição Épica",
                "prompt": "[ Pressione ENTER ou Clique para Prosseguir ]"
            })
            
            # Tag Épica de Abertura / Moldura Superior
            tag_str = f"❖  {info['tag'].upper()}  ❖"
            tag_surf = self.font_interlude_tag.render(tag_str, True, (215, 175, 80))
            tag_rect = tag_surf.get_rect(center=(cx, top_y + 35))
            screen.blit(tag_surf, tag_rect)
            
            # Título de Ato em Destaque Luminoso
            act_header = info["act_title"].upper()
            act_surf = self.font_interlude_act.render(act_header, True, (255, 230, 130))
            act_rect = act_surf.get_rect(center=(cx, top_y + 75))
            screen.blit(act_surf, act_rect)
            
            # Subtítulo Poético / Atmosférico
            sub_str = f"« {info['subtitle']} »"
            sub_surf = self.font_interlude_sub.render(sub_str, True, (240, 215, 175))
            sub_rect = sub_surf.get_rect(center=(cx, top_y + 115))
            screen.blit(sub_surf, sub_rect)
            
            # Divisor Ornamental
            div_txt = "❖ ────────── ◆ ────────── ❖"
            div_surf = self.font_prompt.render(div_txt, True, (175, 135, 55))
            div_rect = div_surf.get_rect(center=(cx, top_y + 148))
            screen.blit(div_surf, div_rect)
            
            # Nome do Beat / Local de Abertura
            if self.beat_name:
                name_surf = self.font_title.render(self.beat_name, True, (250, 245, 230))
                name_rect = name_surf.get_rect(center=(cx, top_y + 185))
                screen.blit(name_surf, name_rect)
                start_desc_y = top_y + 230
            else:
                start_desc_y = top_y + 195
                
            # Linhas de Ambientação Estendidas (até 8 linhas pré-calculadas)
            line_h = self.font_desc.get_linesize() + 2
            for i, line in enumerate(self.desc_lines):
                if line.strip():
                    d_surf = self.font_desc.render(line, True, (220, 210, 195))
                    d_rect = d_surf.get_rect(center=(cx, start_desc_y + (i * line_h)))
                    screen.blit(d_surf, d_rect)
                    
            # Indicador Pulsante Dourado Específico do Ato
            prompt_color = (pulse_val, int(pulse_val * 0.85), int(pulse_val * 0.45))
            prompt_text = info.get("prompt", "[ Pressione ENTER ou Clique para Continuar ]")
            prompt_surf = self.font_prompt.render(prompt_text, True, prompt_color)
            prompt_rect = prompt_surf.get_rect(center=(cx, top_y + self.card_interlude_h - 38))
            screen.blit(prompt_surf, prompt_rect)
            
        else:
            # =========================================================================
            # TRANSIÇÃO PADRÃO DE BEAT (BEATS 2-5, 7-10, 12-14)
            # =========================================================================
            screen.blit(self.overlay_surf, (0, 0))
            screen.blit(self.card_surf, (self.card_x, self.card_y))
            
            # Título do Ato / Capítulo (Dourado luminoso)
            act_title, _ = get_act_and_chapter_title(self.current_beat)
            act_surf = self.font_act.render(act_title.upper(), True, (240, 205, 95))
            act_rect = act_surf.get_rect(center=(cx, self.card_y + 45))
            screen.blit(act_surf, act_rect)
            
            # Divisor decorativo
            div_txt = "◆ ──────── ❖ ──────── ◆"
            div_surf = self.font_prompt.render(div_txt, True, (160, 130, 60))
            div_rect = div_surf.get_rect(center=(cx, self.card_y + 80))
            screen.blit(div_surf, div_rect)
            
            # Nome do Local (Marfim / Branco suave)
            name_surf = self.font_title.render(self.beat_name, True, (245, 240, 225))
            name_rect = name_surf.get_rect(center=(cx, self.card_y + 120))
            screen.blit(name_surf, name_rect)
            
            # Breve descrição de ambientação
            start_desc_y = self.card_y + 175
            line_h = self.font_desc.get_linesize()
            for i, line in enumerate(self.desc_lines):
                if line.strip():
                    d_surf = self.font_desc.render(line, True, (205, 200, 190))
                    d_rect = d_surf.get_rect(center=(cx, start_desc_y + (i * line_h)))
                    screen.blit(d_surf, d_rect)
                    
            # Prompt Pulsante: [ Pressione ENTER ou Clique para Avançar ]
            prompt_color = (pulse_val, int(pulse_val * 0.85), int(pulse_val * 0.5))
            prompt_surf = self.font_prompt.render("[ Pressione ENTER ou Clique para Continuar ]", True, prompt_color)
            prompt_rect = prompt_surf.get_rect(center=(cx, self.card_y + self.card_h - 40))
            screen.blit(prompt_surf, prompt_rect)