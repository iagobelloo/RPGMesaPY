"""
Player Card e Faixa de Condições 5E (RPGMesaPY).
Fase 3 do Redesign UI/UX — Contrato Zero Garbage por Frame.
Comparação estrita de escalares no sync(), lerp suave de PV e tooltips com regras 5e.
"""

from typing import Optional, Any
import pygame
from ui.asset_manager import AssetManager
from ..theme import Palette, Layout
from ..render_cache import FrameFactory, IconAtlas, default_text_cache
from ..base import UIWidget


# Dicionário canônico de regras 5E para as condições
CONDITION_RULES: dict[str, str] = {
    "Esquivando": "Esquiva (Dodge): Ataques contra você têm desvantagem; testes de Destreza têm vantagem.",
    "Envenenado": "Envenenado: Desvantagem em jogadas de ataque e testes de habilidade.",
    "Atordoado": "Atordoado: Incapacitado, não pode se mover. Falha em testes de Força e Destreza.",
    "Incapacitado": "Incapacitado: Não pode realizar ações nem reações.",
    "Caído": "Caído (Prone): Desvantagem nos próprios ataques. Ataques a 5 pés têm vantagem.",
    "Abençoado": "Bênção: +1d4 em jogadas de ataque e testes de resistência.",
    "Invisível": "Invisível: Vantagem em ataques contra inimigos. Ataques recebidos têm desvantagem.",
    "Amedrontado": "Amedrontado: Desvantagem em testes e ataques enquanto a fonte do medo estiver visível.",
    "Cego": "Cego: Falha em testes de visão. Desvantagem em ataques; ataques recebidos têm vantagem.",
    "Surdo": "Surdo: Falha em testes que exigem audição.",
    "Agarrado": "Agarrado: Deslocamento reduzido a 0 pés.",
    "Contido": "Contido: Deslocamento 0. Desvantagem em ataques. Ataques recebidos têm vantagem.",
    "Paralisado": "Paralisado: Incapacitado. Ataques recebidos a 5 pés que acertarem são críticos.",
    "Inconsciente": "Inconsciente: Incapacitado, indefeso. Larga itens e cai ao chão.",
}


class ConditionBadgeStrip(UIWidget):
    """
    Faixa horizontal de até 6 badges de condições ativas (18x18 px cada).
    Gera tooltip informativo das regras D&D 5E ao posicionar o cursor.
    """

    MAX_BADGES: int = 6
    BADGE_SIZE: int = 18
    BADGE_GAP: int = 3

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect):
        super().__init__(rect)
        self._conditions: list[str] = []
        self._badge_surfs: list[pygame.Surface] = []
        self._badge_rects: list[pygame.Rect] = []
        self._hover_condition: Optional[str] = None
        self._hover_rect: Optional[pygame.Rect] = None

    def set_conditions(self, conditions: list[str]) -> None:
        """Atualiza a lista de condições ativas caso haja alteração de conteúdo."""
        if conditions != self._conditions:
            self._conditions = list(conditions)
            self.invalidate()

    def get_hover_tooltip(self) -> Optional[tuple[str, pygame.Rect]]:
        """Retorna o texto de regra 5E e a âncora caso o cursor esteja sobre uma badge."""
        if self._hover_condition and self._hover_rect:
            rule = CONDITION_RULES.get(self._hover_condition, f"Condição: {self._hover_condition}")
            return (rule, self._hover_rect)
        return None

    def _rebuild(self) -> None:
        """Pré-renderiza as superfícies das badges e calcula posições relativas."""
        self._badge_surfs.clear()
        self._badge_rects.clear()

        if not self._conditions:
            return

        font_badge = AssetManager.get_font(10, bold=True)
        total = len(self._conditions)
        display_count = min(total, self.MAX_BADGES)
        has_overflow = total > self.MAX_BADGES

        for i in range(display_count):
            bx = self.rect.x + i * (self.BADGE_SIZE + self.BADGE_GAP)
            by = self.rect.y
            b_rect = pygame.Rect(bx, by, self.BADGE_SIZE, self.BADGE_SIZE)
            self._badge_rects.append(b_rect)

            surf = pygame.Surface((self.BADGE_SIZE, self.BADGE_SIZE), pygame.SRCALPHA)
            surf.fill(Palette.TRANSPARENT)

            if has_overflow and i == self.MAX_BADGES - 1:
                # Badge de contagem excedente (+N)
                remaining = total - (self.MAX_BADGES - 1)
                pygame.draw.rect(surf, (40, 30, 20, 230), (0, 0, self.BADGE_SIZE, self.BADGE_SIZE), border_radius=3)
                pygame.draw.rect(surf, Palette.GOLD, (0, 0, self.BADGE_SIZE, self.BADGE_SIZE), width=1, border_radius=3)
                txt = default_text_cache.get(f"+{remaining}", font_badge, color=Palette.GOLD_HI)
                surf.blit(txt, ((self.BADGE_SIZE - txt.get_width()) // 2, (self.BADGE_SIZE - txt.get_height()) // 2))
            else:
                cond = self._conditions[i]
                # Fundo e ícone específico por condição
                bg_col = (30, 20, 16, 230)
                border_col = Palette.BRONZE

                if cond == "Esquivando":
                    border_col = Palette.ALLY
                    icon_surf = IconAtlas.get("shield", size=12, color=Palette.ALLY)
                elif cond == "Abençoado":
                    border_col = Palette.GOLD_HI
                    icon_surf = IconAtlas.get("sparkle", size=12, color=Palette.GOLD_HI)
                elif cond in ("Envenenado", "Atordoado"):
                    border_col = (180, 160, 40)
                    icon_surf = IconAtlas.get("lightning", size=12, color=(200, 180, 50))
                elif cond in ("Incapacitado", "Paralisado", "Inconsciente"):
                    border_col = Palette.BLOOD
                    icon_surf = IconAtlas.get("diamond", size=12, color=Palette.BLOOD)
                elif cond == "Caído":
                    border_col = Palette.PARCH_DIM
                    icon_surf = IconAtlas.get("boot", size=12, color=Palette.PARCH_DIM)
                else:
                    icon_surf = IconAtlas.get("eye", size=12, color=Palette.PARCHMENT)

                pygame.draw.rect(surf, bg_col, (0, 0, self.BADGE_SIZE, self.BADGE_SIZE), border_radius=3)
                pygame.draw.rect(surf, border_col, (0, 0, self.BADGE_SIZE, self.BADGE_SIZE), width=1, border_radius=3)
                surf.blit(icon_surf, ((self.BADGE_SIZE - 12) // 2, (self.BADGE_SIZE - 12) // 2))

            self._badge_surfs.append(surf)

    def handle_event(self, event: pygame.event.Event) -> str:
        if not (self.visible and self.enabled):
            return ""

        if event.type == pygame.MOUSEMOTION:
            self._hover_condition = None
            self._hover_rect = None
            for idx, rect in enumerate(self._badge_rects):
                if rect.collidepoint(event.pos):
                    if idx < len(self._conditions):
                        self._hover_condition = self._conditions[idx]
                        self._hover_rect = rect
                    break

        return super().handle_event(event)

    def _draw_self(self, surface: pygame.Surface) -> None:
        for surf, rect in zip(self._badge_surfs, self._badge_rects):
            surface.blit(surf, rect.topleft)


class PlayerCardWidget(UIWidget):
    """
    Bloco B1 do HUD: Informações vitais do protagonista (1280x720).
    Localizado em Rect(12, 12, 312, 116).
    Exibe retrato chanfrado 92x92, nome, nível, classe, PV com lerp e cor por faixa,
    CA com ícone shield, Ouro com ícone coin e badges de condição ativas.
    """

    def __init__(self, rect: tuple[int, int, int, int] | pygame.Rect = Layout.PLAYER_CARD):
        super().__init__(rect)

        # Escalares internos para detecção de mudança (Zero Garbage)
        self._name: str = ""
        self._level: int = -1
        self._cls: str = ""
        self._race: str = ""
        self._gender: str = ""
        self._hp: int = -1
        self._hp_max: int = -1
        self._hp_shown: float = 0.0
        self._ac: int = -1
        self._gold: int = -1
        self._portrait_key: Any = None

        # Geometria da barra de PV (184x16 px em x=116, y=50)
        self._bar_local_rect: pygame.Rect = pygame.Rect(116, 50, 184, 16)
        self._hp_fill: pygame.Rect = pygame.Rect(self.rect.x + 117, self.rect.y + 51, 0, 14)
        self._hp_color: tuple[int, int, int] = Palette.ALLY

        # Caches de superfícies pré-renderizadas
        self._static: Optional[pygame.Surface] = None
        self._hp_text_surf: Optional[pygame.Surface] = None
        self._hp_text_pos: tuple[int, int] = (0, 0)

        # Faixa de Condições como componente filho
        badge_rect = pygame.Rect(self.rect.x + 116, self.rect.y + 92, 184, 18)
        self.badges: ConditionBadgeStrip = ConditionBadgeStrip(badge_rect)
        self.add_child(self.badges)

    def sync(self, player: dict) -> None:
        """
        Sincroniza o estado do jogador comparando apenas escalares primitivos.
        Zero Garbage por frame: não cria tuplas ou assinaturas temporárias.
        """
        name = str(player.get("name") or player.get("nome") or "Herói")
        race = str(player.get("race") or player.get("raca") or "Humano")
        cls_name = str(player.get("class") or player.get("classe") or "Guerreiro")
        gender = str(player.get("gender") or player.get("genero") or "male")
        level = int(player.get("level") or player.get("nivel") or 1)
        hp = int(player.get("hp_current", player.get("hp", player.get("pv_atual", 10))))
        hp_max = max(1, int(player.get("hp_max", player.get("pv_max", 10))))
        ac = int(player.get("ac", player.get("ca", 10)))
        gold = int(player.get("gold", player.get("ouro", 0)))

        # Chave do retrato
        portrait_key = (
            player.get("portrait")
            or player.get("race")
            or player.get("classe")
            or player.get("gender")
        )

        conditions = player.get("conditions") or player.get("condicoes") or []
        self.badges.set_conditions(conditions)

        # Verifica se algo dos textos/estáticos mudou
        needs_rebuild = False
        if (
            name != self._name
            or level != self._level
            or cls_name != self._cls
            or race != self._race
            or gender != self._gender
            or ac != self._ac
            or gold != self._gold
            or portrait_key != self._portrait_key
        ):
            self._name = name
            self._level = level
            self._cls = cls_name
            self._race = race
            self._gender = gender
            self._ac = ac
            self._gold = gold
            self._portrait_key = portrait_key
            needs_rebuild = True

        # Verifica se o valor de PV mudou
        if hp != self._hp or hp_max != self._hp_max:
            if self._hp == -1:
                self._hp_shown = float(hp)
            self._hp = hp
            self._hp_max = hp_max
            self._update_hp_text()

        if needs_rebuild:
            self.invalidate()

    def _update_hp_text(self) -> None:
        """Renderiza o texto de PV ('12/12') cacheado apenas quando os valores mudam."""
        font = AssetManager.get_font(11, bold=True)
        txt = f"{self._hp}/{self._hp_max}"
        self._hp_text_surf = default_text_cache.get(
            txt,
            font,
            color=Palette.WHITE,
            shadow=True,
            shadow_color=Palette.INK,
        )
        bar_cx = self.rect.x + self._bar_local_rect.centerx
        bar_cy = self.rect.y + self._bar_local_rect.centery
        self._hp_text_pos = (
            bar_cx - self._hp_text_surf.get_width() // 2,
            bar_cy - self._hp_text_surf.get_height() // 2,
        )

    def update(self, dt: float) -> None:
        """
        Interpolação (lerp) suave da barra de PV e cálculo in-place da largura do fill.
        """
        super().update(dt)

        # Lerp suave do PV mostrado
        diff = self._hp - self._hp_shown
        if abs(diff) > 0.05:
            self._hp_shown += diff * min(1.0, dt * 10.0)
        else:
            self._hp_shown = float(self._hp)

        # Atualiza a largura do fill in-place (Zero Garbage)
        max_fill_w = 182
        ratio = max(0.0, min(1.0, self._hp_shown / max(1, self._hp_max)))
        self._hp_fill.width = round(max_fill_w * ratio)

        # Cor dinâmica por faixa de PV
        if ratio > 0.50:
            self._hp_color = Palette.ALLY
        elif ratio > 0.20:
            self._hp_color = Palette.GOLD
        else:
            self._hp_color = Palette.BLOOD

    def _rebuild(self) -> None:
        """
        Assa a camada estática do Player Card em uma única Surface de 312x116:
        painel gótico, retrato chanfrado, textos de nome/nível e ícones de CA/Ouro.
        """
        w, h = self.rect.w, self.rect.h
        self._static = FrameFactory.panel((w, h), style="gothic").copy()

        # 1. Retrato chanfrado 92x92 em (12, 12)
        portrait_rect = pygame.Rect(12, 12, 92, 92)
        portrait_raw = AssetManager.get_hero_icon(self._race, self._cls, self._gender, size=(92, 92))
        if portrait_raw is None:
            portrait_raw = AssetManager.get_portrait_sprite(self._name, size=(92, 92))

        if portrait_raw is not None:
            # Aplica máscara chanfrada
            mask = FrameFactory.chamfer_mask((92, 92), cut=8)
            masked_surf = pygame.Surface((92, 92), pygame.SRCALPHA)
            scaled = pygame.transform.smoothscale(portrait_raw, (92, 92))
            masked_surf.blit(scaled, (0, 0))
            masked_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            self._static.blit(masked_surf, portrait_rect.topleft)
        else:
            # Silhueta estilizada caso ainda não haja sprite
            mask = FrameFactory.chamfer_mask((92, 92), cut=8)
            pygame.draw.rect(self._static, (24, 18, 14), portrait_rect)
            icon_ph = IconAtlas.get("diamond", size=40, color=Palette.GOLD)
            self._static.blit(icon_ph, (12 + (92 - 40) // 2, 12 + (92 - 40) // 2))

        # Borda chanfrada de reforço do retrato
        border_pts = [
            (12 + 8, 12),
            (12 + 92 - 8, 12),
            (12 + 92, 12 + 8),
            (12 + 92, 12 + 92 - 8),
            (12 + 92 - 8, 12 + 92),
            (12 + 8, 12 + 92),
            (12, 12 + 92 - 8),
            (12, 12 + 8),
        ]
        pygame.draw.polygon(self._static, Palette.GOLD, border_pts, width=1)

        # 2. Nome do protagonista (font 16 bold, x=116, y=12)
        font_name = AssetManager.get_font(16, bold=True)
        name_txt = self._name or "Herói"
        name_surf = default_text_cache.get(
            name_txt,
            font_name,
            color=Palette.GOLD_HI,
            shadow=True,
            shadow_color=Palette.INK,
        )
        self._static.blit(name_surf, (116, 12))

        # 3. Nível e Classe ("Nv X – Classe", x=116, y=32)
        font_sub = AssetManager.get_font(12, bold=False)
        sub_txt = f"Nv {max(1, self._level)} - {self._cls or 'Guerreiro'}"
        sub_surf = default_text_cache.get(
            sub_txt,
            font_sub,
            color=Palette.PARCH_DIM,
            shadow=True,
            shadow_color=Palette.INK,
        )
        self._static.blit(sub_surf, (116, 32))

        # 4. Fundo escuro e borda da barra de PV em (116, 50, 184, 16)
        pygame.draw.rect(self._static, (14, 10, 8), self._bar_local_rect)
        pygame.draw.rect(self._static, Palette.BRONZE, self._bar_local_rect, width=1)

        # 5. CA e Ouro em y=72
        # Escudo de CA
        icon_shield = IconAtlas.get("shield", size=16, color=Palette.GOLD)
        self._static.blit(icon_shield, (116, 71))
        font_stats = AssetManager.get_font(12, bold=True)
        ac_surf = default_text_cache.get(
            f"CA {max(0, self._ac)}",
            font_stats,
            color=Palette.PARCHMENT,
            shadow=True,
            shadow_color=Palette.INK,
        )
        self._static.blit(ac_surf, (136, 72))

        # Moeda de Ouro
        icon_coin = IconAtlas.get("coin", size=16, color=Palette.GOLD)
        self._static.blit(icon_coin, (196, 71))
        gold_surf = default_text_cache.get(
            f"{max(0, self._gold)} PO",
            font_stats,
            color=Palette.PARCHMENT,
            shadow=True,
            shadow_color=Palette.INK,
        )
        self._static.blit(gold_surf, (216, 72))

        # Atualiza a posição e texto de PV
        self._update_hp_text()

    def _draw_self(self, surface: pygame.Surface) -> None:
        """
        Zero garbage: blita a camada estática assada, preenche o fill de PV in-place
        e blita o texto de PV pré-renderizado.
        """
        if self._static:
            surface.blit(self._static, self.rect.topleft)

        # Preenchimento animado da barra de PV (fill in-place sem alocação)
        if self._hp_fill.width > 0:
            surface.fill(self._hp_color, self._hp_fill)

        # Texto do PV sobre a barra
        if self._hp_text_surf:
            surface.blit(self._hp_text_surf, self._hp_text_pos)
