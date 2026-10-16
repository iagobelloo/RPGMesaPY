"""
Caches de Renderização e Fábricas de Elementos Visuais.
Parte da Fase 1 do Redesign UI/UX (RPGMesaPY).
Contrato Zero Garbage: Nenhuma Surface é alocada dentro de draw().
"""

from collections import OrderedDict
import math
import pygame
from .theme import Palette, ButtonState


class TextCache:
    """
    Cache LRU de superfícies de texto pré-renderizadas.
    Usado estritamente em _rebuild() e tratadores de eventos, NUNCA em draw().
    """

    def __init__(self, capacity: int = 512):
        self.capacity: int = capacity
        self._store: OrderedDict = OrderedDict()

    def get(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, ...] = Palette.PARCHMENT,
        shadow: bool = False,
        shadow_color: tuple[int, ...] = Palette.INK,
        shadow_offset: tuple[int, int] = (1, 1),
    ) -> pygame.Surface:
        """Obtém ou renderiza a superfície de texto com cache LRU."""
        key = (text, id(font), tuple(color), shadow, tuple(shadow_color), shadow_offset)
        if key in self._store:
            self._store.move_to_end(key)
            return self._store[key]

        if not text:
            surf = pygame.Surface((1, max(1, font.get_height())), pygame.SRCALPHA)
            surf.fill(Palette.TRANSPARENT)
        elif shadow:
            base_surf = font.render(text, True, color)
            shadow_surf = font.render(text, True, shadow_color)
            ox, oy = shadow_offset
            w = base_surf.get_width() + abs(ox)
            h = base_surf.get_height() + abs(oy)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            # Desenha a sombra deslocada
            sh_x = max(0, ox)
            sh_y = max(0, oy)
            surf.blit(shadow_surf, (sh_x, sh_y))
            # Desenha o texto principal por cima
            tx = max(0, -ox)
            ty = max(0, -oy)
            surf.blit(base_surf, (tx, ty))
        else:
            surf = font.render(text, True, color)

        if len(self._store) >= self.capacity:
            self._store.popitem(last=False)

        self._store[key] = surf
        return surf

    def clear(self) -> None:
        """Limpa o cache em reinicializações."""
        self._store.clear()


# Instância global padrão de cache de texto
default_text_cache = TextCache(capacity=512)


class FrameFactory:
    """
    Fábrica e repositório de molduras góticas pré-renderizadas.
    Cachê permanente indexado por (tipo, tamanho, variante).
    """

    _cache: dict[tuple, pygame.Surface | dict[ButtonState, pygame.Surface]] = {}

    @classmethod
    def chamfer_mask(cls, size: tuple[int, int], cut: int = 10) -> pygame.Surface:
        """
        Retorna uma máscara alfa com cantos chanfrados nos 4 cantos.
        Útil para retratos e recortes estilizados de sprites.
        """
        key = ("chamfer_mask", size, cut)
        if key in cls._cache:
            return cls._cache[key]  # type: ignore

        w, h = size
        w = max(4, w)
        h = max(4, h)
        c = min(cut, w // 2 - 1, h // 2 - 1)
        c = max(1, c)

        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        mask.fill(Palette.TRANSPARENT)
        points = [
            (c, 0),
            (w - c, 0),
            (w, c),
            (w, h - c),
            (w - c, h),
            (c, h),
            (0, h - c),
            (0, c),
        ]
        pygame.draw.polygon(mask, (255, 255, 255, 255), points)
        cls._cache[key] = mask
        return mask

    @classmethod
    def panel(cls, size: tuple[int, int], style: str = "gothic") -> pygame.Surface:
        """
        Cria uma moldura de painel gótico completa: fundo couro/painel escuro,
        borda bronze chanfrada, filete interno e cantoneiras douradas decoradas.
        """
        key = ("panel", size, style)
        if key in cls._cache:
            return cls._cache[key]  # type: ignore

        w, h = size
        w = max(8, w)
        h = max(8, h)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill(Palette.TRANSPARENT)

        c = 8 if (w >= 60 and h >= 60) else 4
        # Polígono externo
        points = [
            (c, 0),
            (w - c, 0),
            (w, c),
            (w, h - c),
            (w - c, h),
            (c, h),
            (0, h - c),
            (0, c),
        ]

        if style == "tooltip":
            bg_color = (20, 16, 12, 240)
            border_color = Palette.BRONZE
            inner_color = (60, 46, 28, 160)
        else:
            bg_color = Palette.PANEL_BG
            border_color = Palette.BRONZE
            inner_color = Palette.PANEL_INNER

        # 1. Fundo chanfrado
        pygame.draw.polygon(surf, bg_color, points)

        # 2. Borda externa bronze
        pygame.draw.polygon(surf, border_color, points, width=1)

        # 3. Filete interno a 3 px
        if w > 16 and h > 16:
            ci = max(2, c - 2)
            inner_points = [
                (ci + 2, 3),
                (w - ci - 3, 3),
                (w - 4, ci + 2),
                (w - 4, h - ci - 3),
                (w - ci - 3, h - 4),
                (ci + 2, h - 4),
                (3, h - ci - 3),
                (3, ci + 2),
            ]
            pygame.draw.polygon(surf, inner_color, inner_points, width=1)

        # 4. Cantoneiras góticas em L reforçadas
        corner_len = min(12, max(4, c + 4))
        # Topo-Esquerda
        pygame.draw.line(surf, Palette.GOLD, (c, 1), (c + corner_len, 1), 1)
        pygame.draw.line(surf, Palette.GOLD, (1, c), (1, c + corner_len), 1)
        pygame.draw.circle(surf, Palette.GOLD_HI, (c, c), 1)

        # Topo-Direita
        pygame.draw.line(surf, Palette.GOLD, (w - c - 1, 1), (w - c - 1 - corner_len, 1), 1)
        pygame.draw.line(surf, Palette.GOLD, (w - 2, c), (w - 2, c + corner_len), 1)
        pygame.draw.circle(surf, Palette.GOLD_HI, (w - c - 1, c), 1)

        # Fundo-Esquerda
        pygame.draw.line(surf, Palette.GOLD, (c, h - 2), (c + corner_len, h - 2), 1)
        pygame.draw.line(surf, Palette.GOLD, (1, h - c - 1), (1, h - c - 1 - corner_len), 1)
        pygame.draw.circle(surf, Palette.GOLD_HI, (c, h - c - 1), 1)

        # Fundo-Direita
        pygame.draw.line(surf, Palette.GOLD, (w - c - 1, h - 2), (w - c - 1 - corner_len, h - 2), 1)
        pygame.draw.line(surf, Palette.GOLD, (w - 2, h - c - 1), (w - 2, h - c - 1 - corner_len), 1)
        pygame.draw.circle(surf, Palette.GOLD_HI, (w - c - 1, h - c - 1), 1)

        cls._cache[key] = surf
        return surf

    @classmethod
    def button_states(cls, size: tuple[int, int], variant: str = "menu") -> dict[ButtonState, pygame.Surface]:
        """
        Retorna dicionário de superfícies pré-renderizadas para cada ButtonState.
        Compartilhadas entre todos os botões do mesmo tamanho.
        """
        key = ("button_states", size, variant)
        if key in cls._cache:
            return cls._cache[key]  # type: ignore

        w, h = size
        w = max(6, w)
        h = max(6, h)
        cut = 5 if (w >= 48 and h >= 32) else 3

        def _make_button_surface(bg, border, corner_color, corner_len, inner_line=None, shadow_top=False):
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill(Palette.TRANSPARENT)
            pts = [
                (cut, 0),
                (w - cut, 0),
                (w, cut),
                (w, h - cut),
                (w - cut, h),
                (cut, h),
                (0, h - cut),
                (0, cut),
            ]
            # Fundo chanfrado
            pygame.draw.polygon(s, bg, pts)

            # Sombra interna no topo para estado PRESSED
            if shadow_top and h > 6:
                pygame.draw.line(s, (0, 0, 0, 140), (cut, 1), (w - cut, 1), 1)
                pygame.draw.line(s, (0, 0, 0, 90), (cut, 2), (w - cut, 2), 1)

            # Filete interno sutil
            if inner_line and w > 12 and h > 12:
                ci = max(1, cut - 2)
                ipts = [
                    (ci + 2, 2),
                    (w - ci - 3, 2),
                    (w - 3, ci + 2),
                    (w - 3, h - ci - 3),
                    (w - ci - 3, h - 3),
                    (ci + 2, h - 3),
                    (2, h - ci - 3),
                    (2, ci + 2),
                ]
                pygame.draw.polygon(s, inner_line, ipts, width=1)

            # Borda chanfrada
            pygame.draw.polygon(s, border, pts, width=1)

            # Cantoneiras em L
            if corner_len > 0 and corner_color:
                # Topo-Esquerda
                pygame.draw.line(s, corner_color, (cut, 1), (cut + corner_len, 1), 1)
                pygame.draw.line(s, corner_color, (1, cut), (1, cut + corner_len), 1)
                # Topo-Direita
                pygame.draw.line(s, corner_color, (w - cut - 1, 1), (w - cut - 1 - corner_len, 1), 1)
                pygame.draw.line(s, corner_color, (w - 2, cut), (w - 2, cut + corner_len), 1)
                # Fundo-Esquerda
                pygame.draw.line(s, corner_color, (cut, h - 2), (cut + corner_len, h - 2), 1)
                pygame.draw.line(s, corner_color, (1, h - cut - 1), (1, h - cut - 1 - corner_len), 1)
                # Fundo-Direita
                pygame.draw.line(s, corner_color, (w - cut - 1, h - 2), (w - cut - 1 - corner_len, h - 2), 1)
                pygame.draw.line(s, corner_color, (w - 2, h - cut - 1), (w - 2, h - cut - 1 - corner_len), 1)

            return s

        # 1. IDLE: Couro escuro, borda bronze 1 px, cantoneiras curtas (6 px)
        surf_idle = _make_button_surface(
            bg=(28, 22, 16, 235),
            border=Palette.BRONZE,
            corner_color=Palette.GOLD,
            corner_len=min(6, w // 4),
            inner_line=(70, 52, 28, 120),
        )

        # 2. HOVER: Borda dourada, cantoneiras estendidas (12 px), brilho interno, realce
        surf_hover = _make_button_surface(
            bg=(42, 32, 22, 250),
            border=Palette.GOLD,
            corner_color=Palette.GOLD_HI,
            corner_len=min(12, w // 3),
            inner_line=(140, 110, 45, 180),
        )
        # Losangos decorativos laterais no HOVER
        if w >= 80:
            cy = h // 2
            # Esquerda
            pygame.draw.polygon(
                surf_hover,
                Palette.GOLD_HI,
                [(6, cy), (8, cy - 2), (10, cy), (8, cy + 2)],
            )
            # Direita
            pygame.draw.polygon(
                surf_hover,
                Palette.GOLD_HI,
                [(w - 11, cy), (w - 9, cy - 2), (w - 7, cy), (w - 9, cy + 2)],
            )

        # 3. PRESSED: Fundo mais escuro (INK), rebaixamento tátil, sombra interna
        surf_pressed = _make_button_surface(
            bg=(14, 10, 6, 255),
            border=(80, 56, 26),
            corner_color=Palette.BRONZE,
            corner_len=min(4, w // 5),
            inner_line=None,
            shadow_top=True,
        )

        # 4. DISABLED: Dessaturado, borda cinza, sem cantoneiras douradas
        surf_disabled = _make_button_surface(
            bg=(28, 26, 24, 180),
            border=Palette.DISABLED,
            corner_color=None,
            corner_len=0,
            inner_line=None,
        )

        states_dict = {
            ButtonState.IDLE: surf_idle,
            ButtonState.HOVER: surf_hover,
            ButtonState.PRESSED: surf_pressed,
            ButtonState.DISABLED: surf_disabled,
        }
        cls._cache[key] = states_dict
        return states_dict

    @classmethod
    def glow(cls, size: tuple[int, int], color: tuple[int, ...] = Palette.GOLD, radius: int = 4) -> pygame.Surface:
        """
        Gera uma aura/brilho suave pré-renderizada para efeitos de destaque.
        Zero garbage por frame ao desenhar seleções e anéis pulsantes.
        """
        key = ("glow", size, tuple(color), radius)
        if key in cls._cache:
            return cls._cache[key]  # type: ignore

        w, h = size
        gw = w + radius * 2
        gh = h + radius * 2
        surf = pygame.Surface((gw, gh), pygame.SRCALPHA)
        surf.fill(Palette.TRANSPARENT)

        cr, cg, cb = color[0], color[1], color[2]
        for r in range(radius, 0, -1):
            alpha = int(90 * (1.0 - (r / (radius + 1))))
            step_rect = pygame.Rect(radius - r, radius - r, w + r * 2, h + r * 2)
            pygame.draw.rect(surf, (cr, cg, cb, alpha), step_rect, width=1, border_radius=4)

        cls._cache[key] = surf
        return surf

    @classmethod
    def ornament_divider(cls, width: int) -> pygame.Surface:
        """
        Desenha um divisor ornamental gótico: duas linhas horizontais
        afunilando nas extremidades com um losango central desenhado sem glifos.
        """
        key = ("ornament_divider", width)
        if key in cls._cache:
            return cls._cache[key]  # type: ignore

        w = max(40, width)
        h = 9
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill(Palette.TRANSPARENT)

        cx = w // 2
        cy = h // 2

        # 1. Linhas horizontais com afunilamento
        left_end = cx - 14
        right_start = cx + 14
        pygame.draw.line(surf, Palette.BRONZE, (8, cy), (left_end, cy), 1)
        pygame.draw.line(surf, Palette.BRONZE, (right_start, cy), (w - 8, cy), 1)

        # Realce dourado no centro da linha
        if left_end > 30:
            pygame.draw.line(surf, Palette.GOLD, (left_end - 24, cy), (left_end, cy), 1)
            pygame.draw.line(surf, Palette.GOLD, (right_start, cy), (right_start + 24, cy), 1)

        # 2. Losangos menores de suporte
        pygame.draw.polygon(
            surf,
            Palette.GOLD,
            [(cx - 10, cy), (cx - 8, cy - 2), (cx - 6, cy), (cx - 8, cy + 2)],
        )
        pygame.draw.polygon(
            surf,
            Palette.GOLD,
            [(cx + 6, cy), (cx + 8, cy - 2), (cx + 10, cy), (cx + 8, cy + 2)],
        )

        # 3. Losango principal central (sem glifo, desenhado proceduralmente)
        pts_diamond = [
            (cx, cy - 4),
            (cx + 5, cy),
            (cx, cy + 4),
            (cx - 5, cy),
        ]
        pygame.draw.polygon(surf, Palette.GOLD_HI, pts_diamond)
        pygame.draw.polygon(surf, Palette.GOLD_SHADOW, pts_diamond, width=1)
        pygame.draw.circle(surf, Palette.WHITE, (cx, cy), 1)

        cls._cache[key] = surf
        return surf


class IconAtlas:
    """
    Atlas de ícones vetoriais procedurais cacheados.
    Elimina dependência de glifos unicode/emojis ausentes na fonte.
    """

    NAMES: tuple[str, ...] = (
        "sword",
        "shield",
        "boot",
        "lightning",
        "sparkle",
        "eye",
        "speech",
        "campfire",
        "map",
        "backpack",
        "book",
        "gear",
        "coin",
        "chevron",
        "diamond",
    )

    _cache: dict[tuple[str, int, tuple[int, ...]], pygame.Surface] = {}

    @classmethod
    def get(
        cls,
        name: str,
        size: int = 24,
        color: tuple[int, ...] | None = None,
    ) -> pygame.Surface:
        """Obtém ou desenha proceduralmente um ícone vetorial do atlas."""
        target_color = Palette.GOLD if color is None else color
        color_tuple = tuple(target_color)
        key = (name, size, color_tuple)
        if key in cls._cache:
            return cls._cache[key]

        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill(Palette.TRANSPARENT)

        scale = size / 24.0

        def pt(x: float, y: float) -> tuple[int, int]:
            return (round(x * scale), round(y * scale))

        def clamp_w(w: float) -> int:
            return max(1, round(w * scale))

        col = color_tuple
        hi = Palette.GOLD_HI
        dim = Palette.BRONZE

        # Desenho vetorial de cada ícone do catálogo
        if name == "sword":
            # Espada diagonal: lâmina afiada, guarda e cabo
            pygame.draw.line(surf, col, pt(6, 18), pt(18, 6), clamp_w(2))
            pygame.draw.line(surf, hi, pt(10, 14), pt(19, 5), clamp_w(1))
            # Ponta da lâmina
            pygame.draw.polygon(surf, hi, [pt(18, 6), pt(21, 3), pt(16, 8)])
            # Guarda transversal
            pygame.draw.line(surf, dim, pt(6, 14), pt(10, 18), clamp_w(2))
            # Cabo e pomo
            pygame.draw.line(surf, dim, pt(6, 18), pt(3, 21), clamp_w(2))
            pygame.draw.circle(surf, hi, pt(3, 21), clamp_w(1.5))

        elif name == "shield":
            # Escudo heráldico medieval
            pts = [
                pt(4, 4),
                pt(20, 4),
                pt(20, 13),
                pt(12, 21),
                pt(4, 13),
            ]
            pygame.draw.polygon(surf, col, pts, width=clamp_w(2))
            # Fenda central / emblema
            pygame.draw.line(surf, hi, pt(12, 6), pt(12, 17), clamp_w(1))
            pygame.draw.line(surf, hi, pt(8, 10), pt(16, 10), clamp_w(1))

        elif name == "boot":
            # Bota de aventureiro: cano alto, salto e biqueira
            pts = [
                pt(7, 4),
                pt(13, 4),
                pt(13, 13),
                pt(19, 15),
                pt(20, 18),
                pt(18, 20),
                pt(7, 20),
                pt(7, 13),
            ]
            pygame.draw.polygon(surf, col, pts, width=clamp_w(2))
            # Sola/salto
            pygame.draw.line(surf, hi, pt(7, 20), pt(19, 20), clamp_w(2))
            pygame.draw.line(surf, dim, pt(7, 18), pt(9, 18), clamp_w(2))

        elif name == "lightning":
            # Raio em zigue-zague angular
            pts = [
                pt(13, 2),
                pt(7, 12),
                pt(12, 12),
                pt(10, 22),
                pt(18, 10),
                pt(13, 10),
            ]
            pygame.draw.polygon(surf, col, pts)
            pygame.draw.lines(surf, hi, True, pts, clamp_w(1))

        elif name == "sparkle":
            # Estrela mágica de 4 pontas
            pts = [
                pt(12, 3),
                pt(14, 10),
                pt(21, 12),
                pt(14, 14),
                pt(12, 21),
                pt(10, 14),
                pt(3, 12),
                pt(10, 10),
            ]
            pygame.draw.polygon(surf, col, pts)
            pygame.draw.circle(surf, hi, pt(12, 12), clamp_w(2))

        elif name == "eye":
            # Olho de observação místico
            pts = [
                pt(3, 12),
                pt(12, 6),
                pt(21, 12),
                pt(12, 18),
            ]
            pygame.draw.polygon(surf, col, pts, width=clamp_w(2))
            # Íris e pupila
            pygame.draw.circle(surf, hi, pt(12, 12), clamp_w(3))
            pygame.draw.circle(surf, Palette.INK, pt(12, 12), clamp_w(1.5))

        elif name == "speech":
            # Balão de diálogo com cauda
            pts = [
                pt(4, 5),
                pt(20, 5),
                pt(20, 16),
                pt(12, 16),
                pt(7, 20),
                pt(8, 16),
                pt(4, 16),
            ]
            pygame.draw.polygon(surf, col, pts, width=clamp_w(2))
            # Linhas de prosa interna
            pygame.draw.line(surf, hi, pt(7, 9), pt(17, 9), clamp_w(1))
            pygame.draw.line(surf, hi, pt(7, 12), pt(14, 12), clamp_w(1))

        elif name == "campfire":
            # Fogueira: toras na base e labaredas subindo
            # Toras cruzadas
            pygame.draw.line(surf, dim, pt(5, 19), pt(19, 15), clamp_w(2))
            pygame.draw.line(surf, dim, pt(5, 15), pt(19, 19), clamp_w(2))
            # Chamas
            flames = [
                pt(12, 3),
                pt(15, 9),
                pt(17, 8),
                pt(16, 15),
                pt(8, 15),
                pt(7, 9),
                pt(10, 10),
            ]
            pygame.draw.polygon(surf, col, flames)
            pygame.draw.circle(surf, hi, pt(12, 12), clamp_w(2.5))

        elif name == "map":
            # Pergaminho de mapa com cantos dobrados e rota
            pts = [
                pt(4, 5),
                pt(19, 4),
                pt(20, 18),
                pt(5, 19),
            ]
            pygame.draw.polygon(surf, col, pts, width=clamp_w(2))
            # Trilha pontilhada e 'X' de tesouro
            pygame.draw.line(surf, hi, pt(7, 14), pt(11, 10), clamp_w(1))
            pygame.draw.line(surf, hi, pt(11, 10), pt(14, 14), clamp_w(1))
            # 'X' no mapa
            pygame.draw.line(surf, Palette.BLOOD, pt(15, 8), pt(18, 11), clamp_w(1))
            pygame.draw.line(surf, Palette.BLOOD, pt(18, 8), pt(15, 11), clamp_w(1))

        elif name == "backpack":
            # Mochila de aventureiro: corpo, aba superior, fecho e bolso
            # Corpo
            pygame.draw.rect(surf, col, pygame.Rect(pt(5, 8), pt(14, 13)), width=clamp_w(2), border_radius=clamp_w(2))
            # Aba superior
            pygame.draw.polygon(surf, hi, [pt(4, 8), pt(20, 8), pt(17, 13), pt(7, 13)])
            # Fivela central
            pygame.draw.circle(surf, Palette.WHITE, pt(12, 14), clamp_w(1.5))
            # Alça superior
            pygame.draw.arc(surf, dim, pygame.Rect(pt(8, 4), pt(8, 6)), math.pi, 2 * math.pi, clamp_w(1))

        elif name == "book":
            # Livro/Grimório aberto
            # Capa externa
            pygame.draw.line(surf, dim, pt(3, 19), pt(12, 16), clamp_w(2))
            pygame.draw.line(surf, dim, pt(21, 19), pt(12, 16), clamp_w(2))
            # Páginas abertas
            p1 = [pt(4, 7), pt(11, 6), pt(11, 16), pt(4, 17)]
            p2 = [pt(13, 6), pt(20, 7), pt(20, 17), pt(13, 16)]
            pygame.draw.polygon(surf, col, p1, width=clamp_w(1))
            pygame.draw.polygon(surf, col, p2, width=clamp_w(1))
            # Lombada central
            pygame.draw.line(surf, hi, pt(12, 5), pt(12, 18), clamp_w(2))

        elif name == "gear":
            # Roda dentada / engrenagem
            center = pt(12, 12)
            r_inner = round(5 * scale)
            r_outer = round(9 * scale)
            pygame.draw.circle(surf, col, center, r_outer, width=clamp_w(2))
            pygame.draw.circle(surf, col, center, r_inner, width=clamp_w(1.5))
            # Dentes ortogonais e diagonais
            for angle in (0, 45, 90, 135, 180, 225, 270, 315):
                rad = math.radians(angle)
                x1 = center[0] + math.cos(rad) * (r_outer - 1)
                y1 = center[1] + math.sin(rad) * (r_outer - 1)
                x2 = center[0] + math.cos(rad) * (r_outer + 3 * scale)
                y2 = center[1] + math.sin(rad) * (r_outer + 3 * scale)
                pygame.draw.line(surf, hi, (round(x1), round(y1)), (round(x2), round(y2)), clamp_w(2))

        elif name == "coin":
            # Moeda de ouro com relevo
            center = pt(12, 12)
            pygame.draw.circle(surf, col, center, round(9 * scale), width=clamp_w(2))
            pygame.draw.circle(surf, dim, center, round(6 * scale), width=clamp_w(1))
            # Losango central gravado
            diamond_pts = [
                pt(12, 8),
                pt(15, 12),
                pt(12, 16),
                pt(9, 12),
            ]
            pygame.draw.polygon(surf, hi, diamond_pts)

        elif name == "chevron":
            # Seta grossa em '>' para chevrons de iniciativa e navegação
            pts = [
                pt(8, 5),
                pt(16, 12),
                pt(8, 19),
            ]
            pygame.draw.lines(surf, col, False, pts, clamp_w(3))

        elif name == "diamond":
            # Losango ornamental clássico ◆
            pts = [
                pt(12, 3),
                pt(19, 12),
                pt(12, 21),
                pt(5, 12),
            ]
            pygame.draw.polygon(surf, col, pts)
            pygame.draw.polygon(surf, hi, pts, width=clamp_w(1))
            pygame.draw.circle(surf, Palette.WHITE, pt(12, 12), clamp_w(1.5))

        else:
            # Fallback limpo caso seja solicitado nome não mapeado
            pygame.draw.rect(surf, col, pygame.Rect(pt(4, 4), pt(16, 16)), width=clamp_w(1))

        cls._cache[key] = surf
        return surf
