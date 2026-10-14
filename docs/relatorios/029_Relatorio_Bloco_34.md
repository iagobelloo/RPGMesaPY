# Relatório de Execução: Bloco 34 (Fase 1) - O Arsenal do Herói

## 1. Visão Geral
O **Bloco 34** engloba a implementação do consumo de itens do inventário, em especial os utilitários e poções curativas. O sistema permite o cálculo da cura baseada nos dados do item e o roteamento correto de tempo (Turnos em Exploração versus Combate).

## 2. Alterações Realizadas

### A. Parser de Dados (`core/dice_engine.py`)
- Adicionada a função estática `parse_and_roll_dice(dice_string)` ao `DiceEngine`. Ela lê valores complexos (ex: "2d4+2", "1d8", "3d6-1"), executa as rolagens e retorna a matemática limpa (int).

### B. O Roteador de Consumo (`core/game_engine.py`)
- Injetada a validação do tipo de ação `"USAR_ITEM"`.
- O código mapeia o input textual para encontrar o item real dentro do banco de dados `data/items.json`.
- A quantidade do inventário lógico (`self.game_state["inventory"]`) é decrementada, respeitando a posse do item.
- A **Bifurcação de Turno** foi finalizada:
  - Se `game_mode == "EXPLORACAO"`, o jogador se cura, o log é exibido e a UI retorna ao usuário livremente.
  - Se `game_mode == "COMBATE"`, a ação cai na regra do *Soft-Lock Prevent*. A interface NÃO é devolvida; em vez disso, o turno flui para a Matemática e depois chama o motor de `process_enemies_turn_batch`, garantindo que os inimigos revidem no mesmo ciclo da UI Queue, com a *saída dupla combinada*.

### C. A Narrativa Visceral (`ai_client.py`)
- Modificada a instrução estrita da Fase 2 para as Poções. Em vez de simplesmente "Você tomou uma poção", o LLM é instruído a relatar espasmos, amargor do sangue, vidro quebrando entre dentes e fisicalidade explícita exigida pelo design *Dark Fantasy*.

## 3. Correção Lógica e Duplicação (Bugfix)
- **Problema de Duplicação Identificado:** Originalmente, o uso de um item em combate imprimia dois diálogos de narrativa (um criado no router e outro recriado no pipeline normal de fase 2 pós-matemática). 
- **Solução (Anti-Duplicação):** A lógica foi refatorada. Ao invés de o motor roteador invocar o Mestre, ele empacota a string `"[SISTEMA] Usou Poção..."` dentro do JSON como `log_precalculado`. A `resolve_action` simplesmente absorve esse log bruto e a fase final (Fase 2 padrão) toma controle exclusivo sobre a geração textual, mesclando com o contra-ataque do monstro.

## 4. Resultados do Teste Mock
O `test_bloco_34.py` provou que:
1. O HP subiu para a matemática correta através de 2d4+2.
2. O inventário deduziu corretamente (`3 -> 2`).
3. O LLM gerou com sucesso o *Flavor* amargo para o consumo de itens.
4. O ciclo dos inimigos foi ativado, unificando a cura e o ataque sofrido no mesmo *chat bubble*.
