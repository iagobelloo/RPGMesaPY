# PROMPT DE COMANDO - MOTOR ARGON (GEMINI 4 ARGON)
## PACOTE DE POLIMENTO GERAL E REFINAMENTO TÉCNICO: RPGMESAPY

> **MODO DE EXECUÇÃO**: Diretiva Máxima de Engenharia de Software. Execute todas as alterações de código diretamente nos arquivos-alvo indicados. Sem divagações, sem placeholders e com consumo estrito de tokens. Cada bloco é atômico, determinístico e autossuficiente.

---

### CONTEXTO TÉCNICO DO PROJETO
- **Repositório**: RPGMesaPY (Python 3.12+ / Pygame-CE / Google GenAI SDK).
- **Arquitetura**: Separação estrita em camadas:
  - Fase 0 (Classificador NLP e Intenção)
  - Fase 1 (Motor Mecânico D&D 5e / Dados)
  - Fase 2 (Tradutor Narrativo Visceral na persona do Menestrel Maelor)
  - Interface Gráfica Pygame HUD (Contrato Zero Garbage por Frame).

---

### BLOCO 1: IA & API GEMINI (MIGRAÇÃO CHATS.CREATE, CASCATA 503 E FALLBACK DE REAÇÃO)

#### 1.1 Arquivo-Alvo: `ai_master/ai_client.py`
- **Problema**: O uso de `self.client.models.generate_content(...)` dispara o aviso de Automatic Function Calling (AFC) e não preserva contexto conversacional limpo; quedas do modelo padrão em momentos de pico (erro HTTP 503 / Model Overloaded) interrompem a sessão; contra-ataques inimigos caem em fallbacks genéricos de diálogo ou ataque do jogador.
- **Ações Exatas**:
  1. **Expansão da Cascata de Modelos**:
     - No método `__init__` (linha ~39) e `_get_models_cascade()` (linha ~106):
     - Atualizar a lista de fallbacks adicionando `gemini-2.5-flash` e `gemini-2.0-flash`.
     - Ordem canônica de tentativa:
       ```python
       self.fallback_models = [
           "gemini-3.5-flash-lite",
           "gemini-2.5-flash",
           "gemini-2.0-flash",
           "gemini-flash-lite-latest",
           "gemini-flash-latest"
       ]
       ```
  2. **Migração para `chats.create` em `parse_player_intent`** (linha ~582):
     - Substituir a chamada `self.client.models.generate_content(...)` por sessão de chat dedicada com schema JSON:
       ```python
       chat = self.client.chats.create(
           model=model,
           config=genai.types.GenerateContentConfig(
               system_instruction=sys_instr,
               response_mime_type="application/json",
               temperature=0.0
           )
       )
       response = chat.send_message(prompt)
       raw_text = response.text or "{}"
       ```
  3. **Migração para `chats.create` em `generate_narrative_from_log`** (linha ~746):
     - Substituir a chamada `self.client.models.generate_content(...)` por sessão de chat dedicada:
       ```python
       chat = self.client.chats.create(
           model=model,
           config=genai.types.GenerateContentConfig(
               system_instruction=sys_instr,
               temperature=0.6
           )
       )
       response = chat.send_message(prompt)
       if response.text and response.text.strip():
           narrative = response.text.strip()
           self.model_name = model
           break
       ```
  4. **Fallback Narrativo Específico de Contra-Ataque Inimigo** em `_create_visceral_fallback` (linha ~782):
     - Adicionar caso de precedência logo acima do ataque genérico:
       ```python
       # Contra-ataque de Inimigos / Turno das Ameaças
       if any(w in log_lower for w in ["acerta o ataque", "erra o ataque", "contra-atacam", "tenta alcançar", "desferiu contra você", "acerta com crítico"]) or "contra-ataque" in intencao_lower:
           if any(w in log_lower for w in ["acerta", "dano", "ferido"]):
               return (
                   "As lâminas e presas inimigas rompem o espaço em um contragolpe feroz! "
                   "O aço adversário morde sua guarda e a dor arde nos músculos, exigindo recuperação imediata sob o impacto brutal.\n\n"
                   "Você pode devolver um golpe rápido de represália, fechar a postura defensiva com escudo ou recuar para manter a distância. O que você faz?"
               )
           else:
               return (
                   "O contra-ataque inimigo sibila a centímetros de sua carne, fendendo apenas o ar viciado e a poeira das cinzas. "
                   "O adversário cambaleia levemente, frustrado pelo desvio no instante crucial.\n\n"
                   "Você pode aproveitar a brecha aberta pelo erro dele, desferir um golpe punitivo ou reposicionar seus passos. O que você faz?"
               )
       ```

---

### BLOCO 2: D&D 5E & BALANCEAMENTO (ENCONTRO BEAT 2, CA/AC E NOMES DE MONSTROS)

#### 2.1 Arquivo-Alvo: `data/campaign.json`
- **Problema**: Beat 2 ("Planície dos Uivos") possui um `m_dire_wolf` (CR 1, 37 PV, +5 ataque, derruba oponente) ao lado de um `m_bandit`. Para um personagem de nível 1 em combate solo, o encontro quebra a curva matemática da 5ª Edição e causa wipe injusto no início da jornada.
- **Ação Exata**:
  - No nó `"2"`, substituir a lista `"enemies"` de `["m_dire_wolf", "m_bandit"]` para `["m_bandit", "m_bandit"]`. Ajustar `environment_prompt` mantendo a ambientação de emboscada de foras-da-lei na planície.

#### 2.2 Arquivo-Alvo: `core/combat_system.py`
- **Problema**: Disparidade de nomenclatura onde o jogador possui atributos `"ac"` e `"ca"`. Em `process_enemies_turn_batch` (linha ~841), lê-se apenas `player_character.get("ca", 10)`, ignorando `ac` caso preenchido apenas sob o padrão inglês da ficha D&D 5e.
- **Ação Exata**:
  - Padronizar leitura resiliente de Classe de Armadura:
    ```python
    "ca": player_character.get("ca", player_character.get("ac", 10))
    ```
  - Sempre que a CA for modificada temporária ou permanentemente (escudo, armadura, bônus de cobertura), manter ambas as chaves sincronizadas:
    ```python
    player_character["ac"] = novo_valor_ca
    player_character["ca"] = novo_valor_ca
    ```

#### 2.3 Arquivo-Alvo: `core/story_engine.py` e `core/game_engine.py`
- **Problema**: Monstros são instanciados com sufixos hexadecimais aleatórios como `Bandido a90f` ou `Lobo Terrível 3b1c` via `uuid.uuid4()[:4]` em `spawn_enemies_from_list` (linha ~581). Isso quebra a estética clássica de mesa de RPG.
- **Ação Exata**:
  - Substituir o gerador de UUID por contagem sequencial limpa indexada por tipo de criatura na cena (`Bandido 1`, `Bandido 2`).
  - Implementação em `core/story_engine.py`:
    ```python
    monster_counts: Dict[str, int] = {}
    for enemy_id in enemies_to_spawn:
        ...
        base_name = monster_instance.get('name', 'Criatura')
        monster_counts[base_name] = monster_counts.get(base_name, 0) + 1
        narrative_id = f"{base_name} {monster_counts[base_name]}"
    ```
  - Garantir compatibilidade em `core/game_engine.py:find_combat_target` e nos parsers regex para localizar `Bandido 1`, `1`, ou `Bandido`.

---

### BLOCO 3: MORTE & CHECKPOINT (DÉJÀ VU EXCLUSIVO BEAT 15, LOAD_GAME E DESCARTE ASSÍNCRONO)

#### 3.1 Arquivo-Alvo: `core/game_engine.py`
- **Problema**:
  1. A lógica do Déjà Vu (retorno no tempo com preservação de memória e segredo do chefe) é uma mecânica narrativa exclusiva do Clímax (Beat 15 - Covil do Tirano das Cinzas). Mortes ocorridas nos Beats 1 a 14 não devem acionar mecânica de loop, mas sim recarregar o último save/checkpoint seguro.
  2. Quando o herói é derrotado durante o turno de resposta dos inimigos, narrativas assíncronas do ataque anterior do jogador ainda chegam à fila da UI, gerando confusão de eventos após a tela de morte.
- **Ações Exatas**:
  1. **Restrição Estrita do Déjà Vu** em `resolve_player_death` (linha ~1848):
     - Validar incondicionalmente:
       ```python
       if int(self.story.current_beat) == 15 and meta.get("loop_count", 0) == 0:
           # Executa exclusivamente a mecânica do Loop 1 do Beat 15 (Déjà Vu)
       ```
  2. **Tratamento de Morte nos Beats 1 a 14**:
     - Limpar `active_combat_targets` e `active_visual_npcs`.
     - Recarregar o estado persistido chamando `self.load_game(self.current_save_slot)` caso o slot exista em disco. Se não houver arquivo físico, restaurar para o checkpoint canônico (`last_checkpoint_beat`, com HP no máximo, modo `EXPLORACAO`).
     - Emitir a mensagem de despertar e transição de beat para a Taverna ou Acampamento Seguro.
  3. **Descarte de Mensagens e Narrativas Pendentes em Caso de Morte no Turno**:
     - Em `_async_turn_processor` (linha ~3188 a 3215):
       ```python
       if pc.get("hp_current", 0) <= 0:
           # O herói caiu durante o turno: anular player_bubble e descartar narrativas pendentes
           player_bubble = ""
           while not self.ui_queue.empty():
               try:
                   msg = self.ui_queue.get_nowait()
                   # Preserva apenas logs do sistema se necessário, descartando narrativas de combate defasadas
               except Exception:
                   break
           self.resolve_player_death()
           return
       ```

---

### BLOCO 4: UI & HOTBAR ZERO SOBREPOSIÇÃO (LAYOUT, TAMANHOS E ATALHOS)

#### 4.1 Arquivos-Alvo: `ui/widgets/theme.py`, `ui/widgets/base.py`, `ui/widgets/hud/action_bar.py`
- **Problema**: Em resolução 1280x720, os slots da hotbar (96x52) sofrem com sobreposição de texto em palavras de 10+ caracteres, ícones grandes de 24px disputam largura com o rótulo, e o badge de atalho `[1]` sobrepõe os cantos dos textos.
- **Ações Exatas**:
  1. **Constantes de Layout** em `ui/widgets/theme.py`:
     - Modificar dimensões de slot para garantir folga:
       ```python
       SLOT: tuple[int, int] = (104, 52)
       SLOT_WIDE: tuple[int, int] = (152, 52)
       ```
  2. **Renderização de Botões da Hotbar** em `ui/widgets/base.py` (`UIButton._rebuild`):
     - Para botões de variante `action`:
       - Definir `icon_sz = 16` fixo (eliminando ícones de 24px).
       - Fonte do botão em tamanho `11` bold.
       - Posição do atalho de teclado (`hotkey`): fixar no canto superior direito absoluto `(w - hotkey_w - 4, 3)`, desenhado em tamanho compacto (8px bold) com fundo semitransparente sutil para não interferir na área horizontal do ícone + texto.
       - Centralização horizontal rigorosa do conjunto `[Ícone 16px] [Espaço 4px] [Rótulo 11px]`.
  3. **Geometria da Hotbar Tática** em `ui/widgets/hud/action_bar.py`:
     - Recalcular largura total da hotbar de combate (`combat_w = 152 + (4 * 104) + (4 * Layout.GAP) + 20 = 620px`).
     - Centralizar com `combat_x = Layout.STAGE_CX - combat_w // 2`.

---

### BLOCO 5: CHAT TYPEWRITER REAL (FLUXO CADENCIADO CARACTERE A CARACTERE)

#### 5.1 Arquivo-Alvo: `ui/widgets/hud/chat_console.py`
- **Problema**: O `NarrativeLogView` atual insere linhas inteiras pré-renderizadas a cada 60ms através de `_pending_typewriter_lines`, resultando em um efeito de blocos saltando em vez de uma digitação suave fluida.
- **Ações Exatas**:
  1. Refatorar `NarrativeLogView` para suportar fluxo contínuo de caracteres em `update(dt)`:
     - Adicionar estado:
       - `self._typing_text: str = ""` (texto completo da mensagem atual sendo digitada)
       - `self._typing_speaker: str = ""`
       - `self._typing_kind: str = "narration"`
       - `self._typing_index: float = 0.0` (índice fracionário de caracteres revelados)
       - `self._typing_speed: float = 45.0` (45 caracteres por segundo)
       - `self._typing_queue: deque[tuple[str, str, str]] = deque()` (mensagens narrativas enfileiradas)
  2. **Lógica de Avanço no `update(dt)`**:
     - Quando houver mensagem ativa, avançar `_typing_index += _typing_speed * dt`.
     - Montar o texto visível parcial `current_slice = _typing_text[:int(_typing_index)]`.
     - Re-envolver linhas apenas para a mensagem em digitação, mantendo o histórico de mensagens já finalizadas intacto no deque `_lines`.
  3. **Descarga Instantânea (`flush_typewriter`)**:
     - Ao clicar no console narrativo ou receber mensagens de sistema/dano/combate, completar a mensagem imediatamente (`_typing_index = len(_typing_text)`), convertê-la em linhas definitivas e passar para a próxima.
  4. **Princípio Zero Garbage**:
     - Não recriar fontes; reaproveitar `default_text_cache.get(...)` com as strings parciais da linha ativa.

---

### BLOCO 6: DADOS LIMPOS & LOGS ESTÉTICOS

#### 6.1 Arquivos-Alvo: `core/combat_system.py`, `core/game_engine.py`
- **Problema**: Logs mecânicos de combate apresentam strings poluídas com marcadores desnecessários, saltos de linha em excesso e formatações inconsistentes.
- **Ações Exatas**:
  1. Padronizar todas as mensagens de dados e combate no formato de uma linha elegante:
     - **Ataque do Herói**:
       `🎲 [Ataque] {Arma}: d20 ({dado}) + {mod} = {total} vs CA {ca} ➔ {Acerto/Erro}! ({dano} dano)`
     - **Contra-ataque Inimigo**:
       `⚔️ [{Inimigo}]: d20 ({dado}) + {mod} = {total} vs CA {ca} ➔ {Acerto/Erro}! ({dano} dano)`
     - **Testes de Perícia**:
       `🎲 [Perícia] {Nome} CD {cd}: d20 ({dado}) + {mod} = {total} ➔ {Sucesso/Falha}!`
     - **Consumíveis / Cura**:
       `✨ [Cura] {Item}: +{pv} PV recuperados (PV: {atual}/{max})`
  2. Eliminar linhas redundantes de separadores e manter apenas logs significativos para a leitura do jogador.

---

### RESTRIÇÕES NEGATIVAS E REGRAS INVIOLÁVEIS (NEGATIVE CONSTRAINTS)

1. **PROIBIDO** utilizar `self.client.models.generate_content(...)` em novos fluxos do `ai_client.py`. Use obrigatoriamente sessões `chats.create`.
2. **PROIBIDO** disparar a mecânica de Déjà Vu fora do Beat 15 (Covil do Tirano das Cinzas). Beats 1 a 14 devem sempre recarregar save/checkpoint seguro.
3. **PROIBIDO** gerar nomes de monstros de combate com sufixos hexadecimais (`uuid4`). Utilize exclusivamente numeração limpa (`Bandido 1`, `Bandido 2`).
4. **PROIBIDO** manter `m_dire_wolf` no Beat 2 de `data/campaign.json`. O encontro deve conter apenas `["m_bandit", "m_bandit"]`.
5. **PROIBIDO** alocar novas superfícies (`pygame.Surface` ou chamadas `font.render`) a cada frame no método `_draw_self` dos widgets. Respeite o contrato Zero Garbage por Frame.
6. **PROIBIDO** quebrar assinaturas de métodos públicos de `SessionManager`, `AIGameMaster` ou `CombatSystem`.

---

### CRITÉRIOS DE ACEITE E VALIDAÇÃO MATEMÁTICA

O motor Argon deve criar o arquivo de teste `tests/test_argon_polimento.py` cobrindo e validando:

1. **Teste de Cascata e Sessão Chat**:
   - `test_gemini_models_cascade_includes_expanded_fallbacks`: Assegura que `gemini-2.5-flash` e `gemini-2.0-flash` constam na cascata.
   - `test_extract_intent_and_narrative_use_chats_create`: Mocka o cliente e valida que `chats.create` é invocado em vez de `models.generate_content`.
   - `test_enemy_counter_attack_fallback`: Valida que logs com contra-ataques inimigos acionam o texto específico em `_create_visceral_fallback`.
2. **Teste de Balanceamento Beat 2 e Nomes Limpos**:
   - `test_beat_2_enemies_balance`: Carrega `data/campaign.json` e asserta `campaign["2"]["enemies"] == ["m_bandit", "m_bandit"]`.
   - `test_monster_spawn_clean_sequential_names`: Instancia dois bandidos e confirma IDs `Bandido 1` e `Bandido 2`, sem caracteres hexadecimais.
   - `test_combat_player_ca_ac_synchronization`: Garante que `player_character["ac"]` e `player_character["ca"]` permanecem idênticos.
3. **Teste de Morte e Checkpoint**:
   - `test_death_in_beat_1_to_14_reloads_checkpoint`: Morte no Beat 2 restaura Beat 1/checkpoint seguro e NÃO aciona loop de déjà vu.
   - `test_death_in_beat_15_triggers_deja_vu`: Morte no Beat 15 com `loop_count == 0` aciona o déjà vu mantendo segredo do dragão.
4. **Teste de UI e Hotbar**:
   - `test_hotbar_slot_dimensions_and_icon_size`: Valida que botões de ação usam `icon_sz == 16`, largura >= 100px e fonte 11 bold.

#### Comando de Execução:
```bash
python -m pytest tests/test_argon_polimento.py -v
```
Critério de Sucesso: **100% dos testes aprovados (green pass)** sem regressão na suíte principal.

