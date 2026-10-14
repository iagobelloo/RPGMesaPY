# Relatório de Execução - Bloco 25

## Reforço do Parser de Intenção e Ativação Mecânica do Modo Combate

**Data:** 05/10/2026
**Especialista:** Dev Backend D&D

### Visão Geral

Este relatório detalha as correções implementadas no Bloco 25, focadas nas camadas Controller e Model (Backend) para garantir que a intenção de combate declarada pelo jogador sempre resulte em resolução mecânica, impedindo que a IA (Mestre) ignore ações bélicas e gere finais de cena prematuros ou genéricos.

### Problemas Identificados

1.  **AI Hallucination no Parser:** O LLM ignorava a instrução de ataque em algumas iterações e forçava uma "narrativa" ou "exploração" porque falhava em setar a chave `intencao_cena` corretamente para `"iniciar_combate"`.
2.  **Perda de Sincronia de Alvos (Target Desync):** Mesmo se o jogo entrasse em `"COMBATE"`, se o Mestre esquecesse de enviar a estrutura correta em `novos_inimigos`, a variável `active_combat_targets` do motor não era populada. Isso causava a auto-resolução do combate instantaneamente (0 alvos restantes) antes mesmo de processar o dano.

### Soluções Implementadas

#### 1. FASE 0: Parser Lógico (ai_client.py)
*   Adicionada uma Trava Implacável de Combate (Hard-lock) na rotina de extração JSON `parse_player_action`.
*   Agora, se o `tipo_acao` retornado for `ataque` ou `magia`, e a chave `alvo` contiver qualquer valor válido diferente de "nenhum", o backend sobrescreve a chave `intencao_cena` forçando-a para `"iniciar_combate"`. O motor parou de depender exclusivamente da inteligência da LLM para ativar a transição.

#### 2. FASE 1: Matemática & Controlador (core/game_engine.py)
*   **Auto-Instanciação de Segurança (Fallback de Bestiário):** Na função `_async_turn_processor`, foi criado um sistema de proteção para a lista de inimigos. Se o `game_mode` for `"COMBATE"`, a rotina varre os `alvos_raw` enviados pelo LLM. Caso o Mestre tenha se esquecido de criar o alvo nos `novos_inimigos`, o core agora detecta o ID do alvo ausente, busca a melhor equivalência no `BESTIARIO_5E` (por substring) e o **auto-instancia na memória** (com PV, CA e Status corretos).
*   Se nenhuma string bater, aplica-se um perfil padrão genérico (ex: "goblin" CA 10 PV 10) para evitar travamentos silenciosos.

#### 3. FASE 2: Gatilho Visceral Narrativo (core/game_engine.py)
*   A estrutura de contexto (`scene_state`) enviada à IA para gerar a narrativa final foi enriquecida com `game_mode`.
*   Se a intenção for `iniciar_combate`, injetamos a diretiva `combat_alert`: `"ALERTA: COMBATE INICIADO! Narre visceralmente a primeira troca de golpes de acordo com o log matemático."`
*   Isso força o LLM a reconhecer a transição de exploração para combate e traduzir as rolagens matemáticas ativamente em sua resposta de texto.

### Conclusão e Testes
O backend agora está completamente blindado contra esquecimentos (hallucinations) de instanciamento de alvo e transição de estado. O Motor (Core Python) possui autoridade máxima sobre a transição para modo de Batalha (Initiative Loop) e se auto-alimentará se a inteligência artificial tentar driblar as regras mecânicas. A Camada de View e as Regras D&D 5e permanecem intocadas, isoladas como especificado.
