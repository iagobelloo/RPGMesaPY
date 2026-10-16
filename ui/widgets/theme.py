"""
Design System, Paleta de Cores e Constantes de Layout.
Parte da Fase 1 do Redesign UI/UX (RPGMesaPY).
"""

from enum import Enum, auto
import pygame


class Palette:
    """Paleta de cores canônica inspirada em Darkest Dungeon / Baldur's Gate 3."""
    INK = (12, 8, 4)
    LEATHER = (24, 18, 14)
    PANEL_BG = (18, 14, 11, 224)
    BRONZE = (110, 80, 42)
    GOLD = (212, 175, 55)
    GOLD_HI = (245, 215, 110)
    PARCHMENT = (225, 210, 180)
    PARCH_DIM = (160, 145, 120)
    BLOOD = (150, 28, 24)
    ALLY = (70, 130, 80)
    DISABLED = (70, 64, 58)

    # Cores utilitárias complementares
    WHITE = (245, 245, 245)
    BLACK = (0, 0, 0)
    PANEL_BORDER = (110, 80, 42)
    PANEL_INNER = (80, 58, 30)
    GOLD_SHADOW = (74, 58, 18)
    TRANSPARENT = (0, 0, 0, 0)


class ButtonState(Enum):
    """Estados interativos de botões e seletores da UI."""
    IDLE = auto()
    HOVER = auto()
    PRESSED = auto()
    DISABLED = auto()


class Layout:
    """Constantes canônicas de resolução 1280x720 e geometria da interface."""
    W: int = 1280
    H: int = 720
    M: int = 12

    # Menu Principal
    MENU_TITLE_CY: int = 150
    MENU_DIVIDER_Y: int = 192
    MENU_SUB_CY: int = 222
    MENU_FRAME: pygame.Rect = pygame.Rect(452, 280, 376, 312)
    MENU_BTN: tuple[int, int] = (312, 50)
    MENU_BTN_Y: tuple[int, int, int, int] = (312, 374, 436, 510)

    # HUD In-Game
    PLAYER_CARD: pygame.Rect = pygame.Rect(12, 12, 312, 116)
    INITIATIVE: pygame.Rect = pygame.Rect(400, 10, 480, 60)
    SYSTEM_DOCK: pygame.Rect = pygame.Rect(1120, 12, 148, 48)
    CHAT_CONSOLE: pygame.Rect = pygame.Rect(12, 372, 456, 336)
    STAGE_CX: int = 874
    BAR_Y: int = 640
    BAR_H: int = 68
    SLOT: tuple[int, int] = (104, 52)
    SLOT_WIDE: tuple[int, int] = (152, 52)
    GAP: int = 8
    PAD: int = 10
    TOKEN_FEET_Y: int = 560
    NAMEPLATE: tuple[int, int] = (120, 26)
    NAMEPLATE_DY: int = 14
