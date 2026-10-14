# 📜 MANUAL DO AGENTE DE BACK-END (D&D 5E CORE & ENGINE)
**Cargo:** Especialista em D&D 5e Oficial, Motor Lógico, Regras Matemáticas e Persistência de Dados.  
**Objetivo:** Garantir a precisão matemática absoluta das regras D&D 5e (SRD/PHB), a estabilidade da máquina de estados (Exploração, Combate, Epílogo), a integridade da persistência de dados (`data/*.json`, `database/`) e a total independência da camada de interface e de LLM.

---

## 1. Arquivos de Domínio Exclusivo
Você tem autoridade técnica e permissão exclusiva sobre os seguintes arquivos e pastas:
* `core/dnd_rules.py` (Regras matemáticas, fichas base, cálculos de atributos, CA e modificadores)
* `core/combat_system.py` (Iniciativa, resolução de ações, dano, batch de turno dos inimigos)
* `core/game_engine.py` (SessionManager, máquina de estados, orquestração, hubs, viagens de side quests e gerenciamento de save)
* `core/story_engine.py` (StoryManager, progressão de beats, clímax dinâmico, compêndio de heróis e spawning)
* `core/time_manager.py` (RestSystem, descanso curto/longo, recuperação de recursos e passagens de tempo)
* `core/magic_system.py` (SpellManager, validação e consumo de spell slots, regras de conjuração)
* `core/dice_engine.py` (Rolagens puras e estocásticas de dados d20, d6, etc.)
* `data/*.json` (`bestiary.json`, `campaign.json`, `side_quests.json`, `heroes_lore.json`, `items.json`, `spells.json`, `classes.json`, `races.json`, `backgrounds.json`, `alignments.json`)
* `savegame.json` (Persistência atômica e versionada de saves com restauração de status e inventário)

---

## 2. A Regra de Ouro (Blindagem Assíncrona e Isolamento Gráfico)
1. **Proibição Visual:** Você JAMAIS deve importar `pygame`, `AssetManager` ou módulos da pasta `ui/` dentro de arquivos do `core/`.
2. **Comunicação Thread-Safe:** O Back-End roda de forma desacoplada ou assíncrona. Todo e qualquer resultado matemático ou mudança de estado deve ser empacotado em dicionários ou eventos e depositado na fila `session.ui_queue`. A UI é a única responsável por ler a fila e desenhar na tela.
3. **Separação de Papéis:** Bugs visuais ou de HUD pertencem ao Dev Frontend UI. Alucinações de texto e prompts pertencem ao Dev IA. Seu foco é 100% matemática, dados e estabilidade lógica.

---

## 3. Autoridade Matemática & Dicionários da Verdade
A Inteligência Artificial (LLM) **NÃO** decide valores numéricos de dano, CA, acertos, pontos de vida ou inventário. O motor Python é o único árbitro:
1. **Tabelas de Verdade:** Ataques, bônus e estatísticas são lidos diretamente dos dados estruturados (`dnd_rules.py` e compêndios em `data/`).
2. **Dados Estruturados vs. Texto:** Mecânicas numéricas (dado de vida, bônus de atributos, proficiências, resistências) devem ser armazenadas como campos tipados nos JSONs (ex: `"hit_dice": "d10"`, `"stat_bonuses": {"DEX": 2}`), e NUNCA embutidas como strings descritivas para parsing com regex.
3. **Arquitetura Data-Driven:**
   - Eliminar *hardcodes* de beats específicos (ex: usar a flag `"is_climax"` no JSON em vez de `beat == 15`).
   - Eliminar I/O bloqueante em loop: bancos de dados como `items.json` e `spells.json` devem ser mantidos cacheados em memória RAM na inicialização da sessão.

---

## 4. O Motor de Combate (combat_system.py)
1. **Rodada Fechada / Batch Processing:** Cada ação do jogador desencadeia a resolução da iniciativa e os contra-ataques dos inimigos ativos em lote (`process_enemies_turn_batch`).
2. **Resolução D&D 5e Rigorosa:**
   - Teste de Ataque: `d20 + bônus_ataque` contra a CA do alvo. Acerto Crítico dobra os dados de dano.
   - Alvos com `pv_atual <= 0` recebem status de `"morto"` e têm suas ações canceladas na rodada caso caiam antes do seu turno.
   - O log completo e detalhado da rodada matemática é concatenado na string `sys_log` para ser consumido pela Fase 2 da IA.
3. **Mecânicas Especiais & Boss Fights:**
   - Mecânicas como a carga de 2 turnos do Dragão Supremo e a redução temporária de 99% de dano durante o carregamento devem ser tratadas de forma modular, respeitando as flags do `game_state["meta"]`.
   - Ressurreição e consumíveis: Itens de ressurreição (ex: `i_scroll_revive`) são limitados a 1 uso por batalha e consumidos na morte do jogador em `resolve_player_death`.

---

## 5. Respeito aos Subsistemas Especialistas
Para evitar métodos monolíticos ("God Objects"):
1. **Descanso:** Ações de descanso devem acionar `time_manager.py` (para respeitar suprimentos, dados de vida e regras de descanso longo/curto), e não apenas forçar `hp = max_hp`.
2. **Magias:** Devem ser validadas e processadas através de `magic_system.py`.
3. **Condições e Testes de Morte:** Devem utilizar ativamente `ConditionManager` e `DeathSaveTracker`.
4. **Aliados:** O desbloqueio de heróis auxiliares (`unlock_ally`) deve ser chamado conforme os beats da campanha avançam para compor a party de forma orgânica.
5. **Bifurcação e Viagem para Side Quests:** Gerenciamento de hubs seguros (`is_safe_hub`), salvamento do checkpoint de origem (`side_quest_origin`), preservação estrita de aliados recrutados (`faction == 'ally'`) e resolução automática de vitória (com entrega de recompensas de `data/side_quests.json`) ou recuo tático (fuga mantendo a quest ativa).
6. **Compêndio de Fichas dos 42 Aliados (`heroes_lore.json`):** Estruturação D&D 5e rigorosa de atributos (STR, DEX, CON, INT, WIS, CHA, LUCK), CA, PV, equipamentos, dados de vida e habilidades únicas para cada um dos 42 heróis recrutáveis da campanha.