"""
Orquestrador Raiz do HUD In-Game (RPGMesaPY).
Fase 6 do Redesign UI/UX — Contrato Zero Garbage por Frame.
Orquestra os 5 blocos do HUD:
- B1: Player Card (PlayerCardWidget)
- B2: Fita de Iniciativa / Plaqueta de Localização (InitiativeBannerWidget)
- B3: Console Narrativo e Chat (ChatConsoleWidget)
- B4: Hotbar Tática, Flyouts e Faixa de Economia (TacticalActionBarWidget)
- B5: System Dock (SystemDockWidget)
- Singleton de Tooltip (TooltipWidget)
"""

from typing import Optional, Any
import pygame
from ..theme import Layout
from ..base import UIWidget, TooltipWidget, CONSUMED
from .player_card import PlayerCardWidget
from .initiative_banner import InitiativeBannerWidget, InitiativeEntry
from .chat_console import ChatConsoleWidget
from .action_bar import TacticalActionBarWidget, BarMode
from .system_dock import SystemDockWidget


class InGameHUD(UIWidget):
    """
    Controlador raiz que agrega e sincroniza todos os módulos visuais do HUD in-game.
    Gerencia z-order de eventos, roteamento inteligente de teclado e exibição de tooltips.
    """

    def __init__(self):
        super().__init__((0, 0, Layout.W, Layout.H))

        # Inst instanciação dos 5 blocos canônicos
        self.player_card: PlayerCardWidget = PlayerCardWidget()
        self.initiative: InitiativeBannerWidget = InitiativeBannerWidget()
        self.console: ChatConsoleWidget = ChatConsoleWidget()
        self.action_bar: TacticalActionBarWidget = TacticalActionBarWidget()
        self.dock: SystemDockWidget = SystemDockWidget()

        # Tooltip como camada superior de renderização
        self.tooltip: TooltipWidget = TooltipWidget()

        # Z-order de desenho: base widgets registrados como filhos
        self.children = [
            self.player_card,
            self.initiative,
            self.console,
            self.action_bar,
            self.dock,
        ]

    def push_narration(self, speaker: str, text: str, kind: str = "narration") -> None:
        """Envia mensagem ao console narrativo do Maelor."""
        self.console.push_message(speaker, text, kind)

    def sync(self, session: Any) -> None:
        """
        Lê game_state/session uma vez por frame e repassa escalares aos subcomponentes.
        Zero Garbage: Apenas comparações escalares.
        """
        if not session:
            return

        game_state = getattr(session, "game_state", {}) or {}

        # 1. Player Card
        player = game_state.get("player_character") or getattr(session, "player", None) or getattr(session, "character", None)
        if isinstance(player, dict):
            self.player_card.sync(player)
        elif hasattr(player, "__dict__"):
            self.player_card.sync(player.__dict__)

        # 2. Modo Combate vs Exploração
        in_combat = (getattr(session, "game_mode", "") == "COMBATE") or bool(getattr(session, "active_combat_targets", None))
        if in_combat:
            entries: list[InitiativeEntry] = []

            # Herói como participante
            p_dict = player if isinstance(player, dict) else (player.__dict__ if hasattr(player, "__dict__") else {})
            p_name = str(p_dict.get("name") or p_dict.get("nome") or "Herói")
            p_hp = int(p_dict.get("hp_current", p_dict.get("hp", p_dict.get("pv_atual", 10))))
            p_hp_max = max(1, int(p_dict.get("hp_max", p_dict.get("pv_max", 10))))
            p_init = int(p_dict.get("initiative", 12))
            p_portrait = str(p_dict.get("race") or p_dict.get("class") or "Humano")
            entries.append(InitiativeEntry(
                uid="player",
                name=p_name,
                faction="hero",
                initiative=p_init,
                hp=p_hp,
                hp_max=p_hp_max,
                portrait_key=p_portrait
            ))

            # Inimigos de session.active_combat_targets
            targets = getattr(session, "active_combat_targets", {}) or {}
            if isinstance(targets, dict):
                for uid, target in targets.items():
                    if isinstance(target, dict):
                        if target.get("status") == "morto":
                            continue
                        t_name = str(target.get("name") or uid)
                        t_faction = str(target.get("faction") or "enemy")
                        t_hp = int(target.get("hp_current", target.get("hp", target.get("pv_atual", 10))))
                        t_hp_max = max(1, int(target.get("hp_max", target.get("pv_max", 10))))
                        t_init = int(target.get("initiative", 10))
                        t_port = str(target.get("portrait_key") or target.get("sprite_key") or target.get("id") or uid)
                        entries.append(InitiativeEntry(
                            uid=str(uid),
                            name=t_name,
                            faction=t_faction,
                            initiative=t_init,
                            hp=t_hp,
                            hp_max=t_hp_max,
                            portrait_key=t_port
                        ))

            # Ordena por iniciativa decrescente
            entries.sort(key=lambda e: e.initiative, reverse=True)

            active_uid = str(getattr(session, "active_combatant_id", "") or "player")
            round_no = int(getattr(session, "round_number", getattr(session, "combat_turn", 1)) or 1)

            self.initiative.set_combat(True)
            self.initiative.set_order(entries, active_uid, round_no)
            self.action_bar.set_mode(BarMode.COMBAT)
        else:
            self.initiative.set_combat(False)
            beat = game_state.get("story_beat", 1)
            story = getattr(session, "story", None)
            camp_data = getattr(story, "campaign_data", {}) if story else {}
            beat_info = camp_data.get(str(beat), {}) if isinstance(camp_data, dict) else {}
            loc = str(beat_info.get("name", "Taverna do Dragão Acordado"))
            day = int(game_state.get("current_day", 1))
            self.initiative.set_location_time(loc, f"Dia {day}, Noite")
            self.action_bar.set_mode(BarMode.EXPLORATION)

        # 3. Alvo Selecionado
        target_name = getattr(session, "selected_target_name", None)
        self.action_bar.set_target(target_name)

        # 4. Faixa de Economia 5E
        action_avail = bool(getattr(session, "action_available", True))
        bonus_avail = bool(getattr(session, "bonus_action_available", True))
        move_ft = int(getattr(session, "movement_available_ft", 30))
        reaction_avail = bool(getattr(session, "reaction_available", True))
        self.action_bar.set_economy(action_avail, bonus_avail, move_ft, reaction_avail)

    def handle_event(self, event: pygame.event.Event) -> str:
        if not (self.visible and self.enabled):
            return ""

        # 1. Se o Console Narrativo está em foco digitando:
        # Suspende as hotkeys de combate e do dock para não disparar ações
        if self.console.has_focus:
            if event.type == pygame.KEYDOWN:
                # O chat consome as teclas de digitação
                chat_action = self.console.handle_event(event)
                return chat_action

        # 2. Roteamento de eventos na ordem inversa de z-order:
        # Dock -> Action Bar (com flyout) -> Console -> Iniciativa -> PlayerCard
        action = super().handle_event(event)

        # 3. Coleta e posicionamento de tooltips dinâmicos
        tooltip_req = (
            self.dock.get_tooltip_request()
            or self.initiative.get_tooltip_request()
            or self.player_card.badges.get_hover_tooltip()
        )

        if tooltip_req:
            txt, anchor = tooltip_req
            self.tooltip.show(txt, anchor)
        else:
            self.tooltip.hide()

        return action

    def update(self, dt: float) -> None:
        super().update(dt)
        self.tooltip.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Desenha os blocos da HUD e o Tooltip sempre no topo de tudo.
        Zero Garbage por frame.
        """
        if not self.visible:
            return

        super().draw(surface)
        self.tooltip.draw(surface)
