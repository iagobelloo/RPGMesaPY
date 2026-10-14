import os
import math
from typing import Optional, Dict
import pygame
from ui.asset_manager import AssetManager

# --- Nova Paleta de Cores: Fantasia Medieval ---
COLOR_WOOD_DARK = (62, 39, 35)      # #3E2723 (Madeira Escura)
COLOR_PARCHMENT = (245, 230, 204)   # #F5E6CC (Pergaminho)
COLOR_GOLD = (212, 175, 55)         # #D4AF37 (Dourado Envelhecido)
COLOR_INK = (26, 26, 26)            # #1A1A1A (Tinta Escura para leitura no pergaminho)

COLOR_BG = (15, 15, 15)             # Fundo absoluto
COLOR_PANEL_BG = COLOR_WOOD_DARK    # Fundo dos painéis base
COLOR_BORDER = COLOR_GOLD
COLOR_TEXT = COLOR_PARCHMENT        # Texto sobre a madeira
COLOR_TEXT_DIM = (150, 130, 100)
COLOR_ACCENT = (180, 40, 40)        # Destaques / Seleção (Vermelho Sangue)

_PANEL_SURF_CACHE = {}
_BUTTON_BG_CACHE = {}

def clear_hud_cache():
    """Limpa caches de superfícies pré-renderizadas do HUD."""
    _PANEL_SURF_CACHE.clear()
    _BUTTON_BG_CACHE.clear()

def clean_tofu_glyphs(text: str) -> str:
    """Substitui caracteres exóticos que geram tofu/quadrados brancos na fonte Retro Gaming."""
    if not text:
        return ""
    replacements = {
        "⚔": "",
        "🛡": "",
        "❖": "",
        "─": "-",
        "◆": "*",
        "«": '"',
        "»": '"',
        "★": "",
        "➔": "->",
        "♂": "",
        "♀": "",
        "🔒": "",
        "✓": "[OK]",
        "⚡": "",
        "✨": "",
        "🌟": "",
        "🎲": "",
        "💀": "",
        "—": "-",
        "■": "*",
        "□": "-",
        "•": "-",
    }
    res = text
    for k, v in replacements.items():
        res = res.replace(k, v)
    if "\n" in text:
        return "\n".join(" ".join(line.split()) for line in res.splitlines())
    return " ".join(res.split())

def draw_ui_panel(screen: pygame.Surface, rect: pygame.Rect, asset_name: str = "wood_panel"):
    """Desenha um painel UI usando um Retro Panel programático com cache de superfície."""
    key = (rect.width, rect.height)
    panel_surf = _PANEL_SURF_CACHE.get(key)
    if panel_surf is None:
        panel_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        panel_surf.fill((20, 20, 20, 220))
        pygame.draw.rect(panel_surf, (212, 175, 55), panel_surf.get_rect(), 2)
        _PANEL_SURF_CACHE[key] = panel_surf
    screen.blit(panel_surf, (rect.x, rect.y))

def draw_ui_button(screen: pygame.Surface, rect: pygame.Rect, text: str, font: pygame.font.Font, is_hover: bool = False, is_ready: bool = True):
    """Desenha um botão lógico puro com cache de superfície para o fundo."""
    key = (rect.width, rect.height, is_hover, is_ready)
    btn_surf = _BUTTON_BG_CACHE.get(key)
    if btn_surf is None:
        # Cores (Alma de Taverna)
        bg_color = (56, 34, 21, 200) # Marrom Madeira Quente
        if not is_ready:
            bg_color = (30, 20, 15, 200)
        elif is_hover:
            bg_color = (92, 46, 46, 200) # Madeira Avermelhada
            
        border_color = (192, 133, 82) # Ouro Envelhecido / Madeira Clara
        if not is_ready:
            border_color = (80, 60, 40)
            
        btn_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, bg_color, btn_surf.get_rect(), border_radius=6)
        pygame.draw.rect(btn_surf, border_color, btn_surf.get_rect(), 3, border_radius=6)
        _BUTTON_BG_CACHE[key] = btn_surf
        
    screen.blit(btn_surf, (rect.x, rect.y))
        
    font.set_bold(True)
    # Texto Centralizado com sanitização de caracteres exóticos
    text_color = (245, 245, 230) # Bege claro / branco
    if not is_ready:
        text_color = (120, 120, 120)
    display_text = clean_tofu_glyphs(text)
    txt_surf = font.render(display_text, True, text_color)
    tx = rect.x + (rect.width - txt_surf.get_width()) // 2
    ty = rect.y + (rect.height - txt_surf.get_height()) // 2
    screen.blit(txt_surf, (tx, ty))

def get_wrapped_text_dimensions(text: str, font: pygame.font.Font, max_width: int, fixed_line_height: int = None) -> tuple:
    """Calcula as dimensões finais e quebra o texto em linhas dadas uma largura máxima."""
    if not text: return 0, 0, []
    
    paragraphs = text.split("\n")
    lines = []
    max_line_width = 0
    
    for para in paragraphs:
        if not para.strip():
            lines.append("")
            continue
            
        words = para.split(" ")
        current_line = ""
        
        for word in words:
            if not word: continue
            
            if font.size(word)[0] > max_width:
                if current_line:
                    lines.append(current_line.rstrip())
                    w = font.size(current_line.rstrip())[0]
                    if w > max_line_width: max_line_width = w
                    current_line = ""
                temp_w = ""
                for char in word:
                    if font.size(temp_w + char)[0] <= max_width:
                        temp_w += char
                    else:
                        lines.append(temp_w)
                        w = font.size(temp_w)[0]
                        if w > max_line_width: max_line_width = w
                        temp_w = char
                current_line = temp_w + " "
                continue
                
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.rstrip())
                w = font.size(current_line.rstrip())[0]
                if w > max_line_width: max_line_width = w
                current_line = word + " "
                
        if current_line:
            lines.append(current_line.rstrip())
            w = font.size(current_line.rstrip())[0]
            if w > max_line_width: max_line_width = w

    line_h = fixed_line_height if fixed_line_height else font.get_linesize()
    total_height = len(lines) * line_h
    return max_line_width, total_height, lines

def draw_text_wrapped(surface: pygame.Surface, text: str, font: pygame.font.Font, color: tuple, rect: pygame.Rect, fixed_line_height: int = None):
    """Desenha texto com quebra de linha automática (Word Wrap) dentro de um pygame.Rect."""
    _, _, lines = get_wrapped_text_dimensions(text, font, rect.width, fixed_line_height)
    y_offset = rect.y
    line_h = fixed_line_height if fixed_line_height else font.get_linesize()
    
    for line in lines:
        if y_offset + font.get_height() > rect.bottom:
            break
        if line:
            txt_surf = font.render(line, True, color)
            surface.blit(txt_surf, (rect.x, y_offset))
        y_offset += line_h

class Panel:
    """Classe base para modais e painéis na tela."""
    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.is_visible = False
        
        # Fontes Rústicas (Tenta usar fontes nativas que pareçam medievais)
        self.font_title = AssetManager.get_font(26, bold=True, italic=True)
        self.font_body = AssetManager.get_font(18)

    def draw(self, screen: pygame.Surface):
        if not self.is_visible:
            return
            
        draw_ui_panel(screen, self.rect, "wood_panel")
        
        if self.title:
            # Título num "banner" dourado no topo
            title_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 40)
            pygame.draw.rect(screen, COLOR_GOLD, title_rect)
            pygame.draw.rect(screen, (40, 20, 15), title_rect, 2)
            
            title_surf = self.font_title.render(self.title, True, COLOR_WOOD_DARK)
            screen.blit(title_surf, (self.rect.x + (self.rect.width - title_surf.get_width()) // 2, self.rect.y + 5))

    def handle_event(self, event: pygame.event.Event):
        pass

class MainMenuPanel(Panel):
    """Painel inicial (Menu de Abertura)."""
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, title="Crônicas da Taverna")
        
        from ui.asset_manager import AssetManager
        sw, sh = 1280, 720
        raw_bg = AssetManager.get_image("background", "menu_bg")
        self.bg_image = pygame.transform.scale(raw_bg, (sw, sh))
        
        self.overlay = pygame.Surface((sw, sh))
        self.overlay.set_alpha(150)
        self.overlay.fill((0, 0, 0))
        
        # Botões centralizados
        btn_w, btn_h = 260, 46
        btn_x = x + (width - btn_w) // 2
        self.btn_new_game = pygame.Rect(btn_x, y + 80, btn_w, btn_h)
        self.btn_load_game = pygame.Rect(btn_x, y + 138, btn_w, btn_h)
        self.btn_manual = pygame.Rect(btn_x, y + 196, btn_w, btn_h)
        self.btn_quit = pygame.Rect(btn_x, y + 254, btn_w, btn_h)
        
    def _draw_button(self, screen, rect, text, is_active=True):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        draw_ui_button(screen, rect, text, self.font_title, is_hover, is_active)

    def draw(self, screen: pygame.Surface):
        if not self.is_visible: return
        
        screen.blit(self.bg_image, (0, 0))
        screen.blit(self.overlay, (0, 0))
        
        # Título Flutuante Cinematográfico
        title_font = AssetManager.get_font(62, bold=True, italic=True)
        title_text = self.title
        
        # Sombra (Text Shadow)
        shadow_surf = title_font.render(title_text, True, (0, 0, 0))
        screen.blit(shadow_surf, (self.rect.x + (self.rect.width - shadow_surf.get_width()) // 2 + 3, self.rect.y - 40 + 3))
        
        # Texto Principal Dourado/Amarelado
        title_surf = title_font.render(title_text, True, (229, 192, 123)) # #E5C07B
        screen.blit(title_surf, (self.rect.x + (self.rect.width - title_surf.get_width()) // 2, self.rect.y - 40))
        
        self._draw_button(screen, self.btn_new_game, "Nova Campanha", True)
        self._draw_button(screen, self.btn_load_game, "Carregar Jogo", True)
        self._draw_button(screen, self.btn_manual, "Manual do Jogador", True)
        self._draw_button(screen, self.btn_quit, "Sair", True)

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.is_visible: return ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_new_game.collidepoint(event.pos): return "action_new_game"
            if self.btn_load_game.collidepoint(event.pos): return "action_load_game"
            if hasattr(self, "btn_manual") and self.btn_manual.collidepoint(event.pos): return "action_player_manual"
            if self.btn_quit.collidepoint(event.pos): return "action_quit"
        return ""

class ChatBox:
    """Caixa de digitação in-game encapsulada."""
    def __init__(self, x: int, y: int, width: int, height: int, max_chars: int = 100):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = AssetManager.get_font(16)
        self.max_chars = max_chars
        self.active = True
        self._bg_surface = None
        self._recreate_bg_surface()
        
    def _recreate_bg_surface(self):
        """Cria ou atualiza a superfície de fundo translúcida uma única vez."""
        self._bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self._bg_surface.fill((15, 15, 15, 210))
        pygame.draw.rect(self._bg_surface, (180, 150, 50), self._bg_surface.get_rect(), 2)

    def draw(self, screen: pygame.Surface):
        if self._bg_surface is None or self._bg_surface.get_size() != (self.rect.width, self.rect.height):
            self._recreate_bg_surface()
        screen.blit(self._bg_surface, (self.rect.x, self.rect.y))
        
        cursor = ""
        if self.active and (pygame.time.get_ticks() % 1000) < 500:
            cursor = "|"
            
        txt_surf = self.font.render(self.text + cursor, True, (240, 230, 200))
        screen.blit(txt_surf, (self.rect.x + 15, self.rect.y + 10))
        
    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.active: return ""
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.text.strip():
                    res = self.text.strip()
                    self.text = ""
                    return res
            else:
                if len(self.text) < self.max_chars and event.unicode.isprintable():
                    self.text += event.unicode
        return ""

TextInputBar = ChatBox


class CharacterSheetOverlay(Panel):
    """Overlay exibido ao segurar/apertar TAB durante o jogo."""
    def __init__(self, width: int, height: int):
        # Vai ocupar uma janela razoável
        super().__init__(40, 40, width - 80, height - 80, title="Ficha do Personagem")
        self.game_state_ref = None

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        if not self.is_visible or not self.game_state_ref: return
        
        pc = self.game_state_ref.get("player_character")
        if not pc: return

        # Dividimos em 3 painéis internos (Esquerda: Stats, Meio: Status, Direita: Inventário)
        inner_y = self.rect.y + 60
        font_b = AssetManager.get_font(16, bold=True)
        font_n = AssetManager.get_font(16)
        
        # --- PAINEL ESQUERDO: Atributos ---
        left_x = self.rect.x + 20
        screen.blit(self.font_title.render("Atributos", True, COLOR_GOLD), (left_x, inner_y))
        
        attrs = pc.get("attributes", {})
        attr_order = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for i, a in enumerate(attr_order):
            val = attrs.get(a, 10)
            mod = (val - 10) // 2
            mod_str = f"+{mod}" if mod >= 0 else str(mod)
            txt = f"{a}: {val} ({mod_str})"
            screen.blit(font_b.render(txt, True, COLOR_TEXT), (left_x, inner_y + 40 + (i * 30)))
            
        # --- PAINEL CENTRAL: Status de Combate ---
        mid_x = self.rect.x + (self.rect.width // 3) + 20
        screen.blit(self.font_title.render("Status", True, COLOR_GOLD), (mid_x, inner_y))
        
        hp_cur = pc.get("hp_current", 0)
        hp_max = pc.get("hp_max", 0)
        
        screen.blit(font_b.render(f"Nome: {pc.get('name')}", True, COLOR_TEXT), (mid_x, inner_y + 40))
        screen.blit(font_n.render(f"{pc.get('race')} {pc.get('class')}", True, COLOR_TEXT_DIM), (mid_x, inner_y + 65))
        
        hp_color = (100, 255, 100) if hp_cur > (hp_max // 2) else (255, 100, 100)
        screen.blit(font_b.render(f"HP: {hp_cur} / {hp_max}", True, hp_color), (mid_x, inner_y + 100))
        screen.blit(font_b.render(f"Armadura: {pc.get('equipped_armor').capitalize()} {'(+Escudo)' if pc.get('has_shield') else ''}", True, COLOR_TEXT), (mid_x, inner_y + 130))
        
        # --- PAINEL DIREITO: Inventário ---
        right_x = self.rect.x + ((self.rect.width // 3) * 2) + 20
        screen.blit(self.font_title.render("Inventário & Magias", True, COLOR_GOLD), (right_x, inner_y))
        
        inventory = pc.get("inventory", [])
        if not inventory:
            screen.blit(font_n.render("Mochila vazia.", True, COLOR_TEXT_DIM), (right_x, inner_y + 40))
        else:
            for i, item in enumerate(inventory):
                screen.blit(font_n.render(f"• {item}", True, COLOR_TEXT), (right_x, inner_y + 40 + (i * 25)))
        
        screen.blit(self.font_body.render("Pressione TAB para fechar.", True, COLOR_TEXT_DIM), (self.rect.centerx - 80, self.rect.bottom - 30))

def calculate_backpack_load(pc: dict, game_state: dict = None) -> tuple:
    """Calcula (slots_ocupados, slots_maximos) da mochila (Base 10 + Mod FOR, mín 10, máx 14).
    - Armas, armaduras e itens gerais: 1 slot cada.
    - Poções, pergaminhos e elixires: 1 slot a cada 3 unidades.
    - Rações e suprimentos de viagem: 1 slot a cada 5 unidades.
    """
    if not pc or not isinstance(pc, dict):
        return 0, 10

    from core.dice_engine import DiceEngine
    attrs = pc.get("attributes") or pc.get("atributos") or {}
    str_val = 10
    if isinstance(attrs, dict):
        str_val = attrs.get("STR", attrs.get("FOR", attrs.get("Força", 10)))
    mod_for = DiceEngine.calculate_modifier(int(str_val))
    max_slots = max(10, min(14, 10 + mod_for))

    if pc.get("load_slots_used") is not None:
        return int(pc["load_slots_used"]), max_slots

    potion_count = 0
    ration_count = 0
    general_items = 0
    counted_consumable_ids = set()

    gs_inv = game_state.get("inventory", {}) if isinstance(game_state, dict) else {}
    if isinstance(gs_inv, dict):
        for it_id, count in gs_inv.items():
            if not isinstance(count, (int, float)) or count <= 0:
                continue
            low = str(it_id).lower()
            counted_consumable_ids.add(low)
            if any(k in low for k in ("ration", "racao", "ração", "suprimento", "supply")):
                ration_count += int(count)
            elif any(k in low for k in ("potion", "pocao", "poção", "scroll", "pergaminho", "antidote", "elixir", "herb", "erva")):
                potion_count += int(count)
            else:
                general_items += int(count)

    pc_inv = pc.get("inventory")
    if isinstance(pc_inv, dict):
        for it_id, count in pc_inv.items():
            if not isinstance(count, (int, float)) or count <= 0:
                continue
            low = str(it_id).lower()
            if low in counted_consumable_ids:
                continue
            if any(k in low for k in ("ration", "racao", "ração", "suprimento", "supply")):
                ration_count += int(count)
            elif any(k in low for k in ("potion", "pocao", "poção", "scroll", "pergaminho", "antidote", "elixir", "herb", "erva")):
                potion_count += int(count)
            else:
                general_items += int(count)
    elif isinstance(pc_inv, list):
        for item in pc_inv:
            low = str(item).lower()
            if any(k in low for k in ("ration", "racao", "ração", "suprimento", "supply")):
                if not any(k in c for c in counted_consumable_ids for k in ("ration", "racao")):
                    ration_count += 1
            elif any(k in low for k in ("potion", "pocao", "poção", "scroll", "pergaminho", "antidote", "elixir", "herb", "erva")):
                if not counted_consumable_ids:
                    potion_count += 1
            else:
                general_items += 1

    # Conta também equipamentos ativos se não houver itens gerais listados
    equip = pc.get("equipment", {})
    if isinstance(equip, dict) and general_items == 0:
        if equip.get("weapon") and str(equip.get("weapon")).lower() not in ("desarmado", "nenhum", ""):
            general_items += 1
        if equip.get("armor") and str(equip.get("armor")).lower() not in ("roupas comuns", "trajes", "nenhum", "nenhuma", ""):
            general_items += 1
        if pc.get("has_shield") or (equip.get("shield") and str(equip.get("shield")).lower() not in ("nenhum", "")):
            general_items += 1

    used_slots = general_items + ((potion_count + 2) // 3) + ((ration_count + 4) // 5)
    return used_slots, max_slots


class BackpackModal(Panel):
    """Mochila do Aventureiro: Painel dedicado a Armas, Armaduras, Acessórios, Consumíveis e Ouro."""
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, title="")
        self.game_state_ref = None
        self.font_title = AssetManager.get_font(24, bold=True)
        self.font_b = AssetManager.get_font(18, bold=True)
        self.font_n = AssetManager.get_font(16)
        self.font_s = AssetManager.get_font(14)
        self.font_btn = AssetManager.get_font(13, bold=True)
        self.font_tiny = AssetManager.get_font(12, bold=True)
        self._item_buttons = {}   # item_id -> pygame.Rect
        self._equip_buttons = {}  # item_name -> pygame.Rect
        self._items_db_cache = None
        self.last_load_info = (0, 10)
        self.last_load_str = "Carga: [□□□□□□□□□□] 0 / 10 Slots"

    def get_load_capacity(self, pc: dict = None) -> tuple:
        """Retorna (slots_usados, slots_maximos) para o herói atual."""
        if pc is None and self.game_state_ref:
            pc = self.game_state_ref.get("player_character", {})
        return calculate_backpack_load(pc, self.game_state_ref)

    def _get_player_consumables(self) -> list:
        """Coleta consumíveis disponíveis de game_state e pc de forma sincronizada."""
        if not self.game_state_ref:
            return []
            
        import json
        if self._items_db_cache is None:
            try:
                with open("data/items.json", "r", encoding="utf-8") as f:
                    self._items_db_cache = json.load(f)
            except Exception:
                self._items_db_cache = {}
                
        consumables_db = self._items_db_cache.get("consumables", {})
        results = []
        
        # 1. Verifica game_state["inventory"] (dicionário de contadores)
        gs_inv = self.game_state_ref.get("inventory", {})
        if isinstance(gs_inv, dict):
            for it_id, count in gs_inv.items():
                if count > 0:
                    item_info = None
                    for c_key, c_val in consumables_db.items():
                        if c_val.get("id") == it_id or c_key == it_id:
                            item_info = c_val
                            break
                    if item_info:
                        results.append({
                            "id": item_info.get("id", it_id),
                            "name": item_info.get("name", it_id),
                            "count": count,
                            "desc": item_info.get("description", ""),
                            "dice": item_info.get("dice_value", "")
                        })
                    else:
                        results.append({
                            "id": it_id,
                            "name": it_id.replace("i_", "").replace("_", " ").title(),
                            "count": count,
                            "desc": "Item consumível",
                            "dice": ""
                        })
                        
        # 2. Verifica pc["inventory"] se for lista
        pc = self.game_state_ref.get("player_character", {})
        pc_inv = pc.get("inventory")
        if isinstance(pc_inv, list):
            from collections import Counter
            counts = Counter(pc_inv)
            for it_name, count in counts.items():
                for c_key, c_val in consumables_db.items():
                    if c_val.get("name", "").lower() == str(it_name).lower() or c_val.get("id", "").lower() == str(it_name).lower():
                        c_id = c_val.get("id")
                        if not any(r["id"] == c_id for r in results):
                            results.append({
                                "id": c_id,
                                "name": c_val.get("name", it_name),
                                "count": count,
                                "desc": c_val.get("description", ""),
                                "dice": c_val.get("dice_value", "")
                            })
                        break
                        
        return results

    def draw(self, screen: pygame.Surface):
        if not self.is_visible or not self.game_state_ref:
            return
        pc = self.game_state_ref.get("player_character")
        if not pc:
            return

        # Tenta carregar textura de mochila ou desenha painel de couro/madeira com moldura rica
        bg_surf = AssetManager.get_image("ui", "backpack_bg")
        if bg_surf is not None:
            bg_scaled = AssetManager.get_scaled(bg_surf, (self.rect.width, self.rect.height))
            screen.blit(bg_scaled, (self.rect.x, self.rect.y))
        else:
            draw_ui_panel(screen, self.rect, "wood_panel")
            inner_rect = pygame.Rect(self.rect.x + 12, self.rect.y + 12, self.rect.width - 24, self.rect.height - 24)
            pygame.draw.rect(screen, (32, 24, 18), inner_rect, border_radius=6)
            pygame.draw.rect(screen, COLOR_GOLD, inner_rect, 2, border_radius=6)

        mouse_pos = pygame.mouse.get_pos()
        col_w = (self.rect.width - 80) // 2
        left_x = self.rect.x + 35
        right_x = self.rect.x + 35 + col_w + 20

        # Cabeçalho Principal
        title_txt = self.font_title.render("Mochila do Aventureiro", True, COLOR_GOLD)
        screen.blit(title_txt, (self.rect.centerx - title_txt.get_width() // 2, self.rect.y + 22))

        # --- COLUNA ESQUERDA: Equipamento & Riquezas ---
        cur_y = self.rect.y + 65
        screen.blit(self.font_b.render("Equipamento Ativo", True, (240, 220, 180)), (left_x, cur_y))
        cur_y += 28

        equip = pc.get("equipment", {}) if isinstance(pc.get("equipment"), dict) else {}
        weapon_txt = equip.get('weapon', pc.get('equipped_weapon', 'Desarmado'))
        armor_txt = equip.get('armor', pc.get('equipped_armor', 'Roupas Comuns'))
        shield_txt = equip.get('shield') or ("Sim (+2 CA)" if pc.get('has_shield') else "Nenhum")
        acc_txt = equip.get('accessory', pc.get('equipped_accessory', 'Nenhum'))

        items_equip = [
            ("Arma:", weapon_txt),
            ("Armadura:", armor_txt),
            ("Escudo:", shield_txt),
            ("Acessório:", acc_txt),
            ("Classe de Armadura:", f"{pc.get('ac', 10)} CA")
        ]
        for label, val in items_equip:
            screen.blit(self.font_s.render(label, True, COLOR_GOLD), (left_x, cur_y))
            screen.blit(self.font_s.render(str(val), True, (230, 230, 230)), (left_x + 160, cur_y))
            cur_y += 22

        cur_y += 10
        screen.blit(self.font_b.render("Riquezas & Capacidade", True, (240, 220, 180)), (left_x, cur_y))
        cur_y += 24
        gold = pc.get("gold", 15)
        screen.blit(self.font_n.render(f"Moedas de Ouro: {gold} PO", True, (255, 215, 0)), (left_x, cur_y))
        cur_y += 22

        used_slots, max_slots = self.get_load_capacity(pc)
        self.last_load_info = (used_slots, max_slots)
        filled_blocks = min(used_slots, max_slots)
        empty_blocks = max(0, max_slots - filled_blocks)
        self.last_load_str = f"Carga: [{'■' * filled_blocks}{'□' * empty_blocks}] {used_slots} / {max_slots} Slots"

        load_color = (235, 110, 80) if used_slots >= max_slots else (210, 195, 165)
        screen.blit(self.font_s.render(f"Carga: {used_slots} / {max_slots} Slots", True, load_color), (left_x, cur_y))
        cur_y += 18

        # Barra visual de blocos de carga
        seg_gap = 3
        seg_w = max(8, (col_w - (max_slots - 1) * seg_gap) // max_slots)
        for s_idx in range(max_slots):
            seg_rect = pygame.Rect(left_x + s_idx * (seg_w + seg_gap), cur_y, seg_w, 10)
            if s_idx < used_slots:
                fill_c = (200, 75, 50) if used_slots > max_slots else COLOR_GOLD
                pygame.draw.rect(screen, fill_c, seg_rect, border_radius=2)
            else:
                pygame.draw.rect(screen, (55, 45, 35), seg_rect, border_radius=2)
            pygame.draw.rect(screen, (130, 110, 80), seg_rect, 1, border_radius=2)
        cur_y += 20

        self._equip_buttons.clear()
        screen.blit(self.font_b.render("Itens Gerais de Viagem", True, (240, 220, 180)), (left_x, cur_y))
        cur_y += 24
        inv = pc.get("inventory", [])
        if isinstance(inv, list):
            from core.dnd_rules import ARMAS_5E, ARMADURAS_5E
            for it in inv[:6]:
                it_str = str(it)
                it_lower = it_str.lower()
                is_weapon = it_lower in ARMAS_5E or any(w in it_lower for w in ["espada", "machado", "arco", "adaga", "rapieira", "lança", "martelo", "maça", "clava", "bordão", "besta", "montante"])
                is_armor = it_lower in ARMADURAS_5E or any(w in it_lower for w in ["armadura", "cota", "brunea", "escudo", "traje", "couro", "peitoral"])
                is_equippable = is_weapon or is_armor

                is_currently_equipped = (
                    (is_weapon and it_lower == str(weapon_txt).lower()) or
                    (is_armor and (it_lower == str(armor_txt).lower() or (it_lower == "escudo" and pc.get("has_shield"))))
                )

                it_label = f"• {it_str}"
                if len(it_label) > 22:
                    it_label = it_label[:20] + ".."
                screen.blit(self.font_s.render(it_label, True, (200, 200, 200)), (left_x, cur_y))

                if is_currently_equipped:
                    eq_tag = self.font_tiny.render("(Equipado)", True, (100, 220, 120))
                    screen.blit(eq_tag, (left_x + col_w - 75, cur_y + 1))
                elif is_equippable:
                    btn_eq = pygame.Rect(left_x + col_w - 75, cur_y - 2, 70, 22)
                    self._equip_buttons[it_str] = btn_eq
                    label_btn = "Empunhar" if is_weapon else "Equipar"
                    draw_ui_button(screen, btn_eq, label_btn, self.font_tiny, btn_eq.collidepoint(mouse_pos), True)

                cur_y += 23

        # --- COLUNA DIREITA: Consumíveis Interativos ---
        self._item_buttons.clear()
        r_y = self.rect.y + 65
        screen.blit(self.font_b.render("Consumíveis da Mochila", True, (240, 220, 180)), (right_x, r_y))
        r_y += 28

        consumables = self._get_player_consumables()
        if not consumables:
            screen.blit(self.font_n.render("Nenhum consumível disponível no momento.", True, (160, 160, 160)), (right_x, r_y))
        else:
            for item in consumables:
                if r_y > self.rect.bottom - 70:
                    break
                it_name_txt = f"{item['name']} (x{item['count']})"
                screen.blit(self.font_b.render(it_name_txt, True, (255, 255, 255)), (right_x, r_y + 2))

                sub_txt = item['dice'] if item['dice'] else (item['desc'][:36] + "..." if len(item['desc']) > 36 else item['desc'])
                screen.blit(self.font_s.render(sub_txt, True, (200, 190, 160)), (right_x, r_y + 22))

                btn_use = pygame.Rect(right_x + col_w - 85, r_y + 4, 75, 28)
                self._item_buttons[item['id']] = btn_use
                draw_ui_button(screen, btn_use, "Usar", self.font_btn, btn_use.collidepoint(mouse_pos), True)
                r_y += 48

        footer_txt = self.font_s.render("Pressione ESC, TAB ou clique fora para fechar a mochila.", True, (180, 170, 150))
        screen.blit(footer_txt, (self.rect.centerx - footer_txt.get_width() // 2, self.rect.bottom - 30))

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.is_visible:
            return ""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for item_id, btn_rect in self._item_buttons.items():
                if btn_rect.collidepoint(mouse_pos):
                    return f"use_item:{item_id}"
            for item_name, btn_rect in getattr(self, "_equip_buttons", {}).items():
                if btn_rect.collidepoint(mouse_pos):
                    return f"equip_weapon:{item_name}"
            if not self.rect.collidepoint(mouse_pos):
                return "close_backpack"
        elif event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_TAB]:
            return "close_backpack"
        return ""


BESTIARY_LORE = {
    "goblin": {
        "name": "Goblin Emboscador",
        "descricao": "Pequenos humanoides astutos que habitam cavernas e ruínas sombrias.",
        "pontos_fortes": "Ataques surpresa furtivos e grande agilidade.",
        "fraquezas": "Baixa resistência física e covardia quando isolados.",
        "tatico": "Furtivos e rápidos. Não deixe que cerquem você nas sombras."
    },
    "kobold": {
        "name": "Kobold Mineiro",
        "descricao": "Humanoides reptilianos que veneram dragões e habitam galerias subterrâneas.",
        "pontos_fortes": "Vantagem tática de bando e armadilhas letais.",
        "fraquezas": "Extremamente frágeis e sensíveis à luz solar.",
        "tatico": "Fracos individualmente, mas letais em bandos e armadilhas."
    },
    "esqueleto": {
        "name": "Esqueleto Ancestral",
        "descricao": "Restos mortais reanimados por magia profana antiga.",
        "pontos_fortes": "Imunidade a veneno, sangramento e exaustão.",
        "fraquezas": "Vulnerabilidade severa a dano contundente (maças e martelos).",
        "tatico": "Imunes ao cansaço, vulneráveis a dano contundente de maças."
    },
    "lobo_atroz": {
        "name": "Lobo Atroz",
        "descricao": "Predadores gigantescos que caçam em matilhas coordenadas pelas florestas.",
        "pontos_fortes": "Faro aguçado e ataques de derrubada coordenados.",
        "fraquezas": "Ataques de fogo e magias de controle de terreno.",
        "tatico": "Derrubam a presa para ataques com vantagem em matilha."
    },
    "ogro": {
        "name": "Ogro Brutal",
        "descricao": "Gigantescos brutamontes guiados pela fome insaciável e força descomunal.",
        "pontos_fortes": "Dano massivo corpo a corpo e enorme quantidade de vida.",
        "fraquezas": "Baixa destreza e pouca astúcia mental.",
        "tatico": "Golpes massivos capazes de quebrar escudos. Mantenha distância."
    },
    "aranha_gigante": {
        "name": "Aranha Gigante",
        "descricao": "Aracnídeos colossais que tecem teias pegajosas nas profundezas.",
        "pontos_fortes": "Veneno paralisante e capacidade de prender alvos em teias.",
        "fraquezas": "Vulnerabilidade ao fogo para queimar suas teias.",
        "tatico": "Evite ficar preso nas teias e proteja-se contra seu veneno."
    },
    "manticora": {
        "name": "Manticora Alada",
        "descricao": "Monstruosidade com corpo de leão, asas de morcego e cauda de escorpião.",
        "pontos_fortes": "Voo ágil e espinhos de cauda disparados à distância.",
        "fraquezas": "Dano mágico concentrado em suas asas.",
        "tatico": "Force o combate em ambientes fechados para impedi-la de voar."
    },
    "supreme_dragon": {
        "name": "O Tirano das Cinzas",
        "descricao": "O lendário dragão das cinzas ancestrais cujo fogo derreteu reinos antigos.",
        "pontos_fortes": "Sopro de cinzas devastador e escamas impenetráveis.",
        "fraquezas": "Vulnerável após a destruição do Orbe de Cinzas.",
        "tatico": "O Tirano das Cinzas. Escamas impenetráveis até a quebra do Orbe!"
    },
    "boss_final": {
        "name": "O Tirano das Cinzas",
        "descricao": "O lendário dragão das cinzas ancestrais cujo fogo derreteu reinos antigos.",
        "pontos_fortes": "Sopro de cinzas devastador e escamas impenetráveis.",
        "fraquezas": "Vulnerável após a destruição do Orbe de Cinzas.",
        "tatico": "O Tirano das Cinzas. Escamas impenetráveis até a quebra do Orbe!"
    },
}


class GrimoireModal(Panel):
    """Grimório de Habilidades, Árvore de Progressão Visual, Bestiário, Diário e Ficha do Herói em livro aberto (800x600)."""
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, title="")
        self.game_state_ref = None
        self.session_ref = None
        self.font_title = AssetManager.get_font(20, bold=True)
        self.font_b = AssetManager.get_font(18, bold=True)
        self.font_n = AssetManager.get_font(16)
        self.font_s = AssetManager.get_font(14)
        self.font_btn = AssetManager.get_font(13, bold=True)
        self.font_tiny = AssetManager.get_font(12)
        self.font_glyph = AssetManager.get_font(20, bold=True)
        self.font_num_big = AssetManager.get_font(28, bold=True)

        self.btn_level_up = pygame.Rect(x + width // 2 + 32, y + height - 76, (width // 2) - 76, 36)
        self._spell_buttons = {}  # spell_id -> pygame.Rect
        self._monster_buttons = {} # monster_id -> pygame.Rect
        self.selected_monster = "goblin"

        # 4 Abas Temáticas
        self.active_tab = "items"  # "items" por padrão para compatibilidade legada; main.py define "habilidades"
        tab_w = 125
        tab_h = 28
        start_tab_x = x + width - (tab_w * 4 + 25)
        self.tab_skills_rect = pygame.Rect(start_tab_x, y + 26, tab_w, tab_h)
        self.tab_bestiary_rect = pygame.Rect(start_tab_x + tab_w + 4, y + 26, tab_w, tab_h)
        self.tab_journal_rect = pygame.Rect(start_tab_x + (tab_w + 4) * 2, y + 26, tab_w, tab_h)
        self.tab_status_rect = pygame.Rect(start_tab_x + (tab_w + 4) * 3, y + 26, tab_w, tab_h)

        # Aliases para compatibilidade legada
        self.tab_items_rect = self.tab_status_rect
        self.tab_spells_rect = self.tab_skills_rect
        self._item_buttons = {}

        self._spells_db_cache = None
        self._items_db_cache = None
        self._heroes_lore_cache = None
        self._campaign_data_cache = None
        self._side_quests_cache = None

        # Estado da aba Diário / Missões
        self.journal_filter = "ativas"  # "ativas", "rumores", "concluidas"
        self.selected_quest_id = "main_campaign"  # "main_campaign" ou id da quest
        self._quest_buttons = {}  # quest_id -> pygame.Rect
        self.btn_main_campaign = pygame.Rect(0, 0, 0, 0)
        self.btn_filter_active = pygame.Rect(0, 0, 0, 0)
        self.btn_filter_rumors = pygame.Rect(0, 0, 0, 0)
        self.btn_filter_completed = pygame.Rect(0, 0, 0, 0)
        self.btn_accept_quest = pygame.Rect(0, 0, 0, 0)
        self.btn_travel_quest = pygame.Rect(0, 0, 0, 0)

        # Estado e hitboxes da Ficha & Equipamentos (Aba Status)
        self._equip_slot_rects = {} # "weapon", "armor", "shield", "accessory" -> pygame.Rect
        self.btn_open_backpack = pygame.Rect(0, 0, 0, 0)
        self.last_load_info = (0, 10)
        self.last_load_str = ""

        # Estado e nós da Árvore de Habilidades Visual
        self.selected_skill_node = "sk_warrior_1"
        self._skill_icon_rects = {} # sk_id -> pygame.Rect (40x40)
        self._skill_node_rects = {} # sk_id -> pygame.Rect (card inteiro)
        self.btn_learn_skill = pygame.Rect(0, 0, 0, 0)

        # Estado do Modal/Overlay de Level Up Interativo
        self.level_up_modal_open = False
        self.level_up_points_left = 2
        self.level_up_alloc = {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
        self.btn_confirm_level_up = pygame.Rect(0, 0, 0, 0)
        self.btn_cancel_level_up = pygame.Rect(0, 0, 0, 0)
        self._lvlup_plus_rects = {}
        self._lvlup_minus_rects = {}

        # Cache de texto formatado (Zero word-wrap por frame)
        self._text_surface_cache = {}

        # =====================================================================
        # SUPERFÍCIES PRÉ-RENDERIZADAS (Zero Garbage por Frame / 60 FPS)
        # =====================================================================
        # 1. Pedestal de pedra elíptico com sombra suave para o herói em pé
        self._pedestal_surf = pygame.Surface((190, 48), pygame.SRCALPHA)
        # Sombra elíptica projetada no chão
        pygame.draw.ellipse(self._pedestal_surf, (22, 16, 12, 120), (8, 22, 174, 24))
        # Base de pedra chanfrada
        pygame.draw.ellipse(self._pedestal_surf, (78, 70, 62), (18, 12, 154, 24))
        # Topo polido do pedestal
        pygame.draw.ellipse(self._pedestal_surf, (135, 125, 112), (18, 8, 154, 20))
        # Anel rúnico decorativo em bronze/ouro
        pygame.draw.ellipse(self._pedestal_surf, (190, 150, 60), (22, 10, 146, 16), 2)

        # 2. Molduras pré-renderizadas dos 4 slots de equipamento (largura total 330x42)
        self._equip_slot_surf = pygame.Surface((330, 42))
        self._equip_slot_surf.fill((234, 224, 202))
        pygame.draw.rect(self._equip_slot_surf, (222, 212, 188), (2, 2, 326, 38))
        pygame.draw.rect(self._equip_slot_surf, (160, 130, 80), (0, 0, 330, 42), 1, border_radius=4)

        self._equip_slot_hover_surf = pygame.Surface((330, 42))
        self._equip_slot_hover_surf.fill((246, 238, 218))
        pygame.draw.rect(self._equip_slot_hover_surf, (230, 215, 175), (2, 2, 326, 38))
        pygame.draw.rect(self._equip_slot_hover_surf, COLOR_GOLD, (0, 0, 330, 42), 1, border_radius=4)

        # 3. Molduras quadradas de ícones de habilidades (40x40) nos 3 estados
        self._skill_icon_frames = {}
        for state, border_col, bg_col, inner_col in [
            ("acquired", (215, 175, 45), (55, 42, 18), (245, 215, 95)),
            ("available", (230, 145, 30), (70, 48, 16), (255, 195, 80)),
            ("locked", (100, 92, 85), (38, 35, 32), (65, 60, 56)),
        ]:
            surf = pygame.Surface((40, 40))
            surf.fill(bg_col)
            pygame.draw.rect(surf, inner_col, (2, 2, 36, 36), 1)
            pygame.draw.rect(surf, border_col, (0, 0, 40, 40), 2, border_radius=3)
            self._skill_icon_frames[state] = surf

        # 4. Caixas dos atributos D&D 5e (98x52)
        self._attr_box_surf = pygame.Surface((98, 52))
        self._attr_box_surf.fill((234, 224, 202))
        pygame.draw.rect(self._attr_box_surf, (215, 202, 175), (2, 2, 94, 48))
        pygame.draw.rect(self._attr_box_surf, (160, 140, 110), (0, 0, 98, 52), 1, border_radius=4)

        # 5. Telas do Modal de Level Up
        self._levelup_overlay_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self._levelup_overlay_surf.fill((14, 10, 8, 210))

        self._levelup_card_surf = pygame.Surface((540, 440))
        self._levelup_card_surf.fill(COLOR_PARCHMENT)
        inner_c = pygame.Rect(8, 8, 524, 424)
        pygame.draw.rect(self._levelup_card_surf, (238, 228, 206), inner_c, border_radius=6)
        pygame.draw.rect(self._levelup_card_surf, COLOR_WOOD_DARK, (0, 0, 540, 440), 4, border_radius=6)
        pygame.draw.rect(self._levelup_card_surf, COLOR_GOLD, inner_c, 2, border_radius=6)

    def get_load_capacity(self, pc: dict = None) -> tuple:
        """Calcula a capacidade de carga da mochila sincronizada."""
        if pc is None and self.game_state_ref:
            pc = self.game_state_ref.get("player_character", {})
        return calculate_backpack_load(pc, self.game_state_ref)

    def _get_cached_text(self, text: str, font: pygame.font.Font, color: tuple) -> pygame.Surface:
        """Garante que strings estáticas sejam renderizadas uma única vez na GPU."""
        key = (text, id(font), color)
        if key not in self._text_surface_cache:
            self._text_surface_cache[key] = font.render(text, True, color)
        return self._text_surface_cache[key]

    def _format_item_name(self, item_id: str) -> str:
        """Traduz IDs técnicos de itens para nomes elegantes em português."""
        if not item_id:
            return ""
        if self._items_db_cache is None:
            import json
            try:
                with open("data/items.json", "r", encoding="utf-8") as f:
                    self._items_db_cache = json.load(f)
            except Exception:
                self._items_db_cache = {}
        if isinstance(self._items_db_cache, dict):
            for cat, items_map in self._items_db_cache.items():
                if isinstance(items_map, dict):
                    for k, v in items_map.items():
                        if isinstance(v, dict) and (v.get("id") == item_id or k == item_id):
                            return v.get("name", item_id)
        known = {
            "i_shortbow": "Arco Curto",
            "i_potion_healing": "Poção de Cura",
            "i_elven_shortbow": "Arco Élfico",
            "i_amulet_health": "Amuleto de Saúde",
            "i_mithral_dagger": "Adaga de Mithral",
            "i_shadow_leather": "Couro Sombrio",
            "i_potion_greater_healing": "Poção de Cura Maior",
            "i_heraldic_shield": "Escudo Heráldico",
            "i_ring_protection": "Anel de Proteção",
            "i_adamantine_breastplate": "Peitoral de Adamante",
            "i_runic_blade": "Espada Rúnica",
            "i_scroll_revive": "Pergaminho de Reviver",
            "i_greatsword_runic": "Espadão Rúnico",
            "i_radiant_amulet": "Amuleto de Radiância"
        }
        if item_id in known:
            return known[item_id]
        return item_id.replace("i_", "").replace("_", " ").title()

    def _get_hero_name(self, hero_id: str) -> str:
        """Resolve o nome canônico do herói associado à quest."""
        if not hero_id:
            return ""
        if self.session_ref and hasattr(self.session_ref, "story"):
            hero_data = self.session_ref.story.get_hero_lore(hero_id)
            if hero_data and "name" in hero_data:
                return f"{hero_data['name']} ({hero_id})"
        if self._heroes_lore_cache is None:
            import json
            try:
                with open("data/heroes_lore.json", "r", encoding="utf-8") as f:
                    self._heroes_lore_cache = json.load(f)
            except Exception:
                self._heroes_lore_cache = {}
        if isinstance(self._heroes_lore_cache, dict) and hero_id in self._heroes_lore_cache:
            h = self._heroes_lore_cache[hero_id]
            return f"{h.get('name', hero_id)} ({hero_id})"
        return hero_id

    def _get_current_beat(self) -> int:
        if self.session_ref and hasattr(self.session_ref, "story"):
            return self.session_ref.story.current_beat
        if self.game_state_ref:
            return self.game_state_ref.get("story_beat", 1)
        return 1

    def _get_campaign_data(self) -> dict:
        if self.session_ref and hasattr(self.session_ref, "story"):
            return self.session_ref.story.campaign_data
        if self._campaign_data_cache is None:
            import json
            try:
                with open("data/campaign.json", "r", encoding="utf-8") as f:
                    self._campaign_data_cache = json.load(f)
            except Exception:
                self._campaign_data_cache = {}
        return self._campaign_data_cache

    def _get_beat_name(self, beat_num: int) -> str:
        cdata = self._get_campaign_data()
        b_info = cdata.get(str(beat_num), {})
        return b_info.get("name", f"Capítulo {beat_num}")

    def _get_beat_environment(self, beat_num: int) -> str:
        cdata = self._get_campaign_data()
        b_info = cdata.get(str(beat_num), {})
        return b_info.get("environment_prompt", "Terras assoladas por ventos de cinzas e perigos ocultos.")

    def _get_side_quests_data(self) -> dict:
        if self.session_ref and hasattr(self.session_ref, "story") and self.session_ref.story.side_quests_data:
            return self.session_ref.story.side_quests_data
        if self._side_quests_cache is None:
            import json
            try:
                with open("data/side_quests.json", "r", encoding="utf-8") as f:
                    self._side_quests_cache = json.load(f)
            except Exception:
                self._side_quests_cache = {}
        return self._side_quests_cache

    def _get_quest_by_id(self, quest_id: str) -> dict:
        if self.game_state_ref:
            log = self.game_state_ref.get("quest_log", [])
            if isinstance(log, list):
                for q in log:
                    if isinstance(q, dict) and q.get("id") == quest_id:
                        return q
        sq_db = self._get_side_quests_data()
        if quest_id in sq_db:
            return sq_db[quest_id]
        return {}

    def _get_formatted_objectives(self, quest_data: dict) -> list:
        objs = quest_data.get("objectives", [])
        is_done = quest_data.get("status") == "concluida"
        res = []
        if isinstance(objs, list) and objs:
            for item in objs:
                if isinstance(item, dict):
                    res.append({
                        "text": item.get("text", str(item)),
                        "done": is_done or item.get("done", False)
                    })
                else:
                    res.append({
                        "text": str(item),
                        "done": is_done
                    })
        elif quest_data.get("objective"):
            res.append({
                "text": str(quest_data.get("objective")),
                "done": is_done
            })
        else:
            q_id = quest_data.get("id", "")
            sq_db = self._get_side_quests_data()
            if q_id in sq_db and "objectives" in sq_db[q_id]:
                for item in sq_db[q_id]["objectives"]:
                    res.append({
                        "text": str(item),
                        "done": is_done
                    })
        return res

    def _get_active_and_completed_quests(self) -> tuple:
        if not self.game_state_ref:
            return [], []
        log = self.game_state_ref.get("quest_log", [])
        if not isinstance(log, list):
            return [], []
        active = [q for q in log if isinstance(q, dict) and q.get("status") == "ativa"]
        completed = [q for q in log if isinstance(q, dict) and q.get("status") == "concluida"]
        return active, completed

    def _get_rumor_quests(self) -> list:
        """Retorna missões secundárias do ato atual que ainda não foram aceitas (não estão no quest_log)."""
        if self.session_ref and hasattr(self.session_ref, "story"):
            act_quests = self.session_ref.story.get_available_quests_for_current_act()
        else:
            sq_db = self._get_side_quests_data()
            beat = self._get_current_beat()
            act = 1 if beat <= 5 else (2 if beat <= 10 else 3)
            act_quests = [q for q in sq_db.values() if isinstance(q, dict) and q.get("act", 1) == act]

        logged_ids = set()
        if self.game_state_ref:
            log = self.game_state_ref.get("quest_log", [])
            if isinstance(log, list):
                for q in log:
                    if isinstance(q, dict) and "id" in q:
                        logged_ids.add(q["id"])

        rumors = [q for q in act_quests if isinstance(q, dict) and q.get("id") not in logged_ids]
        return rumors

    def _get_player_consumables(self) -> list:
        """Coleta consumíveis disponíveis para compatibilidade legada."""
        bm = BackpackModal(0, 0, 800, 600)
        bm.game_state_ref = self.game_state_ref
        return bm._get_player_consumables()

    def _get_player_spells(self) -> list:
        if not self.game_state_ref:
            return []
        import json
        if self._spells_db_cache is None:
            try:
                with open("data/spells.json", "r", encoding="utf-8") as f:
                    self._spells_db_cache = json.load(f)
            except Exception:
                self._spells_db_cache = {}

        pc = self.game_state_ref.get("player_character", {})
        char_class = pc.get("class", "").lower()
        known = pc.get("spells", [])
        is_caster = any(c in char_class for c in ["mago", "clerigo", "clérigo", "paladino", "patrulheiro"]) or bool(pc.get("spell_slots"))

        results = []
        for escola, magias in self._spells_db_cache.items():
            for s_key, s_data in magias.items():
                s_id = s_data.get("id", s_key)
                s_name = s_data.get("name", s_key)
                if known:
                    if s_id in known or s_name in known or s_key in known:
                        results.append(s_data)
                elif is_caster:
                    results.append(s_data)
        return results

    def _get_class_skill_tree(self, char_class: str) -> list:
        """Retorna a Árvore de Habilidades Visual com 4 Tiers (Nv 1, 2, 3, 5) para as 6 classes."""
        c = (char_class or "Guerreiro").lower()
        if "clerigo" in c or "clérigo" in c or "cleric" in c:
            return [
                {
                    "id": "sk_cleric_1", "canonical_id": "disciple_of_life",
                    "icon_file": "skill_cleric_1_discipulo_vida.png",
                    "level": 1, "glyph": "+", "name": "Bênção da Cura",
                    "desc": "Magias de cura restauram +2 + Nível da magia em PV adicionais aos aliados feridos.",
                    "short_desc": "+2+Nv PV em curas divinas."
                },
                {
                    "id": "sk_cleric_2", "canonical_id": "channel_divinity_preserve_life",
                    "icon_file": "skill_cleric_2_preservar_vida.png",
                    "level": 2, "glyph": "S", "name": "Canalizar Divindade",
                    "desc": "Expulsa mortos-vivos num raio de 9 metros ou preserva a vida de aliados próximos.",
                    "short_desc": "Expulsar mortos-vivos ou curar aliados."
                },
                {
                    "id": "sk_cleric_3", "canonical_id": "spiritual_weapon",
                    "icon_file": "skill_cleric_3_arma_espiritual.png",
                    "level": 3, "glyph": "D", "name": "Escudo da Fé",
                    "desc": "Aura sagrada protetora que concede +2 de CA e resistência mística contra as trevas.",
                    "short_desc": "+2 de CA e proteção sagrada."
                },
                {
                    "id": "sk_cleric_5", "canonical_id": "destroy_undead",
                    "icon_file": "skill_cleric_5_destruir_mortos_vivos.png",
                    "level": 5, "glyph": "*", "name": "Fogo Radiante",
                    "desc": "Chamas celestiais purificadoras somam +1d8 de dano radiante aos seus ataques e preces.",
                    "short_desc": "+1d8 dano radiante adicional."
                }
            ]
        elif "paladino" in c or "paladin" in c:
            return [
                {
                    "id": "sk_paladin_1", "canonical_id": "lay_on_hands",
                    "icon_file": "skill_paladin_1_cura_pelas_maos.png",
                    "level": 1, "glyph": "+", "name": "Cura pelas Mãos",
                    "desc": "Reserva de toque curativo divino que restaura PV ou expurga venenos e doenças.",
                    "short_desc": "Cura sagrada com toque das mãos."
                },
                {
                    "id": "sk_paladin_2", "canonical_id": "divine_smite",
                    "icon_file": "skill_paladin_2_destruicao_divina.png",
                    "level": 2, "glyph": "Z", "name": "Destruição Divina",
                    "desc": "Canaliza energia sagrada nos golpes da arma, causando +2d8 de dano radiante extra.",
                    "short_desc": "+2d8 dano radiante no acerto."
                },
                {
                    "id": "sk_paladin_3", "canonical_id": "sacred_oath_devotion",
                    "icon_file": "skill_paladin_3_aura_protecao.png",
                    "level": 3, "glyph": "C", "name": "Aura de Coragem",
                    "desc": "Você e seus aliados próximos tornam-se completamente imunes ao medo em batalha.",
                    "short_desc": "Imunidade total a medo para o grupo."
                },
                {
                    "id": "sk_paladin_5", "canonical_id": "extra_attack_paladin",
                    "icon_file": "skill_paladin_5_ataque_extra_sagrado.png",
                    "level": 5, "glyph": "X", "name": "Golpe Abençoado Extra",
                    "desc": "Desfere dois ataques com armas por turno, ambos imbuídos de convicção e glória.",
                    "short_desc": "Dois ataques sagrados por turno."
                }
            ]
        elif "mago" in c or "wizard" in c or "mage" in c:
            return [
                {
                    "id": "sk_wizard_1", "canonical_id": "arcane_recovery",
                    "icon_file": "skill_wizard_1_recuperacao_arcana.png",
                    "level": 1, "glyph": "O", "name": "Recuperação Arcana",
                    "desc": "Restaura espaços de magia gastos durante descansos breves através de pura meditação.",
                    "short_desc": "Restaura espaços de magia em repouso."
                },
                {
                    "id": "sk_wizard_2", "canonical_id": "sculpt_spells",
                    "icon_file": "skill_wizard_2_evocacao_potente.png",
                    "level": 2, "glyph": "F", "name": "Evocação Potente",
                    "desc": "Esculpe feitiços destrutivos para que aliados na área de efeito não sofram dano.",
                    "short_desc": "Protege aliados de magias de área."
                },
                {
                    "id": "sk_wizard_3", "canonical_id": "potent_cantrip",
                    "icon_file": "skill_wizard_3_escudo_arcano.png",
                    "level": 3, "glyph": "E", "name": "Escudo Arcano",
                    "desc": "Reação mística instantânea que ergue uma barreira invisível concedendo +5 de CA.",
                    "short_desc": "+5 de CA como reação defensiva."
                },
                {
                    "id": "sk_wizard_5", "canonical_id": "arcane_overload",
                    "icon_file": "skill_wizard_5_mestre_elementos.png",
                    "level": 5, "glyph": "*", "name": "Mestre dos Elementos",
                    "desc": "Soma seu modificador de INT ao dano de todas as magias elementais preparadas.",
                    "short_desc": "+Mod INT em todo dano elemental."
                }
            ]
        elif "patrulheiro" in c or "ranger" in c:
            return [
                {
                    "id": "sk_ranger_1", "canonical_id": "favored_enemy",
                    "icon_file": "skill_ranger_1_marca_cacador.png",
                    "level": 1, "glyph": "T", "name": "Marca do Caçador",
                    "desc": "Foca na presa escolhida causando +1d6 de dano adicional em todos os acertos.",
                    "short_desc": "+1d6 de dano contra o alvo marcado."
                },
                {
                    "id": "sk_ranger_2", "canonical_id": "archery_style",
                    "icon_file": "skill_ranger_2_estilo_arquearia.png",
                    "level": 2, "glyph": "A", "name": "Estilo Arquearia",
                    "desc": "Precisão mortal inata que concede +2 de bônus em jogadas de ataque à distância.",
                    "short_desc": "+2 em ataques com arcos e bestas."
                },
                {
                    "id": "sk_ranger_3", "canonical_id": "colossus_slayer",
                    "icon_file": "skill_ranger_3_matador_colossos.png",
                    "level": 3, "glyph": "K", "name": "Matador de Colossos",
                    "desc": "Causa +1d8 de dano extra em armas contra alvos que já estejam com ferimentos.",
                    "short_desc": "+1d8 extra contra inimigos feridos."
                },
                {
                    "id": "sk_ranger_5", "canonical_id": "extra_attack_ranger",
                    "icon_file": "skill_ranger_5_rajada_flechas.png",
                    "level": 5, "glyph": "R", "name": "Rajada de Flechas",
                    "desc": "Dispara projéteis em rápida sucessão, executando dois ataques a cada ação.",
                    "short_desc": "Dois ataques à distância por ação."
                }
            ]
        elif "ladino" in c or "rogue" in c:
            return [
                {
                    "id": "sk_rogue_1", "canonical_id": "sneak_attack",
                    "icon_file": "skill_rogue_1_ataque_furtivo.png",
                    "level": 1, "glyph": "D", "name": "Ataque Furtivo",
                    "desc": "Causa +1d6 de dano em ataques com acuidade se tiver vantagem ou aliado próximo.",
                    "short_desc": "+1d6 furtivo com vantagem ou aliado."
                },
                {
                    "id": "sk_rogue_2", "canonical_id": "cunning_action",
                    "icon_file": "skill_rogue_2_acao_ardilosa.png",
                    "level": 2, "glyph": "P", "name": "Ação Ardilosa",
                    "desc": "Permite usar Disparada, Desengajar ou Esconder-se como ação bônus a cada turno.",
                    "short_desc": "Disparar/Esconder como ação bônus."
                },
                {
                    "id": "sk_rogue_3", "canonical_id": "assassinate",
                    "icon_file": "skill_rogue_3_emboscada_mortal.png",
                    "level": 3, "glyph": "M", "name": "Emboscada Mortal",
                    "desc": "Golpes contra inimigos surpreendidos tornam-se acertos críticos automáticos.",
                    "short_desc": "Crítico garantido em surpresa."
                },
                {
                    "id": "sk_rogue_5", "canonical_id": "uncanny_dodge",
                    "icon_file": "skill_rogue_5_esquiva_sobrenatural.png",
                    "level": 5, "glyph": "S", "name": "Esquiva Sobrenatural",
                    "desc": "Usa reação ágil para reduzir pela metade o dano de um ataque que o atinja.",
                    "short_desc": "Reduz dano recebido pela metade."
                }
            ]
        else: # Guerreiro
            return [
                {
                    "id": "sk_warrior_1", "canonical_id": "second_wind",
                    "icon_file": "skill_fighter_1_retomar_folego.png",
                    "level": 1, "glyph": "X", "name": "Retomar o Fôlego",
                    "desc": "Recupera 1d10 + Nível de PV em combate com pura disciplina como ação bônus.",
                    "short_desc": "Cura 1d10+Nv PV como ação bônus."
                },
                {
                    "id": "sk_warrior_2", "canonical_id": "action_surge",
                    "icon_file": "skill_fighter_2_surto_acao.png",
                    "level": 2, "glyph": "Z", "name": "Surto de Ação",
                    "desc": "Executa uma ação marcial extra completa no mesmo turno de batalha.",
                    "short_desc": "Ação marcial extra no turno."
                },
                {
                    "id": "sk_warrior_3", "canonical_id": "champion_focus",
                    "icon_file": "skill_fighter_3_foco_campeao.png",
                    "level": 3, "glyph": "*", "name": "Foco do Campeão",
                    "desc": "Crítico marcial aprimorado em rolagens de 19 ou 20 no d20 contra qualquer alvo.",
                    "short_desc": "Crítico em 19 ou 20 no d20."
                },
                {
                    "id": "sk_warrior_5", "canonical_id": "extra_attack_fighter",
                    "icon_file": "skill_fighter_5_ataque_extra.png",
                    "level": 5, "glyph": "X", "name": "Ataque Extra",
                    "desc": "Desfere dois golpes com armas ao invés de um a cada ação de Ataque.",
                    "short_desc": "Dois ataques marciais por ação."
                }
            ]

    def _get_skill_state(self, sk: dict, pc: dict) -> str:
        """Retorna 'acquired', 'available' ou 'locked'."""
        hero_lvl = pc.get("level", 1)
        req_lvl = sk["level"]
        has_lvlup = pc.get("has_pending_level_up") or (pc.get("xp", 0) >= pc.get("xp_to_next_level", 300))
        if hero_lvl >= req_lvl:
            return "acquired"
        if has_lvlup and req_lvl == hero_lvl + 1:
            return "available"
        return "locked"

    def open_level_up_modal(self, pc: dict = None):
        """Abre o modal/overlay de Level Up com escolha de bônus de atributos."""
        if pc is None and self.game_state_ref:
            pc = self.game_state_ref.get("player_character", {})
        self.level_up_modal_open = True
        self.level_up_points_left = 2
        self.level_up_alloc = {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}

    def _apply_level_up_choices(self, pc: dict) -> dict:
        """Aplica os bônus de atributo selecionados e a nova habilidade de classe ao personagem."""
        if not pc:
            return {}

        # Se sobraram pontos não distribuídos, aloca no atributo primário da classe
        char_class = pc.get("class", "Guerreiro").lower()
        primary_attr = "STR"
        if any(k in char_class for k in ("ladino", "patrulheiro")):
            primary_attr = "DEX"
        elif "mago" in char_class:
            primary_attr = "INT"
        elif "clerigo" in char_class or "clérigo" in char_class:
            primary_attr = "WIS"
        elif "paladino" in char_class:
            primary_attr = "STR" if self.level_up_alloc.get("STR", 0) >= self.level_up_alloc.get("CHA", 0) else "CHA"

        if self.level_up_points_left > 0:
            self.level_up_alloc[primary_attr] = self.level_up_alloc.get(primary_attr, 0) + self.level_up_points_left
            self.level_up_points_left = 0

        # Aplica bônus de atributos sincronizando chaves PT (FOR/DES/CON/INT/SAB/CAR) e EN (STR/DEX/CON/INT/WIS/CHA)
        attr_pt_map = {
            "STR": "FOR",
            "DEX": "DES",
            "CON": "CON",
            "INT": "INT",
            "WIS": "SAB",
            "CHA": "CAR",
        }
        attrs = pc.setdefault("attributes", {})
        for attr, bonus in self.level_up_alloc.items():
            if bonus > 0:
                pt_key = attr_pt_map.get(attr, attr)
                base_val = attrs.get(attr, attrs.get(pt_key, 10))
                new_val = base_val + bonus
                attrs[attr] = new_val
                attrs[pt_key] = new_val

        # Desbloqueia a nova habilidade de classe se atingiu o tier (registrando ID UI + canonical_id do motor D&D)
        next_lvl = pc.get("level", 1) + 1
        skill_tree = self._get_class_skill_tree(pc.get("class", "Guerreiro"))
        ab_list = pc.setdefault("abilities", [])
        unlocked_skills = pc.setdefault("unlocked_skills", [])
        for sk in skill_tree:
            if sk["level"] <= next_lvl:
                if sk["level"] == next_lvl and sk["name"] not in ab_list:
                    ab_list.append(sk["name"])
                if sk["id"] not in unlocked_skills:
                    unlocked_skills.append(sk["id"])
                canon_id = sk.get("canonical_id")
                if canon_id and canon_id not in unlocked_skills:
                    unlocked_skills.append(canon_id)

        self.level_up_modal_open = False
        return self.level_up_alloc

    def draw(self, screen: pygame.Surface):
        if not self.is_visible or not self.game_state_ref:
            return
        pc = self.game_state_ref.get("player_character")
        if not pc:
            return

        # Desenha livro aberto
        book_surf = AssetManager.get_image("ui", "open_book")
        if book_surf is not None:
            book_scaled = AssetManager.get_scaled(book_surf, (self.rect.width, self.rect.height))
            screen.blit(book_scaled, (self.rect.x, self.rect.y))
        else:
            page_w_half = self.rect.width // 2
            pygame.draw.rect(screen, COLOR_PARCHMENT, (self.rect.x, self.rect.y, page_w_half, self.rect.height))
            pygame.draw.rect(screen, COLOR_PARCHMENT, (self.rect.x + page_w_half, self.rect.y, page_w_half, self.rect.height))
            pygame.draw.rect(screen, COLOR_WOOD_DARK, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 4)
            pygame.draw.line(screen, COLOR_WOOD_DARK, (self.rect.x + page_w_half, self.rect.y), (self.rect.x + page_w_half, self.rect.bottom), 4)

        mouse_pos = pygame.mouse.get_pos()
        left_x = self.rect.x + 48
        page_w = (self.rect.width // 2) - 76
        right_x = self.rect.x + (self.rect.width // 2) + 32

        # Renderização das 4 Abas
        tabs = [
            ("habilidades", "Habilidades", self.tab_skills_rect),
            ("bestiario", "Bestiário", self.tab_bestiary_rect),
            ("diario", "Diário / Missões", self.tab_journal_rect),
            ("status", "Ficha & Equip.", self.tab_status_rect),
        ]
        for tid, tlabel, trect in tabs:
            is_active = (self.active_tab == tid) or (tid == "habilidades" and self.active_tab == "spells") or (tid == "status" and self.active_tab == "items")
            color_bg = COLOR_GOLD if is_active else (210, 200, 180)
            pygame.draw.rect(screen, color_bg, trect, border_radius=4)
            pygame.draw.rect(screen, COLOR_WOOD_DARK, trect, 2, border_radius=4)
            txt_t = self.font_btn.render(tlabel, True, COLOR_WOOD_DARK if is_active else COLOR_INK)
            screen.blit(txt_t, (trect.centerx - txt_t.get_width() // 2, trect.centery - txt_t.get_height() // 2))

        # =====================================================================
        # ABA 1: HABILIDADES (Árvore Visual com 4 Tiers & Ícones Quadrados) ou ABA SPELLS
        # =====================================================================
        if self.active_tab in ("habilidades", "spells"):
            # --- PÁGINA ESQUERDA: Magias / Descrição da Habilidade Selecionada ---
            cur_y = self.rect.y + 62
            screen.blit(self.font_b.render("Grimório de Magias", True, COLOR_INK), (left_x, cur_y))
            cur_y += 24
            slots = pc.get("spell_slots", {})
            slots_str = " | ".join(f"Nv {l}: {q}" for l, q in sorted(slots.items())) if slots else "Sem espaços arcanos (Marcial)."
            screen.blit(self.font_s.render(slots_str, True, (90, 80, 70)), (left_x, cur_y))
            cur_y += 28

            self._spell_buttons.clear()
            spells = self._get_player_spells()
            if not spells:
                screen.blit(self.font_n.render("Nenhuma magia registrada no grimório.", True, (120, 110, 100)), (left_x, cur_y))
                cur_y += 50
            else:
                for s in spells[:3]:
                    s_id = s.get("id", s.get("name"))
                    s_name = f"{s.get('name', 'Magia')} (Nv {s.get('level', 1)})"
                    screen.blit(self.font_s.render(s_name, True, COLOR_INK), (left_x, cur_y + 2))
                    s_desc = s.get("damage_dice", "") or s.get("mechanical_action", "")
                    screen.blit(self.font_tiny.render(s_desc, True, (100, 90, 80)), (left_x, cur_y + 18))

                    btn_cast = pygame.Rect(left_x + page_w - 75, cur_y + 2, 70, 24)
                    self._spell_buttons[s_id] = btn_cast
                    draw_ui_button(screen, btn_cast, "Conjurar", self.font_btn, btn_cast.collidepoint(mouse_pos), True)
                    cur_y += 40

            # Painel Inferior Esquerdo: Detalhes da Habilidade Selecionada na Árvore
            cur_y = max(cur_y + 10, self.rect.y + 260)
            pygame.draw.line(screen, (190, 180, 160), (left_x, cur_y), (left_x + page_w, cur_y), 1)
            cur_y += 8

            skill_tree = self._get_class_skill_tree(pc.get("class", "Guerreiro"))
            selected_sk = next((s for s in skill_tree if s["id"] == self.selected_skill_node), skill_tree[0])
            sel_state = self._get_skill_state(selected_sk, pc)

            screen.blit(self.font_b.render(f"Detalhes: {selected_sk['name']}", True, COLOR_INK), (left_x, cur_y))
            cur_y += 24

            # Mostra ícone quadrado 40x40 e metadados (com suporte a textura de assets/ui/skills/)
            icon_surf = self._skill_icon_frames[sel_state]
            screen.blit(icon_surf, (left_x, cur_y))
            sk_tex_left = AssetManager.get_skill_icon(selected_sk, size=(34, 34))
            if sk_tex_left is not None:
                screen.blit(sk_tex_left, (left_x + 3, cur_y + 3))
            else:
                g_surf = self.font_glyph.render(selected_sk["glyph"], True, COLOR_GOLD if sel_state != "locked" else (160, 150, 140))
                screen.blit(g_surf, (left_x + (40 - g_surf.get_width()) // 2, cur_y + (40 - g_surf.get_height()) // 2))

            state_label = "Adquirida [OK]" if sel_state == "acquired" else ("Disponível" if sel_state == "available" else f"Requer Nível {selected_sk['level']}")
            state_color = (35, 120, 35) if sel_state == "acquired" else ((195, 120, 20) if sel_state == "available" else (120, 80, 60))
            screen.blit(self.font_btn.render(f"Tier {selected_sk['level']} • {state_label}", True, state_color), (left_x + 50, cur_y + 2))
            screen.blit(self.font_tiny.render(f"Classe: {pc.get('class', 'Guerreiro')}", True, (90, 80, 70)), (left_x + 50, cur_y + 22))
            cur_y += 50

            desc_rect = pygame.Rect(left_x, cur_y, page_w, 110)
            draw_text_wrapped(screen, selected_sk["desc"], self.font_s, (75, 65, 55), desc_rect)

            if sel_state == "available":
                self.btn_learn_skill = pygame.Rect(left_x, self.rect.bottom - 74, page_w, 32)
                draw_ui_button(screen, self.btn_learn_skill, "Aprender Habilidade", self.font_b, self.btn_learn_skill.collidepoint(mouse_pos), True)
            else:
                self.btn_learn_skill = pygame.Rect(0, 0, 0, 0)

            # --- PÁGINA DIREITA: Árvore de Habilidades Visual com 4 Tiers ---
            r_y = self.rect.y + 62
            screen.blit(self.font_b.render(f"Árvore de Habilidades — {pc.get('class', 'Guerreiro')}", True, COLOR_INK), (right_x, r_y))
            r_y += 20
            screen.blit(self.font_tiny.render("Clique em um ícone para inspecionar • 4 Tiers de Classe", True, (100, 90, 80)), (right_x, r_y))
            r_y += 24

            self._skill_icon_rects.clear()
            self._skill_node_rects.clear()
            tier_h = 88
            node_x = right_x + 10

            for idx, sk in enumerate(skill_tree):
                sk_id = sk["id"]
                req_lvl = sk["level"]
                state = self._get_skill_state(sk, pc)
                is_selected = (self.selected_skill_node == sk_id)

                # Linha conectora vertical entre os tiers
                if idx < len(skill_tree) - 1:
                    next_state = self._get_skill_state(skill_tree[idx + 1], pc)
                    line_col = COLOR_GOLD if next_state != "locked" else (160, 150, 135)
                    pygame.draw.line(screen, line_col, (node_x + 20, r_y + 38), (node_x + 20, r_y + tier_h), 3)

                # Ícone Quadrado 40x40 pré-renderizado com moldura rica
                icon_rect = pygame.Rect(node_x, r_y, 40, 40)
                self._skill_icon_rects[sk_id] = icon_rect
                card_rect = pygame.Rect(node_x, r_y - 2, page_w - 20, 52)
                self._skill_node_rects[sk_id] = card_rect

                # Destaque de seleção ou hover no card
                is_hover = card_rect.collidepoint(mouse_pos)
                if is_selected or is_hover:
                    bg_c = (228, 218, 192) if is_selected else (236, 228, 210)
                    pygame.draw.rect(screen, bg_c, card_rect, border_radius=4)
                    pygame.draw.rect(screen, COLOR_GOLD if is_selected else (190, 180, 160), card_rect, 2 if is_selected else 1, border_radius=4)

                # Desenha o ícone quadrado 40x40 (com suporte a textura de assets/ui/skills/)
                screen.blit(self._skill_icon_frames[state], (icon_rect.x, icon_rect.y))
                sk_tex_node = AssetManager.get_skill_icon(sk, size=(34, 34))
                if sk_tex_node is not None:
                    screen.blit(sk_tex_node, (icon_rect.x + 3, icon_rect.y + 3))
                else:
                    glyph_c = COLOR_GOLD if state != "locked" else (150, 140, 130)
                    g_surf = self.font_glyph.render(sk["glyph"], True, glyph_c)
                    screen.blit(g_surf, (icon_rect.x + (40 - g_surf.get_width()) // 2, icon_rect.y + (40 - g_surf.get_height()) // 2))

                # Informações da Habilidade ao lado do ícone
                info_x = node_x + 50
                name_col = COLOR_INK if state != "locked" else (100, 90, 80)
                screen.blit(self.font_btn.render(f"Nv {req_lvl}: {sk['name']}", True, name_col), (info_x, r_y + 2))

                badge_str = "Adquirida [OK]" if state == "acquired" else ("Disponível" if state == "available" else f"Nv {req_lvl}")
                badge_col = (35, 120, 35) if state == "acquired" else ((195, 120, 20) if state == "available" else (130, 80, 60))
                screen.blit(self.font_tiny.render(badge_str, True, badge_col), (right_x + page_w - 95, r_y + 3))

                screen.blit(self.font_tiny.render(sk["short_desc"], True, (90, 80, 70)), (info_x, r_y + 24))
                r_y += tier_h

        # =====================================================================
        # ABA LEGADA: ITENS / CONSUMÍVEIS (Bloco 7)
        # =====================================================================
        elif self.active_tab == "items":
            cur_y = self.rect.y + 62
            screen.blit(self.font_b.render("Itens e Consumíveis", True, COLOR_INK), (left_x, cur_y))
            cur_y += 30
            self._item_buttons.clear()
            consumables = self._get_player_consumables()
            for item in consumables:
                item_id = item.get("id")
                item_name = f"{item.get('name', 'Item')} (x{item.get('count', 1)})"
                screen.blit(self.font_s.render(item_name, True, COLOR_INK), (left_x, cur_y + 2))
                btn_use = pygame.Rect(left_x + page_w - 75, cur_y + 2, 70, 24)
                self._item_buttons[item_id] = btn_use
                draw_ui_button(screen, btn_use, "Usar", self.font_btn, btn_use.collidepoint(mouse_pos), True)
                cur_y += 36

        # =====================================================================
        # ABA 2: BESTIÁRIO (Compêndio de Criaturas Progressivo)
        # =====================================================================
        elif self.active_tab == "bestiario":
            # Página Esquerda: Lista de Monstros Conhecidos e Desconhecidos
            cur_y = self.rect.y + 65
            screen.blit(self.font_b.render("Compêndio de Criaturas", True, COLOR_INK), (left_x, cur_y))
            cur_y += 26

            from core.dnd_rules import BESTIARIO_5E
            
            # Conjunto de monstros já descobertos na jornada
            discovered_raw = self.game_state_ref.get("discovered_monsters", []) if self.game_state_ref else []
            discovered_set = {str(m).lower().strip() for m in discovered_raw}
            
            # Inclui monstros ativos em combate como descobertos
            if self.game_state_ref:
                for ent in self.game_state_ref.get("active_entities", []):
                    if isinstance(ent, dict):
                        if ent.get("id"): discovered_set.add(str(ent["id"]).lower())
                        if ent.get("tipo_bestiario"): discovered_set.add(str(ent["tipo_bestiario"]).lower())
                targets = self.game_state_ref.get("active_combat_targets", {})
                if isinstance(targets, dict):
                    for t in targets.values():
                        if isinstance(t, dict):
                            if t.get("id"): discovered_set.add(str(t["id"]).lower())
                            if t.get("tipo_bestiario"): discovered_set.add(str(t["tipo_bestiario"]).lower())

            compendium_keys = ["goblin", "kobold", "esqueleto", "lobo_atroz", "ogro", "aranha_gigante", "manticora", "boss_final"]
            self._monster_buttons.clear()

            for m_key in compendium_keys:
                clean_key = m_key.replace("m_", "").lower()
                is_discovered = (m_key in discovered_set or clean_key in discovered_set or any(clean_key in d or d in clean_key for d in discovered_set))

                m_btn = pygame.Rect(left_x, cur_y, page_w, 24)
                self._monster_buttons[m_key] = m_btn
                is_sel = self.selected_monster == m_key
                bg_c = (210, 195, 160) if is_sel else (235, 225, 205)
                pygame.draw.rect(screen, bg_c, m_btn, border_radius=3)
                pygame.draw.rect(screen, COLOR_WOOD_DARK if is_sel else (180, 170, 150), m_btn, 1, border_radius=3)

                if is_discovered:
                    lore = BESTIARY_LORE.get(clean_key, {})
                    m_label = lore.get("name") or clean_key.replace("_", " ").title()
                    screen.blit(self.font_s.render(f"- {m_label}", True, COLOR_WOOD_DARK if is_sel else COLOR_INK), (left_x + 8, cur_y + 4))
                else:
                    screen.blit(self.font_s.render("- ??? (Desconhecido) [Oculto]", True, (130, 115, 100)), (left_x + 8, cur_y + 4))

                cur_y += 28

            # Página Direita: Ficha de Detalhes ou Silhueta Misteriosa
            r_y = self.rect.y + 65
            sel_clean = self.selected_monster.replace("m_", "").lower()
            is_sel_discovered = (self.selected_monster in discovered_set or sel_clean in discovered_set or any(sel_clean in d or d in sel_clean for d in discovered_set))

            if is_sel_discovered:
                mon_data = BESTIARIO_5E.get(self.selected_monster, BESTIARIO_5E.get(f"m_{sel_clean}", {}))
                lore = BESTIARY_LORE.get(sel_clean, {
                    "name": sel_clean.replace("_", " ").title(),
                    "descricao": "Monstruosidade perigosa catalogada pelos aventureiros.",
                    "pontos_fortes": "Ataques ferozes e instinto predatório.",
                    "fraquezas": "Coordenação defensiva do grupo.",
                    "tatico": "Ataque com sabedoria e explore suas fraquezas de alcance."
                })

                m_title = lore.get("name", sel_clean.title())
                screen.blit(self.font_b.render(f"Ficha: {m_title}", True, COLOR_INK), (right_x, r_y))
                r_y += 24

                # Box de visualização com Sprite do Inimigo
                sprite_box = pygame.Rect(right_x, r_y, 90, 90)
                pygame.draw.rect(screen, (230, 220, 198), sprite_box, border_radius=4)
                pygame.draw.rect(screen, (175, 155, 125), sprite_box, 1, border_radius=4)
                m_sprite = AssetManager.get_enemy_sprite(self.selected_monster)
                if m_sprite:
                    scaled_m = AssetManager.get_scaled(m_sprite, (80, 80))
                    screen.blit(scaled_m, (right_x + 5, r_y + 5))

                # Estatísticas ao lado do sprite
                info_x = right_x + 100
                ca_val = mon_data.get("ca", 12)
                pv_val = mon_data.get("pv_max", mon_data.get("pv", 18))
                xp_val = mon_data.get("xp", 100)
                screen.blit(self.font_btn.render(f"CA: {ca_val}", True, COLOR_INK), (info_x, r_y + 4))
                screen.blit(self.font_btn.render(f"PV: ~{pv_val} PV", True, COLOR_INK), (info_x, r_y + 24))
                screen.blit(self.font_btn.render(f"XP: +{xp_val} XP", True, COLOR_INK), (info_x, r_y + 44))
                screen.blit(self.font_tiny.render("Catalogado [OK]", True, (35, 120, 35)), (info_x, r_y + 68))
                r_y += 98

                # Descrição
                screen.blit(self.font_btn.render("Descrição:", True, COLOR_INK), (right_x, r_y))
                r_y += 18
                draw_text_wrapped(screen, lore.get("descricao", ""), self.font_tiny, (80, 70, 60), pygame.Rect(right_x, r_y, page_w, 40))
                r_y += 36

                # Pontos Fortes e Fraquezas
                screen.blit(self.font_tiny.render(f"+ Fortes: {lore.get('pontos_fortes', '')}", True, (130, 40, 20)), (right_x, r_y))
                r_y += 16
                screen.blit(self.font_tiny.render(f"- Fraqueza: {lore.get('fraquezas', '')}", True, (30, 110, 40)), (right_x, r_y))
                r_y += 20

                # Conselho Tático
                screen.blit(self.font_btn.render("Conselho Tático do Mestre:", True, COLOR_INK), (right_x, r_y))
                r_y += 18
                draw_text_wrapped(screen, lore.get("tatico", ""), self.font_s, (90, 80, 70), pygame.Rect(right_x, r_y, page_w, 60))

            else:
                # Monstro Não Descoberto
                screen.blit(self.font_b.render("Criatura Desconhecida", True, (120, 105, 90)), (right_x, r_y))
                r_y += 24

                # Box misteriosa com silhueta / interrogação
                sprite_box = pygame.Rect(right_x, r_y, 90, 90)
                pygame.draw.rect(screen, (215, 205, 185), sprite_box, border_radius=4)
                pygame.draw.rect(screen, (160, 145, 120), sprite_box, 1, border_radius=4)
                q_surf = self.font_num_big.render("?", True, (140, 125, 105))
                screen.blit(q_surf, (right_x + (90 - q_surf.get_width()) // 2, r_y + (90 - q_surf.get_height()) // 2))

                info_x = right_x + 100
                screen.blit(self.font_btn.render("CA: ???", True, (130, 115, 100)), (info_x, r_y + 4))
                screen.blit(self.font_btn.render("PV: ???", True, (130, 115, 100)), (info_x, r_y + 24))
                screen.blit(self.font_btn.render("XP: ???", True, (130, 115, 100)), (info_x, r_y + 44))
                screen.blit(self.font_tiny.render("Não Descoberto", True, (150, 70, 50)), (info_x, r_y + 68))
                r_y += 105

                screen.blit(self.font_b.render("Mistério das Terras Ermas:", True, COLOR_INK), (right_x, r_y))
                r_y += 22
                unseen_msg = (
                    "Criatura ainda não avistada nesta jornada.\n\n"
                    "Explore masmorras, aceite contratos na guilda ou avance na campanha para "
                    "catalogar suas fraquezas e conselhos táticos neste compêndio."
                )
                draw_text_wrapped(screen, unseen_msg, self.font_s, (100, 90, 80), pygame.Rect(right_x, r_y, page_w, 150))

        # =====================================================================
        # ABA 3: DIÁRIO / MISSÕES (Campanha Principal & Secundárias)
        # =====================================================================
        elif self.active_tab == "diario":
            active_quests, completed_quests = self._get_active_and_completed_quests()
            rumor_quests = self._get_rumor_quests()

            self.btn_accept_quest = pygame.Rect(0, 0, 0, 0)
            self.btn_travel_quest = pygame.Rect(0, 0, 0, 0)

            all_known_ids = ["main_campaign"] + [q.get("id") for q in active_quests + completed_quests + rumor_quests if q.get("id")]
            if self.selected_quest_id not in all_known_ids:
                if self.journal_filter == "ativas" and active_quests:
                    self.selected_quest_id = active_quests[0].get("id", "main_campaign")
                elif self.journal_filter == "rumores" and rumor_quests:
                    self.selected_quest_id = rumor_quests[0].get("id", "main_campaign")
                elif self.journal_filter == "concluidas" and completed_quests:
                    self.selected_quest_id = completed_quests[0].get("id", "main_campaign")
                else:
                    self.selected_quest_id = "main_campaign"

            cur_y = self.rect.y + 65
            screen.blit(self.font_b.render("Diário de Missões", True, COLOR_INK), (left_x, cur_y))
            cur_y += 28

            # Card da Campanha Principal
            self.btn_main_campaign = pygame.Rect(left_x, cur_y, page_w, 46)
            is_mc_sel = (self.selected_quest_id == "main_campaign")
            is_mc_hov = self.btn_main_campaign.collidepoint(mouse_pos)
            mc_bg = (215, 200, 165) if is_mc_sel else ((230, 220, 200) if is_mc_hov else (238, 228, 208))
            pygame.draw.rect(screen, mc_bg, self.btn_main_campaign, border_radius=4)
            pygame.draw.rect(screen, COLOR_GOLD if is_mc_sel else (180, 170, 150), self.btn_main_campaign, 2 if is_mc_sel else 1, border_radius=4)
            beat_curr = self._get_current_beat()
            screen.blit(self.font_btn.render("Missão Principal: O Chamado das Cinzas", True, (140, 50, 10) if is_mc_sel else COLOR_INK), (left_x + 8, cur_y + 6))
            screen.blit(self.font_tiny.render(f"Jornada Geral • Capítulo {beat_curr} de 15", True, (90, 80, 70)), (left_x + 8, cur_y + 25))
            cur_y += 54

            # Sub-header de Missões Secundárias e 3 Filtros
            screen.blit(self.font_btn.render("Missões Secundárias:", True, COLOR_INK), (left_x, cur_y))
            cur_y += 20

            btn_w = (page_w - 8) // 3
            btn_h = 32
            self.btn_filter_active = pygame.Rect(left_x, cur_y, btn_w, btn_h)
            self.btn_filter_rumors = pygame.Rect(left_x + btn_w + 4, cur_y, btn_w, btn_h)
            self.btn_filter_completed = pygame.Rect(left_x + (btn_w + 4) * 2, cur_y, page_w - ((btn_w + 4) * 2), btn_h)

            is_act_sel = (self.journal_filter == "ativas")
            f_act_bg = COLOR_GOLD if is_act_sel else (225, 215, 195)
            pygame.draw.rect(screen, f_act_bg, self.btn_filter_active, border_radius=4)
            pygame.draw.rect(screen, COLOR_WOOD_DARK if is_act_sel else (180, 170, 150), self.btn_filter_active, 1, border_radius=4)
            lbl_act = self.font_tiny.render(f"Ativas ({len(active_quests)})", True, COLOR_WOOD_DARK if is_act_sel else COLOR_INK)
            screen.blit(lbl_act, (self.btn_filter_active.centerx - lbl_act.get_width() // 2, self.btn_filter_active.centery - lbl_act.get_height() // 2))

            is_rum_sel = (self.journal_filter == "rumores")
            f_rum_bg = (210, 185, 130) if is_rum_sel else (225, 215, 195)
            pygame.draw.rect(screen, f_rum_bg, self.btn_filter_rumors, border_radius=4)
            pygame.draw.rect(screen, COLOR_WOOD_DARK if is_rum_sel else (180, 170, 150), self.btn_filter_rumors, 1, border_radius=4)
            lbl_rum = self.font_tiny.render(f"Rumores ({len(rumor_quests)})", True, COLOR_WOOD_DARK if is_rum_sel else COLOR_INK)
            screen.blit(lbl_rum, (self.btn_filter_rumors.centerx - lbl_rum.get_width() // 2, self.btn_filter_rumors.centery - lbl_rum.get_height() // 2))

            is_comp_sel = (self.journal_filter == "concluidas")
            f_comp_bg = (50, 130, 50) if is_comp_sel else (225, 215, 195)
            pygame.draw.rect(screen, f_comp_bg, self.btn_filter_completed, border_radius=4)
            pygame.draw.rect(screen, COLOR_WOOD_DARK if is_comp_sel else (180, 170, 150), self.btn_filter_completed, 1, border_radius=4)
            lbl_comp = self.font_tiny.render(f"Feitas ({len(completed_quests)})", True, (245, 245, 230) if is_comp_sel else COLOR_INK)
            screen.blit(lbl_comp, (self.btn_filter_completed.centerx - lbl_comp.get_width() // 2, self.btn_filter_completed.centery - lbl_comp.get_height() // 2))
            cur_y += 40

            # Lista de Missões Secundárias
            self._quest_buttons.clear()
            quests_list = active_quests if self.journal_filter == "ativas" else (rumor_quests if self.journal_filter == "rumores" else completed_quests)

            if not quests_list:
                ph_rect = pygame.Rect(left_x, cur_y, page_w, 130)
                pygame.draw.rect(screen, (235, 225, 205), ph_rect, border_radius=4)
                pygame.draw.rect(screen, (190, 180, 160), ph_rect, 1, border_radius=4)
                if self.journal_filter == "ativas":
                    msg = "Nenhuma missão secundária ativa no momento.\n\nExplore a aba 'Rumores' para aceitar contratos."
                elif self.journal_filter == "rumores":
                    msg = "Nenhum boato novo neste capítulo.\n\nFale com taverneiros e viajantes para novas pistas."
                else:
                    msg = "Nenhuma missão secundária concluída até agora."
                draw_text_wrapped(screen, msg, self.font_tiny, (100, 90, 80), pygame.Rect(left_x + 10, cur_y + 12, page_w - 20, 110))
            else:
                for q in quests_list[:5]:
                    q_id = q.get("id", "")
                    q_rect = pygame.Rect(left_x, cur_y, page_w, 48)
                    self._quest_buttons[q_id] = q_rect
                    is_sel = (self.selected_quest_id == q_id)
                    is_hov = q_rect.collidepoint(mouse_pos)
                    bg_c = (215, 200, 165) if is_sel else ((230, 220, 200) if is_hov else (238, 228, 208))
                    pygame.draw.rect(screen, bg_c, q_rect, border_radius=4)
                    pygame.draw.rect(screen, COLOR_GOLD if is_sel else (180, 170, 150), q_rect, 2 if is_sel else 1, border_radius=4)

                    icon_txt = "[OK]" if self.journal_filter == "concluidas" else ("[+]" if self.journal_filter == "rumores" else "[o]")
                    icon_col = (30, 120, 30) if self.journal_filter == "concluidas" else ((180, 110, 20) if self.journal_filter == "rumores" else (160, 90, 20))
                    screen.blit(self.font_btn.render(icon_txt, True, icon_col), (left_x + 8, cur_y + 6))

                    q_title = q.get("title", "Missão")
                    if len(q_title) > 26: q_title = q_title[:25] + "..."
                    screen.blit(self.font_btn.render(q_title, True, COLOR_WOOD_DARK if is_sel else COLOR_INK), (left_x + 32, cur_y + 6))

                    sub_txt = f"Ato {q.get('act', 1)} • Nv {q.get('recommended_level', 1)}"
                    screen.blit(self.font_tiny.render(sub_txt, True, (90, 80, 70)), (left_x + 32, cur_y + 26))
                    cur_y += 54

            # Página Direita de Missões
            r_y = self.rect.y + 65

            if self.selected_quest_id == "main_campaign":
                screen.blit(self.font_b.render("Campanha: O Chamado das Cinzas", True, COLOR_INK), (right_x, r_y))
                r_y += 24
                beat = self._get_current_beat()
                act = 1 if beat <= 5 else (2 if beat <= 10 else 3)
                act_title = "Ato I: A Marcha das Terras Baixas" if act == 1 else ("Ato II: Os Bastilhões Decaídos" if act == 2 else "Ato III: A Forja do Tirano")
                screen.blit(self.font_s.render(act_title, True, (140, 50, 15)), (right_x, r_y))
                r_y += 20
                b_name = self._get_beat_name(beat)
                screen.blit(self.font_s.render(f"Capítulo Atual: Beat {beat} de 15 — {b_name}", True, COLOR_INK), (right_x, r_y))
                r_y += 24
                pygame.draw.line(screen, (190, 180, 160), (right_x, r_y), (right_x + page_w, r_y), 1)
                r_y += 8

                screen.blit(self.font_btn.render("Objetivo Principal:", True, COLOR_INK), (right_x, r_y))
                r_y += 18
                m_desc = "O Tirano das Cinzas corrompeu o reino. Reúna aliados na Taverna e quebre o Orbe de Obsidiana no Beat 15."
                draw_text_wrapped(screen, m_desc, self.font_tiny, (80, 70, 60), pygame.Rect(right_x, r_y, page_w, 65))
                r_y += 70

                screen.blit(self.font_btn.render("Origem do Herói:", True, COLOR_INK), (right_x, r_y))
                r_y += 18
                prologue = self.game_state_ref.get("prologue", "")
                if not prologue:
                    prologue = f"Você é {pc.get('name', 'o herói')}, um {pc.get('race')} {pc.get('class')} forjando seu destino."
                draw_text_wrapped(screen, prologue, self.font_tiny, (80, 70, 60), pygame.Rect(right_x, r_y, page_w, 80))
            else:
                quest_data = self._get_quest_by_id(self.selected_quest_id)
                if quest_data:
                    is_concluded = (quest_data.get("status") == "concluida")
                    is_active = (quest_data.get("status") == "ativa")
                    is_rumor = not is_concluded and not is_active

                    screen.blit(self.font_b.render(quest_data.get("title", "Missão"), True, COLOR_INK), (right_x, r_y))
                    r_y += 24
                    badge_txt = "CONCLUÍDA [OK]" if is_concluded else ("RUMOR DISPONÍVEL" if is_rumor else "EM ANDAMENTO")
                    badge_col = (30, 130, 30) if is_concluded else ((180, 110, 20) if is_rumor else (160, 90, 20))
                    screen.blit(self.font_btn.render(f"[{badge_txt}]", True, badge_col), (right_x, r_y))
                    r_y += 22
                    draw_text_wrapped(screen, quest_data.get("description", ""), self.font_tiny, (70, 60, 50), pygame.Rect(right_x, r_y, page_w, 54))
                    r_y += 58

                    objectives = self._get_formatted_objectives(quest_data)
                    for obj in objectives[:3]:
                        chk_box = pygame.Rect(right_x, r_y + 1, 13, 13)
                        pygame.draw.rect(screen, (240, 235, 220), chk_box, border_radius=2)
                        pygame.draw.rect(screen, (110, 100, 90), chk_box, 1, border_radius=2)
                        draw_text_wrapped(screen, obj.get("text", ""), self.font_tiny, COLOR_INK, pygame.Rect(right_x + 18, r_y, page_w - 18, 26))
                        r_y += 28

                    if is_rumor:
                        self.btn_accept_quest = pygame.Rect(right_x, self.rect.bottom - 70, page_w, 28)
                        draw_ui_button(screen, self.btn_accept_quest, "Aceitar Missão", self.font_b, self.btn_accept_quest.collidepoint(mouse_pos), True)
                    elif is_active:
                        # Missões são orgânicas: remoção completa de viagem rápida/teletransporte
                        self.btn_travel_quest = pygame.Rect(0, 0, 0, 0)

        # =====================================================================
        # ABA 4: STATUS (Ficha & Equipamentos do Herói com Pedestal 2.5D e Carga)
        # =====================================================================
        elif self.active_tab == "status":
            # --- PÁGINA ESQUERDA: O Herói, Pedestal, Slots de Equipamento & Carga ---
            cur_y = self.rect.y + 60
            screen.blit(self.font_title.render(pc.get("name", "Herói"), True, COLOR_INK), (left_x, cur_y))
            cur_y += 24
            screen.blit(self.font_s.render(f"Nível {pc.get('level', 1)} • {pc.get('race', 'Humano')} {pc.get('class', 'Guerreiro')}", True, (95, 80, 65)), (left_x, cur_y))
            cur_y += 24

            # Vitrine do Herói sobre Pedestal de Pedra com sombra elíptica
            pedestal_box = pygame.Rect(left_x, cur_y, page_w, 140)
            pygame.draw.rect(screen, (230, 220, 198), pedestal_box, border_radius=6)
            pygame.draw.rect(screen, (175, 155, 125), pedestal_box, 1, border_radius=6)

            # Blita pedestal pré-renderizado centralizado na base do box
            ped_x = left_x + (page_w - 190) // 2
            ped_y = cur_y + 92
            screen.blit(self._pedestal_surf, (ped_x, ped_y))

            # Sprite 2.5D do Personagem em Pé sobre o Pedestal
            hero_sprite = AssetManager.get_entity_sprite(pc, kind="corpo")
            if hero_sprite:
                # Escala proporcionalmente para caber em 110x110
                sw, sh = hero_sprite.get_size()
                scale_factor = min(110 / max(1, sw), 110 / max(1, sh))
                final_size = (int(sw * scale_factor), int(sh * scale_factor))
                scaled_hero = AssetManager.get_scaled(hero_sprite, final_size)
                hero_x = left_x + (page_w - scaled_hero.get_width()) // 2
                hero_y = ped_y + 16 - scaled_hero.get_height()
                screen.blit(scaled_hero, (hero_x, hero_y))

            cur_y += 148

            # Grid 2x2 dos 4 Slots de Equipamento ([Arma], [Armadura], [Escudo], [Acessório])
            screen.blit(self.font_btn.render("Equipamento Ativo:", True, COLOR_INK), (left_x, cur_y))
            cur_y += 20

            equip = pc.get("equipment", {}) if isinstance(pc.get("equipment"), dict) else {}
            weapon_val = equip.get("weapon") or pc.get("equipped_weapon") or "Desarmado"
            armor_val = equip.get("armor") or pc.get("equipped_armor") or "Trajes Comuns"
            shield_val = equip.get("shield") or ("Escudo (+2 CA)" if pc.get("has_shield") else "Nenhum")
            acc_val = equip.get("accessory") or pc.get("equipped_accessory") or "Nenhum"

            slot_configs = [
                ("weapon", "ARMA", weapon_val),
                ("armor", "ARMADURA", armor_val),
                ("shield", "ESCUDO", shield_val),
                ("accessory", "ACESSÓRIO", acc_val),
            ]

            self._equip_slot_rects.clear()
            slot_w = page_w
            slot_h = 42

            for s_i, (s_key, s_tag, s_val) in enumerate(slot_configs):
                sx = left_x
                sy = cur_y + s_i * (slot_h + 3)
                s_rect = pygame.Rect(sx, sy, slot_w, slot_h)
                self._equip_slot_rects[s_key] = s_rect

                is_hov = s_rect.collidepoint(mouse_pos)
                slot_bg = self._equip_slot_hover_surf if is_hov else self._equip_slot_surf
                screen.blit(AssetManager.get_scaled(slot_bg, (slot_w, slot_h)), (sx, sy))

                tag_surf = self.font_tiny.render(s_tag, True, (135, 95, 30))
                screen.blit(tag_surf, (sx + 8, sy + 4))
                val_surf = self.font_btn.render(str(s_val), True, COLOR_INK)
                screen.blit(val_surf, (sx + 8, sy + 20))

            cur_y += 4 * (slot_h + 3) + 8

            # Indicador Visual de Capacidade de Carga da Mochila
            used_slots, max_slots = self.get_load_capacity(pc)
            self.last_load_info = (used_slots, max_slots)
            filled_blocks = min(used_slots, max_slots)
            empty_blocks = max(0, max_slots - filled_blocks)
            self.last_load_str = f"Carga: [{'■' * filled_blocks}{'□' * empty_blocks}] {used_slots} / {max_slots} Slots"

            screen.blit(self.font_btn.render(f"Capacidade de Carga: {used_slots} / {max_slots} Slots", True, COLOR_INK), (left_x, cur_y))
            cur_y += 18

            # Barra gráfica com quadradinhos/blocos discretos
            seg_gap = 2
            seg_w = max(6, (page_w - (max_slots - 1) * seg_gap) // max_slots)
            for s_idx in range(max_slots):
                b_rect = pygame.Rect(left_x + s_idx * (seg_w + seg_gap), cur_y, seg_w, 10)
                if s_idx < used_slots:
                    fill_c = (210, 80, 50) if used_slots > max_slots else COLOR_GOLD
                    pygame.draw.rect(screen, fill_c, b_rect, border_radius=2)
                else:
                    pygame.draw.rect(screen, (220, 210, 190), b_rect, border_radius=2)
                pygame.draw.rect(screen, (140, 125, 95), b_rect, 1, border_radius=2)

            cur_y += 20

            # Botão de Gerenciar / Abrir Mochila
            self.btn_open_backpack = pygame.Rect(left_x, self.rect.bottom - 74, page_w, 32)
            draw_ui_button(screen, self.btn_open_backpack, "Abrir Mochila & Trocar Equipamento", self.font_btn, self.btn_open_backpack.collidepoint(mouse_pos), True)

            # --- PÁGINA DIREITA: Atributos D&D 5e, Métricas de Combate & Level Up ---
            r_y = self.rect.y + 60
            screen.blit(self.font_b.render("Atributos & Modificadores (D&D 5e)", True, COLOR_INK), (right_x, r_y))
            r_y += 26

            attrs = pc.get("attributes", {})
            attr_keys = [("STR", "FOR"), ("DEX", "DES"), ("CON", "CON"), ("INT", "INT"), ("WIS", "SAB"), ("CHA", "CAR")]
            card_w = (page_w - 16) // 3
            card_h = 50

            from core.dice_engine import DiceEngine
            for a_idx, (en_key, pt_key) in enumerate(attr_keys):
                ax = right_x + (a_idx % 3) * (card_w + 8)
                ay = r_y + (a_idx // 3) * (card_h + 8)

                screen.blit(AssetManager.get_scaled(self._attr_box_surf, (card_w, card_h)), (ax, ay))
                val = attrs.get(en_key, attrs.get(pt_key, 10))
                mod = DiceEngine.calculate_modifier(val)
                mod_str = f"+{mod}" if mod >= 0 else str(mod)

                screen.blit(self.font_tiny.render(f"{pt_key} ({en_key})", True, (120, 95, 55)), (ax + 6, ay + 4))
                score_str = f"{val} ({mod_str})"
                screen.blit(self.font_btn.render(score_str, True, COLOR_INK), (ax + 6, ay + 24))

            r_y += (card_h * 2 + 18)

            # Métricas de Combate D&D 5e
            screen.blit(self.font_b.render("Métricas de Combate", True, COLOR_INK), (right_x, r_y))
            r_y += 24

            # Barra de Vida (PV)
            hp_cur = pc.get("hp_current", 10)
            hp_max = max(1, pc.get("hp_max", 10))
            screen.blit(self.font_btn.render(f"Pontos de Vida (PV): {hp_cur} / {hp_max}", True, COLOR_INK), (right_x, r_y))
            r_y += 18

            hp_bar_rect = pygame.Rect(right_x, r_y, page_w, 12)
            pygame.draw.rect(screen, (220, 210, 190), hp_bar_rect, border_radius=3)
            hp_ratio = max(0.0, min(1.0, hp_cur / hp_max))
            if hp_ratio > 0:
                hp_col = (40, 150, 40) if hp_ratio > 0.5 else ((200, 140, 30) if hp_ratio > 0.25 else (180, 40, 40))
                pygame.draw.rect(screen, hp_col, (right_x, r_y, int(page_w * hp_ratio), 12), border_radius=3)
            pygame.draw.rect(screen, (120, 105, 80), hp_bar_rect, 1, border_radius=3)
            r_y += 22

            # 4 mini-cards 2x2 para Métricas de Combate sem qualquer colisão de texto
            ac_val = pc.get("ac", pc.get("ca", 10))
            init_val = pc.get("initiative", 0)
            init_str = f"+{init_val}" if init_val >= 0 else str(init_val)
            speed_val = pc.get("speed", 9)
            prof_val = pc.get("proficiency_bonus", 2)
            gold_val = pc.get("gold", 15)

            metric_w = (page_w - 8) // 2
            metric_h = 36
            metric_items = [
                ("Classe de Armadura", f"{ac_val} CA"),
                ("Iniciativa", init_str),
                ("Deslocamento", f"{speed_val}m"),
                ("Bônus Prof.", f"+{prof_val}"),
            ]
            for m_i, (m_lbl, m_val) in enumerate(metric_items):
                mx = right_x + (m_i % 2) * (metric_w + 8)
                my = r_y + (m_i // 2) * (metric_h + 6)
                m_rect = pygame.Rect(mx, my, metric_w, metric_h)
                pygame.draw.rect(screen, (244, 236, 218), m_rect, border_radius=4)
                pygame.draw.rect(screen, (190, 175, 145), m_rect, 1, border_radius=4)
                screen.blit(self.font_tiny.render(m_lbl, True, (110, 90, 65)), (mx + 8, my + 3))
                val_surf = self.font_b.render(m_val, True, COLOR_INK)
                screen.blit(val_surf, (mx + 8, my + 17))
            r_y += (metric_h * 2 + 12)

            # Experiência e Subir de Nível
            xp = pc.get("xp", 0)
            xp_next = pc.get("xp_to_next_level", 300)
            screen.blit(self.font_b.render(f"Experiência: {xp} / {xp_next} XP  •  Ouro: {gold_val} PO", True, COLOR_INK), (right_x, r_y))
            r_y += 22

            xp_bar_rect = pygame.Rect(right_x, r_y, page_w, 10)
            pygame.draw.rect(screen, (220, 210, 190), xp_bar_rect, border_radius=3)
            xp_ratio = max(0.0, min(1.0, xp / max(1, xp_next)))
            if xp_ratio > 0:
                pygame.draw.rect(screen, COLOR_GOLD, (right_x, r_y, int(page_w * xp_ratio), 10), border_radius=3)
            pygame.draw.rect(screen, (120, 105, 80), xp_bar_rect, 1, border_radius=3)
            r_y += 20

            # Botão de Level Up destacado
            has_pending = pc.get("has_pending_level_up") or (xp >= xp_next)
            self.btn_level_up = pygame.Rect(right_x, self.rect.bottom - 74, page_w, 32)
            if has_pending:
                draw_ui_button(screen, self.btn_level_up, "Subir de Nível!", self.font_b, self.btn_level_up.collidepoint(mouse_pos), True)
            else:
                draw_ui_button(screen, self.btn_level_up, f"Nível {pc.get('level', 1)} Consolidado", self.font_btn, False, False)

        # Rodapé do livro aberto
        screen.blit(self.font_s.render("Pressione TAB ou ESC para fechar o grimório.", True, (100, 90, 80)), (self.rect.centerx - 120, self.rect.bottom - 26))

        # =====================================================================
        # MODAL / OVERLAY INTERATIVO DE LEVEL UP
        # =====================================================================
        if self.level_up_modal_open:
            self._draw_level_up_modal(screen, pc, mouse_pos)

    def _draw_level_up_modal(self, screen: pygame.Surface, pc: dict, mouse_pos: tuple):
        """Renderiza o modal de Level Up com distribuição de atributos e nova habilidade."""
        # Escurece o livro com overlay pré-alocado
        screen.blit(self._levelup_overlay_surf, (self.rect.x, self.rect.y))

        # Centraliza o card de pergaminho
        card_w, card_h = 540, 440
        card_x = self.rect.centerx - card_w // 2
        card_y = self.rect.centery - card_h // 2
        screen.blit(self._levelup_card_surf, (card_x, card_y))

        cur_lvl = pc.get("level", 1)
        next_lvl = cur_lvl + 1
        class_name = pc.get("class", "Guerreiro")

        m_y = card_y + 20
        title_txt = self.font_title.render(f"Ascensão de Nível: Nível {cur_lvl} -> Nível {next_lvl}", True, (150, 45, 10))
        screen.blit(title_txt, (card_x + (card_w - title_txt.get_width()) // 2, m_y))
        m_y += 30

        # Ganhos Automáticos de Classe
        from core.dnd_rules import CLASSES, get_modifier
        cls_data = CLASSES.get(class_name, {})
        dado_vida = cls_data.get("dado_vida", 8)
        con_val = pc.get("attributes", {}).get("CON", 10)
        pv_gain = max(1, (dado_vida // 2) + 1 + get_modifier(con_val))
        prof_bonus = 2 if next_lvl < 5 else 3

        gains_txt = f"Ganhos de Classe: +{pv_gain} PV Máximo (d{dado_vida})  •  Bônus Proficiência: +{prof_bonus}"
        screen.blit(self.font_btn.render(gains_txt, True, COLOR_INK), (card_x + 30, m_y))
        m_y += 24
        pygame.draw.line(screen, (190, 175, 145), (card_x + 30, m_y), (card_x + card_w - 30, m_y), 1)
        m_y += 12

        # Nova Habilidade de Classe Desbloqueada
        skill_tree = self._get_class_skill_tree(class_name)
        new_skill = next((s for s in skill_tree if s["level"] == next_lvl), None)
        screen.blit(self.font_b.render("Nova Habilidade de Classe:", True, COLOR_INK), (card_x + 30, m_y))
        m_y += 24

        if new_skill:
            sk_box = pygame.Rect(card_x + 30, m_y, card_w - 60, 50)
            pygame.draw.rect(screen, (225, 215, 190), sk_box, border_radius=4)
            pygame.draw.rect(screen, COLOR_GOLD, sk_box, 1, border_radius=4)

            # Ícone 40x40 dourado
            screen.blit(self._skill_icon_frames["available"], (sk_box.x + 5, sk_box.y + 5))
            g_surf = self.font_glyph.render(new_skill["glyph"], True, COLOR_GOLD)
            screen.blit(g_surf, (sk_box.x + 5 + (40 - g_surf.get_width()) // 2, sk_box.y + 5 + (40 - g_surf.get_height()) // 2))

            screen.blit(self.font_b.render(f"{new_skill['name']} (Nv {new_skill['level']})", True, (130, 40, 10)), (sk_box.x + 55, sk_box.y + 6))
            screen.blit(self.font_tiny.render(new_skill["short_desc"], True, (80, 70, 60)), (sk_box.x + 55, sk_box.y + 26))
        else:
            screen.blit(self.font_s.render("Aprimoramento Marcial e Espaços Arcanos Fortalecidos.", True, (90, 80, 70)), (card_x + 30, m_y))
        m_y += 62

        # Distribuição de Pontos de Atributo (+2 em 1 ou +1 em 2)
        pygame.draw.line(screen, (190, 175, 145), (card_x + 30, m_y), (card_x + card_w - 30, m_y), 1)
        m_y += 10

        points_msg = f"Aprimoramento de Atributos: {self.level_up_points_left} pontos restantes (+2 em 1 ou +1 em 2)"
        screen.blit(self.font_b.render(points_msg, True, (140, 50, 10) if self.level_up_points_left > 0 else (40, 120, 40)), (card_x + 30, m_y))
        m_y += 26

        self._lvlup_plus_rects.clear()
        self._lvlup_minus_rects.clear()
        attr_items = [("STR", "Força"), ("DEX", "Destreza"), ("CON", "Constituição"), ("INT", "Inteligência"), ("WIS", "Sabedoria"), ("CHA", "Carisma")]
        row_w = (card_w - 80) // 2

        attrs = pc.get("attributes", {})
        for idx, (a_code, a_name) in enumerate(attr_items):
            rx = card_x + 30 + (idx % 2) * (row_w + 20)
            ry = m_y + (idx // 2) * 32
            base_val = attrs.get(a_code, 10)
            bonus = self.level_up_alloc.get(a_code, 0)
            total_val = base_val + bonus

            btn_m = pygame.Rect(rx + row_w - 56, ry, 24, 24)
            btn_p = pygame.Rect(rx + row_w - 26, ry, 24, 24)
            self._lvlup_minus_rects[a_code] = btn_m
            self._lvlup_plus_rects[a_code] = btn_p

            screen.blit(self.font_btn.render(f"{a_name}: {total_val}", True, COLOR_INK), (rx, ry + 3))
            if bonus > 0:
                screen.blit(self.font_tiny.render(f"(+{bonus})", True, (40, 130, 40)), (rx + 110, ry + 5))

            draw_ui_button(screen, btn_m, "-", self.font_b, btn_m.collidepoint(mouse_pos), bonus > 0)
            draw_ui_button(screen, btn_p, "+", self.font_b, btn_p.collidepoint(mouse_pos), self.level_up_points_left > 0 and bonus < 2)

        m_y += 114

        # Botões de Ação do Modal
        btn_modal_w = 190
        self.btn_cancel_level_up = pygame.Rect(card_x + 60, card_y + card_h - 52, btn_modal_w, 34)
        self.btn_confirm_level_up = pygame.Rect(card_x + card_w - btn_modal_w - 60, card_y + card_h - 52, btn_modal_w, 34)

        draw_ui_button(screen, self.btn_cancel_level_up, "Voltar", self.font_btn, self.btn_cancel_level_up.collidepoint(mouse_pos), True)
        confirm_label = "Confirmar Evolução" if self.level_up_points_left == 0 else "Distribuir e Confirmar"
        draw_ui_button(screen, self.btn_confirm_level_up, confirm_label, self.font_b, self.btn_confirm_level_up.collidepoint(mouse_pos), True)

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.is_visible:
            return ""

        # Eventos do Modal Interativo de Level Up
        if self.level_up_modal_open:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # Botões [+] para alocar atributo
                for a_code, p_rect in self._lvlup_plus_rects.items():
                    if p_rect.collidepoint(mouse_pos) and self.level_up_points_left > 0:
                        cur_b = self.level_up_alloc.get(a_code, 0)
                        if cur_b < 2:
                            self.level_up_alloc[a_code] = cur_b + 1
                            self.level_up_points_left -= 1
                            return ""

                # Botões [-] para remover atributo
                for a_code, m_rect in self._lvlup_minus_rects.items():
                    if m_rect.collidepoint(mouse_pos):
                        cur_b = self.level_up_alloc.get(a_code, 0)
                        if cur_b > 0:
                            self.level_up_alloc[a_code] = cur_b - 1
                            self.level_up_points_left += 1
                            return ""

                # Botão Cancelar
                if self.btn_cancel_level_up.collidepoint(mouse_pos):
                    self.level_up_modal_open = False
                    return ""

                # Botão Confirmar
                if self.btn_confirm_level_up.collidepoint(mouse_pos):
                    if self.game_state_ref:
                        pc = self.game_state_ref.get("player_character")
                        self._apply_level_up_choices(pc)
                    else:
                        self.level_up_modal_open = False
                    return "level_up"

            elif event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE]:
                self.level_up_modal_open = False
                return ""
            return ""

        # Eventos normais do Grimório aberto
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # Clique em [Usar] item (aba legada items)
            if self.active_tab == "items":
                for item_id, btn_rect in self._item_buttons.items():
                    if btn_rect.collidepoint(mouse_pos):
                        return f"use_item:{item_id}"

            # Troca de abas
            if self.tab_skills_rect.collidepoint(mouse_pos):
                self.active_tab = "spells" if self.active_tab in ("items", "spells") else "habilidades"
                return ""
            if self.tab_bestiary_rect.collidepoint(mouse_pos):
                self.active_tab = "bestiario"
                return ""
            if self.tab_journal_rect.collidepoint(mouse_pos):
                self.active_tab = "diario"
                return ""
            if self.tab_status_rect.collidepoint(mouse_pos):
                self.active_tab = "items" if self.active_tab in ("items", "spells") else "status"
                return ""

            # Aba Habilidades: seleção de nós na árvore e botões
            if self.active_tab == "habilidades":
                for sk_id, node_rect in self._skill_node_rects.items():
                    icon_rect = self._skill_icon_rects.get(sk_id)
                    if node_rect.collidepoint(mouse_pos) or (icon_rect and icon_rect.collidepoint(mouse_pos)):
                        self.selected_skill_node = sk_id
                        return ""
                if self.btn_learn_skill and self.btn_learn_skill.collidepoint(mouse_pos):
                    if self.game_state_ref:
                        pc = self.game_state_ref.get("player_character")
                        self.open_level_up_modal(pc)
                    return "open_level_up_modal"

            # Aba Status: abrir mochila ou subir de nível
            if self.active_tab == "status":
                if self.btn_open_backpack and self.btn_open_backpack.collidepoint(mouse_pos):
                    return "open_backpack"
                for slot_key, slot_rect in self._equip_slot_rects.items():
                    if slot_rect.collidepoint(mouse_pos):
                        return "open_backpack"

            # Bestiário: seleção de monstro
            for m_id, b_rect in self._monster_buttons.items():
                if b_rect.collidepoint(mouse_pos):
                    self.selected_monster = m_id
                    return ""

            # Diário / Missões
            if self.active_tab == "diario":
                if self.btn_main_campaign.collidepoint(mouse_pos):
                    self.selected_quest_id = "main_campaign"
                    return ""
                if self.btn_filter_active.collidepoint(mouse_pos):
                    self.journal_filter = "ativas"
                    active_quests, _ = self._get_active_and_completed_quests()
                    if active_quests:
                        self.selected_quest_id = active_quests[0].get("id", "main_campaign")
                    else:
                        self.selected_quest_id = "main_campaign"
                    return ""
                if self.btn_filter_rumors.collidepoint(mouse_pos):
                    self.journal_filter = "rumores"
                    rumors = self._get_rumor_quests()
                    if rumors:
                        self.selected_quest_id = rumors[0].get("id", "main_campaign")
                    else:
                        self.selected_quest_id = "main_campaign"
                    return ""
                if self.btn_filter_completed.collidepoint(mouse_pos):
                    self.journal_filter = "concluidas"
                    _, completed = self._get_active_and_completed_quests()
                    if completed:
                        self.selected_quest_id = completed[0].get("id", "main_campaign")
                    else:
                        self.selected_quest_id = "main_campaign"
                    return ""
                for q_id, b_rect in self._quest_buttons.items():
                    if b_rect.collidepoint(mouse_pos):
                        self.selected_quest_id = q_id
                        return ""
                if self.btn_accept_quest and self.btn_accept_quest.collidepoint(mouse_pos):
                    return f"accept_side_quest:{self.selected_quest_id}"
                # A viagem é orgânica pela narrativa: botão e ação de teletransporte removidos!

            # Clique em [Conjurar] magia
            for spell_id, btn_rect in self._spell_buttons.items():
                if btn_rect.collidepoint(mouse_pos):
                    return f"cast_spell:{spell_id}"

            # Botão Level Up (na aba status)
            if self.game_state_ref:
                pc = self.game_state_ref.get("player_character")
                if pc and (pc.get("has_pending_level_up") or pc.get("xp", 0) >= pc.get("xp_to_next_level", 300)) and self.btn_level_up.collidepoint(mouse_pos):
                    self.open_level_up_modal(pc)
                    return "open_level_up_modal"

            # Clique fora fecha
            if not self.rect.collidepoint(mouse_pos):
                return "close_grimoire"
        elif event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_TAB]:
            return "close_grimoire"
        return ""

class LoadingDiceAnimation:
    """Motor de animação frame-a-frame do dado d20 pixel art (Zero Garbage a 60 FPS)."""
    def __init__(self):
        self.frames = []
        self.last_update = 0
        self.current_frame = 0
        self.frame_delay = 85
        self.angle = 0

        self.result_value: Optional[int] = None
        self.result_label: str = ""
        self.result_until: int = 0
        self._result_die_cache: Dict[int, pygame.Surface] = {}
        self._result_banner_cache: Dict[tuple, pygame.Surface] = {}

        self.font_banner = AssetManager.get_font(15, bold=True)
        self.font_num_big = AssetManager.get_font(22, bold=True)

        base_dir = os.path.normpath("assets/ui/dice_loading")
        if os.path.exists(base_dir):
            for i in range(1, 20):
                file_path = os.path.join(base_dir, f"frame_{i}.png")
                if os.path.exists(file_path):
                    try:
                        raw = pygame.image.load(file_path)
                        try:
                            surf = raw.convert_alpha()
                        except pygame.error:
                            surf = raw
                        self.frames.append(surf)
                    except Exception:
                        pass
                else:
                    break

        # Superfície base para fallback do polígono rotativo (zero alocação por frame)
        self.poly_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        points = [(32, 0), (64, 20), (52, 64), (12, 64), (0, 20)]
        pygame.draw.polygon(self.poly_surface, COLOR_GOLD, points)
        pygame.draw.polygon(self.poly_surface, (100, 70, 20), points, 3)

        # 1. Bandeja / Medalhão circular gótico de madeira escura e bronze (_tray_surf) pré-renderizado
        self._tray_surf = pygame.Surface((164, 72), pygame.SRCALPHA)
        pygame.draw.ellipse(self._tray_surf, (0, 0, 0, 145), (8, 16, 148, 52))
        pygame.draw.ellipse(self._tray_surf, (42, 26, 16, 250), (12, 8, 140, 52))
        pygame.draw.ellipse(self._tray_surf, (135, 98, 45, 255), (12, 8, 140, 52), 3)
        pygame.draw.ellipse(self._tray_surf, (82, 20, 18, 255), (24, 15, 116, 38))
        pygame.draw.ellipse(self._tray_surf, COLOR_GOLD, (24, 15, 116, 38), 2)
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            rx = int(82 + 62 * math.cos(rad))
            ry = int(34 + 21 * math.sin(rad))
            pygame.draw.circle(self._tray_surf, COLOR_GOLD, (rx, ry), 2)

        # 2. Faixa de pergaminho (_banner_surf) abaixo com "Rolando o Destino..." pré-renderizada
        self._banner_surf = self._build_banner_surface("Rolando o Destino...", COLOR_PARCHMENT, COLOR_GOLD, COLOR_INK)

        # Pré-aquece faces de resultado para 1 e 20
        self._get_result_die_surface(20)
        self._get_result_die_surface(1)

    def _build_banner_surface(self, text: str, bg_color: tuple, border_color: tuple, text_color: tuple) -> pygame.Surface:
        tw, th = self.font_banner.size(text)
        bw = max(230, tw + 36)
        bh = 34
        surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
        pygame.draw.rect(surf, (12, 8, 6, 190), (2, 3, bw - 4, bh - 3), border_radius=6)
        pygame.draw.rect(surf, bg_color, (0, 0, bw - 4, bh - 4), border_radius=6)
        pygame.draw.rect(surf, border_color, (0, 0, bw - 4, bh - 4), 2, border_radius=6)
        pygame.draw.rect(surf, (65, 45, 25), (3, 3, bw - 10, bh - 10), 1, border_radius=4)
        txt_s = self.font_banner.render(text, True, text_color)
        surf.blit(txt_s, ((bw - 4 - tw) // 2, (bh - 4 - th) // 2))
        return surf

    def _get_result_die_surface(self, value: int) -> pygame.Surface:
        val = max(1, min(20, int(value)))
        if val in self._result_die_cache:
            return self._result_die_cache[val]

        surf = pygame.Surface((96, 96), pygame.SRCALPHA)
        cx, cy = 48, 48
        r_out = 39
        r_in = 21

        if val == 20:
            # 20 Natural: Brilho dourado radiante + rubi imperial
            c_outer = (215, 70, 45)
            c_inner = (240, 95, 55)
            c_edge = (255, 230, 120)
            c_text = (255, 245, 175)
            pygame.draw.circle(surf, (255, 215, 70, 75), (cx, cy), 45)
        elif val == 1:
            # 1 Natural: Carmesim sombrio / sangue escuro
            c_outer = (75, 18, 16)
            c_inner = (105, 24, 20)
            c_edge = (150, 95, 65)
            c_text = (240, 80, 70)
        else:
            c_outer = (176, 50, 37)
            c_inner = (217, 78, 59)
            c_edge = (229, 192, 123)
            c_text = (255, 235, 180)

        outer_pts = []
        for k in range(6):
            ang = k * (math.pi / 3.0) - (math.pi / 2.0)
            outer_pts.append((int(cx + r_out * math.cos(ang)), int(cy + r_out * math.sin(ang))))

        inner_pts = []
        for k in range(3):
            ang = k * (2.0 * math.pi / 3.0) - (math.pi / 2.0)
            inner_pts.append((int(cx + r_in * math.cos(ang)), int(cy + r_in * math.sin(ang))))

        pygame.draw.polygon(surf, c_outer, outer_pts)
        pygame.draw.polygon(surf, c_inner, inner_pts)

        for k in range(3):
            p_in = inner_pts[k]
            p_next = inner_pts[(k + 1) % 3]
            pygame.draw.line(surf, c_edge, p_in, p_next, 2)
            pygame.draw.line(surf, c_edge, p_in, outer_pts[k * 2], 2)
            pygame.draw.line(surf, c_edge, p_in, outer_pts[(k * 2 + 1) % 6], 2)
            pygame.draw.line(surf, c_edge, p_in, outer_pts[(k * 2 - 1) % 6], 2)

        pygame.draw.polygon(surf, c_edge, outer_pts, 3)
        pygame.draw.polygon(surf, (36, 16, 11), outer_pts, 2)

        val_str = str(val)
        fg_s = self.font_num_big.render(val_str, True, c_text)
        outline_s = self.font_num_big.render(val_str, True, (0, 0, 0))
        # Contorno preto sólido de 2px nos 8 sentidos ao redor do centro para nitidez impecável
        for ox in (-2, -1, 0, 1, 2):
            for oy in (-2, -1, 0, 1, 2):
                if ox != 0 or oy != 0:
                    surf.blit(outline_s, outline_s.get_rect(center=(cx + ox, cy + 2 + oy)))
        surf.blit(fg_s, fg_s.get_rect(center=(cx, cy + 2)))

        self._result_die_cache[val] = surf
        return surf

    def trigger_roll_result(self, value: int, label: str = "", duration_ms: int = 1100):
        """Crava o d20 na tela por ~1.1s exibindo o valor sorteado e destaque para 20 ou 1 Natural."""
        val = max(1, min(20, int(value)))
        self.result_value = val
        self.result_label = str(label or "").strip()
        self.result_until = pygame.time.get_ticks() + max(100, int(duration_ms))

        # Garante que a superfície do dado e do banner já estão em cache antes do draw()
        self._get_result_die_surface(val)
        cache_key = (val, self.result_label)
        if cache_key not in self._result_banner_cache:
            if val == 20:
                banner_txt = f">> 20 CRÍTICO! << {self.result_label}".strip()
                self._result_banner_cache[cache_key] = self._build_banner_surface(
                    banner_txt, (55, 36, 14), (255, 215, 65), (255, 225, 90)
                )
            elif val == 1:
                banner_txt = f"1 FALHA CRÍTICA! {self.result_label}".strip()
                self._result_banner_cache[cache_key] = self._build_banner_surface(
                    banner_txt, (42, 12, 12), (195, 45, 40), (245, 95, 85)
                )
            else:
                banner_txt = self.result_label if self.result_label else f"Resultado d20: {val}"
                self._result_banner_cache[cache_key] = self._build_banner_surface(
                    banner_txt, COLOR_PARCHMENT, COLOR_GOLD, COLOR_INK
                )

    def is_showing_result(self) -> bool:
        return self.result_value is not None and pygame.time.get_ticks() < self.result_until

    def draw(self, screen: pygame.Surface, cx: int, cy: int):
        now = pygame.time.get_ticks()

        # 1. Bandeja circular gótica sob o dado
        tray_rect = self._tray_surf.get_rect(center=(cx, cy + 20))
        screen.blit(self._tray_surf, tray_rect)

        # 2. Modo de revelação de resultado cravado (~1.1s)
        if self.result_value is not None and now < self.result_until:
            die_surf = self._get_result_die_surface(self.result_value)
            shake_x = int(math.sin(now * 0.08) * 3) if self.result_value == 1 else 0
            die_rect = die_surf.get_rect(center=(cx + shake_x, cy - 6))
            screen.blit(die_surf, die_rect)

            cache_key = (self.result_value, self.result_label)
            banner_surf = self._result_banner_cache.get(cache_key, self._banner_surf)
            banner_rect = banner_surf.get_rect(center=(cx, cy + 62))
            screen.blit(banner_surf, banner_rect)
            return

        # 3. Modo de giro contínuo com quique vertical suave (math.sin)
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame += 1
            self.angle = (self.angle + 15) % 360

        bounce_y = int(math.sin(now * 0.012) * 6)

        if self.frames:
            idx = self.current_frame % len(self.frames)
            surf = self.frames[idx]
            rect = surf.get_rect(center=(cx, cy - 8 + bounce_y))
            screen.blit(surf, rect)
        else:
            rotated_surf = pygame.transform.rotate(self.poly_surface, self.angle)
            rect = rotated_surf.get_rect(center=(cx, cy - 8 + bounce_y))
            screen.blit(rotated_surf, rect)

        banner_rect = self._banner_surf.get_rect(center=(cx, cy + 62))
        screen.blit(self._banner_surf, banner_rect)


# =============================================================================
# HUD DO JOGADOR (Painel retrô semitransparente com layout de eixo Y dinâmico)
# =============================================================================

_PRIMARY_HUD_FONT = os.path.normpath("assets/fonts/Retro Gaming.ttf")
_FALLBACK_HUD_FONT = os.path.normpath("assets/fonts/pixel_font.ttf")
HUD_FONT_PATH = _PRIMARY_HUD_FONT if os.path.exists(_PRIMARY_HUD_FONT) else _FALLBACK_HUD_FONT
_HUD_FONT_CACHE = {}


def load_hud_font(size: int) -> pygame.font.Font:
    """Carrega a fonte Retro Gaming do HUD com fallback seguro para pixel_font.ttf e Arial."""
    from ui.asset_manager import AssetManager
    return AssetManager.get_font(size)


def _lighten(color: tuple, amount: int = 60) -> tuple:
    return tuple(min(255, c + amount) for c in color[:3])


class PlayerHUD:
    """HUD do herói: retrato + Nome/Nível + barras PV, PM, PA, XP (as que existirem).

    Todo o posicionamento vertical nasce de `current_y += altura + SPACING`;
    o painel calcula a própria altura a partir das linhas visíveis.
    """

    PADDING = 10
    SPACING = 6
    PORTRAIT = 64
    PORTRAIT_GAP = 12
    LABEL_GAP = 8
    BAR_W = 170
    PANEL_ALPHA = 190
    PANEL_COLOR = (12, 10, 16)

    COLOR_PV_HIGH = (60, 170, 60)
    COLOR_PV_MID = (210, 150, 40)
    COLOR_PV_LOW = (190, 40, 40)
    COLOR_PM = (60, 90, 210)
    COLOR_PA = (220, 120, 40)
    COLOR_XP = (200, 160, 30)

    def __init__(self, x: int = 12, y: int = 12):
        self.origin = (x, y)
        self.font_label = load_hud_font(16)
        self.font_name = load_hud_font(20)
        self._panel_cache = {}
        self.rect = pygame.Rect(x, y, 0, 0)

    # ------------------------------------------------------------ dados
    def _pv_color(self, ratio: float) -> tuple:
        if ratio > 0.5:
            return self.COLOR_PV_HIGH
        if ratio > 0.25:
            return self.COLOR_PV_MID
        return self.COLOR_PV_LOW

    def _build_rows(self, player: dict) -> list:
        rows = []

        hp_cur = player.get("hp_current", 0)
        hp_max = max(1, player.get("hp_max", 1))
        rows.append({"label": "PV", "cur": hp_cur, "max": hp_max,
                     "color": self._pv_color(hp_cur / hp_max)})

        if player.get("mp_max"):
            rows.append({"label": "PM", "cur": player.get("mp_current", 0),
                         "max": player["mp_max"], "color": self.COLOR_PM})

        slots = player.get("spell_slots")
        if isinstance(slots, dict) and slots:
            txt = "  ".join(f"{lvl}:{qtd}" for lvl, qtd in sorted(slots.items(), key=lambda kv: str(kv[0])))
            rows.append({"label": "MAGIAS", "text": txt})

        if player.get("action_points") is not None:
            ap = player.get("action_points", 0)
            rows.append({"label": "PA", "cur": ap,
                         "max": max(1, player.get("action_points_max", ap)), "color": self.COLOR_PA})

        gold = player.get("gold", 15)
        rows.append({"label": "OURO", "text": f"{gold} PO"})

        if player.get("has_pending_level_up") or player.get("xp", 0) >= player.get("xp_to_next_level", 300):
            rows.append({"label": "NÍVEL", "text": "! SUBIR DE NÍVEL!", "blink": True})
        return rows

    # ------------------------------------------------------------ desenho
    def _get_panel_surface(self, w: int, h: int) -> pygame.Surface:
        key = (w, h)
        if key not in self._panel_cache:
            surf = pygame.Surface((w, h))
            surf.fill(self.PANEL_COLOR)
            surf.set_alpha(self.PANEL_ALPHA)
            self._panel_cache[key] = surf
        return self._panel_cache[key]

    @staticmethod
    def _blit_text(screen, font, text, color, pos, shadow=True):
        if shadow:
            screen.blit(font.render(text, True, (0, 0, 0)), (pos[0] + 1, pos[1] + 1))
        surf = font.render(text, True, color)
        screen.blit(surf, pos)
        return surf

    def _draw_bar(self, screen, rect: pygame.Rect, cur, mx, color):
        pygame.draw.rect(screen, (28, 22, 22), rect)
        ratio = max(0.0, min(1.0, cur / max(mx, 1)))
        fill_w = int(rect.width * ratio)
        if fill_w > 0:
            pygame.draw.rect(screen, color, (rect.x, rect.y, fill_w, rect.height))
            pygame.draw.line(screen, _lighten(color), (rect.x, rect.y), (rect.x + fill_w - 1, rect.y))
        pygame.draw.rect(screen, (95, 75, 45), rect, 1)

        value = f"{cur}/{mx}"
        tw, th = self.font_label.size(value)
        self._blit_text(screen, self.font_label, value, COLOR_PARCHMENT,
                        (rect.x + (rect.width - tw) // 2, rect.y + (rect.height - th) // 2))

    def draw(self, screen: pygame.Surface, player: dict) -> pygame.Rect:
        if not player:
            self.rect = pygame.Rect(self.origin[0], self.origin[1], 0, 0)
            return self.rect

        try:
            self.font_label.get_height()
        except (pygame.error, Exception):
            self.font_label = load_hud_font(16)
            self.font_name = load_hud_font(20)

        fl, fn = self.font_label, self.font_name
        rows = self._build_rows(player)

        # --- Métricas dinâmicas (nada de Y absoluto por barra) ---
        row_h = fl.get_height() + 4
        label_w = max(fl.size(r["label"])[0] for r in rows)
        name_txt = str(player.get("name", "Desconhecido"))
        level_txt = f"Nv. {player.get('level', 1)}"
        header_h = fn.get_height()

        content_w = max(label_w + self.LABEL_GAP + self.BAR_W,
                        fn.size(name_txt)[0] + 16 + fl.size(level_txt)[0])
        content_h = header_h + self.SPACING + len(rows) * (row_h + self.SPACING) - self.SPACING

        x, y = self.origin
        w = self.PADDING + self.PORTRAIT + self.PORTRAIT_GAP + content_w + self.PADDING
        h = self.PADDING + max(self.PORTRAIT, content_h) + self.PADDING

        # --- Painel retrô semitransparente ---
        screen.blit(self._get_panel_surface(w, h), (x, y))
        pygame.draw.rect(screen, COLOR_GOLD, (x, y, w, h), 2)
        pygame.draw.rect(screen, (70, 50, 25), (x + 3, y + 3, w - 6, h - 6), 1)

        # --- Retrato (ícone do herói) com downscaling de alta definição e moldura dark fantasy elegante ---
        px, py = x + self.PADDING, y + self.PADDING
        icon = AssetManager.get_hero_icon(player.get("race"), player.get("class"),
                                          player.get("gender") or player.get("genero"),
                                          size=(self.PORTRAIT, self.PORTRAIT))
        scaled_icon = AssetManager.progressive_downscale(icon, (self.PORTRAIT, self.PORTRAIT))
        screen.blit(scaled_icon, (px, py))

        # Moldura dark fantasy elegante
        pygame.draw.rect(screen, (10, 8, 6), (px - 2, py - 2, self.PORTRAIT + 4, self.PORTRAIT + 4), 1, border_radius=4)
        pygame.draw.rect(screen, COLOR_GOLD, (px, py, self.PORTRAIT, self.PORTRAIT), 2, border_radius=3)
        pygame.draw.rect(screen, (160, 115, 55), (px + 2, py + 2, self.PORTRAIT - 4, self.PORTRAIT - 4), 1)
        c_len = 6
        for cx_pt, cy_pt in [(px, py), (px + self.PORTRAIT - c_len, py), (px, py + self.PORTRAIT - 1), (px + self.PORTRAIT - c_len, py + self.PORTRAIT - 1)]:
            pygame.draw.line(screen, (255, 230, 140), (cx_pt, cy_pt), (cx_pt + c_len, cy_pt), 2)

        # --- Coluna de dados ---
        col_x = px + self.PORTRAIT + self.PORTRAIT_GAP
        current_y = py

        self._blit_text(screen, fn, name_txt, (255, 255, 255), (col_x, current_y))
        lvl_w, lvl_h = fl.size(level_txt)
        self._blit_text(screen, fl, level_txt, COLOR_GOLD,
                        (col_x + content_w - lvl_w, current_y + (header_h - lvl_h) // 2))
        current_y += header_h + self.SPACING

        bar_x = col_x + label_w + self.LABEL_GAP
        blink_on = (pygame.time.get_ticks() % 1000) < 600

        for row in rows:
            lbl_h = fl.size(row["label"])[1]
            self._blit_text(screen, fl, row["label"], COLOR_PARCHMENT,
                            (col_x, current_y + (row_h - lbl_h) // 2))

            if "cur" in row:
                self._draw_bar(screen, pygame.Rect(bar_x, current_y, self.BAR_W, row_h),
                               row["cur"], row["max"], row["color"])
            elif not row.get("blink") or blink_on:
                color = (255, 215, 0) if row.get("blink") else COLOR_TEXT_DIM
                txt_h = fl.size(row["text"])[1]
                self._blit_text(screen, fl, row["text"], color,
                                (bar_x, current_y + (row_h - txt_h) // 2))

            current_y += row_h + self.SPACING

        self.rect = pygame.Rect(x, y, w, h)
        return self.rect


class QuickActionBar:
    """Barra compacta de atalhos rápidos de ação do jogador (Mochila, Grimório, Observar/Atacar, Dialogar, Descansar)."""
    def __init__(self, x: int, y: int, width: int, height: int = 28):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = AssetManager.get_font(13, bold=True)
        self.is_combat = False
        self._rebuild_buttons()

    def set_combat_mode(self, is_combat: bool):
        if self.is_combat != is_combat:
            self.is_combat = is_combat
            self._rebuild_buttons()

    def _rebuild_buttons(self):
        if self.is_combat:
            self.btn_configs = [
                {"id": "attack",    "label": "⚔ Atacar"},
                {"id": "inventory", "label": "Mochila"},
                {"id": "grimoire",  "label": "Grimório"},
                {"id": "observe",   "label": "Observar"},
                {"id": "talk",      "label": "Dialogar"},
            ]
        else:
            self.btn_configs = [
                {"id": "inventory", "label": "Mochila"},
                {"id": "grimoire",  "label": "Grimório"},
                {"id": "observe",   "label": "Observar"},
                {"id": "talk",      "label": "Dialogar"},
                {"id": "rest",      "label": "Descansar"},
            ]
        self.buttons = []
        btn_w = (self.rect.width - ((len(self.btn_configs) - 1) * 4)) // len(self.btn_configs)
        for i, cfg in enumerate(self.btn_configs):
            b_rect = pygame.Rect(self.rect.x + i * (btn_w + 4), self.rect.y, btn_w, self.rect.height)
            self.buttons.append({"id": cfg["id"], "label": cfg["label"], "rect": b_rect})

    def draw(self, screen: pygame.Surface, is_combat: bool = None):
        if is_combat is not None and is_combat != self.is_combat:
            self.set_combat_mode(is_combat)
        mouse_pos = pygame.mouse.get_pos()
        for b in self.buttons:
            is_hover = b["rect"].collidepoint(mouse_pos)
            if b["id"] == "attack":
                bg_col = (180, 45, 35) if not is_hover else (225, 65, 50)
                pygame.draw.rect(screen, bg_col, b["rect"], border_radius=4)
                pygame.draw.rect(screen, COLOR_GOLD if is_hover else (255, 180, 50), b["rect"], 2, border_radius=4)
                txt = self.font.render(clean_tofu_glyphs(b["label"]), True, (255, 255, 255))
                screen.blit(txt, (b["rect"].centerx - txt.get_width() // 2, b["rect"].centery - txt.get_height() // 2))
            else:
                draw_ui_button(screen, b["rect"], b["label"], self.font, is_hover, True)

    def handle_event(self, event: pygame.event.Event) -> str:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for b in self.buttons:
                if b["rect"].collidepoint(event.pos):
                    return b["id"]
        return ""


class PlayerManualModal(Panel):
    """Manual do Jogador In-Game com 6 capítulos essenciais (5ª Edição D&D).

    Zero Garbage a 60 FPS: textos quebrados em cache e superfícies pré-renderizadas.
    Suporta navegação por abas laterais, botões Anterior/Próximo e atalhos ESC, F1, H.
    """

    CHAPTERS = [
        {
            "id": "chat",
            "tab": "1. Chat & Comandos",
            "header": "Comunicação e Narração Livre",
            "text": (
                "No RPGMesaPY, você pode conversar e agir livremente digitando na caixa de texto inferior. "
                "O Mestre da IA interpreta suas ações dentro das regras oficiais da 5ª Edição de D&D.\n\n"
                "Instruções e Dicas:\n"
                "- Digite ações naturais como 'Procuro por armadilhas' ou 'Pergunto ao taverneiro sobre os boatos'.\n"
                "- O Mestre responderá solicitando testes apropriados de Perícia (Percepção, Investigação, etc.).\n"
                "- Use a barra de Ações Rápidas no canto inferior para atalhos diretos de exploração e combate.\n"
                "- Suas falas aparecem no painel esquerdo identificadas com seu retrato e nome."
            )
        },
        {
            "id": "exploracao",
            "tab": "2. Exploração",
            "header": "Navegação e Pontos de Interesse",
            "text": (
                "A exploração do mundo ocorre de forma viva, atmosférica e orgânica.\n\n"
                "Mecânicas de Exploração:\n"
                "- Interaja com o ambiente clicando em NPCs, portas ou áreas de interesse narrativo.\n"
                "- Fique atento às descrições do Menestrel: pistas valiosas surgem nos detalhes visuais e sonoros.\n"
                "- A transição entre os cenários respeita a geografia dos ermos, sem viagens instantâneas artificiais.\n"
                "- Converse com os habitantes locais para desbloquear novas informações no Diário de Aventuras."
            )
        },
        {
            "id": "combate",
            "tab": "3. Regras de Combate",
            "header": "Conflitos Táticos e Turnos D&D 5e",
            "text": (
                "Quando o perigo é iminente, as armas são desembainhadas e a iniciativa é declarada.\n\n"
                "Fases do Combate:\n"
                "- Iniciativa: Um d20 somado à sua Destreza define a ordem de ação de todos em campo.\n"
                "- Ação de Ataque: Teste d20 + Bônus de Ataque contra a Classe de Armadura (CA) do alvo.\n"
                "- 20 Natural: Acerto Crítico espetacular! Causa dano massivo ampliado.\n"
                "- 1 Natural: Falha Crítica, seu ataque erra desastrosamente.\n"
                "- Clique diretamente nos inimigos no tabuleiro ou use o botão Atacar na barra de ações."
            )
        },
        {
            "id": "mochila",
            "tab": "4. Grimório & Ficha",
            "header": "Gerenciamento de Ficha e Inventário",
            "text": (
                "Seu livro de aventuras reúne tudo o que seu herói carrega e conhece.\n\n"
                "Recursos do Grimório (Tecla TAB):\n"
                "- Ficha de Personagem: Visualize atributos base, bônus raciais, CA, deslocamento e proficiências.\n"
                "- Diário de Missões: Consulte missões ativas e concluídas com objetivos e recompensas.\n"
                "- Bestiário: Criaturas catalogadas revelam CA, pontos fracos, resistências e conselhos táticos.\n"
                "- Subir de Nível: Ao acumular XP suficiente, distribua atributos e receba novas habilidades de classe."
            )
        },
        {
            "id": "sobrevivencia",
            "tab": "5. Sobrevivência",
            "header": "Descanso e Gestão de Recursos",
            "text": (
                "As provações nos ermos exigem cautela e gerenciamento consciente de seus limites.\n\n"
                "Regras de Descanso:\n"
                "- Descanso Curto (1 hora): Permite utilizar Dados de Vida (HD) para recuperar Pontos de Vida (PV).\n"
                "- Descanso Longo (8 horas): Recupera todos os PVs e habilidades de classe na Taverna ou acampamento.\n"
                "- Gestão de Poções: Mantenha suprimentos na mochila para momentos críticos em batalha.\n"
                "- Cuidado com a morte: Se seus PVs chegarem a 0, você ficará à beira do abismo."
            )
        },
        {
            "id": "dejavu",
            "tab": "6. Ecos Temporais",
            "header": "O Enigma das Cinzas e Déjà-Vu",
            "text": (
                "Estranhas anomalias cercam a Taverna do Javali Caolho e seus arredores.\n\n"
                "O Fenômeno Temporal:\n"
                "- Ecos do passado insistem em se repetir nos diálogos de certos aldeões e viajantes.\n"
                "- Observe inconsistências no tempo, objetos familiares e frases que parecem já ter sido ouvidas.\n"
                "- A verdade por trás do Tirano das Cinzas está entrelaçada a essas distorções temporais.\n"
                "- Suas escolhas ao longo dos três Atos determinarão se o ciclo será quebrado ou eterno."
            )
        }
    ]

    def __init__(self, x: int = 220, y: int = 80, width: int = 840, height: int = 560):
        super().__init__(x, y, width, height, title="Manual do Jogador - 5ª Edição D&D")
        self.font_h = AssetManager.get_font(20, bold=True)
        self.font_tab = AssetManager.get_font(14, bold=True)
        self.font_text = AssetManager.get_font(15)
        self.font_page = AssetManager.get_font(14, bold=True)
        self.font_nav = AssetManager.get_font(14, bold=True)

        self.current_chapter = 0

        # Layout interno
        sidebar_w = 210
        margin = 16
        top_bar_h = 44

        # Botão Fechar no canto superior direito
        self.btn_close = pygame.Rect(self.rect.right - 42, self.rect.y + 7, 32, 30)

        # Abas verticais da barra lateral
        self.tab_rects = []
        tab_y = self.rect.y + top_bar_h + margin
        tab_h = 38
        tab_gap = 8
        for i in range(len(self.CHAPTERS)):
            t_rect = pygame.Rect(self.rect.x + margin, tab_y + i * (tab_h + tab_gap), sidebar_w, tab_h)
            self.tab_rects.append(t_rect)

        # Área de conteúdo (Pergaminho à direita)
        content_x = self.rect.x + margin + sidebar_w + margin
        content_y = self.rect.y + top_bar_h + margin
        content_w = self.rect.width - (sidebar_w + margin * 3)
        content_h = self.rect.height - (top_bar_h + margin * 2)
        self.content_rect = pygame.Rect(content_x, content_y, content_w, content_h)

        # Botões de navegação no rodapé da área de conteúdo
        nav_btn_w, nav_btn_h = 130, 32
        self.btn_prev = pygame.Rect(self.content_rect.x + 20, self.content_rect.bottom - nav_btn_h - 14, nav_btn_w, nav_btn_h)
        self.btn_next = pygame.Rect(self.content_rect.right - nav_btn_w - 20, self.content_rect.bottom - nav_btn_h - 14, nav_btn_w, nav_btn_h)

        # Pré-cálculo de linhas de texto (Zero Garbage a 60 FPS)
        self._chapter_lines = {}
        usable_text_w = self.content_rect.width - 40
        for idx, ch in enumerate(self.CHAPTERS):
            _, _, lines = get_wrapped_text_dimensions(ch["text"], self.font_text, usable_text_w, fixed_line_height=22)
            self._chapter_lines[idx] = lines

        # Cache de fundo de pergaminho
        self._parchment_surf = pygame.Surface((self.content_rect.width, self.content_rect.height))
        self._parchment_surf.fill((244, 236, 218))
        pygame.draw.rect(self._parchment_surf, (190, 175, 145), (0, 0, self.content_rect.width, self.content_rect.height), 2, border_radius=6)
        pygame.draw.rect(self._parchment_surf, (225, 215, 195), (3, 3, self.content_rect.width - 6, self.content_rect.height - 6), 1, border_radius=5)

    def draw(self, screen: pygame.Surface):
        if not self.is_visible:
            return

        # Painel de madeira de fundo
        draw_ui_panel(screen, self.rect, "wood_panel")

        # Topo dourado com título
        title_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 42)
        pygame.draw.rect(screen, (32, 22, 16), title_rect)
        pygame.draw.rect(screen, COLOR_GOLD, title_rect, 2)
        t_surf = self.font_title.render(self.title, True, COLOR_GOLD)
        screen.blit(t_surf, (self.rect.x + 20, self.rect.y + 8))

        # Botão Fechar [X]
        mouse_pos = pygame.mouse.get_pos()
        draw_ui_button(screen, self.btn_close, "X", self.font_h, self.btn_close.collidepoint(mouse_pos), True)

        # Abas laterais de capítulos
        for i, ch in enumerate(self.CHAPTERS):
            t_rect = self.tab_rects[i]
            is_active = (i == self.current_chapter)
            is_hover = t_rect.collidepoint(mouse_pos)

            if is_active:
                pygame.draw.rect(screen, (70, 50, 30), t_rect, border_radius=4)
                pygame.draw.rect(screen, COLOR_GOLD, t_rect, 2, border_radius=4)
                tab_txt = self.font_tab.render(ch["tab"], True, (255, 235, 170))
            elif is_hover:
                pygame.draw.rect(screen, (50, 38, 25), t_rect, border_radius=4)
                pygame.draw.rect(screen, (200, 170, 90), t_rect, 1, border_radius=4)
                tab_txt = self.font_tab.render(ch["tab"], True, COLOR_GOLD)
            else:
                pygame.draw.rect(screen, (35, 26, 18), t_rect, border_radius=4)
                pygame.draw.rect(screen, (100, 80, 55), t_rect, 1, border_radius=4)
                tab_txt = self.font_tab.render(ch["tab"], True, (180, 165, 140))

            screen.blit(tab_txt, (t_rect.x + 12, t_rect.centery - tab_txt.get_height() // 2))

        # Card de pergaminho de conteúdo
        screen.blit(self._parchment_surf, (self.content_rect.x, self.content_rect.y))

        ch = self.CHAPTERS[self.current_chapter]
        cy = self.content_rect.y + 18

        # Cabeçalho do capítulo
        hdr_surf = self.font_h.render(ch["header"], True, (120, 25, 15))
        screen.blit(hdr_surf, (self.content_rect.x + 20, cy))
        cy += 28

        # Divisor suave
        pygame.draw.line(screen, (190, 175, 145), (self.content_rect.x + 20, cy), (self.content_rect.right - 20, cy), 1)
        cy += 14

        # Texto do capítulo
        lines = self._chapter_lines.get(self.current_chapter, [])
        line_h = 22
        for line in lines:
            if cy + self.font_text.get_height() > self.btn_prev.y - 10:
                break
            if line:
                l_surf = self.font_text.render(line, True, COLOR_INK)
                screen.blit(l_surf, (self.content_rect.x + 20, cy))
            cy += line_h

        # Rodapé de navegação
        has_prev = (self.current_chapter > 0)
        has_next = (self.current_chapter < len(self.CHAPTERS) - 1)

        draw_ui_button(screen, self.btn_prev, "< Anterior", self.font_nav, self.btn_prev.collidepoint(mouse_pos), has_prev)
        draw_ui_button(screen, self.btn_next, "Próximo >", self.font_nav, self.btn_next.collidepoint(mouse_pos), has_next)

        # Indicador de página centralizado
        page_str = f"Capítulo {self.current_chapter + 1} de {len(self.CHAPTERS)}"
        page_surf = self.font_page.render(page_str, True, (110, 95, 75))
        screen.blit(page_surf, (self.content_rect.centerx - page_surf.get_width() // 2, self.btn_prev.centery - page_surf.get_height() // 2))

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.is_visible:
            return ""

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_F1, pygame.K_h):
                self.is_visible = False
                return "close"
            elif event.key == pygame.K_LEFT and self.current_chapter > 0:
                self.current_chapter -= 1
                return f"chapter_{self.current_chapter}"
            elif event.key == pygame.K_RIGHT and self.current_chapter < len(self.CHAPTERS) - 1:
                self.current_chapter += 1
                return f"chapter_{self.current_chapter}"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_close.collidepoint(event.pos):
                self.is_visible = False
                return "close"

            for i, t_rect in enumerate(self.tab_rects):
                if t_rect.collidepoint(event.pos):
                    self.current_chapter = i
                    return f"chapter_{i}"

            if self.btn_prev.collidepoint(event.pos) and self.current_chapter > 0:
                self.current_chapter -= 1
                return f"chapter_{self.current_chapter}"

            if self.btn_next.collidepoint(event.pos) and self.current_chapter < len(self.CHAPTERS) - 1:
                self.current_chapter += 1
                return f"chapter_{self.current_chapter}"

            # Clique fora do modal fecha o Manual
            if not self.rect.collidepoint(event.pos):
                self.is_visible = False
                return "close"

        return ""


