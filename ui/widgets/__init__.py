"""
Subpacote de Widgets e Design System UI/UX do RPGMesaPY.
Fases 1 a 6: Infraestrutura, Menu Principal, 5 Blocos do HUD, Nameplates e Orquestrador InGameHUD.
"""

from .theme import Palette, ButtonState, Layout
from .render_cache import TextCache, FrameFactory, IconAtlas, default_text_cache
from .base import CONSUMED, UIWidget, UIButton, TooltipWidget
from .main_menu import MainMenuWidget
from .hud.player_card import PlayerCardWidget, ConditionBadgeStrip, CONDITION_RULES
from .hud.initiative_banner import InitiativeBannerWidget, InitiativeEntry
from .hud.chat_console import NarrativeLogView, ChatInputField, ChatConsoleWidget
from .hud.action_bar import (
    BarMode,
    TacticalActionBarWidget,
    ActionFlyoutWidget,
    ActionEconomyStrip,
    COMBAT_SLOTS,
    EXPLORATION_SLOTS,
)
from .hud.system_dock import SystemDockWidget
from .hud.nameplate import TokenNameplate
from .hud.hud_root import InGameHUD

__all__ = [
    "Palette",
    "ButtonState",
    "Layout",
    "TextCache",
    "FrameFactory",
    "IconAtlas",
    "default_text_cache",
    "CONSUMED",
    "UIWidget",
    "UIButton",
    "TooltipWidget",
    "MainMenuWidget",
    "PlayerCardWidget",
    "ConditionBadgeStrip",
    "CONDITION_RULES",
    "InitiativeBannerWidget",
    "InitiativeEntry",
    "NarrativeLogView",
    "ChatInputField",
    "ChatConsoleWidget",
    "BarMode",
    "TacticalActionBarWidget",
    "ActionFlyoutWidget",
    "ActionEconomyStrip",
    "COMBAT_SLOTS",
    "EXPLORATION_SLOTS",
    "SystemDockWidget",
    "TokenNameplate",
    "InGameHUD",
]
