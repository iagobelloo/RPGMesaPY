# Relatório de Correção: Bloco 39 (Restauração da Estética Pixel Art e Centralização de Fontes)

**Status:** Concluído com Sucesso ✅

## 1. O Problema Original
A tentativa anterior de resolver problemas de codificação UTF-8 resultou na substituição de todas as fontes por `SysFont("Arial")`. Isso quebrou a Direção de Arte de Dark Fantasy do jogo e causou grandes quedas de FPS devido à instanciação contínua de objetos `Font` dentro do loop de renderização (Memory Leaks).

## 2. A Solução Implementada

### 2.1 Gestor Central de Fontes (AssetManager)
Modificamos o ficheiro `ui/asset_manager.py` para incluir o método `get_font()`.
- **Cache de Desempenho:** As fontes são agora instanciadas uma única vez e armazenadas num dicionário (cache) em memória `_fonts`, utilizando uma tupla `(size, bold, italic)` como chave, prevenindo o Memory Leak e a queda de FPS.
- **Carregamento da Fonte Pixel Art:** O sistema tenta carregar o arquivo customizado do utilizador (`assets/fonts/pixel_font.ttf`).
- **Fallback de Segurança:** Caso a fonte não seja encontrada, usamos blocos `try/except` para instanciar a "Arial" (`SysFont`) com as proporções requeridas sem estourar nenhum erro no ecrã do jogador.
- **Suporte Extendido:** O método `get_font` foi atualizado com suporte nativo aos atributos `bold` e `italic` sem conflitar as chaves em cache.

### 2.2 Refatoração Global das Interfaces
Percorremos todos os painéis e ecrãs do jogo substituindo a chamada direta por requisições ao Gestor Central de Ativos (`AssetManager.get_font(...)`):
- `ui/scene_renderer.py` (HUD de topo, Balões de Diálogo, Títulos Narrativos)
- `ui/hud_components.py` (Caixa de Chat, Overlay da Ficha do Personagem, Painel Principal, Grimório)
- `ui/menu_components.py` (Criação de Personagem, Modais de Seleção de Raças/Classes, Sessão Zero, Diário de Aventuras, Menus de Pausa)
- `ui/renderer.py` (Módulo Visual Legado, convertendo a fonte padrão de *Cambria* para a nova pipeline)

### 2.3 Tratamento UTF-8 Rigoroso (JSON)
Confirmámos de ponta-a-ponta, através de buscas em regex na codebase de forma automatizada, que todos os processos de manipulação e abertura de ficheiros (função `open`) a nível do Backend e Frontend (incluindo `core/game_engine.py`, `core/story_engine.py`, etc) contêm a flag estrita `encoding='utf-8'`. Os acentos portugueses (ex: Clérigo, Herói) agora renderizam na perfeição dentro da fonte pixel art e não corrompem os loaders JSON.

## 3. Próximos Passos
Com a interface polida e a estética em rigor com a narrativa Dark Fantasy, sugerimos progredir em direção aos novos blocos de mecânicas avançadas (como UUID dinâmico de inimigos, remoção e purga de cadáveres do ecrã e as condições de vitória do boss final em `Bloco 40`). 

A integração visual está estável. Tudo limpo!
