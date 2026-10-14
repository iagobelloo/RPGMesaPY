import pygame
from typing import Dict, Any, Optional, List

from ui.hud_components import (
    Panel, draw_ui_panel, draw_ui_button, clean_tofu_glyphs, PlayerManualModal,
    COLOR_BG, COLOR_BORDER, COLOR_TEXT, COLOR_ACCENT, 
    COLOR_TEXT_DIM, COLOR_PANEL_BG, COLOR_WOOD_DARK, 
    COLOR_PARCHMENT, COLOR_GOLD, COLOR_INK
)
from core.game_engine import CharacterBuilder
from ui.asset_manager import AssetManager

class SelectionModal(Panel):
    """Modal de Pop-up para selecionar um item de uma lista (Ex: Raças)."""
    
    def __init__(self, x: int, y: int, width: int, height: int, title: str, items: List[str], lore_dict: dict):
        super().__init__(x, y, width, height, title)
        self.items = items
        self.lore_dict = lore_dict
        self.btn_w, self.btn_h = 150, 35
        self.rects = []
        self.hover_item = None
        
        cols = 3
        start_x = self.rect.x + (width - (cols * (self.btn_w + 10))) // 2
        start_y = self.rect.y + 60
        
        for i, item in enumerate(self.items):
            col = i % cols
            row = i // cols
            r = pygame.Rect(start_x + (col * (self.btn_w + 10)), start_y + (row * (self.btn_h + 10)), self.btn_w, self.btn_h)
            self.rects.append((r, item))
            
    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        if not self.is_visible: return
        
        mouse_pos = pygame.mouse.get_pos()
        self.hover_item = None
        
        for r, item in self.rects:
            is_hover = r.collidepoint(mouse_pos)
            if is_hover: self.hover_item = item
            
            pygame.draw.rect(screen, COLOR_ACCENT if is_hover else COLOR_PARCHMENT, r)
            pygame.draw.rect(screen, COLOR_GOLD, r, 2)
            
            surf = self.font_body.render(item, True, COLOR_TEXT if is_hover else COLOR_INK)
            screen.blit(surf, (r.x + (r.width - surf.get_width())//2, r.y + (r.height - surf.get_height())//2))
            
        # Área de Lore no 1/3 inferior
        lore_rect = pygame.Rect(self.rect.x + 20, self.rect.y + self.rect.height - 80, self.rect.width - 40, 60)
        pygame.draw.rect(screen, COLOR_BG, lore_rect)
        pygame.draw.rect(screen, COLOR_BORDER, lore_rect, 1)
        
        lore_text = "Passe o mouse sobre uma opção para ler os detalhes."
        if self.hover_item and self.hover_item in self.lore_dict:
            lore_text = self.lore_dict[self.hover_item]
            
        # Wrap Lore Text
        words = lore_text.split()
        lines = []
        curr_line = ""
        for w in words:
            if self.font_body.size(curr_line + w)[0] < lore_rect.width - 20:
                curr_line += w + " "
            else:
                lines.append(curr_line)
                curr_line = w + " "
        lines.append(curr_line)
        
        for i, line in enumerate(lines[:3]): # Máx 3 linhas
            txt = AssetManager.get_font(14, italic=True).render(line, True, COLOR_TEXT_DIM)
            screen.blit(txt, (lore_rect.x + 10, lore_rect.y + 5 + (i * 18)))

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if not self.is_visible: return None
        if event.type == pygame.MOUSEBUTTONDOWN:
            for r, item in self.rects:
                if r.collidepoint(event.pos): return item
        return None


def _format_race_description(item_name: str, data: dict, selected_class: str = "") -> str:
    from core.dnd_rules import ITENS_UNICOS_RACIAIS, get_protagonist_gender_info
    desc = data.get("descricao_ui", "")
    bonus_list = []
    for attr, val in data.get("atributos", {}).items():
        if val > 0:
            bonus_list.append(f"+{val} {attr[:3].upper()}")
    bonus_str = ", ".join(bonus_list)

    parts = [desc]
    if bonus_str:
        parts.append(f"Bônus: {bonus_str}")

    racial_item = ITENS_UNICOS_RACIAIS.get(item_name)
    if racial_item:
        parts.append(f"Item Único Racial: {racial_item['name']} ({racial_item['effect']})")

    ref_class = selected_class or "Guerreiro"
    g_info = get_protagonist_gender_info(item_name, ref_class)
    parts.append(f"Arquétipo ({g_info['class_display']}): {g_info['label']} {g_info['symbol']}")
    return " | ".join(parts)

def _format_class_description(item_name: str, data: dict, selected_race: str = "") -> str:
    from core.dnd_rules import EQUIPAMENTOS_5E, ITENS_UNICOS_RACIAIS, get_protagonist_gender_info
    desc = data.get("descricao_ui", "")
    dado = data.get("dado_vida", 8)
    parts = [desc, f"Dado de Vida: d{dado}"]

    eq_list = EQUIPAMENTOS_5E.get(item_name, {}).get("iniciais", [])
    if len(eq_list) >= 2:
        parts.append(f"Equipamento de Classe: {eq_list[0]} & {eq_list[1]}")

    ref_race = selected_race or "Humano"
    g_info = get_protagonist_gender_info(ref_race, item_name)
    parts.append(f"Arquétipo: {g_info['label']} {g_info['symbol']} ({g_info['class_display']})")

    racial_item = ITENS_UNICOS_RACIAIS.get(ref_race)
    if racial_item:
        parts.append(f"Item Único Racial ({ref_race}): {racial_item['name']}")
    return " | ".join(parts)

def _format_standard_description(item_name: str, data: dict) -> str:
    return data.get("descricao_ui", "")

class GenericSelectionPanel(Panel):
    """Painel de seleção genérico parametrizado para telas full-screen (DRY / Zero Garbage por frame)."""
    def __init__(
        self,
        items: List[str],
        bg_image_name: str,
        data_dict: dict,
        format_description_fn: Optional[Any] = None,
        button_labels: Optional[Dict[str, str]] = None,
        button_tags: Optional[Dict[str, str]] = None
    ):
        super().__init__(0, 0, 1280, 720, "")
        self.items = items
        self.data_dict = data_dict
        self.format_description_fn = format_description_fn
        self.button_labels = button_labels or {}
        self.button_tags = button_tags or {}

        raw_bg = AssetManager.get_image("background", bg_image_name)
        self.bg_image = pygame.transform.scale(raw_bg, (1280, 720))

        self.rects = []
        self.hover_item = None

        start_x = 185
        start_y = 178
        btn_w, btn_h = 440, 30

        for i, item in enumerate(self.items):
            r = pygame.Rect(start_x, start_y + (i * btn_h), btn_w, btn_h)
            self.rects.append((r, item))

        self.btn_back = pygame.Rect(40, 720 - 70, 150, 45)
        self.font_ink = AssetManager.get_font(20, bold=True)
        self.font_ink_small = AssetManager.get_font(16, bold=True)
        self.font_desc = AssetManager.get_font(18)
        self.desc_rect = pygame.Rect(660, 211, 480, 480)

        # Pré-cálculo de quebras de texto (Zero Garbage e zero word-wrap a cada frame a 60 FPS)
        from ui.hud_components import get_wrapped_text_dimensions
        self._desc_cache = {}
        for item in self.items:
            if item in self.data_dict:
                data = self.data_dict[item]
                if self.format_description_fn:
                    full_text = self.format_description_fn(item, data)
                else:
                    full_text = data.get("descricao_ui", "")
                _, _, lines = get_wrapped_text_dimensions(full_text, self.font_desc, self.desc_rect.width, fixed_line_height=30)
                self._desc_cache[item] = lines

    def draw(self, screen: pygame.Surface):
        if not self.is_visible:
            return
        screen.blit(self.bg_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        self.hover_item = None
        color_ink = (40, 20, 10)

        for r, item in self.rects:
            is_hover = r.collidepoint(mouse_pos)
            if is_hover:
                self.hover_item = item
                # Desenho direto na tela: zero alocações por frame!
                pygame.draw.rect(screen, (139, 0, 0), r, 2, border_radius=4)

            label_text = self.button_labels.get(item, item)
            txt_surf = self.font_ink.render(clean_tofu_glyphs(label_text), True, color_ink)
            rect = txt_surf.get_rect(midleft=(r.left + 15, r.centery - 2))
            screen.blit(txt_surf, rect)

            tag_text = self.button_tags.get(item, "")
            if tag_text:
                tag_color = (145, 35, 45) if "♀" in tag_text else (45, 70, 105)
                tag_surf = self.font_ink_small.render(clean_tofu_glyphs(tag_text), True, tag_color)
                tag_rect = tag_surf.get_rect(midright=(r.right - 14, r.centery - 1))
                screen.blit(tag_surf, tag_rect)

        # Botão Voltar (Permite fechar o modal sem trocar de opção)
        from ui.hud_components import draw_ui_button
        draw_ui_button(screen, self.btn_back, "Voltar", self.font_ink_small, self.btn_back.collidepoint(mouse_pos), True)

        # Balão de Descrição (Lado Direito) usando linhas pré-calculadas
        if self.hover_item and self.hover_item in self._desc_cache:
            lines = self._desc_cache[self.hover_item]
            y_offset = self.desc_rect.y
            line_h = 30
            for line in lines:
                if y_offset + self.font_desc.get_height() > self.desc_rect.bottom:
                    break
                if line:
                    txt_surf = self.font_desc.render(line, True, color_ink)
                    screen.blit(txt_surf, (self.desc_rect.x, y_offset))
                y_offset += line_h

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if not self.is_visible:
            return None
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "CANCEL"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if hasattr(self, "btn_back") and self.btn_back.collidepoint(event.pos):
                return "CANCEL"
            for r, item in self.rects:
                if r.collidepoint(event.pos):
                    return item
        return None

class RaceSelectionPanel(GenericSelectionPanel):
    """Tela full-screen dedicada à seleção de Raças, com background customizado e indicativo de gênero/item racial."""
    def __init__(self, items: List[str], selected_class: str = ""):
        from core.dnd_rules import RACAS_5E, get_protagonist_gender_info
        self.selected_class = selected_class
        btn_labels = {}
        btn_tags = {}
        ref_cls = selected_class or "Guerreiro"
        for r_name in items:
            g_info = get_protagonist_gender_info(r_name, ref_cls)
            if selected_class:
                btn_labels[r_name] = f"{r_name} ({g_info['symbol']})"
                btn_tags[r_name] = f"{g_info['symbol']} {g_info['label']}"
            else:
                btn_labels[r_name] = r_name
                btn_tags[r_name] = f"{g_info['symbol']}"

        super().__init__(
            items,
            "races_bg",
            RACAS_5E,
            lambda item, data: _format_race_description(item, data, self.selected_class),
            button_labels=btn_labels,
            button_tags=btn_tags
        )
        self.racas_data = RACAS_5E

class ClassSelectionPanel(GenericSelectionPanel):
    """Tela full-screen dedicada à seleção de Classes, com background customizado e indicativo de gênero (♂/♀)."""
    def __init__(self, items: List[str], selected_race: str = ""):
        from core.dnd_rules import CLASSES, get_protagonist_gender_info
        self.selected_race = selected_race
        btn_labels = {}
        btn_tags = {}
        ref_race = selected_race or "Humano"
        for c_name in items:
            g_info = get_protagonist_gender_info(ref_race, c_name)
            btn_labels[c_name] = f"{g_info['class_display']} ({g_info['symbol']})"
            btn_tags[c_name] = f"{g_info['symbol']} {g_info['label']}"

        super().__init__(
            items,
            "class_bg",
            CLASSES,
            lambda item, data: _format_class_description(item, data, self.selected_race),
            button_labels=btn_labels,
            button_tags=btn_tags
        )
        self.class_data = CLASSES

class BackgroundSelectionPanel(GenericSelectionPanel):
    """Tela full-screen dedicada à seleção de Antecedentes."""
    def __init__(self, items: List[str]):
        from core.dnd_rules import ANTECEDENTES_5E
        super().__init__(items, "backgrounds_bg", ANTECEDENTES_5E, _format_standard_description)
        self.bg_data = ANTECEDENTES_5E

class AlignmentSelectionPanel(GenericSelectionPanel):
    """Tela full-screen dedicada à seleção de Tendências."""
    def __init__(self, items: List[str]):
        from core.dnd_rules import TENDENCIAS_5E
        super().__init__(items, "tendencies_bg", TENDENCIAS_5E, _format_standard_description)
        self.al_data = TENDENCIAS_5E

class CharacterCreationPanel(Panel):
    """Ficha Interativa: Tinta no Papel usando um Character Sheet Background fixo."""
    
    def __init__(self, x: int = 0, y: int = 0, width: int = 1280, height: int = 720):
        # A tela de criação é desenhada em resolução nativa 1280x720
        super().__init__(0, 0, 1280, 720, title="")
        
        sw, sh = 1280, 720

        raw_bg = AssetManager.get_image("background", "char_sheet_bg")
        self.bg_image = pygame.transform.scale(raw_bg, (sw, sh))
        
        # 1. Remoção de Placeholders e Limpeza de Textos
        self.player_name = ""
        self.active_input = False
        self.selected_race = ""
        self.selected_class = ""
        self.selected_background = ""
        self.selected_alignment = ""
        
        from core.dnd_rules import (
            RACAS_5E, CLASSES, ANTECEDENTES_5E, TENDENCIAS_5E,
            get_class_base_attributes
        )
        self.base_attributes = get_class_base_attributes(self.selected_class or "Guerreiro")
        
        self.data_lists = {
            "race": list(RACAS_5E.keys()),
            "class": list(CLASSES.keys()),
            "background": list(ANTECEDENTES_5E.keys()),
            "alignment": list(TENDENCIAS_5E.keys())
        }
        self.lore_db = {} 
        
        # O Novo Sistema de Coordenadas Pixel-Perfect (Hitboxes Delimitadas)
        self.hitbox_map = {
            "nome": pygame.Rect(171, 160, 465, 46),
            "race": pygame.Rect(646, 160, 465, 46),
            "class": pygame.Rect(171, 222, 305, 46),
            "background": pygame.Rect(486, 222, 308, 46),
            "alignment": pygame.Rect(805, 222, 305, 46)
        }
        self.coords = {
            "cabecalho": {
                "nome": (298, 168, 330, 35),
                "raca": (755, 168, 350, 35),
                "classe": (298, 228, 172, 35),
                "antecedentes": (700, 228, 92, 35),
                "tendencia": (970, 228, 135, 35)
            },
            "status": {
                "pv": (608, 358), "ca": (702, 358),
                "proficiencia": (655, 434), "iniciativa": (655, 538), "deslocamento": (655, 623)
            },
            "atributos": {
                "forca": {"base": (435, 329), "mod": (510, 329)},
                "destreza": {"base": (435, 390), "mod": (510, 390)},
                "constituicao": {"base": (435, 450), "mod": (510, 450)},
                "inteligencia": {"base": (435, 507), "mod": (510, 507)},
                "sabedoria": {"base": (435, 566), "mod": (510, 568)},
                "carisma": {"base": (435, 628), "mod": (510, 628)}
            },
            "listas": {
                "habilidades": [(800, 378), (800, 408), (800, 430), (800, 455)],
                "equipamento": [(800, 555), (800, 582), (800, 618)]
            }
        }
        
        # Pré-alocação dos Rects de texto do cabeçalho (Zero alocação por frame a 60 FPS)
        c_cabe = self.coords["cabecalho"]
        self.hb_nome = pygame.Rect(*c_cabe["nome"])
        self.hb_raca = pygame.Rect(*c_cabe["raca"])
        self.hb_classe = pygame.Rect(*c_cabe["classe"])
        self.hb_bg = pygame.Rect(*c_cabe["antecedentes"])
        self.hb_align = pygame.Rect(*c_cabe["tendencia"])

        self.btn_cancel = pygame.Rect(40, sh - 70, 150, 45)
        self.btn_start = pygame.Rect(sw - 260, sh - 70, 220, 45)
        
        self.active_modal = None
        self.target_slot = ""
        
        # Anti-Crash Fonts
        self.font_ink = AssetManager.get_font(20, bold=True)
        self.font_ink_small = AssetManager.get_font(16, bold=True)
        self.font_ink_14 = AssetManager.get_font(14, bold=True)
        self.font_ink_12 = AssetManager.get_font(12, bold=True)

        # Badges/Selos de Gênero pré-renderizados (Zero Garbage por frame a 60 FPS)
        self._badge_male_surf = self._build_gender_badge("♂ Masculino", (222, 212, 188, 240), (55, 80, 110), (35, 55, 85))
        self._badge_female_surf = self._build_gender_badge("♀ Feminino", (228, 212, 190, 240), (150, 45, 55), (125, 30, 40))

        # Cache de status derivados (Zero Garbage e zero cálculos pesados a cada frame)
        self._cached_stats = None
        self._stats_dirty = True
        self._last_stats_key = None

        # Overlay do modal pré-alocado (Zero Garbage por frame)
        self._modal_overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        self._modal_overlay.fill((0, 0, 0, 150))

    def _build_gender_badge(self, text: str, bg_col: tuple, border_col: tuple, text_col: tuple) -> pygame.Surface:
        clean_text = clean_tofu_glyphs(text).strip()
        tw, th = self.font_ink_12.size(clean_text)
        bw, bh = max(96, tw + 16), 24
        surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
        pygame.draw.rect(surf, bg_col, (0, 0, bw, bh), border_radius=5)
        pygame.draw.rect(surf, border_col, (0, 0, bw, bh), 2, border_radius=5)
        pygame.draw.rect(surf, COLOR_GOLD, (2, 2, bw - 4, bh - 4), 1, border_radius=4)
        txt_s = self.font_ink_12.render(clean_text, True, text_col)
        surf.blit(txt_s, ((bw - tw) // 2, (bh - th) // 2))
        return surf

    def reset(self):
        """Reseta a ficha para criação limpa de um novo personagem."""
        self.player_name = ""
        self.active_input = False
        self.selected_race = ""
        self.selected_class = ""
        self.selected_background = ""
        self.selected_alignment = ""
        from core.dnd_rules import get_class_base_attributes
        self.base_attributes = get_class_base_attributes("Guerreiro")
        self.active_modal = None
        self.target_slot = ""
        self._cached_stats = None
        self._stats_dirty = True
        self._last_stats_key = None

    def get_current_stats(self) -> dict:
        """Retorna os status derivados atuais usando Standard Array da Classe selecionada e cache de alta performance."""
        current_key = (self.selected_race, self.selected_class, self.selected_background)
        if self._stats_dirty or self._cached_stats is None or self._last_stats_key != current_key:
            from core.dnd_rules import CharacterCalculator, get_class_base_attributes
            self.base_attributes = get_class_base_attributes(self.selected_class or "Guerreiro")
            self._cached_stats = CharacterCalculator.calculate_derived_stats(
                self.base_attributes,
                self.selected_race or "Humano",
                self.selected_class or "Guerreiro",
                self.selected_background or "Soldado"
            )
            # Sincroniza STR e FOR para compatibilidade universal
            if "FOR" in self._cached_stats.get("attributes", {}):
                self._cached_stats["attributes"]["STR"] = self._cached_stats["attributes"]["FOR"]
            self._last_stats_key = current_key
            self._stats_dirty = False
        return self._cached_stats

    def draw(self, screen: pygame.Surface):
        if not self.is_visible: return
        
        # Fundo e UI base (O Extermínio das Caixas)
        screen.blit(self.bg_image, (0, 0))
        
        from ui.hud_components import draw_ui_button
        from core.dnd_rules import get_protagonist_gender_info
        color_ink = (40, 20, 10) # #1A1A1A Tinta Escura
        
        def draw_aligned_text(text: str, coord: tuple, align: str, font: pygame.font.Font, is_active=False, is_hover=False, hitbox=None):
            if not text: return # Ignora se estiver vazio
            txt_surf = font.render(text, True, color_ink)
            rect = txt_surf.get_rect()
            
            if align == "midleft_pad": rect.midleft = (hitbox.left + 8, hitbox.centery)
            elif align == "center": rect.center = coord
            elif align == "bottomleft_offset": rect.bottomleft = (coord[0], coord[1] + 5) # Gravidade no eixo Y (+5)
            
            if hitbox and (is_active or is_hover):
                pygame.draw.rect(screen, (139, 0, 0), hitbox, 2, border_radius=4)
                
            screen.blit(txt_surf, rect)
            
        mouse_pos = pygame.mouse.get_pos()
        
        # 2. Hitboxes Delimitadas por Rects (Cabeçalho - pré-alocadas)
        c_cabe = self.coords["cabecalho"]
        hb_nome = getattr(self, "hb_nome", pygame.Rect(*c_cabe["nome"]))
        hb_raca = getattr(self, "hb_raca", pygame.Rect(*c_cabe["raca"]))
        hb_classe = getattr(self, "hb_classe", pygame.Rect(*c_cabe["classe"]))
        hb_bg = getattr(self, "hb_bg", pygame.Rect(*c_cabe["antecedentes"]))
        hb_align = getattr(self, "hb_align", pygame.Rect(*c_cabe["tendencia"]))
        
        cursor = "|" if self.active_input and (pygame.time.get_ticks() % 1000) < 500 else ""
        
        def draw_hitbox_border(hb, is_active, is_hover):
            if is_active or is_hover:
                pygame.draw.rect(screen, (139, 0, 0), hb, 2, border_radius=4)
                
        def render_padded_text(text, hb, max_w_override=None):
            if text:
                display_text = text
                avail_w = (max_w_override if max_w_override is not None else hb.width) - 6
                # Adaptação de fonte: tenta 20px, 16px, 14px e 12px antes de truncar
                font = self.font_ink
                if font.size(display_text)[0] > avail_w:
                    font = self.font_ink_small
                if font.size(display_text)[0] > avail_w:
                    font = getattr(self, "font_ink_14", AssetManager.get_font(14, bold=True))
                if font.size(display_text)[0] > avail_w:
                    font = getattr(self, "font_ink_12", AssetManager.get_font(12, bold=True))
                while font.size(display_text)[0] > avail_w and len(display_text) > 3:
                    display_text = display_text[:-1]
                if len(display_text) < len(text):
                    display_text = display_text.rstrip() + "..."
                        
                txt_surf = font.render(display_text, True, color_ink)
                rect = txt_surf.get_rect(midleft=(hb.left + 4, hb.centery))
                screen.blit(txt_surf, rect)
                
        # Nome
        draw_hitbox_border(self.hitbox_map["nome"], self.active_input, self.hitbox_map["nome"].collidepoint(mouse_pos))
        render_padded_text(self.player_name + cursor, hb_nome)
        
        # Indicativo de Gênero quando Raça e Classe estão selecionadas
        has_both = bool(self.selected_race and self.selected_class)
        gender_info = get_protagonist_gender_info(self.selected_race or "Humano", self.selected_class or "Guerreiro")

        # Dropdown Raça (+ Badge de Gênero à direita quando Raça e Classe preenchidas)
        draw_hitbox_border(self.hitbox_map["race"], False, self.hitbox_map["race"].collidepoint(mouse_pos))
        if has_both:
            badge_surf = self._badge_female_surf if gender_info["gender"] == "female" else self._badge_male_surf
            render_padded_text(self.selected_race, hb_raca, max_w_override=hb_raca.width - badge_surf.get_width() - 8)
            badge_rect = badge_surf.get_rect(midright=(hb_raca.right - 4, hb_raca.centery))
            screen.blit(badge_surf, badge_rect)
        else:
            render_padded_text(self.selected_race, hb_raca)
        
        # Dropdown Classe (Nome flexionado sem tofu quando Raça e Classe preenchidas)
        draw_hitbox_border(self.hitbox_map["class"], False, self.hitbox_map["class"].collidepoint(mouse_pos))
        class_text = f"{gender_info['class_display']}" if has_both else self.selected_class
        render_padded_text(clean_tofu_glyphs(class_text), hb_classe)
        
        draw_hitbox_border(self.hitbox_map["background"], False, self.hitbox_map["background"].collidepoint(mouse_pos))
        render_padded_text(self.selected_background, hb_bg)
        
        draw_hitbox_border(self.hitbox_map["alignment"], False, self.hitbox_map["alignment"].collidepoint(mouse_pos))
        render_padded_text(self.selected_alignment, hb_align)
        
        # 3. Status Dinâmicos (center) via Cache de Alta Performance
        stats = self.get_current_stats()
        from core.dnd_rules import RACAS_5E
        
        attr_map = {"FOR": "forca", "DES": "destreza", "CON": "constituicao", "INT": "inteligencia", "SAB": "sabedoria", "CAR": "carisma"}
        for attr_key, attr_pt in attr_map.items():
            # Coluna 1: Atributo Base (apenas quando classe estiver selecionada)
            if self.selected_class:
                base_val = self.base_attributes.get(attr_key, stats["attributes"].get(attr_key, 10))
                draw_aligned_text(str(base_val), self.coords["atributos"][attr_pt]["base"], "center", self.font_ink)
            
            # Coluna 2: Bônus Racial (apenas quando raça estiver selecionada)
            if self.selected_race:
                r_bonus = RACAS_5E.get(self.selected_race, {}).get("bonus", {}).get(attr_key, 0)
                bonus_str = f"+{r_bonus}" if r_bonus > 0 else "0"
                draw_aligned_text(bonus_str, self.coords["atributos"][attr_pt]["mod"], "center", self.font_ink)
            
        if self.selected_class:
            c_stat = self.coords["status"]
            draw_aligned_text(str(stats['ac']), c_stat["ca"], "center", self.font_ink)
            draw_aligned_text(str(stats['initiative']), c_stat["iniciativa"], "center", self.font_ink)
            draw_aligned_text(str(stats['speed']), c_stat["deslocamento"], "center", self.font_ink)
            draw_aligned_text(str(stats['hp_max']), c_stat["pv"], "center", self.font_ink)
            draw_aligned_text("+2", c_stat["proficiencia"], "center", self.font_ink)
        
        # 4. Flutuação das Listas (Habilidades e Equipamento - ocultos até seleção de classe)
        if self.selected_class:
            for i, ab in enumerate(stats["abilities"]):
                if i < len(self.coords["listas"]["habilidades"]):
                    draw_aligned_text(ab, self.coords["listas"]["habilidades"][i], "bottomleft_offset", self.font_ink_small)
                
            for i, eq in enumerate(stats["equipment"]):
                if i < len(self.coords["listas"]["equipamento"]):
                    draw_aligned_text(eq, self.coords["listas"]["equipamento"][i], "bottomleft_offset", self.font_ink_small)

        # Botões
        draw_ui_button(screen, self.btn_cancel, "Cancelar", self.font_body, self.btn_cancel.collidepoint(mouse_pos), True)
        draw_ui_button(screen, self.btn_start, "Iniciar Sessão Zero", self.font_body, self.btn_start.collidepoint(mouse_pos), self._is_ready())
        
        if self.active_modal:
            if getattr(self, "_modal_overlay", None) is None or self._modal_overlay.get_size() != (self.rect.width, self.rect.height):
                self._modal_overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                self._modal_overlay.fill((0, 0, 0, 150))
            screen.blit(self._modal_overlay, (0, 0))
            self.active_modal.draw(screen)

    def _is_ready(self) -> bool:
        return bool(self.player_name.strip() and self.selected_race and self.selected_class and 
                    self.selected_background and self.selected_alignment)
        
    def handle_event(self, event: pygame.event.Event):
        if not self.is_visible: return None
        
        if self.active_modal:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.active_modal = None
                return None
            selected = self.active_modal.handle_event(event)
            if selected:
                if selected != "CANCEL":
                    from core.dnd_rules import get_class_base_attributes
                    if self.target_slot == "race":
                        self.selected_race = selected
                    elif self.target_slot == "class":
                        self.selected_class = selected
                        self.base_attributes = get_class_base_attributes(self.selected_class)
                    elif self.target_slot == "background":
                        self.selected_background = selected
                    elif self.target_slot == "alignment":
                        self.selected_alignment = selected
                    self._stats_dirty = True
                self.active_modal = None
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_input = self.hitbox_map["nome"].collidepoint(event.pos)
                
            for key in ["race", "class", "background", "alignment"]:
                hb = self.hitbox_map[key]
                if hb.collidepoint(event.pos):
                    if key == "race":
                        self.active_modal = RaceSelectionPanel(self.data_lists[key], selected_class=self.selected_class)
                    elif key == "class":
                        self.active_modal = ClassSelectionPanel(self.data_lists[key], selected_race=self.selected_race)
                    elif key == "background":
                        self.active_modal = BackgroundSelectionPanel(self.data_lists[key])
                    elif key == "alignment":
                        self.active_modal = AlignmentSelectionPanel(self.data_lists[key])
                    self.active_modal.is_visible = True
                    self.target_slot = key
                    
            if self.btn_cancel.collidepoint(event.pos): return {"action": "cancel"}
            if self.btn_start.collidepoint(event.pos) and self._is_ready():
                from core.dnd_rules import get_protagonist_gender_info
                stats = self.get_current_stats()
                gender_info = get_protagonist_gender_info(self.selected_race, self.selected_class)

                eq_list = stats.get("equipment", [])
                eq_armor = stats.get("equipped_armor", eq_list[0] if len(eq_list) > 0 else "Trajes")
                eq_weapon = stats.get("equipped_weapon", eq_list[1] if len(eq_list) > 1 else "Adaga de Caça")
                eq_accessory = stats.get("equipped_accessory", eq_list[2] if len(eq_list) > 2 else "")

                final_char = {
                    "name": self.player_name.strip(),
                    "race": self.selected_race,
                    "class": self.selected_class,
                    "class_display": stats.get("class_display", gender_info["class_display"]),
                    "gender": stats.get("gender", gender_info["gender"]),
                    "gender_symbol": stats.get("gender_symbol", gender_info["symbol"]),
                    "gender_label": stats.get("gender_label", gender_info["label"]),
                    "background": self.selected_background,
                    "alignment": self.selected_alignment,
                    "attributes": stats["attributes"],
                    "hp_max": stats["hp_max"],
                    "hp_current": stats["hp_max"],
                    "ac": stats["ac"],
                    "initiative": stats["initiative"],
                    "speed": stats["speed"],
                    "inventory": stats["equipment"],
                    "abilities": stats["abilities"],
                    "proficiencies": stats["proficiencies"],
                    "level": 1,
                    "xp": 0,
                    "xp_to_next_level": stats.get("xp_to_next_level", 300),
                    "luck": stats["attributes"].get("LUCK", 10),
                    "gold": stats.get("gold", 15),
                    "has_shield": stats.get("has_shield", any("escudo" in item.lower() for item in eq_list)),
                    "equipped_armor": eq_armor,
                    "equipped_weapon": eq_weapon,
                    "equipped_accessory": eq_accessory,
                    "equipment": {
                        "weapon": eq_weapon,
                        "armor": eq_armor,
                        "accessory": eq_accessory
                    }
                }
                return {"action": "start", "char": final_char}
                
        elif event.type == pygame.KEYDOWN and self.active_input:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                self.active_input = False
            else:
                if len(self.player_name) < 20 and event.unicode.isprintable():
                    self.player_name += event.unicode
                    
        return None

class SessionZeroPanel(Panel):
    """O painel da Sessão Zero."""
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, title="O Oráculo (Prólogo)")
        
        sw, sh = 1280, 720
        raw_bg = AssetManager.get_image("background", "prologue_bg")
        self.bg_image = pygame.transform.scale(raw_bg, (sw, sh))
        
        self.overlay = pygame.Surface((sw, sh))
        self.overlay.set_alpha(150)
        self.overlay.fill((0, 0, 0))
        
        self.font_ink = AssetManager.get_font(20, bold=True)
        
        self.question = "Carregando as perguntas do Mestre..."
        self.is_prologue = False
        self.player_answer = ""
        self.active_input = True
        
        self.input_rect = pygame.Rect(x + 50, y + height - 120, width - 100, 40)
        self.btn_submit = pygame.Rect(x + width//2 - 100, y + height - 60, 200, 40)
        
    def set_question(self, text: str, is_prologue: bool = False):
        self.question = text
        self.is_prologue = is_prologue
        self.player_answer = ""
        
    def draw(self, screen: pygame.Surface):
        if not self.is_visible: return
        
        screen.blit(self.bg_image, (0, 0))
        
        # Variáveis de Calibragem Expostas (Prólogo / Sessão Zero)
        TEXT_START_X = 160
        TEXT_START_Y = 211
        MAX_WIDTH = 960
        LINE_SPACING = 34
        
        color_ink = (40, 20, 10) # Tinta envelhecida com anti-aliasing
        
        from ui.hud_components import draw_text_wrapped, get_wrapped_text_dimensions
        # Proteção da Margem Inferior: Limitamos a altura do text_rect para terminar antes do botão inferior (que fica em y=600)
        # 600 - 40 (tamanho do botão) = 560.
        text_rect = pygame.Rect(TEXT_START_X, TEXT_START_Y, MAX_WIDTH, 540 - TEXT_START_Y)
        draw_text_wrapped(screen, self.question, self.font_ink, color_ink, text_rect, fixed_line_height=LINE_SPACING)
        
        # Recuperar quantidade de linhas para desenhar o input embaixo
        _, _, lines = get_wrapped_text_dimensions(self.question, self.font_ink, MAX_WIDTH, fixed_line_height=LINE_SPACING)
        start_y = 235
        start_x = TEXT_START_X
        line_spacing = LINE_SPACING
        

        from ui.hud_components import draw_ui_button
        mouse_pos = pygame.mouse.get_pos()
        
        if not self.is_prologue:
            if self.question.startswith("O Oráculo") or self.question.startswith("O Mestre"):
                # Apenas exibe o status de carregamento sem caixa de input
                pass
            else:
                # A linha da resposta será 1 linha abaixo da última linha da pergunta
                answer_line_index = len(lines) + 1
                answer_y = start_y + (answer_line_index * line_spacing)
                
                # Desenha "Sua Resposta: " exatamente na linha
                lbl = self.font_ink.render("Sua Resposta: ", True, color_ink)
                lbl_rect = lbl.get_rect(bottomleft=(start_x, answer_y - 4))
                screen.blit(lbl, lbl_rect)
                
                # Define a hitbox invisível para o input logo após o label
                self.input_rect.x = lbl_rect.right
                self.input_rect.y = answer_y - 25
                self.input_rect.width = MAX_WIDTH - lbl.get_width()
                self.input_rect.height = 30
                
                # Cursor piscante sutil
                import time
                show_cursor = self.active_input and int(time.time() * 2) % 2 == 0
                cursor = "|" if show_cursor else ""
                
                # Renderiza o que o jogador digitou na mesma linha
                ans_surf = self.font_ink.render(self.player_answer + cursor, True, color_ink)
                ans_rect = ans_surf.get_rect(bottomleft=(lbl_rect.right + 5, answer_y - 4))
                screen.blit(ans_surf, ans_rect)
                
                # Botão
                self.btn_submit.centerx = 1280 // 2
                self.btn_submit.y = answer_y + 40
                draw_ui_button(screen, self.btn_submit, "Responder", self.font_title, self.btn_submit.collidepoint(mouse_pos), True)
        else:
            self.btn_submit.centerx = 1280 // 2
            self.btn_submit.y = 600
            draw_ui_button(screen, self.btn_submit, "Entrar no Jogo", self.font_title, self.btn_submit.collidepoint(mouse_pos), True)

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.is_visible: return ""
        
        is_loading = self.question.startswith("O Oráculo") or self.question.startswith("O Mestre")
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_loading:
                self.active_input = self.input_rect.collidepoint(event.pos)
                if self.btn_submit.collidepoint(event.pos):
                    if self.is_prologue: return "start_game"
                    elif self.player_answer.strip(): 
                        ans = self.player_answer.strip()
                        self.player_answer = ""
                        return ans
        elif event.type == pygame.KEYDOWN and self.active_input and not self.is_prologue and not is_loading:
            if event.key == pygame.K_BACKSPACE: self.player_answer = self.player_answer[:-1]
            elif event.key == pygame.K_RETURN:
                if self.player_answer.strip():
                    ans = self.player_answer.strip()
                    self.player_answer = ""
                    return ans
            else:
                if len(self.player_answer) < 80 and event.unicode.isprintable():
                    self.player_answer += event.unicode
        return ""

class PauseMenuPanel(Panel):
    """Menu de Pausa In-Game."""
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, title="Menu de Pausa")
        btn_w, btn_h = 250, 40
        btn_x = x + (width - btn_w) // 2
        
        self.btn_resume = pygame.Rect(btn_x, y + 70, btn_w, btn_h)
        self.btn_journal = pygame.Rect(btn_x, y + 120, btn_w, btn_h)
        self.btn_manual = pygame.Rect(btn_x, y + 170, btn_w, btn_h)
        self.btn_save = pygame.Rect(btn_x, y + 220, btn_w, btn_h)
        self.btn_quit = pygame.Rect(btn_x, y + 270, btn_w, btn_h)
        
    def _draw_button(self, screen, rect, text):
        from ui.hud_components import draw_ui_button
        mouse_pos = pygame.mouse.get_pos()
        draw_ui_button(screen, rect, text, self.font_title, rect.collidepoint(mouse_pos), True)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        if not self.is_visible: return
        self._draw_button(screen, self.btn_resume, "Retomar")
        self._draw_button(screen, self.btn_journal, "Diário de Aventuras")
        self._draw_button(screen, self.btn_manual, "Manual do Jogador")
        self._draw_button(screen, self.btn_save, "Salvar Jogo")
        self._draw_button(screen, self.btn_quit, "Sair para o Menu")

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.is_visible: return ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_resume.collidepoint(event.pos): return "resume"
            if self.btn_journal.collidepoint(event.pos): return "journal"
            if hasattr(self, "btn_manual") and self.btn_manual.collidepoint(event.pos): return "action_player_manual"
            if self.btn_save.collidepoint(event.pos): return "save"
            if self.btn_quit.collidepoint(event.pos): return "quit"
        return ""

class JournalModal(Panel):
    """Diário de Aventuras exibindo NPCs e Quests."""
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, title="Diário de Aventuras")
        self.btn_close = pygame.Rect(x + width//2 - 60, y + height - 50, 120, 35)
        self.game_state_ref = None

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        if not self.is_visible or not self.game_state_ref: return
        
        scroll_rect = pygame.Rect(self.rect.x + 20, self.rect.y + 60, self.rect.width - 40, self.rect.height - 130)
        
        # O fundo agora é escuro (Retro Panel na base), não precisa desenhar pergaminho extra.
        # Apenas mudar as cores do texto para contraste claro.
        
        y_off = scroll_rect.y + 10
        screen.blit(self.font_title.render("Pessoas Conhecidas", True, COLOR_GOLD), (scroll_rect.x + 10, y_off))
        y_off += 35
        
        npcs = self.game_state_ref.get("known_npcs", {})
        if not npcs:
            screen.blit(self.font_body.render("Você ainda não conhece ninguém.", True, COLOR_PARCHMENT), (scroll_rect.x + 20, y_off))
        else:
            from ui.hud_components import draw_text_wrapped
            for name, desc in npcs.items():
                lbl = self.font_body.render(f"• {name}", True, COLOR_ACCENT)
                screen.blit(lbl, (scroll_rect.x + 10, y_off))
                y_off += 25
                desc_rect = pygame.Rect(scroll_rect.x + 30, y_off, scroll_rect.width - 40, 100)
                draw_text_wrapped(screen, desc, self.font_body, COLOR_PARCHMENT, desc_rect)
                y_off += 40

        mouse_pos = pygame.mouse.get_pos()
        from ui.hud_components import draw_ui_button
        draw_ui_button(screen, self.btn_close, "Fechar", self.font_body, self.btn_close.collidepoint(mouse_pos), True)

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.is_visible: return ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_close.collidepoint(event.pos): return "close"
        return ""

class SaveSelectionPanel(Panel):
    """Tela de Seleção de 3 Slots de Salvamento com estética de páginas de pergaminho antigo."""
    
    def __init__(self, x: int = 0, y: int = 0, width: int = 1280, height: int = 720):
        super().__init__(0, 0, 1280, 720, title="")
        
        sw, sh = 1280, 720
        raw_bg = AssetManager.get_image("background", "menu_bg")
        self.bg_image = pygame.transform.scale(raw_bg, (sw, sh))
        
        # Sobreposição translúcida gótica (Zero Garbage por frame)
        self.overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        self.overlay.fill((10, 8, 12, 215))
        
        # Fontes Rústicas
        self.font_header = AssetManager.get_font(28, bold=True)
        self.font_sub = AssetManager.get_font(16, italic=True)
        self.font_card_title = AssetManager.get_font(20, bold=True)
        self.font_hero_name = AssetManager.get_font(22, bold=True)
        self.font_info_bold = AssetManager.get_font(15, bold=True)
        self.font_info = AssetManager.get_font(14)
        self.font_btn = AssetManager.get_font(15, bold=True)
        self.font_btn_sm = AssetManager.get_font(13, bold=True)
        
        # Geometria dos 3 Cards de Pergaminho
        self.card_w = 360
        self.card_h = 515
        self.card_y = 105
        self.cards_rects = [
            pygame.Rect(60, self.card_y, self.card_w, self.card_h),
            pygame.Rect(460, self.card_y, self.card_w, self.card_h),
            pygame.Rect(860, self.card_y, self.card_w, self.card_h)
        ]
        
        # Botão inferior centralizado de retorno ao menu
        self.btn_back = pygame.Rect(sw // 2 - 130, 642, 260, 44)
        
        # Botões interativos dos slots (calculados por slot)
        self.slot_buttons = {}  # slot_num -> {"load": Rect, "new": Rect, "delete": Rect}
        self._init_slot_buttons()
        
        # Pré-renderização da textura do pergaminho do card (Zero Garbage por frame a 60 FPS)
        self._card_bg_surf = self._create_parchment_card_surface()
        
        # Cache de metadados dos slots e retratos
        self.slots_data = []
        self._portrait_cache = {}
        self.refresh_slots()

    def _init_slot_buttons(self):
        for i, card in enumerate(self.cards_rects):
            slot_num = i + 1
            cx = card.centerx
            btn_load = pygame.Rect(cx - 105, card.bottom - 80, 210, 36)
            btn_delete = pygame.Rect(cx - 55, card.bottom - 36, 110, 26)
            btn_new = pygame.Rect(cx - 110, card.bottom - 85, 220, 42)
            self.slot_buttons[slot_num] = {
                "load": btn_load,
                "delete": btn_delete,
                "new": btn_new
            }

    def _create_parchment_card_surface(self) -> pygame.Surface:
        """Pré-renderiza uma página de pergaminho envelhecida com bordas desgastadas e cantoneiras."""
        w, h = self.card_w, self.card_h
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # Fundo do pergaminho envelhecido
        c_parchment = (235, 223, 195)
        c_parchment_dark = (215, 200, 170)
        c_border_wood = (48, 32, 18)
        c_gold = (185, 145, 60)
        c_bronze = (120, 85, 40)
        
        # Corpo do pergaminho com cantos arredondados
        pygame.draw.rect(surf, c_parchment, (0, 0, w, h), border_radius=6)
        
        # Linhas de envelhecimento sutil / textura de pergaminho
        for dy in range(12, h - 12, 38):
            pygame.draw.line(surf, c_parchment_dark, (16, dy), (w - 16, dy), 1)
            
        # Borda externa de madeira rústica
        pygame.draw.rect(surf, c_border_wood, (0, 0, w, h), 3, border_radius=6)
        # Moldura interna de ouro envelhecido
        pygame.draw.rect(surf, c_gold, (6, 6, w - 12, h - 12), 2, border_radius=4)
        # Filete ornamental bronze
        pygame.draw.rect(surf, c_bronze, (10, 10, w - 20, h - 20), 1, border_radius=3)
        
        # Cantoneiras com losangos de ouro
        corner_len = 22
        for (ox, oy, dx, dy) in [(8, 8, 1, 1), (w - 8, 8, -1, 1), (8, h - 8, 1, -1), (w - 8, h - 8, -1, -1)]:
            pygame.draw.line(surf, c_gold, (ox, oy), (ox + dx * corner_len, oy), 2)
            pygame.draw.line(surf, c_gold, (ox, oy), (ox, oy + dy * corner_len), 2)
            lx, ly = ox + dx * 8, oy + dy * 8
            pts = [(lx, ly - 3), (lx + 3, ly), (lx, ly + 3), (lx - 3, ly)]
            pygame.draw.polygon(surf, c_gold, pts)
            
        return surf

    def refresh_slots(self):
        """Atualiza os metadados dos 3 slots de salvamento a partir do SessionManager."""
        from core.game_engine import SessionManager
        self.slots_data = SessionManager.get_all_slots_summary()
        self._portrait_cache.clear()
        for slot in self.slots_data:
            if not slot.get("is_empty"):
                slot_num = slot.get("slot", 1)
                race = slot.get("race", "Humano")
                cls_name = slot.get("class", "Guerreiro")
                gender = slot.get("gender", "male")
                name = slot.get("name", "")
                icon = AssetManager.get_hero_icon(race, cls_name, gender)
                if icon:
                    scaled = pygame.transform.scale(icon, (96, 96))
                else:
                    scaled = AssetManager.get_portrait_sprite(name)
                self._portrait_cache[slot_num] = scaled

    def draw(self, screen: pygame.Surface):
        if not self.is_visible:
            return
            
        # Fundo e sobreposição translúcida
        screen.blit(self.bg_image, (0, 0))
        screen.blit(self.overlay, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()
        c_gold = (245, 215, 110)
        c_ink = (35, 20, 10)
        c_ink_dim = (80, 60, 45)
        c_sep = (160, 125, 60)
        
        # Cabeçalho Principal
        title_surf = self.font_header.render("Crônicas da Taverna • Tomo de Destinos", True, c_gold)
        title_rect = title_surf.get_rect(center=(1280 // 2, 42))
        screen.blit(title_surf, title_rect)
        
        sub_surf = self.font_sub.render("Selecione um pergaminho para retomar sua campanha ou forjar uma nova lenda", True, (215, 200, 175))
        sub_rect = sub_surf.get_rect(center=(1280 // 2, 74))
        screen.blit(sub_surf, sub_rect)
        
        # Renderização dos 3 Cards de Pergaminho
        for i, card_rect in enumerate(self.cards_rects):
            slot_num = i + 1
            slot_data = self.slots_data[i] if i < len(self.slots_data) else {"slot": slot_num, "is_empty": True}
            
            # 1. Blit da página de pergaminho pré-renderizada
            screen.blit(self._card_bg_surf, (card_rect.x, card_rect.y))
            
            # Efeito de hover no card
            if card_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 220, 120), card_rect, 2, border_radius=6)
                
            cx = card_rect.centerx
            btns = self.slot_buttons.get(slot_num, {})
            
            # Cabeçalho do Card (Número Romano do Slot)
            slot_roman = ["I", "II", "III"][i]
            slot_header_txt = f"PERGAMINHO {slot_roman}"
            hdr_surf = self.font_card_title.render(slot_header_txt, True, (130, 20, 20))
            screen.blit(hdr_surf, hdr_surf.get_rect(center=(cx, card_rect.y + 30)))
            
            # Divisor Ornamental superior
            div_txt = "-----------------"
            div_surf = self.font_info.render(div_txt, True, c_sep)
            screen.blit(div_surf, div_surf.get_rect(center=(cx, card_rect.y + 50)))
            
            if not slot_data.get("is_empty"):
                # Retrato do Herói em Moldura Elegante
                portrait_surf = self._portrait_cache.get(slot_num)
                port_y = card_rect.y + 68
                port_rect = pygame.Rect(cx - 48, port_y, 96, 96)
                
                pygame.draw.rect(screen, (30, 20, 15), (cx - 52, port_y - 4, 104, 104), border_radius=4)
                if portrait_surf:
                    screen.blit(portrait_surf, port_rect)
                pygame.draw.rect(screen, (190, 150, 65), (cx - 52, port_y - 4, 104, 104), 2, border_radius=4)
                
                # Nome do Herói
                name_txt = slot_data.get("name", "Herói")
                if len(name_txt) > 20:
                    name_txt = name_txt[:18] + ".."
                name_surf = self.font_hero_name.render(name_txt, True, c_ink)
                screen.blit(name_surf, name_surf.get_rect(center=(cx, card_rect.y + 192)))
                
                # Raça, Classe e Nível
                r_c_txt = f"{slot_data.get('race', '')} {slot_data.get('class', '')} • Nível {slot_data.get('level', 1)}"
                rc_surf = self.font_info_bold.render(r_c_txt, True, (120, 30, 20))
                screen.blit(rc_surf, rc_surf.get_rect(center=(cx, card_rect.y + 220)))
                
                # Divisor interno
                screen.blit(div_surf, div_surf.get_rect(center=(cx, card_rect.y + 242)))
                
                # Localização / Capítulo Atual
                loc_txt = slot_data.get("location", "Ato I • Taverna")
                loc_surf = self.font_info_bold.render(loc_txt, True, c_ink)
                screen.blit(loc_surf, loc_surf.get_rect(center=(cx, card_rect.y + 266)))
                
                # Caixa com Atributos Vitais
                info_start_y = card_rect.y + 296
                hp_cur = slot_data.get("hp_current", 10)
                hp_max = slot_data.get("hp_max", 10)
                gold = slot_data.get("gold", 0)
                day = slot_data.get("current_day", 1)
                quests = slot_data.get("quests_completed", 0)
                
                info_lines = [
                    ("Pontos de Vida:", f"{hp_cur}/{hp_max} PV"),
                    ("Tesouro Acumulado:", f"{gold} PO"),
                    ("Jornada:", f"Dia {day}"),
                    ("Missões Concluídas:", f"{quests}")
                ]
                
                for label, val in info_lines:
                    lbl_surf = self.font_info.render(label, True, c_ink_dim)
                    val_surf = self.font_info_bold.render(val, True, c_ink)
                    screen.blit(lbl_surf, (card_rect.x + 36, info_start_y))
                    screen.blit(val_surf, (card_rect.right - 36 - val_surf.get_width(), info_start_y))
                    info_start_y += 24
                    
                # Botão Continuar Jornada
                btn_load = btns["load"]
                draw_ui_button(screen, btn_load, "Continuar Jornada", self.font_btn, btn_load.collidepoint(mouse_pos), True)
                
                # Botão Excluir (Discreto)
                btn_del = btns["delete"]
                draw_ui_button(screen, btn_del, "Excluir", self.font_btn_sm, btn_del.collidepoint(mouse_pos), True)
                
            else:
                # CARD VAZIO: PÁGINA EM BRANCO PARA NOVA CAMPANHA
                empty_y = card_rect.y + 110
                
                icon_rect = pygame.Rect(cx - 45, empty_y, 90, 110)
                pygame.draw.rect(screen, (220, 205, 175), icon_rect, border_radius=4)
                pygame.draw.rect(screen, (160, 130, 80), icon_rect, 2, border_radius=4)
                
                for ly in range(empty_y + 16, empty_y + 95, 14):
                    pygame.draw.line(screen, (185, 165, 135), (cx - 30, ly), (cx + 30, ly), 1)
                    
                empty_title = self.font_hero_name.render("Slot Vazio", True, c_ink_dim)
                screen.blit(empty_title, empty_title.get_rect(center=(cx, empty_y + 150)))
                
                line1 = self.font_info_bold.render("Nenhum Registro Gravado", True, (130, 80, 40))
                screen.blit(line1, line1.get_rect(center=(cx, empty_y + 185)))
                
                line2 = self.font_info.render("As páginas deste tomo aguardam", True, c_ink_dim)
                line3 = self.font_info.render("a tinta de uma nova lenda...", True, c_ink_dim)
                screen.blit(line2, line2.get_rect(center=(cx, empty_y + 220)))
                screen.blit(line3, line3.get_rect(center=(cx, empty_y + 242)))
                
                btn_new = btns["new"]
                draw_ui_button(screen, btn_new, "+ Nova Campanha", self.font_btn, btn_new.collidepoint(mouse_pos), True)
                
        # Botão inferior "Voltar ao Menu Principal"
        draw_ui_button(screen, self.btn_back, "Voltar ao Menu Principal", self.font_btn, self.btn_back.collidepoint(mouse_pos), True)

    def handle_event(self, event: pygame.event.Event):
        if not self.is_visible:
            return None
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back_to_menu"
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.btn_back.collidepoint(pos):
                return "back_to_menu"
                
            for i in range(3):
                slot_num = i + 1
                slot_data = self.slots_data[i] if i < len(self.slots_data) else {"is_empty": True}
                btns = self.slot_buttons.get(slot_num, {})
                
                if not slot_data.get("is_empty"):
                    if btns.get("load") and btns["load"].collidepoint(pos):
                        return ("load_slot", slot_num)
                    elif btns.get("delete") and btns["delete"].collidepoint(pos):
                        return ("delete_slot", slot_num)
                else:
                    if btns.get("new") and btns["new"].collidepoint(pos):
                        return ("new_game_slot", slot_num)
                        
        return None
