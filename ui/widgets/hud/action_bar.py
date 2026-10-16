"""
Hotbar Tática, Flyouts de Ação e Faixa de Economia 5E (RPGMesaPY).
Fase 5 do Redesign UI/UX — Contrato Zero Garbage por Frame.
Posicionamento centralizado no palco (STAGE_CX = 874, y = 640).
Suporte a COMBAT, LOCKED e EXPLORATION.
Flyouts de Habilidades e Magias abrindo para cima.
"""

from enum import Enum, auto
from typing import Optional, Any
import pygame
from ui.asset_manager import AssetManager
from ..theme import Palette, ButtonState, Layout
from ..render_cache import FrameFactory, IconAtlas, default_text_cache
from ..base import UIWidget, UIButton, CONSUMED


class BarMode(Enum):
    """Modos de operação da Hotbar Tática."""
    COMBAT = auto()
    LOCKED = auto()
    EXPLORATION = auto()


# Definição dos slots canônicos conforme Seção 4.4 do Blueprint
COMBAT_SLOTS = (
    ("attack", "Atacar", "sword", pygame.K_1, True),      # True = slot largo 148x52 + alvo
    ("dodge", "Esquivar", "shield", pygame.K_2, False),    # Slot normal 96x52
    ("disengage", "Recuar", "boot", pygame.K_3, False),
    ("skills", "Habilidades", "lightning", pygame.K_4, False),
    ("spells", "Magias", "sparkle", pygame.K_5, False),
)

EXPLORATION_SLOTS = (
    ("observe", "Observar", "eye", pygame.K_1, False),
    ("talk", "Dialogar", "speech", pygame.K_2, False),
    ("rest", "Descansar", "campfire", pygame.K_3, False),
    ("travel", "Partir", "map", pygame.K_4, False),
)


class ActionEconomyStrip(UIWidget):
    """
    Faixa de economia de ação 5e acima da hotbar (y=616).
    Indica disponibilidade de Ação, Ação Bônus, Movimento e Reação.
    """

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect):
        super().__init__(rect)
        self.action_avail: bool = True
        self.bonus_avail: bool = True
        self.move_ft: int = 30
        self.reaction_avail: bool = True
        self._static: Optional[pygame.Surface] = None

    def set_economy(self, action: bool, bonus: bool, move_ft: int, reaction: bool) -> None:
        """Atualiza a economia de ação comparando apenas escalares primitivos."""
        if (
            action != self.action_avail
            or bonus != self.bonus_avail
            or move_ft != self.move_ft
            or reaction != self.reaction_avail
        ):
            self.action_avail = action
            self.bonus_avail = bonus
            self.move_ft = move_ft
            self.reaction_avail = reaction
            self.invalidate()

    def _rebuild(self) -> None:
        """Assa o painel de economia e os indicadores em uma única Surface."""
        w, h = self.rect.w, self.rect.h
        self._static = pygame.Surface((w, h), pygame.SRCALPHA)
        self._static.fill((16, 12, 10, 220))
        pygame.draw.rect(self._static, Palette.BRONZE, (0, 0, w, h), width=1, border_radius=3)

        font = AssetManager.get_font(11, bold=True)
        cy = h // 2

        items = [
            ("Acao", self.action_avail),
            ("Bonus", self.bonus_avail),
            (f"Mov {self.move_ft // 3}m", self.move_ft > 0),
            ("Reacao", self.reaction_avail),
        ]

        # Distribui os 4 itens horizontalmente
        step_x = w // 4
        for i, (label, active) in enumerate(items):
            ix = i * step_x + step_x // 2
            col = Palette.GOLD_HI if active else (80, 70, 60)
            txt_surf = default_text_cache.get(label, font, color=col)
            # Pip losango
            diamond_pts = [(ix - 32, cy), (ix - 29, cy - 3), (ix - 26, cy), (ix - 29, cy + 3)]
            pygame.draw.polygon(self._static, col, diamond_pts)
            self._static.blit(txt_surf, (ix - 20, cy - txt_surf.get_height() // 2))

    def _draw_self(self, surface: pygame.Surface) -> None:
        if self._static:
            surface.blit(self._static, self.rect.topleft)


class ActionFlyoutWidget(UIWidget):
    """
    Menu popup vertical que abre para CIMA da hotbar (slots de Habilidades e Magias).
    Exibe lista de opções e despacha comandos use_skill e cast_spell.
    """

    def __init__(self):
        super().__init__((0, 0, 300, 220))
        self.visible: bool = False
        self.kind: str = ""
        self.items: list[dict[str, Any]] = []
        self._item_buttons: list[UIButton] = []
        self._static_frame: Optional[pygame.Surface] = None
        self._title_surf: Optional[pygame.Surface] = None

    def open(self, kind: str, items: list[dict[str, Any]], anchor: pygame.Rect) -> None:
        """Abre o flyout posicionado imediatamente acima do botão âncora."""
        self.kind = kind
        self.items = list(items)
        self.visible = True

        # Calcula altura necessária
        item_h = 36
        header_h = 32
        total_h = min(260, header_h + len(items) * (item_h + 4) + 12)
        total_w = 300

        # Ancoragem para cima do botão
        x = anchor.centerx - total_w // 2
        y = anchor.top - total_h - 6

        # Clamping horizontal
        if x < 10:
            x = 10
        elif x + total_w > Layout.W - 10:
            x = Layout.W - 10 - total_w

        self.rect.x = x
        self.rect.y = y
        self.rect.w = total_w
        self.rect.h = total_h

        self.children.clear()
        self._item_buttons.clear()

        # Cria botões para cada item do flyout
        font_size = 12
        for idx, item in enumerate(self.items):
            iy = self.rect.y + header_h + idx * (item_h + 4)
            if iy + item_h > self.rect.bottom - 6:
                break  # Limite de altura

            item_name = str(item.get("name") or item.get("nome") or "Habilidade")
            item_id = str(item.get("id") or item_name)
            action_code = f"use_skill:{item_id}|{item_name}" if kind == "skills" else f"cast_spell:{item_name}"

            sub = str(item.get("cost") or item.get("level_str") or "")
            icon = "lightning" if kind == "skills" else "sparkle"

            btn = UIButton(
                rect=(self.rect.x + 10, iy, total_w - 20, item_h),
                label=item_name,
                action_id=action_code,
                variant="flyout",
                icon=icon,
                sublabel=sub if sub else None,
                font_size=font_size,
                tooltip=item.get("description") or item.get("descricao"),
            )
            self._item_buttons.append(btn)
            self.add_child(btn)

        self.invalidate()

    def close(self) -> None:
        """Fecha o flyout."""
        self.visible = False
        self.children.clear()
        self._item_buttons.clear()

    def handle_event(self, event: pygame.event.Event) -> str:
        if not self.visible:
            return ""

        # Fechar com ESC
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()
            return CONSUMED

        # Clique fora do flyout fecha o menu
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.rect.collidepoint(event.pos):
                self.close()
                return CONSUMED

        # Delega eventos aos botões
        action = super().handle_event(event)
        if action and action != CONSUMED:
            self.close()
            return action

        return action if action else CONSUMED

    def _rebuild(self) -> None:
        """Assa o painel de fundo do flyout e o título."""
        w, h = self.rect.w, self.rect.h
        self._static_frame = FrameFactory.panel((w, h), style="gothic")

        title_str = "Habilidades de Classe" if self.kind == "skills" else "Grimorio de Magias"
        font = AssetManager.get_font(13, bold=True)
        self._title_surf = default_text_cache.get(
            title_str,
            font,
            color=Palette.GOLD_HI,
            shadow=True,
            shadow_color=Palette.INK,
        )

    def _draw_self(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        if self._static_frame:
            surface.blit(self._static_frame, self.rect.topleft)
        if self._title_surf:
            tx = self.rect.x + (self.rect.w - self._title_surf.get_width()) // 2
            surface.blit(self._title_surf, (tx, self.rect.y + 8))
            pygame.draw.line(surface, Palette.BRONZE, (self.rect.x + 12, self.rect.y + 26), (self.rect.right - 12, self.rect.y + 26), 1)


class TacticalActionBarWidget(UIWidget):
    """
    Bloco B4 do HUD: Hotbar Tática centralizada no palco (x=874, y=640, h=68).
    Suporta os modos COMBAT, LOCKED e EXPLORATION.
    Acompanha faixa de economia de ação e flyouts.
    """

    def __init__(self):
        # Dimensões de combate: 152 + (4 * 104) + (4 * 8) + 20 = 620x68 centrada em STAGE_CX=874
        combat_w = Layout.SLOT_WIDE[0] + (4 * Layout.SLOT[0]) + (4 * Layout.GAP) + 20
        combat_x = Layout.STAGE_CX - combat_w // 2
        self._combat_w: int = combat_w
        self._explore_w: int = (4 * Layout.SLOT[0]) + (3 * Layout.GAP) + 20
        super().__init__((combat_x, Layout.BAR_Y, combat_w, Layout.BAR_H))

        self.mode: BarMode = BarMode.COMBAT
        self._locked_target_name: str = ""
        self._selected_target_name: str = "Inimigo"

        # Painéis de fundo assados
        self._bg_combat: Optional[pygame.Surface] = None
        self._bg_explore: Optional[pygame.Surface] = None
        self._locked_banner_surf: Optional[pygame.Surface] = None

        # Faixa de Economia de Ação (y=616)
        econ_rect = pygame.Rect(self.rect.centerx - 170, 616, 340, 20)
        self.economy: ActionEconomyStrip = ActionEconomyStrip(econ_rect)
        self.add_child(self.economy)

        # Flyout de Habilidades e Magias
        self.flyout: ActionFlyoutWidget = ActionFlyoutWidget()
        self.add_child(self.flyout)

        # Criação UMA ÚNICA VEZ de todos os botões (Zero Garbage)
        self._combat_buttons: list[UIButton] = []
        self._explore_buttons: list[UIButton] = []

        # 1. Monta botões de combate
        cur_x = self.rect.x + 10
        by = self.rect.y + 8
        for action_id, label, icon_name, hotkey_val, is_wide in COMBAT_SLOTS:
            bw = Layout.SLOT_WIDE[0] if is_wide else Layout.SLOT[0]
            bh = Layout.SLOT[1]
            sub = "[Alvo: Inimigo]" if is_wide else None
            btn = UIButton(
                rect=(cur_x, by, bw, bh),
                label=label,
                action_id=action_id,
                variant="action",
                icon=icon_name,
                sublabel=sub,
                hotkey=hotkey_val,
                font_size=11,
            )
            self._combat_buttons.append(btn)
            cur_x += bw + Layout.GAP

        # 2. Monta botões de exploração (460x68 centrada em STAGE_CX=874)
        explore_w = self._explore_w
        explore_x = Layout.STAGE_CX - explore_w // 2
        cur_ex = explore_x + 10
        for action_id, label, icon_name, hotkey_val, _ in EXPLORATION_SLOTS:
            bw = Layout.SLOT[0]
            bh = Layout.SLOT[1]
            btn = UIButton(
                rect=(cur_ex, by, bw, bh),
                label=label,
                action_id=action_id,
                variant="action",
                icon=icon_name,
                hotkey=hotkey_val,
                font_size=11,
            )
            self._explore_buttons.append(btn)
            cur_ex += bw + Layout.GAP

        # Registra todos como filhos (visibilidade controlada no set_mode)
        for b in self._combat_buttons:
            self.add_child(b)
        for b in self._explore_buttons:
            self.add_child(b)

        self.set_mode(BarMode.COMBAT)

    def set_mode(self, mode: BarMode, active_name: str = "") -> None:
        """Alterna modo da hotbar sem alocações."""
        self.mode = mode
        self._locked_target_name = active_name

        if mode == BarMode.COMBAT:
            self.rect.w = self._combat_w
            self.rect.x = Layout.STAGE_CX - self._combat_w // 2
            self.economy.visible = True
            for b in self._combat_buttons:
                b.visible = True
                b.set_enabled(True)
            for b in self._explore_buttons:
                b.visible = False

        elif mode == BarMode.LOCKED:
            self.rect.w = self._combat_w
            self.rect.x = Layout.STAGE_CX - self._combat_w // 2
            self.economy.visible = True
            for b in self._combat_buttons:
                b.visible = True
                b.set_enabled(False)
            for b in self._explore_buttons:
                b.visible = False

        elif mode == BarMode.EXPLORATION:
            self.rect.w = self._explore_w
            self.rect.x = Layout.STAGE_CX - self._explore_w // 2
            self.economy.visible = False
            for b in self._combat_buttons:
                b.visible = False
            for b in self._explore_buttons:
                b.visible = True
                b.set_enabled(True)

        self.invalidate()

    def set_target(self, name: Optional[str]) -> None:
        """Atualiza o sub-rótulo do botão de ataque (slot 0)."""
        target_str = name if name else "[Selecione]"
        if target_str != self._selected_target_name:
            self._selected_target_name = target_str
            if self._combat_buttons:
                self._combat_buttons[0].set_label("Atacar", sublabel=f">{target_str}")

    def set_economy(self, action: bool, bonus: bool, move_ft: int, reaction: bool) -> None:
        """Repassa estado para a faixa de economia de ação."""
        self.economy.set_economy(action, bonus, move_ft, reaction)

    def open_skills_flyout(self, skills: list[dict[str, Any]]) -> None:
        """Abre flyout de habilidades sobre o slot 3."""
        if len(self._combat_buttons) > 3:
            anchor = self._combat_buttons[3].rect
            self.flyout.open("skills", skills, anchor)

    def open_spells_flyout(self, spells: list[dict[str, Any]]) -> None:
        """Abre flyout de magias sobre o slot 4."""
        if len(self._combat_buttons) > 4:
            anchor = self._combat_buttons[4].rect
            self.flyout.open("spells", spells, anchor)

    def handle_event(self, event: pygame.event.Event) -> str:
        if not (self.visible and self.enabled):
            return ""

        # Flyout tem prioridade absoluta
        if self.flyout.visible:
            fly_action = self.flyout.handle_event(event)
            if fly_action:
                return fly_action

        # Despacho normal de eventos da Hotbar
        action = super().handle_event(event)

        # Se clicou em Habilidades ou Magias na Hotbar, emite ação ou trata abertura
        if action == "skills":
            # Retorna a ação para o coordenador fornecer a lista ou abrir o flyout
            return "skills"
        elif action == "spells":
            return "spells"

        return action

    def _rebuild(self) -> None:
        """Pré-renderiza molduras de fundo e banner de turno travado."""
        self._bg_combat = FrameFactory.panel((self._combat_w, Layout.BAR_H), style="gothic")
        self._bg_explore = FrameFactory.panel((self._explore_w, Layout.BAR_H), style="gothic")

        if self.mode == BarMode.LOCKED and self._locked_target_name:
            font = AssetManager.get_font(12, bold=True)
            self._locked_banner_surf = default_text_cache.get(
                f"Turno de: {self._locked_target_name}",
                font,
                color=Palette.GOLD_HI,
                shadow=True,
                shadow_color=Palette.INK,
            )
        else:
            self._locked_banner_surf = None

    def _draw_self(self, surface: pygame.Surface) -> None:
        # Fundo da Hotbar
        if self.mode in (BarMode.COMBAT, BarMode.LOCKED):
            if self._bg_combat:
                surface.blit(self._bg_combat, self.rect.topleft)
            # Banner de turno travado
            if self.mode == BarMode.LOCKED and self._locked_banner_surf:
                bx = self.rect.centerx - self._locked_banner_surf.get_width() // 2
                surface.blit(self._locked_banner_surf, (bx, self.rect.y + 2))
        else:
            if self._bg_explore:
                surface.blit(self._bg_explore, self.rect.topleft)
