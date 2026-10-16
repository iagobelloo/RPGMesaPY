"""
Banner de Ordem de Iniciativa e Plaqueta de Local/Hora (RPGMesaPY).
Fase 6 do Redesign UI/UX — Contrato Zero Garbage por Frame.
Bloco B2 do HUD: Layout.INITIATIVE = Rect(400, 10, 480, 60) (centro x=640).
"""

from dataclasses import dataclass
import math
from typing import Optional
import pygame
from ui.asset_manager import AssetManager
from ..theme import Palette, Layout
from ..render_cache import FrameFactory, IconAtlas, default_text_cache
from ..base import UIWidget, CONSUMED


@dataclass(slots=True)
class InitiativeEntry:
    """Entrada individual de participante na fita de iniciativa."""
    uid: str
    name: str
    faction: str  # "hero", "enemy", "ally"
    initiative: int
    hp: int
    hp_max: int
    portrait_key: str


class InitiativeBannerWidget(UIWidget):
    """
    Banner de Iniciativa em combate e Plaqueta de Localização/Tempo fora de combate.
    Suporta anel dourado e glow pulsante no participante ativo, seleção de alvo por clique
    e tooltips informativos por hover.
    """

    MAX_VISIBLE: int = 6

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect = Layout.INITIATIVE):
        super().__init__(rect)
        self.in_combat: bool = False
        self.round_no: int = 1
        self.active_uid: str = ""
        self.entries: list[InitiativeEntry] = []

        # Localização e tempo fora de combate
        self.location: str = "Taverna do Javali"
        self.time_str: str = "Dia 1, Noite"

        # Animação de pulso do chip ativo (Zero Garbage)
        self._pulse_timer: float = 0.0
        self._glow_alpha: int = 128
        self._glow_surf: Optional[pygame.Surface] = None

        # Caches pré-renderizados
        self._static_bg: Optional[pygame.Surface] = None
        self._chip_surfs: list[pygame.Surface] = []
        self._chip_rects: list[pygame.Rect] = []
        self._active_chip_idx: int = -1

        # Hover para tooltip
        self._hover_entry: Optional[InitiativeEntry] = None
        self._hover_rect: Optional[pygame.Rect] = None

    def set_combat(self, in_combat: bool) -> None:
        """Alterna entre fita de combate e plaqueta de exploração."""
        if in_combat != self.in_combat:
            self.in_combat = in_combat
            self.invalidate()

    def set_location_time(self, location: str, time_str: str) -> None:
        """Atualiza a localização e horário fora de combate."""
        if location != self.location or time_str != self.time_str:
            self.location = location
            self.time_str = time_str
            if not self.in_combat:
                self.invalidate()

    def set_order(self, entries: list[InitiativeEntry], active_uid: str, round_no: int) -> None:
        """
        Atualiza a lista de iniciativa comparando escalares e uids.
        Rebake ocorre apenas se a ordem ou elementos mudarem.
        """
        needs_rebuild = False

        if round_no != self.round_no:
            self.round_no = round_no
            needs_rebuild = True

        if active_uid != self.active_uid:
            self.active_uid = active_uid
            needs_rebuild = True

        # Compara lista de entradas
        if len(entries) != len(self.entries):
            needs_rebuild = True
        else:
            for e_new, e_old in zip(entries, self.entries):
                if (
                    e_new.uid != e_old.uid
                    or e_new.hp != e_old.hp
                    or e_new.hp_max != e_old.hp_max
                    or e_new.initiative != e_old.initiative
                ):
                    needs_rebuild = True
                    break

        if needs_rebuild:
            self.entries = list(entries)
            self.in_combat = True
            self.invalidate()

    def update(self, dt: float) -> None:
        super().update(dt)

        # Atualiza a fase do pulso do glow do chip ativo
        if self.in_combat and self._active_chip_idx >= 0:
            self._pulse_timer += dt * 3.5
            # Oscila suavemente entre 90 e 220 de alfa
            self._glow_alpha = int(155 + 65 * math.sin(self._pulse_timer))

    def get_tooltip_request(self) -> Optional[tuple[str, pygame.Rect]]:
        """Retorna texto de status e âncora do participante em hover."""
        if self.in_combat and self._hover_entry and self._hover_rect:
            e = self._hover_entry
            txt = f"{e.name} (Inic: {e.initiative})\nPV: {e.hp}/{e.hp_max}"
            return (txt, self._hover_rect)
        return None

    def handle_event(self, event: pygame.event.Event) -> str:
        if not (self.visible and self.enabled):
            return ""

        # Detecção de hover sobre os chips
        if event.type == pygame.MOUSEMOTION:
            self._hover_entry = None
            self._hover_rect = None
            if self.in_combat:
                for idx, r in enumerate(self._chip_rects):
                    if r.collidepoint(event.pos):
                        if idx < len(self.entries):
                            self._hover_entry = self.entries[idx]
                            self._hover_rect = r
                        break

        # Clique sobre um chip seleciona o alvo
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.in_combat:
                for idx, r in enumerate(self._chip_rects):
                    if r.collidepoint(event.pos):
                        if idx < len(self.entries):
                            target_uid = self.entries[idx].uid
                            return f"select_target:{target_uid}"

        return super().handle_event(event)

    def _rebuild(self) -> None:
        """Assa o painel de fundo e os chips de retrato."""
        w, h = self.rect.w, self.rect.h
        self._static_bg = FrameFactory.panel((w, h), style="gothic").copy()
        self._chip_surfs.clear()
        self._chip_rects.clear()
        self._active_chip_idx = -1

        if not self.in_combat:
            # ------------------------------------ FORA DE COMBATE: Plaqueta de Local/Hora
            font_loc = AssetManager.get_font(13, bold=True)
            font_time = AssetManager.get_font(11, bold=False)

            loc_surf = default_text_cache.get(
                self.location,
                font_loc,
                color=Palette.GOLD_HI,
                shadow=True,
                shadow_color=Palette.INK,
            )
            time_surf = default_text_cache.get(
                self.time_str,
                font_time,
                color=Palette.PARCH_DIM,
                shadow=True,
                shadow_color=Palette.INK,
            )

            icon_map = IconAtlas.get("map", size=18, color=Palette.GOLD)

            # Centraliza o conteúdo na plaqueta
            total_content_w = icon_map.get_width() + 8 + loc_surf.get_width() + 16 + time_surf.get_width()
            start_x = (w - total_content_w) // 2

            self._static_bg.blit(icon_map, (start_x, (h - icon_map.get_height()) // 2))
            cur_x = start_x + icon_map.get_width() + 8

            self._static_bg.blit(loc_surf, (cur_x, (h - loc_surf.get_height()) // 2))
            cur_x += loc_surf.get_width() + 8

            # Divisor losango pequeno central
            diamond = IconAtlas.get("diamond", size=10, color=Palette.BRONZE)
            self._static_bg.blit(diamond, (cur_x, (h - diamond.get_height()) // 2))
            cur_x += diamond.get_width() + 8

            self._static_bg.blit(time_surf, (cur_x, (h - time_surf.get_height()) // 2))
            return

        # ---------------------------------------- EM COMBATE: Fita de Iniciativa
        # 1. Indicador "Rodada N" à esquerda
        font_round = AssetManager.get_font(12, bold=True)
        r_surf = default_text_cache.get(
            f"R {self.round_no}",
            font_round,
            color=Palette.GOLD_HI,
            shadow=True,
            shadow_color=Palette.INK,
        )
        self._static_bg.blit(r_surf, (14, (h - r_surf.get_height()) // 2))
        pygame.draw.line(self._static_bg, Palette.BRONZE, (54, 8), (54, h - 8), 1)

        # 2. Chips de retrato
        chip_start_x = self.rect.x + 64
        display_count = min(len(self.entries), self.MAX_VISIBLE)
        has_overflow = len(self.entries) > self.MAX_VISIBLE

        chip_y = self.rect.y + (h - 40) // 2

        cur_x = chip_start_x
        for i in range(display_count):
            entry = self.entries[i]
            is_active = (entry.uid == self.active_uid)
            if is_active:
                self._active_chip_idx = i

            # Tamanho: 48x48 para o ativo, 40x40 para os normais
            sz = 48 if is_active else 40
            offset_y = -4 if is_active else 0
            chip_rect = pygame.Rect(cur_x, chip_y + offset_y, sz, sz)
            self._chip_rects.append(chip_rect)

            chip_surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
            chip_surf.fill(Palette.TRANSPARENT)

            # Cor da borda por facção
            if entry.faction == "hero":
                border_col = Palette.GOLD_HI if is_active else Palette.GOLD
            elif entry.faction == "ally":
                border_col = Palette.ALLY
            else:
                border_col = Palette.BLOOD

            # Tenta carregar retrato
            portrait = None
            try:
                portrait = AssetManager.get_portrait(entry.portrait_key, size=(sz - 4, sz - 4))
            except Exception:
                portrait = None

            if portrait:
                scaled = pygame.transform.smoothscale(portrait, (sz - 4, sz - 4))
                chip_surf.blit(scaled, (2, 2))
            else:
                # Fundo e silhueta
                pygame.draw.rect(chip_surf, (24, 18, 14), (2, 2, sz - 4, sz - 4))
                ic_name = "sword" if entry.faction == "enemy" else "shield"
                ic = IconAtlas.get(ic_name, size=sz // 2, color=border_col)
                chip_surf.blit(ic, ((sz - ic.get_width()) // 2, (sz - ic.get_height()) // 2))

            # Borda do chip
            border_w = 2 if is_active else 1
            pygame.draw.rect(chip_surf, border_col, (1, 1, sz - 2, sz - 2), width=border_w, border_radius=4)

            # Mini-indicador de PV em barra na base do chip
            hp_ratio = max(0.0, min(1.0, entry.hp / max(1, entry.hp_max)))
            hp_w = round((sz - 6) * hp_ratio)
            pygame.draw.rect(chip_surf, (10, 8, 6), (3, sz - 6, sz - 6, 3))
            if hp_w > 0:
                bar_col = Palette.ALLY if hp_ratio > 0.5 else (Palette.GOLD if hp_ratio > 0.2 else Palette.BLOOD)
                pygame.draw.rect(chip_surf, bar_col, (3, sz - 6, hp_w, 3))

            self._chip_surfs.append(chip_surf)
            cur_x += sz + 6

            # Chevron entre chips (desenhado na camada estática)
            if i < display_count - 1:
                chev_x = cur_x - self.rect.x - 4
                chevron = IconAtlas.get("chevron", size=10, color=Palette.BRONZE)
                self._static_bg.blit(chevron, (chev_x, (h - chevron.get_height()) // 2))

        # Pré-renderiza glow do chip ativo
        self._glow_surf = FrameFactory.glow((48, 48), Palette.GOLD, radius=4)

    def _draw_self(self, surface: pygame.Surface) -> None:
        if self._static_bg:
            surface.blit(self._static_bg, self.rect.topleft)

        if not self.in_combat:
            return

        # Desenha os chips de retrato
        for idx, (surf, rect) in enumerate(zip(self._chip_surfs, self._chip_rects)):
            # Glow pulsante no chip ativo
            if idx == self._active_chip_idx and self._glow_surf:
                self._glow_surf.set_alpha(self._glow_alpha)
                surface.blit(self._glow_surf, (rect.x - 4, rect.y - 4))

            surface.blit(surf, rect.topleft)
