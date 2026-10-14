# Relatório de Atualização - Fase 2 da UI

**Missão:** Refatoração da UI - Prólogo Estático, Clean Menus e Escalonamento de Pixels.
**Perfis:** Dev Frontend UI & Core Logic

A Fase 2 de polimento e correção de UI foi concluída com as seguintes intervenções cirúrgicas:

### 1. Desvinculação do Prólogo Dinâmico (IA)
- O fluxo inicial de transição entre o Menu de Criação (`CHARACTER_CREATION`) e a Sessão Zero (`SESSION_ZERO`) no `main.py` foi completamente reescrito.
- A chamada à inteligência artificial (`ai_master.generate_prologue_questions` e afins) foi desativada e a `SESSION_ZERO` foi ignorada, pulando diretamente para `IN_GAME`.
- Agora, o prólogo carrega o texto estático do arquivo `game_cutscenes.json` sob a chave `"beat_1_prologue"`.
- Respeitando o princípio do encapsulamento da Fase 1, o texto é injetado diretamente criando uma nova instância de `current_bubble_message` e inserindo no histórico (`recent_history`). Assim, a engine de paginação (criada na Fase 1) detecta automaticamente um novo `id` de dicionário e renderiza as páginas de maneira orgânica.

### 2. Painéis Modulares Retrô (`ui/hud_components.py` e `ui/menu_components.py`)
- O carregamento de texturas esticadas ("wood_panel" e "parchment") em modais de menu (como o Menu de Pausa e o Diário) foi removido na origem (`draw_ui_panel`).
- O método foi substituído por uma criação 100% programática (`Surface` com `pygame.SRCALPHA`) que não sofre distorções de escala. Ele desenha um painel semitransparente escuro `(20, 20, 20, 220)` envolto em uma moldura fina, rústica e sólida `(212, 175, 55)` (Ouro Envelhecido).
- As cores de texto do Diário (`JournalModal`) foram invertidas, trocando `COLOR_INK` por `COLOR_PARCHMENT` para um contraste visível e elegante contra os novos painéis escuros.

### 3. Ajuste de Pixel Scaling e Desfoque (`ui/asset_manager.py`)
- Backgrounds borrados foram diagnosticados como vítimas da interpolação de subpixels causada pelo método `pygame.transform.smoothscale`.
- Todos os redimensionamentos de cenário no carregamento (`AssetManager.get_background`) foram corrigidos substituindo `smoothscale` por um `pygame.transform.scale` estrito, forçando bordas rígidas no estilo Pixel Art.
- A função universal de caching (`AssetManager.get_scaled`) teve o seu valor padrão invertido para `smooth=False`, prevenindo distorções futuras no redimensionamento on-the-fly.

Os modais da interface e os cenários do mundo agora apresentam alta legibilidade e respeito à estética medieval e hard-pixel.
