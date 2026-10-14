# Relatório: Missão Bloco 40 - Lixeiro Atrasado e Condição de Fim de Jogo

## 🎯 Objetivo
Manter os inimigos mortos na lista de alvos o tempo suficiente para que o LLM narre suas mortes ("Estado Fantasma"), impedir que sejam alvejados por lógicas de combate ou desenhados na UI, executar um coletor de lixo após a narrativa e gerenciar o fim de jogo (EPILOGO) após derrotar o Boss.

## 🛠️ Modificações Realizadas

### 1. Injeção da Flag de Morte (Estado Fantasma)
- **Arquivo:** `core/combat_system.py`
- A função de aplicação de dano foi ajustada para não deletar imediatamente os inimigos com HP <= 0.
- Agora, quando uma entidade morre (seja NPC ou o Player), a chave `"status": "morto"` é injetada no dicionário da entidade.
- O XP continua sendo calculado e adicionado normalmente no exato momento do dano letal.

### 2. Filtro de Targeting e Cegueira Visual
- **Backend (`core/combat_system.py` e `core/game_engine.py`):**
  - Funções de seleção de alvo (`get_valid_targets`) agora ignoram ativamente qualquer entidade que possua `"status" == "morto"`.
  - O jogador e os inimigos não podem alvejar fantasmas.
- **Frontend (`ui/scene_renderer.py`):**
  - O loop de renderização `draw_in_game` ignora os NPCs mortos. Suas barras de vida e sprites desaparecem instantaneamente da tela ao morrerem.

### 3. Coletor de Lixo Atrasado (Lixeiro Pós-Narrativa)
- **Arquivo:** `core/game_engine.py`
- Modificamos a construção do `temp_state` enviado ao LLM: os cadáveres (com `"status": "morto"`) são enviados na lista `active_combat_targets`, garantindo que o LLM narre o golpe fatal.
- Imediatamente **após** o retorno da narrativa do LLM em `process_turn`, iteramos sobre `active_combat_targets` e `active_visual_npcs`, removendo fisicamente da memória todos os inimigos que possuam a flag `"status": "morto"`.
- Adicionamos um failsafe extra que deleta a chave `"status": "morto"` da resposta caso ela venha ser passada de volta pelo narrador na atualização de status do turno.

### 4. Resolução de Combate e o Fim do Jogo (EPILOGO)
- **Arquivo:** `core/game_engine.py`
- `check_combat_resolution` agora dá prioridade absoluta à morte do jogador (`hp <= 0` ou `"status" == "morto"`).
- Se todos os inimigos estão mortos (`all_dead`):
  - **Beat < 15:** O jogo transiciona para `EXPLORACAO`, e as listas de combate e NPCs visuais são limpas usando `.clear()`.
  - **Beat == 15:** Transiciona o jogo para o novo modo `"EPILOGO"` e insere o prompt de finalização da campanha para o Narrador gerar.
- **Arquivo:** `main.py`
- Os manipuladores de evento da ChatBox foram modificados: no modo `EPILOGO` (ou `GAME_OVER`), as teclas e a renderização da caixa de chat são bloqueadas/ocultas, simulando uma Cutscene Cinematográfica e finalizando o Loop de Gameplay.

## 🚀 Próximos Passos
O jogo agora roda fluidamente através da história, gerencia mortes sem quebrar a UI, e termina adequadamente no Ato Final. Aguardamos as próximas instruções!
