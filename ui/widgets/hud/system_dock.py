"""
System Dock Widget (RPGMesaPY).
Fase 3 do Redesign UI/UX — Contrato Zero Garbage por Frame.
Bloco B5 do HUD: Rect(1120, 12, 148, 48).
Contém os botões Mochila (I), Grimório (G) e Menu/Salvar (Esc).
"""

from typing import Optional
import pygame
from ..theme import Layout
from ..render_cache import FrameFactory
from ..base import UIWidget, UIButton


class SystemDockWidget(UIWidget):
    """
    Dock superior direito para atalhos utilitários do sistema.
    3 botões-ícone 44x44 px: Mochila, Grimório e Menu Principal.
    """

    ITEMS: tuple[tuple[str, str, str, int], ...] = (
        ("inventory", "backpack", "Mochila (I)", pygame.K_i),
        ("grimoire", "book", "Grimorio (G)", pygame.K_g),
        ("system_menu", "gear", "Menu / Salvar (Esc)", pygame.K_ESCAPE),
    )

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect = Layout.SYSTEM_DOCK):
        super().__init__(rect)

        self._static_bg: Optional[pygame.Surface] = None
        self.buttons: list[UIButton] = []

        btn_size = 44
        gap = 6
        pad_x = 4
        pad_y = 2

        for i, (action_id, icon_name, tooltip_txt, hotkey_code) in enumerate(self.ITEMS):
            bx = self.rect.x + pad_x + i * (btn_size + gap)
            by = self.rect.y + pad_y
            btn = UIButton(
                rect=(bx, by, btn_size, btn_size),
                label="",
                action_id=action_id,
                variant="dock",
                icon=icon_name,
                hotkey=hotkey_code,
                tooltip=tooltip_txt,
            )
            self.buttons.append(btn)
            self.add_child(btn)

    def get_tooltip_request(self) -> Optional[tuple[str, pygame.Rect]]:
        """Retorna o tooltip ativo do botão que estiver em HOVER."""
        for btn in self.buttons:
            req = btn.get_tooltip_request()
            if req:
                return req
        return None

    def _rebuild(self) -> None:
        """Assa a moldura do painel de dock."""
        self._static_bg = FrameFactory.panel((self.rect.w, self.rect.h), style="gothic")

    def _draw_self(self, surface: pygame.Surface) -> None:
        """Zero garbage: 1 blit da moldura do dock."""
        if self._static_bg:
            surface.blit(self._static_bg, self.rect.topleft)
