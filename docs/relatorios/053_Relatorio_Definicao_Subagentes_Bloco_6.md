# Relatório 053 - Definição dos Subagentes Oficiais e Base do Bloco 6

## 1. Contexto e Objetivo
Após o grande levantamento arquitetônico e a auditoria de código, dados e interface, iniciamos o **Bloco 6** garantindo a solidez dos nossos especialistas de desenvolvimento.
Para impedir alucinações, invasão de domínios ou alterações indevidas entre interface e lógica de regras, oficializamos a documentação dos três subagentes do projeto e os registramos nativamente no sistema de agentes com permissões controladas.

---

## 2. Manuais e Documentações Atualizados (`.github/agents/`)
Os três manuais de referência do projeto foram totalmente refinados e atualizados para refletir todas as regras e decisões arquitetônicas recentes:

### A) `Dev Backend D&D.md`
- **Domínio Exclusivo:** `core/` (`dnd_rules.py`, `combat_system.py`, `game_engine.py`, `story_engine.py`, `time_manager.py`, `magic_system.py`, `dice_engine.py`), `data/*.json` e `database/connection.py`.
- **Regras Rígidas:**
  - Proibição absoluta de imports de `pygame` ou `ui/` no core.
  - Comunicação estritamente assíncrona e thread-safe via `ui_queue`.
  - Dados matemáticos estruturados nos JSONs (dado de vida, CA, bônus numéricos), eliminando regex em strings descritivas.
  - Eliminação de I/O bloqueante (cache de compêndios em memória RAM).
  - Respeito aos módulos especialistas (`time_manager` para descanso, `magic_system` para magias, `ConditionManager` e `DeathSaveTracker`).
  - Suporte à mecânica do Dragão Supremo (2 turnos de carga com 99% de redução de dano) e limitação de 1 uso de ressurreição por batalha.

### B) `Dev Frontend UI.md`
- **Domínio Exclusivo:** `ui/` (`scene_renderer.py`, `hud_components.py`, `menu_components.py`, `asset_manager.py`), `assets/` e o loop de renderização/eventos em `main.py`.
- **Regras Rígidas:**
  - Proibição absoluta de alterar matemática de combate D&D, rolagens ou prompts de LLM.
  - Regra de Zero Garbage por frame (proibido instanciar `pygame.Surface(..., pygame.SRCALPHA)` continuamente a 60 FPS).
  - Pré-medição de quebras de linha de texto (Word-Wrap calculado apenas na inserção de mensagens no log, nunca a cada frame).
  - Proibição de `time.sleep()` (animações puramente não-bloqueantes).
  - Implementação de limpeza de cache de texturas (`clear_cache`) no `AssetManager` ao mudar de cena para evitar memory leaks.
  - Padronização do Chat e Diálogos: proporção de 40%, renderização top-to-bottom, rolagem com barra dourada e teto de 40 mensagens para estabilidade de RAM.
  - Unificação de painéis de seleção de criação de personagem em classes genéricas (princípio DRY).

### C) `Dev IA e Prompt.agent.md`
- **Domínio Exclusivo:** `ai_master/ai_client.py`, `data/game_cutscenes.json` e diretrizes de prompts.
- **Regras Rígidas:**
  - Proibição de alterar regras D&D ou código Pygame; a narrativa espelha 100% os dados numéricos do `sys_log` do backend.
  - Fase 0 (Parser Mecânico): saída estrita em JSON puro, sem blocos markdown (```json), com tratamento de exceções robusto e fallback seguro para nunca travar a thread.
  - Fase 2 (Mestre Narrador): proibição de repetição estéril de descrições de cenários, injeção ativa de raça/classe/origem no prólogo, marcação de `"npc_falando"` para retratos e controle de memória via janela deslizante (últimos 5-6 turnos).

---

## 3. Registro dos Subagentes no Sistema (`define_subagent`)
Os três especialistas foram registrados com suas respectivas ferramentas de escrita e system prompts invioláveis:
1. `dev_backend_dnd` (Pronto para chamadas via `invoke_subagent`)
2. `dev_frontend_ui` (Pronto para chamadas via `invoke_subagent`)
3. `dev_ia_prompt` (Pronto para chamadas via `invoke_subagent`)

---

## 4. Próximos Passos do Bloco 6
Com a equipe oficializada e documentada, as tarefas da faxina e polimento arquitetônico do Bloco 6 podem ser executadas ordenadamente por cada especialista:
1. **Dev Backend D&D:**
   - Desacoplar dados de `races.json` e `classes.json` (extrair `"hit_dice"` e `"stat_bonuses"` das strings de texto para campos numéricos).
   - Remover entrada órfã `"boss_final"` de `bestiary.json`.
   - Conectar `time_manager.py` à ação de descanso no `game_engine.py`.
   - Limpar arquivos residuais como `core/dnd_rules_backup.py`.
2. **Dev Frontend UI:**
   - Deletar arquivo legado e não utilizado `ui/renderer.py`.
   - Otimizar superfícies alpha e pré-renderizar botões de UI para eliminar gargalos de CPU.
   - Otimizar o word-wrap das mensagens do chat no `scene_renderer.py`.
   - Unificar os painéis de criação de personagem no `menu_components.py`.
3. **Dev IA e Prompt:**
   - Conectar o prólogo gerado à raça, classe, tendência e antecedentes reais da ficha.
   - Garantir fallbacks blindados contra falhas de API no `ai_client.py`.

