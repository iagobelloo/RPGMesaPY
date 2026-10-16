"""
Nameplate de Entidades / Tokens no Palco 2.5D (RPGMesaPY).
Fase 6 do Redesign UI/UX — Contrato Zero Garbage por Frame.
Posicionamento correto 14 px abaixo dos pés (feet_y + 14 = 574),
eliminando sobreposição do nome sobre os pés dos personagens.
"""

from typing import Optional
import pygame
from ui.asset_manager import AssetManager
from ..theme import Palette, Layout
from ..render_cache import default_text_cache


class TokenNameplate:
    """
    Plaqueta cacheada de Nome e PV de entidade (Herói, Inimigos, Aliados).
    Renderizada apenas quando há mudança de status.
    Desenhada abaixo da sombra dos pés (feet_y + NAMEPLATE_DY).
    """

    WIDTH: int = Layout.NAMEPLATE[0]    # 120 px
    HEIGHT: int = Layout.NAMEPLATE[1]   # 26 px
    DY: int = Layout.NAMEPLATE_DY       # 14 px

    def __init__(self, font_size: int = 11):
        self.font_size: int = font_size
        self._name: str = ""
        self._hp: int = -1
        self._hp_max: int = -1
        self._faction: str = ""
        self._surf: Optional[pygame.Surface] = None

    def sync(self, name: str, hp: int, hp_max: int, faction: str = "enemy") -> None:
        """
        Sincroniza os dados da entidade comparando apenas escalares.
        Reassamento da superfície ocorre apenas se houver mudança de valor.
        """
        safe_hp_max = max(1, hp_max)
        safe_hp = max(0, min(hp, safe_hp_max))

        if (
            name != self._name
            or safe_hp != self._hp
            or safe_hp_max != self._hp_max
            or faction != self._faction
            or self._surf is None
        ):
            self._name = name
            self._hp = safe_hp
            self._hp_max = safe_hp_max
            self._faction = faction
            self._rebake()

    def _rebake(self) -> None:
        """Gera a superfície cacheada da plaqueta de 120x26 px."""
        w, h = self.WIDTH, self.HEIGHT
        self._surf = pygame.Surface((w, h), pygame.SRCALPHA)
        self._surf.fill(Palette.TRANSPARENT)

        # Fundo de couro escuro semitransparente
        bg_col = (18, 14, 10, 220)
        pygame.draw.rect(self._surf, bg_col, (0, 0, w, h), border_radius=3)

        # Borda colorida por facção
        if self._faction == "hero":
            border_col = Palette.GOLD
            text_col = Palette.GOLD_HI
        elif self._faction == "ally":
            border_col = Palette.ALLY
            text_col = Palette.PARCHMENT
        else:
            border_col = Palette.BLOOD
            text_col = Palette.PARCHMENT

        pygame.draw.rect(self._surf, border_col, (0, 0, w, h), width=1, border_radius=3)

        # Nome da entidade
        font = AssetManager.get_font(self.font_size, bold=True)
        # Trunca se for muito extenso
        display_name = self._name
        if font.size(display_name)[0] > w - 12:
            display_name = display_name[:11] + ".."

        name_surf = default_text_cache.get(
            display_name,
            font,
            color=text_col,
            shadow=True,
            shadow_color=Palette.INK,
        )
        nx = (w - name_surf.get_width()) // 2
        self._surf.blit(name_surf, (nx, 3))

        # Mini-barra de PV (112x4 px em y=18)
        bar_w = w - 12
        bar_h = 4
        bar_x = 6
        bar_y = 18

        # Fundo da barra
        pygame.draw.rect(self._surf, (10, 8, 6), (bar_x, bar_y, bar_w, bar_h))

        # Preenchimento de PV com cor por faixa
        ratio = max(0.0, min(1.0, self._hp / self._hp_max))
        fill_w = round(bar_w * ratio)

        if fill_w > 0:
            if ratio > 0.50:
                bar_col = Palette.ALLY
            elif ratio > 0.20:
                bar_col = Palette.GOLD
            else:
                bar_col = Palette.BLOOD
            pygame.draw.rect(self._surf, bar_col, (bar_x, bar_y, fill_w, bar_h))

    def draw(self, surface: pygame.Surface, feet_x: int, feet_y: int) -> None:
        """
        Desenha a plaqueta ancorada 14 px abaixo dos pés reais do token.
        Zero garbage por frame: apenas 1 blit da superfície cacheada.
        """
        if self._surf:
            px = feet_x - self.WIDTH // 2
            py = feet_y + self.DY
            surface.blit(self._surf, (px, py))
