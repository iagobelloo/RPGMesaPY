# 🎨 DIRETRIZES DO AGENTE DE FRONT-END (PYGAME & UI)
**Cargo:** Especialista em Interface Gráfica, Pygame, HUD, Renderização e Performance Visual.  
**Objetivo:** Manter a renderização contínua do VTT a 60 FPS lisos, gerenciar a estética Dark Fantasy 2.5D, garantir a separação e ergonomia do layout (Painel de Diálogo/Chat lateral ou inferior vs. Grid de Combate e Cenário) e assegurar ausência total de vazamento de memória (Memory Leaks).

---

## 1. Isolamento de Domínio (Regra de Ouro)
Você tem permissão EXCLUSIVA para ler e editar os seguintes arquivos:
* `ui/scene_renderer.py` (Lógica de renderização de cenas, caixas de diálogo, animações não-bloqueantes, barras de vida)
* `ui/hud_components.py` (GrimoireModal em livro aberto, QuickActionBar, ChatBox, botões de ação, status de combate, janelas de rolagem de dados)
* `ui/menu_components.py` (InventoryBackpackModal, SessionZeroPanel, PauseMenuPanel e telas de criação de personagem)
* `ui/asset_manager.py` (Carregamento centralizado de imagens/fontes, cache de texturas e escalonamento)
* `main.py` (EXCLUSIVAMENTE para setup da janela Pygame, captura de eventos e chamada de renderização)
* `assets/` (Organização de sprites, imagens de fundo e fontes)

**É ESTRITAMENTE PROIBIDO:**
* Alterar a matemática de combate (`core/combat_system.py`), regras D&D (`core/dnd_rules.py`) ou chamadas de LLM (`ai_master/ai_client.py`).
* Se houver falha de cálculo ou regras quebradas, solicite intervenção do Agente de Back-End.

---

## 2. Performance Extrema & Regras de 60 FPS (Zero Garbage por Frame)
1. **Proibido Alocar Surfaces Transparentes no Loop:** NUNCA crie `pygame.Surface((w, h), pygame.SRCALPHA)` a cada frame dentro do loop de renderização (em botões, painéis, barras ou caixas de texto). Superfícies com canal alpha devem ser instanciadas uma única vez ou cacheadas/pré-renderizadas.
2. **Proibido Word-Wrap a Cada Frame:** Quebras de linha e medições de largura de texto devem ser executadas no momento em que a mensagem entra no log (`add_combat_log`), e NÃO a cada frame de desenho do chat.
3. **Proibido `time.sleep()`:** Toda e qualquer animação deve ser não-bloqueante, avançando com base em contadores de frames ou delta time.
4. **Gerenciamento de Cache de Texturas:** O `AssetManager` deve implementar limpeza de cache (`clear_cache`) ao trocar de cenários ou encerrar combates para evitar acúmulo infinito de texturas na RAM.
5. **Pré-renderização de Componentes:** Botões (`draw_ui_button`) e elementos visuais estáticos devem utilizar estados pré-renderizados (Normal, Hover, Desativado) em cache, realizando apenas `blit` durante o ciclo de desenho.

---

## 3. Padrão Visual do VTT & Ergonomia de Tela
1. **Painel de Diálogo e Chat Lateral:**
   - O painel de texto ocupa proporção controlada (ex: até 40% da largura da tela no canto esquerdo ou base).
   - Renderização top-to-bottom clara das mensagens, com suporte a rolagem fluida (`scroll_y`) e barra de rolagem visual dourada/bronze.
   - Limite máximo estrito no histórico de mensagens (ex: limite de 40 mensagens ativas com descarte das mais antigas) para prevenir vazamento de memória e perda de FPS.
2. **Portraits vs. Tokens de Combate:**
   - Imagens com identificador `icone` ou retratos são exclusivas para caixas de diálogo e painéis de quem está falando.
   - Tokens de combate no grid utilizam sprites de corpo inteiro/criatura, escalados de acordo com o tamanho do Bestiário (1 = normal, 2 = grande, 3 = enorme/chefe).
3. **Componentização e DRY:**
   - Componentes visuais idênticos (como painéis de seleção de atributos, raças e classes) devem compartilhar uma classe genérica parametrizada (`GenericSelectionPanel`), evitando código duplicado.
4. **Fallbacks Visuais Seguros:**
   - Caso um sprite ou imagem de fundo falhe ao carregar, o sistema deve renderizar uma forma geométrica estilizada com cores sólidas ou gradiente sem interromper o jogo.
5. **Grimório Bilateral em Livro Aberto (GrimoireModal):**
   - Renderização estética em pergaminho/madeira com abas superiores (`Habilidades`, `Bestiário`, `Diário / Missões`, `Status`).
   - Aba Diário com 3 filtros rápidos (`Ativas`, `Rumores`, `Feitas`) e botões contextuais de ação (`[ Aceitar Missão ★ ]` e `[ Partir em Viagem ➔ ]`).
   - Todos os cálculos de layout de páginas (esquerda/direita) devem ser proporcionais e relativos a `self.rect`, sem poluição de lixo na memória.