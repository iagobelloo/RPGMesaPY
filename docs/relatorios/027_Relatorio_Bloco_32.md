# Relatório de Execução: Bloco 32 - Ciclo de Vida e Morte Punitiva

## 1. Visão Geral
O **Bloco 32** implementou as fundações do sistema de Checkpoint (Hub & Spoke), a resolução de vitória no combate e a punitiva **Cascata de Morte**, estabelecendo o peso de se falhar nas rolagens em um cenário Dark Fantasy.

## 2. Alterações Realizadas (`core/game_engine.py`)

### A. Fundações de Checkpoint e Hub
- Adicionados ao `game_state` as chaves vitais para a persistência do mundo:
  - `last_checkpoint_type`: Local seguro onde o jogador renasce (ex: "TAVERNA").
  - `last_checkpoint_beat`: O instante da campanha em que o save ocorreu.
  - `suprimentos_acampamento`: Limitador para criar atrito durante as explorações fora do Hub (Taverna).

### B. O Gatilho de Vitória (`resolve_combat_victory`)
- **Limpeza e Restauro de Modo:** O Motor agora reconhece automaticamente quando as ameaças no campo (`active_combat_targets`) caem a 0 e transita o jogo devolta para `EXPLORACAO`.
- **Dano Persistente:** O HP do jogador **NÃO** é curado. A Vitória é punitiva; apenas o XP é computado.
- **Saída Narrativa:** Dispara um evento dual, primeiro enviando o ganho de XP bruto para a interface de log, e a seguir despachando um prompt para o Narrador Visceral encerrar a cena de tensão adequadamente.

### C. A Cascata de Morte (`resolve_player_death`)
A morte no RPG passou a ser tratada com uma hierarquia estrita para balancear frustração e desafio.

*   **Condição A (O Déjà Vu do Boss):** Se o jogador for morto no embate contra o Boss Final (Beat 4), ele desperta ofegante. O Snapshot recarrega os atributos exatos de antes do combate começar e a luta recomeça, prevenindo o *permadeath* frustrante apenas nesta etapa.
*   **Condição B (Ressurreição por Item):** Uma verificação de inventário atua como gancho (*hook*). Caso possua um item mítico, o jogador volta imediatamente à vida com penalidades, permitindo a continuidade do combate.
*   **Condição C (Permadeath & Load System):** A regra primária. A IA narra brutalmente o último suspiro do herói. A fila da UI é limpa, enviando um log fatal e bloqueando a progressão para, em seguida, forçar o método `load_game()`. O sistema é religado nas exatas condições mecânicas de seu último descanso real na Taverna ou Acampamento.

## 3. Verificação de Ciclo
O loop de turnos assíncronos (`_async_turn_processor`) foi reestruturado de modo que as verificações de estado (`resolve_player_death` e `resolve_combat_victory`) sejam a última porta lógica processada. Isso garante que:
1. O jogador faça sua ação e sofra a reatividade matemática.
2. A inteligência artificial dos monstros (`process_enemies_turn_batch`) aplique seu lote de danos predatórios e mortais no jogador ou aliados.
3. **Por fim**, as consequências globais (Morte ou Vitória) sejam julgadas antes da UI destravar o terminal para a leitura humana.

## 4. Testes (`test_bloco_32.py`)
Um Mock Script comprovou o Permadeath. O jogador fictício teve o HP zerado em um cenário de embate contra um lacaio. O motor enviou corretamente os blocos JSON de narrativa fatal para a Fila, emitiu o alerta `[SISTEMA FATAL]` e comprovou o reload acionando `load_game()` e reiniciando a máquina de estados.
