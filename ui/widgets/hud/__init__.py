"""
Subpacote de Componentes HUD (RPGMesaPY).
Fases 3 a 6 do Redesign UI/UX:
- B1: Player Card e Condition Badges (player_card.py)
- B2: Fita de Iniciativa e Plaqueta de Localização (initiative_banner.py)
- B3: Console Narrativo e Chat (chat_console.py)
- B4: Hotbar Tática, Flyouts e Faixa de Economia (action_bar.py)
- B5: System Dock (system_dock.py)
- Token Nameplate ancorado nos pés (nameplate.py)
- Orquestrador Raiz InGameHUD (hud_root.py)
"""

from .player_card import PlayerCardWidget, ConditionBadgeStrip, CONDITION_RULES
from .initiative_banner import InitiativeBannerWidget, InitiativeEntry
from .chat_console import NarrativeLogView, ChatInputField, ChatConsoleWidget
from .action_bar import (
    BarMode,
    TacticalActionBarWidget,
    ActionFlyoutWidget,
    ActionEconomyStrip,
    COMBAT_SLOTS,
    EXPLORATION_SLOTS,
)
from .system_dock import SystemDockWidget
from .nameplate import TokenNameplate
from .hud_root import InGameHUD

__all__ = [
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
