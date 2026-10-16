# Relatório 075: Motor Argon, Combate D&D 5e, UI/Hotbar & Polimento Geral (Blocos 1 a 6)

**Projeto:** RPGMesaPY (VTT 2D D&D 5e)  
**Data:** 16/10/2026  
**Documento de Referência:** `docs/prompts/prompt_motor_argon_polimento_geral.md`  
**Status dos Testes:** 100% Aprovados (`11/11` em `tests/test_argon_polimento.py` e `255/255` na suíte global)  
**Coordenação:** Antigravity Architect & Subagente Especialista (`UI & HUD Specialist - Blocos 4 e 5`)  

---

## 1. Visão Geral Executiva

Todas as **6 frentes arquiteturais (Blocos 1 a 6)** especificadas em `docs/prompts/prompt_motor_argon_polimento_geral.md` foram implementadas, auditadas e validadas com cobertura automatizada em `tests/test_argon_polimento.py` e alinhamento de regressão na suíte global do projeto, respeitando integralmente todas as **6 Restrições Negativas** e o **Contrato Zero Garbage por Frame (60 FPS, 1280×720)**.

---

## 2. Detalhamento Técnico das Alterações por Bloco

### Bloco 1: Motor Argon & IA Resiliente (`ai_master/ai_client.py`)
1. **Cascata de Modelos Gemini Expandida**:
   - Atualizado `self.fallback_models` em `AIGameMaster.__init__` e `_get_models_cascade()` para:
     `["gemini-3.5-flash-lite", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash-lite-latest", "gemini-flash-latest"]`.
   - Caso um modelo retorne `404 NOT_FOUND`, `429 RESOURCE_EXHAUSTED` ou timeout, o cliente percorre toda a cascata antes de acionar o fallback determinístico local.
2. **Padronização Estrita em `client.chats.create`**:
   - Migrados `parse_player_intent` e `generate_narrative_from_math` de `self.client.models.generate_content` para sessões de chat via `self.client.chats.create(model=current_model, config=config)` + `chat.send_message(...)`, unificando todas as chamadas da classe `AIGameMaster` no protocolo estável de chat.
3. **Narrativa de Contra-Ataque Inimigo no Fallback Local (`_create_visceral_fallback`)**:
   - Adicionado bloco específico que diferencia semanticamente **acerto inimigo** (*"As lâminas e presas inimigas rompem o espaço em um contragolpe feroz!..."*) de **erro inimigo** (*"O contra-ataque inimigo sibila a centímetros de sua carne..."*), mantendo o gancho interativo obrigatório `"O que você faz?"`.

### Bloco 2: Balanceamento D&D 5e, Sincronia `ca`/`ac` e Identidade de Monstros (`data/campaign.json`, `core/combat_system.py`, `core/story_engine.py`, `core/game_engine.py`, `core/dnd_rules.py`)
1. **Rebalanceamento do Beat 2 (`data/campaign.json`)**:
   - Encontro da *Planície dos Uivos* ajustado de `["m_dire_wolf", "m_bandit"]` para `["m_bandit", "m_bandit"]` (dois Bandidos ND 1/8, 11 PV, CA 12), calibrado para combate solo de Nível 1 nas regras oficiais do D&D 5e.
   - `environment_prompt` atualizado para refletir a dupla de batedores bandidos na estrada de terra.
2. **Sincronia Bidirecional `ca` / `ac`**:
   - Padronizada a leitura `player_character.get("ca", player_character.get("ac", 10))` e sincronização simultânea `player_character["ac"] = valor` e `player_character["ca"] = valor` em:
     - `process_enemies_turn_batch`, `resolve_action`, `resolve_skill_effect` e `roll_initiative_order` (`core/combat_system.py`);
     - `apply_level_up`, `_recalculate_ac` e `cast_spell` (`core/game_engine.py`);
     - `CharacterCalculator.calculate_derived_stats` (`core/dnd_rules.py`).
3. **Eliminação de Hash Hexadecimal e Numeração Sequencial Limpa**:
   - Removido `uuid.uuid4()[:4]` de `StoryManager.spawn_enemies_from_list` (`core/story_engine.py`), gerando nomes e chaves limpas sequenciais (`"Bandido 1"`, `"Bandido 2"`).
   - Refinado `SessionManager.find_combat_target` (`core/game_engine.py`) para resolver com precisão `"Bandido 1"`, `"Bandido 2"`, `"1"`, `"2"`, `"bandido #2"` ou `"Bandido"`, priorizando inimigos vivos sobre abatidos.

### Bloco 3: Protocolo de Morte Real vs Déjà Vu (`core/game_engine.py`, `core/story_engine.py`)
1. **Isolamento Absoluto do Déjà Vu no Beat 15**:
   - `StoryManager.is_climax()` (`core/story_engine.py`) e `SessionManager.resolve_player_death()` (`core/game_engine.py`) agora verificam estritamente `int(self.story.current_beat) == 15 and self.story.is_climax() and meta.get("loop_count", 0) == 0`.
2. **Reload Limpo de Checkpoint nos Beats 1 a 14**:
   - Quando o herói chega a `0 PV` sem `i_scroll_revive` nos Beats 1 a 14:
     - Limpa imediatamente `self.active_combat_targets.clear()` e `self.active_visual_npcs.clear()`;
     - Descarta mensagens narrativas pendentes do turno fatal via `_discard_pending_combat_narratives()`;
     - Recarrega o save do slot ativo via `self.load_game(self.current_save_slot)` (quando existente para a sessão atual) e restaura o estado ao `last_checkpoint_beat` com `hp_current = hp_max`, `status = "vivo"` e `game_mode = "EXPLORACAO"`;
     - Emite exclusivamente o evento `beat_transition` e a narrativa poética de despertar de Maelor no Checkpoint.

### Bloco 4: UI & Hotbar Zero Sobreposição (`ui/widgets/theme.py`, `ui/widgets/base.py`, `ui/widgets/hud/action_bar.py`)
1. **Constantes de Layout (`ui/widgets/theme.py`)**:
   - `Layout.SLOT = (104, 52)` e `Layout.SLOT_WIDE = (152, 52)`.
2. **Geometria Interna de `UIButton` (`ui/widgets/base.py`)**:
   - Para `variant == "action"`: ícone fixado em `16px` (`self._icon_sz = 16`), rótulo em fonte `11px` bold (`self.font_size = 11`), conjunto `[Ícone 16px] + [4px] + [Rótulo 11px]` rigorosamente centralizado na horizontal, e badge de atalho (`hotkey`) em `8px` bold com fundo semitransparente pré-alocado no canto superior direito `(w - hotkey_w - 4, 3)`.
3. **Hotbar Tática (`ui/widgets/hud/action_bar.py`)**:
   - Largura de combate recalculada para `combat_w = 152 + (4 * 104) + (4 * 8) + 20 = 620px`, centralizada em `Layout.STAGE_CX - combat_w // 2` (`x = 564`), e barra de exploração ajustada para `460px`.

### Bloco 5: Chat Typewriter Real Caractere a Caractere (`ui/widgets/hud/chat_console.py`)
1. **Fluxo Contínuo em `NarrativeLogView`**:
   - Adicionados `_typing_text`, `_typing_speaker`, `_typing_kind`, `_typing_index`, `_typing_speed = 45.0` (45 caracteres/s) e `_typing_queue`.
   - `update(dt)` avança `_typing_index += _typing_speed * dt`, fatia `current_slice = _typing_text[:int(_typing_index)]` e re-envolve apenas a mensagem ativa em `_active_typing_lines` reutilizando `default_text_cache.get(...)` (**Zero Garbage em `_draw_self`**).
   - `flush_typewriter()` descarrega instantaneamente o texto ativo e a fila ao clicar no console ou ao receber mensagens de sistema/combate/jogador.

### Bloco 6: Polimento de Logs de Combate e Dados (`core/combat_system.py`, `core/game_engine.py`)
Padronizadas todas as linhas de log matemático para leitura rápida e uniforme:
- **Ataque do Herói**: `🎲 [Ataque] {Arma}: d20 ({dado}) + {mod} = {total} vs CA {ca} ➔ {Acerto/Erro}! ({dano} dano)`
- **Contra-Ataque Inimigo**: `⚔️ [{Inimigo}]: d20 ({dado}) + {mod} = {total} vs CA {ca} ➔ {Acerto/Erro}! ({dano} dano)`
- **Teste de Perícia**: `🎲 [Perícia] {Nome} CD {cd}: d20 ({dado}) + {mod} = {total} ➔ {Sucesso/Falha}!`
- **Cura / Consumível**: `✨ [Cura] {Item}: +{pv} PV recuperados (PV: {atual}/{max})`

---

## 3. Falhas Encontradas, Pontos de Atenção e Melhorias Aplicadas

1. **Falso Positivo de `"dano"` em Erros de Ataque (`(0 dano)`) no Fallback Visceral (`ai_master/ai_client.py`)**:
   - *Falha Identificada:* Com o novo formato do Bloco 6 (`➔ Erro! (0 dano)`), a substring `"dano"` está presente mesmo quando o ataque erra (`0 dano`). A checagem ingênua `if any(w in log_lower for w in ["acerta", "dano", "ferido"])` classificaria qualquer erro com `(0 dano)` como acerto, gerando narrativa de dano sofrido quando o ataque havia errado.
   - *Correção Aplicada:* Adicionada detecção explícita de erro (`is_miss = any(w in log_lower for w in ["erra o ataque", "➔ erro", "➔ falha", "(0 dano)", "(0 de dano)"])`) tanto para o contra-ataque inimigo quanto para o ataque do próprio herói em `_create_visceral_fallback`.
2. **Proteção Contra Saves Órfãos em Disco Durante Reload de Morte (`core/game_engine.py`)**:
   - *Ponto de Atenção:* Se uma sessão em memória (ou teste automatizado) acionar `resolve_player_death()` sem ter salvo previamente no slot, carregar cegamente um arquivo antigo de `saves/save_slot_1.json` pertencente a outro personagem sobrescreveria o personagem da sessão atual.
   - *Melhoria Aplicada:* Adicionada flag `_has_session_save` e validação de metadados do slot (`same_char_save`) em `resolve_player_death()`, garantindo que `load_game` recarregue o checkpoint da sessão sem contaminar sessões em memória nem sobrescrever saves reais do usuário durante testes.
3. **Priorização de Alvos Vivos em `find_combat_target` (`core/game_engine.py`)**:
   - *Melhoria Aplicada:* Quando `"Bandido 1"` é abatido e continua temporariamente no dicionário antes da limpeza pós-turno, um comando genérico `"atacar bandido"` agora prioriza automaticamente `"Bandido 2"` (vivo) em vez de atingir o cadáver de `"Bandido 1"`.
4. **Alinhamento da Suíte Histórica de Testes (`tests/`)**:
   - *Melhoria Aplicada:* Atualizadas asserções legadas de formato de string e cascata de modelos em `test_ai_agent.py`, `test_backend_engine_fixes.py`, `test_backend_integration_audit.py`, `test_items_capacity_and_skills.py`, `test_skills_spells_and_tavern_guard.py`, `test_bloco_7_frontend.py` e `test_bloco_8_transicoes_beats.py` para refletirem os padrões canônicos atuais.

