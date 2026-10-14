# A "Bíblia" do Motor VTT

Este documento contém as **Regras Absolutas de Arquitetura** do projeto. Quaisquer modificações futuras DEVEM seguir estas diretrizes para manter o código saudável e escalável.

## 1. Arquitetura (MVC Estrito)
O projeto é dividido em camadas que não devem se misturar:
- **Engine (Model/Controller):** `core/game_engine.py` mantém o estado do jogo e gerencia mecânicas físicas, dados e salvamentos. NENHUMA lógica do Pygame (renderização) deve existir aqui.
- **UI (View):** `ui/scene_renderer.py`, `ui/hud_components.py` e `ui/menu_components.py`. NENHUMA alteração do estado do jogo (como subtrair HP ou dar Itens) deve acontecer aqui, apenas emitir eventos que o `game_engine.py` consome.
- **AI (AIGameMaster):** `ai_master/ai_client.py`. Recebe estado puro e joga um JSON interpretável. Nunca dita UI ou manipula o Pygame.

## 2. UI Paradigm (Programático e Modular)
- **Grid/Flexbox:** É PROIBIDO usar coordenadas absolutas amarradas a imagens estáticas de tela cheia para a criação de menus ou de UI (Interfaces). Tudo deve ser desenhado na tela usando matemáticas flexíveis de bounding boxes (`pygame.Rect`) baseadas no tamanho da janela (`SCREEN_WIDTH` / `SCREEN_HEIGHT`).
- **Recursos Modulares:** Para desenhar janelas e botões, use a abordagem retrô modular. Painéis devem usar pequenas texturas (`wood_panel.png`, `parchment.png`) escalonadas (`pygame.transform.scale`). 
- **Fallback Estético:** Caso a textura não exista, a UI deve apresentar um fallback *Pixel Art* utilizando caixas geométricas com múltiplas bordas simulando profundidade e sombras. NUNCA use cores chapadas sem profundidade.
- **Legibilidade e Contraste:** Textos sobre fundos escuros DEVEM ser Brancos (#FFFFFF) ou Bege (#F5F5DC). Textos sobre fundos claros (Pergaminho) DEVEM ser Pretos (#000000) ou Tinta (#1A1A1A). Não permita sobreposição (calcule o espaçamento em Y dinamicamente).

## 3. Caminhos de Assets Estritos
O sistema de arquivos deve ser blindado contra diferenças de SO (Windows vs Linux).
- O uso de `os.path.normpath(os.path.join(...))` é OBRIGATÓRIO.
- **Pastas Ativas:**
  - `assets/ui/` (Botões, Painéis, Fontes Visuais).
  - `assets/backgrounds/` (Cenários como tavernas, florestas). O Pygame DEVE redimensioná-los em full-screen no SceneRenderer.
  - `assets/sprites/heroes/` (Tokens de Jogadores). Fallback obrigatório para `hero.png`.
  - `assets/sprites/enemies/` (Tokens de Inimigos/Monstros). Fallback obrigatório para raça simples ou `monster.png`.
  - (Sempre garanta o uso do canal alpha para os tokens lidos via `convert_alpha()`).

## 4. Diretrizes In-Game (Scene Renderer)
- **Redimensionamento Oculto:** O SceneRenderer (`scene_renderer.py`) deve carregar e redimensionar internamente os sprites (`assets/sprites/...`) para que todos fiquem no tamanho padronizado de um Token de Mesa (ex: 128x128).
- **Alinhamento Tático:** Para transparecer a natureza do RPG de mesa:
  - Tokens de Inimigos e do Mestre ficam sempre na metade superior da tela.
  - Tokens de Jogadores (PC) ficam sempre na metade inferior da tela.

## 5. IA Master (AI Client)
- **Domesticação (Alta Fantasia Clássica):** A IA DEVE narrar estritamente no estilo D&D 5e Clássico (Alta Fantasia Heroica). É **ABSOLUTAMENTE PROIBIDO** criar histórias sombrias (edgy), bizarras, escatológicas ou inventar traumas de infância complexos do nada. O mestre deve entregar ganchos de aventuras épicas (ex: salvar a vila, explorar ruínas, boatos em tavernas).
- **A Coleira de Verbosidade:** O Mestre (LLM) é terminantemente proibido de vomitar parágrafos gigantes. O limite é de 3 frases por turno de combate e perguntas de Sessão Zero.
- **Filtro Anti-Lixo:** A IA possui regras sistêmicas rígidas para responder à insanidade de usuários ou comandos vazios (ex: `aaa`) com falas confusas "em personagem", punindo metagaming mas sem quebrar a API ou iniciar combates fictícios.
- **Danos Matemáticos Exatos:** O Mestre não controla as rolagens. Ele recebe o D20 e os Modificadores, usa isso para decidir o sucesso e escreve o JSON de "combat_log" de volta explicando a mecânica (ex: `Rolou D20(15) + STR(3) = 18`).
