"""
Menu Principal Gótico (RPGMesaPY).
Fase 2 do Redesign UI/UX — Contrato Zero Garbage por Frame.
Tudo o que é estático é assado em self._static no _rebuild().
"""

from typing import Optional
import pygame
from ui.asset_manager import AssetManager
from .theme import Palette, ButtonState, Layout
from .render_cache import FrameFactory, default_text_cache
from .base import UIWidget, UIButton, CONSUMED


class MainMenuWidget(UIWidget):
    """
    Widget de tela inteira (1280x720) para o Menu Principal.
    Substitui o antigo MainMenuPanel por uma arquitetura cacheada de alta performance.
    """

    TITLE: str = "Crônicas da Taverna"
    SUBTITLE: str = "O Despertar das Cinzas"

    # Definição canônica dos 4 botões e seus Action IDs legados
    ITEMS: tuple[tuple[str, str], ...] = (
        ("Nova Campanha", "action_new_game"),
        ("Carregar Jogo", "action_load_game"),
        ("Manual do Jogador", "action_player_manual"),
        ("Sair", "action_quit"),
    )

    def __init__(self, background: Optional[pygame.Surface] = None):
        super().__init__((0, 0, Layout.W, Layout.H))
        self._background: Optional[pygame.Surface] = background
        self._static: Optional[pygame.Surface] = None
        self._focus_index: int = -1

        btn_w, btn_h = Layout.MENU_BTN
        btn_x = Layout.MENU_FRAME.centerx - btn_w // 2

        self.buttons: list[UIButton] = []
        for (label, action_id), btn_y in zip(self.ITEMS, Layout.MENU_BTN_Y):
            btn = UIButton(
                rect=(btn_x, btn_y, btn_w, btn_h),
                label=label,
                action_id=action_id,
                variant="menu",
                font_size=18,
            )
            self.buttons.append(btn)
            self.add_child(btn)

        # Aliases para compatibilidade retroativa com referências legadas
        self.btn_new_game = self.buttons[0].rect
        self.btn_load_game = self.buttons[1].rect
        self.btn_player_manual = self.buttons[2].rect
        self.btn_quit = self.buttons[3].rect

    def set_background(self, background: Optional[pygame.Surface]) -> None:
        """Define uma nova imagem de fundo e invalida o cache estático."""
        self._background = background
        self.invalidate()

    def _rebuild(self) -> None:
        """
        Assa tudo o que é estático em uma única Surface de 1280x720:
        fundo, vinheta, título dourado, divisor ornamental, subtítulo,
        moldura modal gótica e divisor pontilhado da opção de saída.
        """
        self._static = pygame.Surface((Layout.W, Layout.H))

        # 1. Fundo ou vinheta
        if self._background:
            self._static.blit(self._background, (0, 0))
            # Vinheta escura atmosférica sobre a imagem de fundo
            vignette = pygame.Surface((Layout.W, Layout.H), pygame.SRCALPHA)
            vignette.fill((10, 6, 4, 110))
            self._static.blit(vignette, (0, 0))
        else:
            self._static.fill(Palette.INK)

        # 2. Título "Crônicas da Taverna" (font 56, centro=(640, 150))
        title_font = AssetManager.get_font(56, bold=True)
        title_surf = default_text_cache.get(
            self.TITLE,
            title_font,
            color=Palette.GOLD_HI,
            shadow=True,
            shadow_color=Palette.INK,
            shadow_offset=(2, 2),
        )
        title_x = (Layout.W - title_surf.get_width()) // 2
        title_y = Layout.MENU_TITLE_CY - title_surf.get_height() // 2
        self._static.blit(title_surf, (title_x, title_y))

        # 3. Divisor ornamental gótico com losango central (y=192)
        divider_surf = FrameFactory.ornament_divider(280)
        divider_x = (Layout.W - divider_surf.get_width()) // 2
        divider_y = Layout.MENU_DIVIDER_Y - divider_surf.get_height() // 2
        self._static.blit(divider_surf, (divider_x, divider_y))

        # 4. Subtítulo "O Despertar das Cinzas" (font 22, centro=(640, 222))
        subtitle_font = AssetManager.get_font(22, bold=False)
        subtitle_surf = default_text_cache.get(
            self.SUBTITLE,
            subtitle_font,
            color=Palette.PARCHMENT,
            shadow=True,
            shadow_color=Palette.INK,
            shadow_offset=(1, 1),
        )
        sub_x = (Layout.W - subtitle_surf.get_width()) // 2
        sub_y = Layout.MENU_SUB_CY - subtitle_surf.get_height() // 2
        self._static.blit(subtitle_surf, (sub_x, sub_y))

        # 5. Moldura modal gótica central (Rect(452, 280, 376, 312))
        modal_frame = FrameFactory.panel(
            (Layout.MENU_FRAME.w, Layout.MENU_FRAME.h),
            style="gothic",
        )
        self._static.blit(modal_frame, Layout.MENU_FRAME.topleft)

        # 6. Divisor pontilhado / sutil antes do botão "Sair" (y=498)
        sep_y = 498
        sep_x_start = Layout.MENU_FRAME.x + 36
        sep_x_end = Layout.MENU_FRAME.right - 36
        dash_len = 6
        space_len = 5
        curr_x = sep_x_start
        while curr_x < sep_x_end:
            line_end = min(curr_x + dash_len, sep_x_end)
            pygame.draw.line(self._static, Palette.BRONZE, (curr_x, sep_y), (line_end, sep_y), 1)
            curr_x += dash_len + space_len

    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Navegação por teclado (Cima/Baixo/Enter) e delegação para botões.
        """
        if not (self.visible and self.enabled):
            return ""

        # Navegação por teclado
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self._change_focus(1)
                return CONSUMED
            elif event.key in (pygame.K_UP, pygame.K_w):
                self._change_focus(-1)
                return CONSUMED
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if 0 <= self._focus_index < len(self.buttons):
                    return self.buttons[self._focus_index].action_id

        # Atualiza foco pelo movimento do mouse
        if event.type == pygame.MOUSEMOTION:
            for idx, btn in enumerate(self.buttons):
                if btn.rect.collidepoint(event.pos):
                    if self._focus_index != idx:
                        self._set_focus(idx)
                    break

        # Delega cliques e hovers aos botões
        return super().handle_event(event)

    def _set_focus(self, new_index: int) -> None:
        """Define o foco em um botão específico e atualiza os estados visuais."""
        self._focus_index = new_index
        for idx, btn in enumerate(self.buttons):
            if idx == self._focus_index:
                btn.state = ButtonState.HOVER
            elif btn.state == ButtonState.HOVER:
                btn.state = ButtonState.IDLE

    def _change_focus(self, delta: int) -> None:
        """Avança ou recua o foco entre os botões."""
        n = len(self.buttons)
        if n == 0:
            return
        if self._focus_index == -1:
            new_idx = 0 if delta > 0 else n - 1
        else:
            new_idx = (self._focus_index + delta) % n
        self._set_focus(new_idx)

    def _draw_self(self, surface: pygame.Surface) -> None:
        """Zero garbage: 1 blit da superfície estática assada."""
        if self._static:
            surface.blit(self._static, (0, 0))
