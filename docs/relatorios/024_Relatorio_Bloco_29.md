# Relatório de Implementação: Bloco 29 (Phase 1)

**Módulo Refatorado:** `core/game_engine.py` (Camada Model/Controller)

A implementação do **Roteador de Intenções e Trava de Turno (Turn Lock)** foi executada rigorosamente conforme os padrões arquiteturais do Core Lógico (Backend D&D).

## O que foi feito:
1. **Remoção da FASE 0 Legada:** O antigo método visual de extração (`parse_player_action`) que acidentalmente injetava `novos_inimigos` foi deprecado neste ciclo. Injetamos o uso exclusivo do extrator JSON Silencioso NLP (`self.ai.parse_player_intent`).
2. **Injeção de Contexto (Estado Dinâmico):** `game_mode` e `active_combat_targets` agora alimentam o NLP de forma pura.
3. **Filtro Macro de Modo:** Convertida a transição forçada de `EXPLORACAO` para `COMBATE` caso o tipo de ação indique ataque.
4. **Roteador Principal Limitado (WIP):** Adicionada estrutura base para rotear as ações. Somente `ATACAR` avança para a Fase 1 (se validado). Ações como `CONJURAR_MAGIA` e afins retornam `[SISTEMA] Em desenvolvimento` devolvendo a fila para a UI (não congela o turno).
5. **Trava de Turno (Turn Lock) Implementada:** O router compara iterativamente (ignorando Case) o(s) alvo(s) devolvidos pelo NLP contra o Dicionário de entidades em `active_combat_targets`.
6. **Resgate de UI:** Se o alvo não existe (é fantasma), o sistema aborta a Ação **imediatamente**, enviando o block message na `ui_queue` (`{"narrativa": "[SISTEMA] Alvo 'x' não encontrado..."}`). Isso é crucial porque **não roda a Fase 1** nem avança o turno para os monstros, devolvendo o controle perfeitamente para o jogador.

## Evidência de Execução (Log de Backend)

Desenvolvemos e rodamos um Mock (`test_turn_lock.py`) validando o comportamento bloqueante ao atacar um alvo não spawnado (Fantasma).

```text
[TESTE] Situação: Modo EXPLORACAO, nenhum alvo ativo.
[TESTE] Input do jogador: 'ataco o lacaio goblin com meu machado'

[AI_MASTER NLP] Intenção Extraída com Sucesso:
{
  "tipo_acao": "ATACAR",
  "recurso_utilizado": "machado",
  "alvo": [
    "lacaio goblin"
  ],
  "intencao_cena": "O jogador desfere um golpe com seu machado contra o lacaio goblin."
}
[Sistema] Bloqueio de Turno: Jogador tentou atacar o alvo inexistente 'lacaio goblin'.

[TESTE] Lendo fila de UI...
Mensagem recebida na UI: {'narrativa': "[SISTEMA] Alvo 'lacaio goblin' não encontrado no combate. Ação cancelada."}
[SUCESSO] Turn Lock (Trava de Turno) funcionou! Ação abortada.
```

O Motor agora está blindado! Para que ataques funcionem futuramente, será preciso amarrar o spawn dos monstros através de eventos Narrativos ou de Hook (`StoryEngine`), conforme for implementado nas próximas Fases. A API antiga baseada em alucinações (AI GM spawnando livremente durante o parse de ataque) não corrompe mais o loop de combate.
