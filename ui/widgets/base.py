"""
Widgets Base do Sistema de Interface UI/UX.
Parte da Fase 1 do Redesign UI/UX (RPGMesaPY).
Contrato Zero Garbage por Frame:
- Nenhuma alocação em draw().
- Textos e superfícies alocados apenas em _rebuild() acionado por _dirty.
- Eventos processados em ordem inversa de z-order.
"""

from typing import Optional
import pygame
from ui.asset_manager import AssetManager
from .theme import Palette, ButtonState, Layout
from .render_cache import FrameFactory, IconAtlas, default_text_cache

# Sentinela de evento consumido pela UI sem disparar ação direta de jogo
CONSUMED = "__consumed__"


class UIWidget:
    """
    Classe base hierárquica para todos os componentes de interface.
    Gerencia geometria, visibilidade, habilitação, filhos e ciclo dirty/rebuild.
    """

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect):
        self.rect: pygame.Rect = pygame.Rect(rect)
        self.visible: bool = True
        self.enabled: bool = True
        self.children: list["UIWidget"] = []
        self._dirty: bool = True

    @property
    def is_visible(self) -> bool:
        return self.visible

    @is_visible.setter
    def is_visible(self, val: bool) -> None:
        self.visible = val

    def invalidate(self) -> None:
        """Marca o widget para reconstrução gráfica no próximo update()."""
        self._dirty = True

    def add_child(self, child: "UIWidget") -> "UIWidget":
        """Adiciona um widget filho à hierarquia."""
        if child not in self.children:
            self.children.append(child)
        return child

    def remove_child(self, child: "UIWidget") -> None:
        """Remove um widget filho da hierarquia."""
        if child in self.children:
            self.children.remove(child)

    def _rebuild(self) -> None:
        """
        Único ponto do ciclo de vida autorizado a alocar Surfaces e renderizar textos.
        Sobrescrito por subclasses.
        """
        pass

    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Propaga o evento pela árvore na ordem inversa dos filhos (topo do z-order primeiro).
        Retorna string de ação ou CONSUMED.
        """
        if not (self.visible and self.enabled):
            return ""

        for child in reversed(self.children):
            action = child.handle_event(event)
            if action:
                return action

        return ""

    def update(self, dt: float) -> None:
        """
        Atualiza o ciclo de vida do widget e dos filhos.
        Reconstrói recursos estáticos se a flag _dirty estiver ativa.
        """
        if self._dirty:
            self._rebuild()
            self._dirty = False

        for child in self.children:
            child.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Desenha o widget e todos os filhos visíveis.
        NUNCA aloca Surfaces ou chama font.render aqui.
        """
        if not self.visible:
            return

        self._draw_self(surface)

        for child in self.children:
            child.draw(surface)

    def _draw_self(self, surface: pygame.Surface) -> None:
        """
        Desenha a representação visual própria deste widget.
        Apenas blits de superfícies pré-renderizadas e preenchimentos diretos.
        """
        pass


class UIButton(UIWidget):
    """
    Botão interativo gótico com estados visuais completos, suporte a ícone,
    sub-rótulo, atalho de teclado e clique cancelável.
    """

    def __init__(
        self,
        rect: tuple[int, int, int, int] | pygame.Rect,
        label: str,
        action_id: str,
        *,
        variant: str = "menu",
        icon: Optional[str] = None,
        sublabel: Optional[str] = None,
        hotkey: Optional[int] = None,
        tooltip: Optional[str] = None,
        font_size: int = 16,
    ):
        super().__init__(rect)
        self.label: str = label
        self.action_id: str = action_id
        self.variant: str = variant
        self.icon_name: Optional[str] = icon
        self.sublabel: Optional[str] = sublabel
        self.hotkey: Optional[int] = hotkey
        self.tooltip: Optional[str] = tooltip
        self.font_size: int = font_size

        self.state: ButtonState = ButtonState.IDLE
        self._pressed_inside: bool = False

        # Caches pré-renderizados
        self._frames: dict[ButtonState, pygame.Surface] = {}
        self._label_surfs: dict[ButtonState, pygame.Surface] = {}
        self._sublabel_surfs: dict[ButtonState, pygame.Surface] = {}
        self._icon_surfs: dict[ButtonState, pygame.Surface] = {}
        self._hotkey_surf: Optional[pygame.Surface] = None

        # Posições relativas pré-calculadas (Zero Garbage)
        self._label_pos: tuple[int, int] = (0, 0)
        self._sublabel_pos: tuple[int, int] = (0, 0)
        self._icon_pos: tuple[int, int] = (0, 0)
        self._hotkey_pos: tuple[int, int] = (0, 0)

    def set_label(self, label: str, sublabel: Optional[str] = None) -> None:
        """Atualiza rótulos e invalida cache apenas se houver mudança de valor."""
        if label != self.label or sublabel != self.sublabel:
            self.label = label
            self.sublabel = sublabel
            self.invalidate()

    def set_enabled(self, enabled: bool) -> None:
        """Altera habilitação do botão e estado visual sem alocações desnecessárias."""
        if enabled != self.enabled:
            self.enabled = enabled
            self.state = ButtonState.IDLE if enabled else ButtonState.DISABLED
            self.invalidate()

    def get_tooltip_request(self) -> Optional[tuple[str, pygame.Rect]]:
        """Retorna texto do tooltip e âncora se estiver com hover ativo."""
        if self.visible and self.enabled and self.state == ButtonState.HOVER and self.tooltip:
            return (self.tooltip, self.rect)
        return None

    def _rebuild(self) -> None:
        """Pré-renderiza molduras, textos por estado e posicionamentos relativos."""
        w, h = self.rect.w, self.rect.h
        self._frames = FrameFactory.button_states((w, h), variant=self.variant)

        font = AssetManager.get_font(self.font_size, bold=True)
        sub_font = AssetManager.get_font(max(10, self.font_size - 4), bold=False)
        hotkey_font = AssetManager.get_font(max(9, self.font_size - 6), bold=True)

        # Paleta de cores do rótulo por estado
        color_map = {
            ButtonState.IDLE: Palette.PARCH_DIM,
            ButtonState.HOVER: Palette.GOLD_HI,
            ButtonState.PRESSED: Palette.GOLD,
            ButtonState.DISABLED: Palette.DISABLED,
        }

        self._label_surfs.clear()
        self._sublabel_surfs.clear()
        self._icon_surfs.clear()

        # Renderiza textos para cada estado via TextCache
        for st, col in color_map.items():
            shadow = (st != ButtonState.DISABLED)
            self._label_surfs[st] = default_text_cache.get(
                self.label,
                font,
                color=col,
                shadow=shadow,
                shadow_color=Palette.INK,
                shadow_offset=(1, 1),
            )
            if self.sublabel:
                sub_col = Palette.PARCH_DIM if st != ButtonState.DISABLED else Palette.DISABLED
                self._sublabel_surfs[st] = default_text_cache.get(
                    self.sublabel,
                    sub_font,
                    color=sub_col,
                    shadow=shadow,
                    shadow_color=Palette.INK,
                    shadow_offset=(1, 1),
                )
            if self.icon_name:
                icon_sz = min(24, max(14, h - 16))
                self._icon_surfs[st] = IconAtlas.get(self.icon_name, size=icon_sz, color=col)

        # Hotkey badge sutil
        if self.hotkey is not None:
            key_name = pygame.key.name(self.hotkey).upper()
            if len(key_name) == 1 or key_name in ("ESC", "TAB", "SPACE"):
                self._hotkey_surf = default_text_cache.get(
                    key_name,
                    hotkey_font,
                    color=Palette.GOLD_HI,
                    shadow=True,
                    shadow_color=Palette.INK,
                )
            else:
                self._hotkey_surf = None
        else:
            self._hotkey_surf = None

        # Cálculo de layout interno
        lbl_surf = self._label_surfs.get(ButtonState.IDLE)
        lbl_w = lbl_surf.get_width() if lbl_surf else 0
        lbl_h = lbl_surf.get_height() if lbl_surf else 0

        icon_surf = self._icon_surfs.get(ButtonState.IDLE)
        icon_w = icon_surf.get_width() if icon_surf else 0
        icon_h = icon_surf.get_height() if icon_surf else 0

        sub_surf = self._sublabel_surfs.get(ButtonState.IDLE)
        sub_w = sub_surf.get_width() if sub_surf else 0
        sub_h = sub_surf.get_height() if sub_surf else 0

        gap = 6
        if self.sublabel and sub_surf:
            # Layout vertical com sublabel
            total_content_w = max(lbl_w, sub_w)
            if icon_surf:
                total_content_w += icon_w + gap

            content_start_x = (w - total_content_w) // 2
            total_content_h = lbl_h + sub_h + 2
            content_start_y = (h - total_content_h) // 2

            if icon_surf:
                self._icon_pos = (content_start_x, (h - icon_h) // 2)
                text_x = content_start_x + icon_w + gap
            else:
                text_x = (w - lbl_w) // 2

            self._label_pos = (text_x, content_start_y)
            self._sublabel_pos = (text_x, content_start_y + lbl_h + 1)
        else:
            # Layout horizontal padrão
            total_content_w = lbl_w + (icon_w + gap if icon_surf else 0)
            content_start_x = (w - total_content_w) // 2

            if icon_surf:
                self._icon_pos = (content_start_x, (h - icon_h) // 2)
                self._label_pos = (content_start_x + icon_w + gap, (h - lbl_h) // 2)
            else:
                self._label_pos = ((w - lbl_w) // 2, (h - lbl_h) // 2)

        if self._hotkey_surf:
            self._hotkey_pos = (w - self._hotkey_surf.get_width() - 6, 4)

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.visible:
            return ""

        # Botão desabilitado consome cliques para não repassar ao palco atrás
        if not self.enabled:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return CONSUMED
            return ""

        # Movimento do mouse -> atualiza HOVER / IDLE
        if event.type == pygame.MOUSEMOTION:
            is_inside = self.rect.collidepoint(event.pos)
            if is_inside:
                if self.state != ButtonState.PRESSED:
                    self.state = ButtonState.HOVER
            else:
                if self.state == ButtonState.HOVER:
                    self.state = ButtonState.IDLE
                elif self.state == ButtonState.PRESSED and not self._pressed_inside:
                    self.state = ButtonState.IDLE
            return ""

        # MOUSEBUTTONDOWN -> inicia clique cancelável
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = ButtonState.PRESSED
                self._pressed_inside = True
                return CONSUMED

        # MOUSEBUTTONUP -> finaliza clique com cancelamento se solto fora
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._pressed_inside:
                self._pressed_inside = False
                if self.rect.collidepoint(event.pos):
                    self.state = ButtonState.HOVER
                    return self.action_id
                else:
                    self.state = ButtonState.IDLE
                    return CONSUMED

        # KEYDOWN -> disparo de hotkey
        if event.type == pygame.KEYDOWN and self.hotkey is not None:
            if event.key == self.hotkey:
                return self.action_id

        return super().handle_event(event)

    def _draw_self(self, surface: pygame.Surface) -> None:
        frame = self._frames.get(self.state, self._frames.get(ButtonState.IDLE))
        if frame:
            surface.blit(frame, self.rect.topleft)

        # Deslocamento tátil de 1 px para baixo no estado PRESSED
        dy = 1 if self.state == ButtonState.PRESSED else 0

        bx, by = self.rect.x, self.rect.y + dy

        # Ícone
        icon_surf = self._icon_surfs.get(self.state)
        if icon_surf:
            surface.blit(icon_surf, (bx + self._icon_pos[0], by + self._icon_pos[1]))

        # Rótulo principal
        label_surf = self._label_surfs.get(self.state)
        if label_surf:
            surface.blit(label_surf, (bx + self._label_pos[0], by + self._label_pos[1]))

        # Sub-rótulo
        if self.sublabel:
            sub_surf = self._sublabel_surfs.get(self.state)
            if sub_surf:
                surface.blit(sub_surf, (bx + self._sublabel_pos[0], by + self._sublabel_pos[1]))

        # Hotkey badge
        if self._hotkey_surf:
            surface.blit(self._hotkey_surf, (bx + self._hotkey_pos[0], by + self._hotkey_pos[1]))


class TooltipWidget(UIWidget):
    """
    Widget de tooltip estilizado com clamping na tela de 1280x720.
    Reconstrói a superfície apenas quando o conteúdo de texto é alterado.
    """

    def __init__(self, font_size: int = 14):
        super().__init__((0, 0, 0, 0))
        self.visible: bool = False
        self.text: str = ""
        self._last_rendered_text: str = ""
        self.font_size: int = font_size
        self._surf: Optional[pygame.Surface] = None

    def show(self, text: str, anchor: pygame.Rect) -> None:
        """Exibe o tooltip com texto formatado e posicionado em relação à âncora."""
        if not text:
            self.hide()
            return

        self.text = text
        self.visible = True

        if self.text != self._last_rendered_text:
            self._last_rendered_text = self.text
            self.invalidate()

        # Calcula dimensões necessárias para posicionamento com clamping
        font = AssetManager.get_font(self.font_size)
        lines = self.text.split("\n")
        max_line_w = max(font.size(l)[0] for l in lines) if lines else 20
        line_h = font.get_linesize() or (self.font_size + 4)
        total_h = len(lines) * line_h + 14
        total_w = max(60, max_line_w + 16)

        # Posicionamento inteligente: preferencialmente acima da âncora
        x = anchor.centerx - total_w // 2
        y = anchor.top - total_h - 6

        # Inverte para baixo se estourar o topo
        if y < 4:
            y = anchor.bottom + 6

        # Clamping nos limites 1280x720
        if x < 4:
            x = 4
        elif x + total_w > Layout.W - 4:
            x = Layout.W - 4 - total_w

        if y + total_h > Layout.H - 4:
            y = Layout.H - 4 - total_h

        if self.rect.w != total_w or self.rect.h != total_h:
            self.invalidate()

        self.rect.x = x
        self.rect.y = y
        self.rect.w = total_w
        self.rect.h = total_h

    def hide(self) -> None:
        """Oculta o tooltip."""
        self.visible = False

    def _rebuild(self) -> None:
        """Renderiza o painel de tooltip e o texto cacheado."""
        if not self.text or self.rect.w <= 0 or self.rect.h <= 0:
            self._surf = None
            return

        w, h = self.rect.w, self.rect.h
        self._surf = FrameFactory.panel((w, h), style="tooltip")

        font = AssetManager.get_font(self.font_size)
        lines = self.text.split("\n")
        line_h = font.get_linesize() or (self.font_size + 4)

        cur_y = 7
        for line in lines:
            line_surf = default_text_cache.get(
                line,
                font,
                color=Palette.PARCHMENT,
                shadow=True,
                shadow_color=Palette.INK,
                shadow_offset=(1, 1),
            )
            self._surf.blit(line_surf, (8, cur_y))
            cur_y += line_h

    def _draw_self(self, surface: pygame.Surface) -> None:
        if self.visible and self._surf:
            surface.blit(self._surf, self.rect.topleft)
