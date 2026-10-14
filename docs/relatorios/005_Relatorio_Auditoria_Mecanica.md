# Relatório de Auditoria Mecânica e Arquitetural (D&D 5e)

Abaixo estão detalhados os apontamentos de arquitetura solicitados para o Módulo de Combate. As falhas apontadas pelo Diretor foram auditadas e as sugestões de melhoria estão devidamente mapeadas.

### 1. Bestiário e Inimigos (core/dnd_rules.py)
**Diagnóstico:** O nosso `BESTIARIO_5E` **JÁ POSSUI** as chaves estruturais completas! Os inimigos cadastrados possuem `pv_max`, `ca`, `cr`, e a sub-chave vital `mods` contendo os atributos (FOR, DES, CON, INT, SAB, CAR).
**O que foi corrigido:** No MVP da Fase 1 (`combat_system.py`), a magia estava rolando Testes de Resistência assumindo o modificador como `+0`. Acabei de criar o *patch* no código para que a magia extraia dinamicamente o modificador correto usando `status.get("mods", {}).get(resist, 0)`! Agora, a Bola de Fogo tem muito mais chance de falhar contra um "Lacaio Goblin" (DES alta) do que contra um Zumbi.

### 2. Movimentação e Posicionamento (VTT vs Teatro da Mente)
**Diagnóstico:** O nosso VTT opera 100% no **Teatro da Mente** no que tange a posições! A Fase 0 (LLM) apenas sabe os *Nomes dos Cenários* (`mudanca_cenario`) e os *Nomes dos Alvos*.
**Falha Estrutural:** Não existe Grid Tático real (matriz X,Y) gerido pelo Pygame no back-end. A IA deduz se a Bola de Fogo atinge dois goblins baseado na *descrição em texto livre* do jogador.
**Melhoria Pós-MVP:** Para plugar a movimentação física de 1,5m, precisaríamos:
1. Adicionar `posição: [X,Y]` em cada monstro no `active_combat_targets`.
2. Fazer o parser devolver `{"movimento": [10, 15]}`.
3. O `game_engine.py` calcular a distância Pitagórica e barrar o movimento se for maior que o `deslocamento_m` do jogador/inimigo.

### 3. Regras e Rolagem de Dados (Magias e Inventário)
**Diagnóstico:** O LLM **NÃO** rola dados. Toda a matemática é feita no Python (`Fase 1 - combat_system.py`). 
**Falha de Magias:** Nós não temos um Dicionário de Magias (como temos um `BESTIARIO_5E`). Se o jogador escreve "Bola de Fogo", a Fase 1 usa uma Regex para tentar achar um dano em formato "XdY" dentro da string ou cai no fallback genérico de `2d6`.
**Falha de Inventário:** Como você bem apontou, a verificação feita foi insegura (`if "poção" in item.lower()`). Sim, se ele bebesse uma "Poção de Veneno", o motor de cura base atual acionaria a restauração de PV!
**Melhoria Pós-MVP:** 
1. Criar um `MAGIAS_5E` em `dnd_rules.py` (contendo dados como `"Bola de Fogo": {"dano": "8d6", "save": "DES"}`).
2. Trocar Strings por IDs exatos de Itens (ex: `"id": "potion_healing_minor"`) no dicionário de Inventário.

### 4. Gestão de Tempo (TurnManager e Iniciativa)
**Diagnóstico:** Não existe fila cronológica ou Rolagem de Iniciativa clássica!
**Arquitetura Atual:** Quando o jogador bate o `Enter`, ele joga o turno dele. No *MESMO* ciclo, a Inteligência Artificial decide a reação imediata (`"reacao_inimigos"`) dos inimigos sobreviventes. Eles contra-atacam instantaneamente.
**Falhas:** 
1. Monstros não atacam sozinhos se o jogador decidir "não fazer nada". 
2. Magias como *Escudo da Fé* (1 minuto) não expiram, pois o `game_state` não possui um contador progressivo de Rounds.
**Melhoria Pós-MVP:** Plugar o `self.turn_manager` que já está criado na classe `SessionManager`, fazendo-o iterar sobre uma lista de `iniciativa` e usar um `round_counter` para debuff/buff.

---
**Conclusão:** O Motor está extremamente sólido como um RPG Narrativo Automatizado. O LLM atua apenas como "Parseador" e "Narrador". Toda a glória matemática está em código, mas carece de tabelas rígidas de Magias e Itens. Seguimos sob sua liderança!
