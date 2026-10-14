# Relatório 068 — Polimento do HUD, Grimório, Bestiário, Diário e Mecânicas de Combate

**Data:** 14/10/2026  
**Responsáveis:** Orquestrador Principal, `dev-frontend-ui`, `dev-backend-dnd`, `dev-ia-prompt`  
**Status:** ✅ Concluído e Validado (Suíte Global de Testes 100% OK)

---

## 1. Resumo Executivo das Implementações

Este ciclo de desenvolvimento solucionou todas as inconsistências visuais, ergonômicas e mecânicas apontadas pelo usuário durante a sessão de testes na Taverna (Beat 1) e na transição para a Planície dos Uivos (Beat 2).

---

## 2. Detalhamento por Área

### 2.1. Assets e Identidade Visual do Grimório e Mochila
* **Fim do Fundo Rosa/Magenta:** Os arquivos de alta definição foram normalizados e vinculados no [`AssetManager`](file:///c:/Users/iagob/RPGMesaPY/ui/asset_manager.py) com suporte aos nomes em português e inglês:
  * `Grimório Aberto.png` $\to$ `open_book.png` e `grimorio_aberto.png`.
  * `Mochila do Aventureiro.png` $\to$ `backpack_bg.png` e `mochila_aventureiro.png`.
* **Proteção contra Magenta:** Se uma textura de interface não for encontrada, o motor não preenche mais com Magenta `(255, 0, 255)`, ativando os painéis procedurais de pergaminho rústico.
* **Retrato do Taverneiro Desvinculado do Menestrel:** O Taverneiro foi isolado do fallback do bardo Maelor, buscando sua própria imagem ou fallback dedicado de hospedeiro.

### 2.2. Ficha & Equipamentos do Personagem (`GrimoireModal`)
* **Zero Sobreposição de Textos:** As métricas de combate da página direita (`Classe de Armadura`, `Iniciativa`, `Deslocamento`, `Bônus Proficiência`) foram remodeladas em **4 mini-cards 2x2 independentes**, eliminando a colisão de textos (`"Classe de Armadur18 CAIniciativa: +1"`).
* **Slots de Equipamento de Largura Total:** Os 4 slots da página esquerda agora ocupam a largura total da página (`page_w` ~324px), permitindo nomes de relíquias e armas longas (ex.: `"Escama Ancestral Incandescente"`) sem truncamento de texto (`..`).
* **Integração do Herói:** Pedestal e token do personagem foram integrados de forma harmônica ao pergaminho do livro aberto.

### 2.3. Diário de Missões e Árvore de Habilidades
* **Filtros do Diário (*Ativas*, *Rumores*, *Concluídas*):** Botões ampliados para 32px de altura, com auto-seleção imediata da primeira missão da categoria ao alternar a aba.
* **Árvore de Habilidades:** Hitbox expandido abrangendo o card inteiro (`card_rect`) e o ícone quadrado (`icon_rect`), tornando a inspeção de nós e a ativação de habilidades intuitiva e responsiva.

### 2.4. Bestiário Progressivo (Névoa de Guerra & Fichas Completas)
* **Descoberta Progressiva:** O motor rastreia `discovered_monsters` no estado do jogo. No Beat 1, criaturas não avistadas são listadas como `??? (Desconhecido) 🔒`, exibindo silhueta de interrogação e mensagem de exploração.
* **Ficha Completa de Monstros Descobertos:** Ao encontrar ou enfrentar a criatura, o Bestiário exibe:
  * Sprite real do monstro no topo da página.
  * Descrição de lore Dark Fantasy.
  * **Pontos Fortes** e **Fraquezas** táticas exploráveis.
  * CA, PV Estimados e Recompensa em XP.

### 2.5. Combate: Escala do Herói, Ataque por Clique e Barra de Atalhos
* **Escala Heroica do Personagem:** O token do herói no tabuleiro foi ampliado de 64px para **104px**, equilibrando sua estatura com a dos monstros humanóides (bandidos e orcs de ~115px).
* **Ataque por Clique Direto:** O motor agora registra as hitboxes dos inimigos no tabuleiro (`hitboxes[f"enemy_{id}"]` e `hitboxes[id]`). Clicar com o mouse sobre qualquer monstro durante o combate dispara imediatamente o ataque contra ele.
* **Feedback Visual de Mira:** Passar o mouse sobre a hitbox do inimigo em combate exibe destaque visual com tooltip `"⚔ Atacar"`.
* **Botão Contextual no `QuickActionBar`:** Em modo de combate (`is_combat`), o botão *Descansar* dá lugar ao botão dourado e vermelho `[⚔ Atacar]`.

### 2.6. Chat, Fala do Jogador e Inteligência Artificial
* **Eliminação de Mensagens Duplicadas:** Removido o envio duplo na fila da engine (`ui_queue.put`). Cada turno gera uma única mensagem narrativa consolidada.
* **Fala do Jogador Registrada no Chat:** Ao teclar Enter na caixa de texto, o turno do jogador é inserido imediatamente no histórico lateral (`[Você]: ...`).
* **Trava Anti-Avanço Involuntário de Beat:** Ações cotidianas na Taverna (*"sair da mesa"*, *"pedir cerveja"*, *"procurar missão"*) são tratadas estritamente como diálogo ou observação de cenário, impedindo transição prematura para o Beat 2.
* **Modelo Gemini & Fallback de Taverna:**
  * Modelo calibrado para o identificador oficial `gemini-2.5-flash`.
  * Fallback offline enriquecido para responder a diálogos de taverna, contratação de missões e rumores sobre a Trilha dos Enforcados sem cair no retorno genérico do menestrel.
* **Dado D20 no Centro da Tela:** Número renderizado com contorno preto sólido de 2px e tipografia destacada em ouro e branco, garantindo legibilidade nítida.

---

## 3. Validação por Testes Automatizados
* [`tests/test_ui_polish_and_fixes.py`](file:///c:/Users/iagob/RPGMesaPY/tests/test_ui_polish_and_fixes.py): 11 testes aprovados.
* [`tests/test_backend_engine_fixes.py`](file:///c:/Users/iagob/RPGMesaPY/tests/test_backend_engine_fixes.py): 7 testes aprovados.
* [`tests/test_ai_prompt_fixes.py`](file:///c:/Users/iagob/RPGMesaPY/tests/test_ai_prompt_fixes.py): 3 testes aprovados.
* Suíte global de testes do repositório: **100% de sucesso**.

