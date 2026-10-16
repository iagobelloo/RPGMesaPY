"""
Console Narrativo e Campo de Entrada de Chat (RPGMesaPY).
Fase 4 do Redesign UI/UX — Contrato Zero Garbage por Frame.
Word-wrap e renderização executados estritamente NA CHEGADA da mensagem.
Suporte nativo a TEXTINPUT, histórico, scrolling suave e indicador de foco.
"""

from collections import deque
from typing import Optional
import pygame
from ui.asset_manager import AssetManager
from ..theme import Palette, Layout
from ..render_cache import FrameFactory, default_text_cache
from ..base import UIWidget, CONSUMED


class NarrativeLogView(UIWidget):
    """
    Visualizador do log narrativo com rolagem por roda do mouse.
    Buffer em deque(maxlen=300).
    Zero Garbage: Superfícies de texto geradas no push_message(), NUNCA no draw().
    """

    LINE_H: int = 18
    MAX_LINES: int = 300

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect):
        super().__init__(rect)

        # Buffer de tuplas (surface, kind)
        self._lines: deque[tuple[pygame.Surface, str]] = deque(maxlen=self.MAX_LINES)
        self._pending_typewriter_lines: deque[tuple[pygame.Surface, str]] = deque()
        self._typewriter_timer: float = 0.0
        self._typewriter_interval: float = 0.06  # Libera linhas progressivamente a cada ~60ms
        self._scroll_offset: int = 0  # 0 = fixo no final (mais recente)
        self._font_size: int = 12

        # Dimensões de visualização
        self._visible_lines_count: int = max(1, self.rect.h // self.LINE_H)

    def flush_typewriter(self) -> None:
        """Despeja todas as linhas pendentes do typewriter instantaneamente."""
        while self._pending_typewriter_lines:
            surf, kind = self._pending_typewriter_lines.popleft()
            self._lines.append((surf, kind))
            if self._scroll_offset > 0:
                self._scroll_offset += 1
                max_scroll = max(0, len(self._lines) - self._visible_lines_count)
                self._scroll_offset = min(self._scroll_offset, max_scroll)

    def update(self, dt: float) -> None:
        super().update(dt)
        if self._pending_typewriter_lines:
            self._typewriter_timer += dt
            while self._pending_typewriter_lines and self._typewriter_timer >= self._typewriter_interval:
                self._typewriter_timer -= self._typewriter_interval
                surf, kind = self._pending_typewriter_lines.popleft()
                self._lines.append((surf, kind))
                if self._scroll_offset > 0:
                    self._scroll_offset += 1
                    max_scroll = max(0, len(self._lines) - self._visible_lines_count)
                    self._scroll_offset = min(self._scroll_offset, max_scroll)

    def push_message(self, speaker: str, text: str, kind: str = "narration") -> None:
        """
        Recebe a mensagem, aplica Word-wrap e assa as linhas no TextCache.
        Custo por evento de chegada, zero custo em draw().
        """
        if not text:
            return

        font = AssetManager.get_font(self._font_size, bold=False)

        # Mapeamento de cor por tipo de narrativa
        color_map = {
            "narration": Palette.PARCHMENT,
            "player": Palette.GOLD_HI,
            "combat": (230, 160, 120),
            "damage": Palette.BLOOD,
            "dice": Palette.GOLD_HI,
            "system": (170, 195, 220),
        }
        text_color = color_map.get(kind, Palette.PARCHMENT)

        # Largura útil para quebra de linha (descontando espaço da scrollbar)
        usable_w = self.rect.w - 14

        paragraphs = str(text).split("\n")
        wrapped_lines: list[str] = []

        for idx, paragraph in enumerate(paragraphs):
            p_text = f"{speaker}: {paragraph}" if (idx == 0 and speaker) else paragraph
            if not p_text.strip():
                wrapped_lines.append("")
                continue

            words = p_text.split(" ")
            current_line = ""
            for word in words:
                if not word:
                    continue
                test_line = f"{current_line} {word}".strip() if current_line else word
                w, _ = font.size(test_line)
                if w <= usable_w:
                    current_line = test_line
                else:
                    if current_line:
                        wrapped_lines.append(current_line)
                    current_line = word

            if current_line:
                wrapped_lines.append(current_line)

        # Renderiza e armazena cada linha com sombra
        new_surfs: list[tuple[pygame.Surface, str]] = []
        for line_str in wrapped_lines:
            render_str = line_str if line_str else " "
            surf = default_text_cache.get(
                render_str,
                font,
                color=text_color,
                shadow=True,
                shadow_color=Palette.INK,
                shadow_offset=(1, 1),
            )
            new_surfs.append((surf, kind))

        if kind == "narration":
            # Narração do Mestre entra na fila do typewriter para digitação suave
            for item in new_surfs:
                self._pending_typewriter_lines.append(item)
        else:
            # Mensagens de combate/dados/jogador descarregam pendências e aparecem imediatamente
            self.flush_typewriter()
            for item in new_surfs:
                self._lines.append(item)
            if self._scroll_offset > 0:
                self._scroll_offset += len(new_surfs)
                max_scroll = max(0, len(self._lines) - self._visible_lines_count)
                self._scroll_offset = min(self._scroll_offset, max_scroll)
            else:
                self._scroll_offset = 0

    def handle_event(self, event: pygame.event.Event) -> str:
        if not (self.visible and self.enabled):
            return ""

        # Clique no log descarrega digitação do typewriter imediatamente
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self._pending_typewriter_lines:
                self.flush_typewriter()
                return CONSUMED

        # Rolagem da roda do mouse (MOUSEWHEEL)
        if event.type == pygame.MOUSEWHEEL:
            total = len(self._lines)
            max_scroll = max(0, total - self._visible_lines_count)

            if event.y > 0:  # Rola para cima (mensagens antigas)
                self._scroll_offset = min(max_scroll, self._scroll_offset + 3)
            elif event.y < 0:  # Rola para baixo (mensagens novas)
                self._scroll_offset = max(0, self._scroll_offset - 3)

            return CONSUMED

        return super().handle_event(event)

    def _draw_self(self, surface: pygame.Surface) -> None:
        total = len(self._lines)
        if total == 0:
            return

        # Define recorte (clip) para evitar vazamento fora do retângulo do log
        prev_clip = surface.get_clip()
        surface.set_clip(self.rect)

        # Calcula fatia de linhas visíveis
        end_idx = total - self._scroll_offset
        start_idx = max(0, end_idx - self._visible_lines_count)

        visible_slice = list(self._lines)[start_idx:end_idx]

        cur_y = self.rect.y + 2
        for surf, _ in visible_slice:
            surface.blit(surf, (self.rect.x + 2, cur_y))
            cur_y += self.LINE_H

        # Restaura clip
        surface.set_clip(prev_clip)

        # Desenha scrollbar dourada sutil se houver overflow
        if total > self._visible_lines_count:
            bar_x = self.rect.right - 5
            bar_y = self.rect.y
            bar_h = self.rect.h
            # Trilha
            pygame.draw.line(surface, (40, 32, 24), (bar_x, bar_y), (bar_x, bar_y + bar_h), 2)

            # Thumb (indicador móvel)
            ratio = self._visible_lines_count / total
            thumb_h = max(14, round(bar_h * ratio))
            max_scroll = max(1, total - self._visible_lines_count)
            scroll_pct = 1.0 - (self._scroll_offset / max_scroll)
            thumb_y = bar_y + round((bar_h - thumb_h) * scroll_pct)

            pygame.draw.line(surface, Palette.GOLD, (bar_x, thumb_y), (bar_x, thumb_y + thumb_h), 2)


class ChatInputField(UIWidget):
    """
    Campo interativo de entrada de texto para interação narrativa com o Maelor.
    Suporte nativo a TEXTINPUT, acentos, cursor piscante, histórico e retorno say:<texto>.
    """

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect):
        super().__init__(rect)
        self.text: str = ""
        self.has_focus: bool = False
        self.is_busy: bool = False

        self._cursor_visible: bool = True
        self._cursor_timer: float = 0.0

        # Histórico de mensagens enviadas
        self._history: list[str] = []
        self._history_idx: int = -1

        # Caches pré-renderizados
        self._rendered_text: str = ""
        self._text_surf: Optional[pygame.Surface] = None
        self._placeholder_surf: Optional[pygame.Surface] = None
        self._busy_surf: Optional[pygame.Surface] = None

    def set_busy(self, busy: bool) -> None:
        """Indica se a IA/Maelor está processando narração, bloqueando input temporariamente."""
        if busy != self.is_busy:
            self.is_busy = busy
            self.invalidate()

    def update(self, dt: float) -> None:
        super().update(dt)

        # Alternância do cursor piscante a cada 500ms
        self._cursor_timer += dt
        if self._cursor_timer >= 0.5:
            self._cursor_timer = 0.0
            self._cursor_visible = not self._cursor_visible

    def _rebuild(self) -> None:
        """Gera superfícies cacheadas de texto e placeholders."""
        font = AssetManager.get_font(13, bold=False)

        # Placeholder quando vazio
        self._placeholder_surf = default_text_cache.get(
            "> Descreva sua acao ou fale com Maelor...",
            font,
            color=Palette.PARCH_DIM,
        )

        # Mensagem de ocupado
        self._busy_surf = default_text_cache.get(
            "Maelor esta narrando...",
            font,
            color=Palette.GOLD_HI,
        )

        # Texto atualmente digitado
        if self.text:
            self._text_surf = default_text_cache.get(
                self.text,
                font,
                color=Palette.WHITE,
                shadow=True,
                shadow_color=Palette.INK,
            )
        else:
            self._text_surf = None

        self._rendered_text = self.text

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.visible:
            return ""

        # Clique do mouse define ganho ou perda de foco
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if not self.has_focus:
                    self.has_focus = True
                    pygame.key.start_text_input()
                return CONSUMED
            else:
                if self.has_focus:
                    self.has_focus = False
                    pygame.key.stop_text_input()

        if not self.has_focus or self.is_busy:
            return ""

        # Entrada nativa de texto com caracteres acentuados
        if event.type == pygame.TEXTINPUT:
            self.text += event.text
            self.invalidate()
            return CONSUMED

        # Teclas especiais de edição e navegação
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]
                    self.invalidate()
                return CONSUMED

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                msg = self.text.strip()
                if msg:
                    self._history.append(msg)
                    self._history_idx = -1
                    self.text = ""
                    self.invalidate()
                    return f"say:{msg}"
                return CONSUMED

            elif event.key == pygame.K_UP:
                # Navega para trás no histórico
                if self._history:
                    if self._history_idx == -1:
                        self._history_idx = len(self._history) - 1
                    elif self._history_idx > 0:
                        self._history_idx -= 1
                    self.text = self._history[self._history_idx]
                    self.invalidate()
                return CONSUMED

            elif event.key == pygame.K_DOWN:
                # Navega para frente no histórico
                if self._history and self._history_idx != -1:
                    if self._history_idx < len(self._history) - 1:
                        self._history_idx += 1
                        self.text = self._history[self._history_idx]
                    else:
                        self._history_idx = -1
                        self.text = ""
                    self.invalidate()
                return CONSUMED

            elif event.key == pygame.K_ESCAPE:
                self.has_focus = False
                pygame.key.stop_text_input()
                return CONSUMED

        return super().handle_event(event)

    def _draw_self(self, surface: pygame.Surface) -> None:
        # Fundo do campo
        pygame.draw.rect(surface, (16, 12, 10), self.rect, border_radius=3)

        # Borda dourada se focado, bronze se inativo
        border_col = Palette.GOLD if self.has_focus else Palette.BRONZE
        pygame.draw.rect(surface, border_col, self.rect, width=1, border_radius=3)

        text_x = self.rect.x + 8
        text_y = self.rect.y + (self.rect.h - 16) // 2

        if self.is_busy:
            if self._busy_surf:
                surface.blit(self._busy_surf, (text_x, text_y))
        elif self.text and self._text_surf:
            surface.blit(self._text_surf, (text_x, text_y))
            # Cursor de digitação (fill in-place sem alocação)
            if self.has_focus and self._cursor_visible:
                cx = text_x + self._text_surf.get_width() + 1
                cursor_rect = pygame.Rect(cx, text_y, 2, 16)
                surface.fill(Palette.GOLD_HI, cursor_rect)
        else:
            if self._placeholder_surf:
                surface.blit(self._placeholder_surf, (text_x, text_y))
            if self.has_focus and self._cursor_visible:
                cursor_rect = pygame.Rect(text_x, text_y, 2, 16)
                surface.fill(Palette.GOLD_HI, cursor_rect)


class ChatConsoleWidget(UIWidget):
    """
    Bloco B3 do HUD: Console Narrativo (1280x720).
    Localizado em Rect(12, 372, 456, 336).
    Composto por cabeçalho gótico com mini-retrato do Maelor, visualizador de
    narrativa (NarrativeLogView) e linha de comando (ChatInputField).
    """

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect = Layout.CHAT_CONSOLE):
        super().__init__(rect)

        # Superfície estática de fundo e cabeçalho
        self._static: Optional[pygame.Surface] = None

        # Filhos internos
        log_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 32, self.rect.w - 20, 250)
        self.log: NarrativeLogView = NarrativeLogView(log_rect)

        input_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 292, self.rect.w - 20, 34)
        self.input: ChatInputField = ChatInputField(input_rect)

        self.add_child(self.log)
        self.add_child(self.input)

    @property
    def has_focus(self) -> bool:
        """Indica se o jogador está com o campo de digitação focado (suspende hotkeys)."""
        return self.input.has_focus

    def push_message(self, speaker: str, text: str, kind: str = "narration") -> None:
        """Adiciona uma nova mensagem de prosa ou sistema ao log narrativo."""
        self.log.push_message(speaker, text, kind)

    def set_busy(self, busy: bool) -> None:
        """Altera status de ocupado do narrador."""
        self.input.set_busy(busy)

    def _rebuild(self) -> None:
        """Assa o painel de moldura gótica e o cabeçalho decorado."""
        w, h = self.rect.w, self.rect.h
        self._static = FrameFactory.panel((w, h), style="gothic").copy()

        # Cabeçalho decorado (h=28 px)
        header_h = 28

        # Mini-retrato do Maelor em (10, 4)
        portrait_raw = None
        try:
            portrait_raw = AssetManager.get_portrait("maelor", size=(22, 22))
        except Exception:
            portrait_raw = None

        if portrait_raw is not None:
            scaled = pygame.transform.smoothscale(portrait_raw, (22, 22))
            self._static.blit(scaled, (10, 3))
            pygame.draw.rect(self._static, Palette.GOLD, (10, 3, 22, 22), width=1)
        else:
            # Ícone alternativo de fala / olho
            icon = FrameFactory.chamfer_mask((22, 22), cut=3)
            pygame.draw.rect(self._static, (30, 22, 16), (10, 3, 22, 22))
            pygame.draw.rect(self._static, Palette.GOLD, (10, 3, 22, 22), width=1)

        # Título "Crônica da Mesa"
        font_header = AssetManager.get_font(13, bold=True)
        header_title = default_text_cache.get(
            "Cronica da Mesa - Maelor",
            font_header,
            color=Palette.GOLD_HI,
            shadow=True,
            shadow_color=Palette.INK,
        )
        self._static.blit(header_title, (38, 7))

        # Divisor sutil abaixo do cabeçalho
        pygame.draw.line(self._static, Palette.BRONZE, (10, header_h), (w - 10, header_h), 1)

    def _draw_self(self, surface: pygame.Surface) -> None:
        """Zero garbage: 1 blit da moldura estática assada."""
        if self._static:
            surface.blit(self._static, self.rect.topleft)
