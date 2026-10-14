# Relatório de Execução: Bloco 33 - O Sistema de Descanso, Atrito e Emboscada Noturna

## 1. Visão Geral
O **Bloco 33** implementou a mecânica de descanso, equilibrando cura vitalícia com risco tangível (Atrito). O jogador agora pode curar suas feridas e salvar o jogo dependendo do ambiente em que tenta repousar, correndo o risco de ser emboscado nas terras ermas.

## 2. Alterações Realizadas

### A. Expansão NLP e Prompt Narrativo (`ai_client.py`)
- O Extrator Silencioso (Fase 0) agora reconhece a ação `DESCANSAR`.
- Adicionadas diretrizes específicas para o Narrador Visceral (Fase 2) gerar diferentes qualidades descritivas: calor do fogo na Taverna, sono reparador no Ermo seguro, ou sobressalto tenso em uma emboscada.

### B. O Roteador de Descanso (`core/game_engine.py`)
Adicionado o fluxo de decisão assíncrono para o descanso na `SessionManager`:
- **Trava de Adrenalina:** Se o jogo já estiver no modo `COMBATE`, o descanso é abortado imediatamente (log e saída limpa para a UI).
- **Descanso no Hub (Beat <= 1):** O jogador recupera 100% de seu HP e reabastece seu único suprimento de acampamento (`suprimentos_acampamento = 1`). A partida é salva.
- **Descanso no Ermo (Beat > 1):**
  - **Falta de Suprimentos:** Tentar descansar sem suprimentos acarreta bloqueio (ação negada).
  - **Com Suprimentos:** O suprimento é consumido e uma rolagem de evento no D20 dita o sucesso.
    - *Sucesso (>= 11):* O herói recupera o HP completamente, o jogo salva no checkpoint "ACAMPAMENTO" e a narrativa de sono reparador é enviada.
    - *Falha (<= 10):* Ocorrerá uma **Emboscada**. A cura de HP é estrita aos 80% do máximo, o estado é forçado de volta para `COMBATE` e um novo inimigo é instanciado sorrateiramente do Bestiário. O jogo não salva para forçar a consequência do perigo.

## 3. Validação de Sucesso (`test_bloco_33.py`)
Um mock isolou o cenário de emboscada. Forçamos a rolagem D20 a falhar enquanto o jogador possuía apenas 5/20 HP:
- O Suprimento caiu para `0`.
- O HP máximo curou para `16/20` (Exatamente 80%).
- O modo `COMBATE` foi reestabelecido.
- Um "Lacaio Esqueleto (Emboscada)" entrou nos `active_combat_targets`.
- A saída em *Dual-Channel* preencheu a `ui_queue` com o alerta do sistema e a excelente prosa visceral de "despertar de sobressalto no escuro empunhando a lâmina". O teste atendeu a todas as métricas exigidas de sucesso.
