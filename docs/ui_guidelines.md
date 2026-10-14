# DIRETRIZES ABSOLUTAS DE UI/UX E ENGENHARIA (RPGMesaPY)

Este documento dita as regras imutáveis de renderização, performance e identidade visual para o motor Pygame deste projeto. Nenhuma refatoração futura pode violar estes paradigmas.

## 1. PERFORMANCE E CARREGAMENTO DE ASSETS (STABLE 60 FPS)
* **Proibido I/O no Loop de Renderização:** É ESTRITAMENTE PROIBIDO usar `pygame.image.load()`, `pygame.transform.scale()` de artes pesadas ou `AssetManager.get_image()` dentro de métodos `draw()` ou `update()`.
* Todos os assets pesados DEVEM ser carregados e redimensionados UMA ÚNICA VEZ no método `__init__` das classes.
* Não use `time.sleep()` em lugar nenhum. Use `pygame.time.get_ticks()` para animações, cursores piscantes e fade-outs.

## 2. PARADIGMA VISUAL (JRPG / POINT-AND-CLICK)
* **Cenários Pré-Renderizados:** O motor NUNCA desenha mesas ou paredes com primitivas (`draw.rect`). O fundo é SEMPRE uma arte isométrica/perspectiva carregada de `assets/backgrounds/` (`menu_bg` ou `tavern`).
* **Resiliência de Assets (Fallbacks):** Se uma imagem não for encontrada, o jogo NÃO PODE crashar. O `AssetManager` deve interceptar o erro silenciosamente e usar placeholders genéricos (ex: `hero.png` genérico, ou `monster.png`).

## 3. A REGRA DO "SANDUÍCHE DE INTERFACE" (MENUS E MODAIS)
Telas estáticas (MainMenu, Criação de Personagem, Menu de Pausa, Grimório) devem seguir estritamente esta ordem de camadas no método `draw`:
1. **Fundo:** `screen.blit` da arte do cenário em tela cheia (Layers inferiores).
2. **Dark Overlay:** Um `pygame.Surface` preto cobrindo a tela inteira com `set_alpha(150)` para desfocar o fundo e gerar contraste.
3. **Painéis UI:** Renderização das caixas modulares (`draw_ui_panel` com texturas de pergaminho/madeira).
4. **Elementos:** Textos e botões sempre em alto contraste por cima dos painéis.

## 4. LAYOUT TÁTICO IN-GAME (TABULEIRO E HUD)
* **Top HUD (Party Bar):** Os status vitais (Rosto 64x64, HP, MP, XP) NUNCA flutuam soltos na tela. Ficam ancorados EXCLUSIVAMENTE em uma barra horizontal limpa no topo da tela.
* **Miniaturas (Tabuleiro Físico):** Inimigos e heróis em combate são miniaturas (aprox. 48x48 a 64x64) alocadas na metade inferior da tela. 
* **Sombras de Contato:** Toda miniatura DEVE ter uma sombra (`pygame.draw.ellipse` translúcido preto) renderizada logo abaixo de seus pés, criando a ilusão de peso sobre a madeira da mesa.
* **Balões de Fala (Speech Bubbles):** Fundo `#FFFFFF`, bordas sólidas `#000000`, texto escuro. Sempre renderizados dinamicamente ACIMA da cabeça da miniatura (`Y - altura_do_balao - margem`), nunca cobrindo as artes.
* **Feedback Dinâmico:** Recompensas de IA (XP, Ouro, Itens) devem acionar *Floating Texts* com animação de subida e fade-out (alpha decrescente). O Input de Chat deve usar limitação matemática de largura para não vazar texto da tela.
