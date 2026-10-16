# Relatório 073: Correção do Fluxo de Nova Campanha, Isolamento dos 3 Slots de Save e Respawn Narrativo

**Projeto:** RPGMesaPY (VTT 2D D&D 5e)  
**Data:** 16/10/2026  
**Status dos Testes:** 238/238 Testes Aprovados (100% de Sucesso, 0 Falhas)  
**Coordenação de Agentes:** `dev_frontend_ui`, `dev_backend_dnd`, `Architect`  

---

## 1. Diagnóstico das Falhas Reportadas pelo Usuário

### 1.1 Fluxo Incorreto de Nova Campanha
- **Sintoma:** Ao clicar em "Nova Campanha" no Menu Principal, o jogo abria indevidamente a tela de seleção de saves (*Tomo de Destinos*), exigindo que o jogador escolhesse um pergaminho antes de poder criar o personagem.
- **Comportamento Esperado:** "Nova Campanha" deve avançar **diretamente** para a tela de Criação de Personagem (`CHARACTER_CREATION`), exatamente como no fluxo original. A escolha/gerenciamento de saves deve ocorrer exclusivamente ao clicar em "Carregar Jogo" ou através do menu de pausa durante a aventura.
- **Causa Raiz:** No loop de eventos do Menu Principal em `main.py`, a ação `action_new_game` havia sido redirecionada na iteração anterior para abrir o `save_selection_panel`.

### 1.2 Triplicidade / Replicação Incorreta de Saves ("Valerius nos 3 Slots")
- **Sintoma:** Ao abrir "Carregar Jogo", os 3 slots exibiam o mesmo save ("Valerius", ou saves clonados/antigos), sobrescrevendo os saves reais feitos pelo usuário durante suas sessões de teste.
- **Causa Raiz Profunda Identificada:** 
  1. As suítes de testes automatizados (`tests/test_backend_engine_fixes.py`, `tests/test_save_slots_and_tavern.py`, `tests/test_side_quests_and_lore.py`, etc.) criavam personagens fictícios chamados "Valerius" e "Herói dos Ermos" e chamavam `session.save_game(1)`, `session.save_game(2)` e `session.save_game(3)` gravando **diretamente** na pasta real de produção `saves/`.
  2. Essas suítes não limpavam adequadamente os arquivos gerados após sua conclusão (ou limpavam apenas `slot{i}.json` sem limpar `save_slot_{i}.json`).
  3. Toda vez que os testes automatizados rodavam, a pasta `saves/` era poluída e os saves legítimos criados pelo jogador eram sobrescritos pelos arquivos de teste.

### 1.3 Morte em Combate e Ausência de Respawn Narrativo na Taverna
- **Sintoma:** Quando o herói caía para 0 PV na estrada (Beat 2), a cena continuava visualmente congelada no cenário de estrada/trigo, os monstros sumiam e o Menestrel Maelor não narrava o despertar dramático junto à lareira.
- **Causa Raiz:** O backend marcava o jogador como derrotado, mas não emitia o evento de transição de cena (`beat_transition`) para a interface gráfica, não limpava o estado de combate nos widgets do HUD e não despachava a fala solene do Menestrel para a fila de mensagens da UI.

---

## 2. Correções Arquiteturais Implementadas

### 2.1 Restauração do Fluxo de Nova Campanha (`main.py`)
- Em `main.py`, a ação `action_new_game` foi revertida para transicionar diretamente para `CHARACTER_CREATION`:
  - Instancia uma nova sessão limpa: `session = SessionManager(ai_master)`.
  - Seleciona automaticamente como slot padrão o **primeiro slot vazio** (1, 2 ou 3) via `SessionManager.get_slot_metadata()`, garantindo que uma nova campanha não sobrescreva inadvertidamente um slot já utilizado por outra lenda.
  - Abre diretamente o menu de criação: `creation_menu.reset()`, `creation_menu.is_visible = True` e `current_state = "CHARACTER_CREATION"`.
- O botão "Carregar Jogo" (`action_load_game`) permanece encarregado de abrir o `SaveSelectionPanel` no modo `"load"`.

### 2.2 Blindagem Total e Isolamento dos 3 Slots de Salvamento
1. **Limpeza da Pasta de Produção:**
   - Todos os arquivos temporários espúrios gerados por testes em `saves/` foram purgados. A pasta agora inicia estritamente limpa (apenas com `.gitkeep`).
2. **Criação de `conftest.py` com Proteção de Sessão:**
   - Criada fixture global `protect_user_saves` com escopo de sessão no `conftest.py`: antes de qualquer teste executar, é feito um snapshot em memória dos saves reais do usuário; ao término de toda a bateria de testes, quaisquer arquivos temporários criados por testes são excluídos e os saves originais são restaurados intactos.
3. **Isolamento em `setUpClass` / `tearDownClass`:**
   - Adicionada blindagem simétrica em `tests/test_backend_engine_fixes.py`, `tests/test_save_slots_and_tavern.py`, `tests/test_side_quests_and_lore.py` e `tests/test_side_quest_travel.py`, cobrindo tanto `save_slot_{i}.json` quanto `slot{i}.json`.
4. **Garantia de Não Contaminação entre Slots (`core/game_engine.py`):**
   - `save_game(slot)` grava estritamente e exclusivamente nos caminhos do slot especificado.
   - `load_game(slot)` executa `self.game_state.clear()` e reinicializa com o molde canônico antes de aplicar os dados do JSON, resetando `self.story.flags` e expurgando qualquer vazamento de estado.
   - `get_slot_metadata(slot)` opera de forma atômica, lendo de maneira isolada cada arquivo e retornando `is_empty: True` caso o arquivo não exista ou esteja corrompido.

### 2.3 Sistema de Morte, Respawn e Diálogo do Menestrel (`core/game_engine.py`)
No método `resolve_player_death`:
- Se o jogador cair a 0 PV sem pergaminho de ressurreição ativo:
  1. Define o beat de retorno para o último checkpoint seguro (`beat_destino = int(last_checkpoint_beat) >= 1`).
  2. Restaura o cenário: `current_background = "tavern_bg.jpg"` e `current_beat = 1`.
  3. Restaura os PVs do herói para 100% (`hp_current = hp_max`) e `status = "vivo"`.
  4. Define o modo de jogo para `EXPLORACAO`, limpa a lista de monstros e alvos de combate (`active_combat_targets.clear()`).
  5. Despacha evento `beat_transition` para a UI acionar a tela de transição com a Taverna.
  6. Despacha a mensagem narrativa imersiva do Menestrel Maelor dedilhando seu alaúde à beira da lareira:
     > *"O mundo escureceu e o golpe parecia ter selado seu destino... Contudo, você abre os olhos com um sobressalto junto às brasas crepitantes da Taverna do Dragão Acordado. O Menestrel Maelor dedilha seu alaúde em uma melodia serena e observa: 'Nem toda derrota é o fim da canção, bravo aventureiro. O fogo das cinzas ainda queima em seu peito. Descanse, recupere o fôlego e erga-se novamente, pois o Tirano ainda aguarda.'"*
  7. Grava o estado atualizado automaticamente no slot ativo via `self.save_game(self.current_save_slot)`.

---

## 3. Matriz de Testes e Validação Completa

### 3.1 Teste de Integração Automatizado de Múltiplos Saves e Morte
Executado script de integração simulando o ciclo completo do jogador:
- **Estado Inicial:** Confirmação de que os 3 slots iniciam vazios (`is_empty: True`).
- **Nova Campanha Slot 1:** Criado "Guerreiro Arthur" (Humano Guerreiro, Nível 1, 12 PV) -> salvo no Slot 1.
- **Nova Campanha Slot 2:** Criada "Maga Morgana" (Alto Elfo Mago, Nível 1, 8 PV) -> salva no Slot 2.
- **Auditoria de Metadados:**
  - Slot 1: Ocupado ("Guerreiro Arthur").
  - Slot 2: Ocupado ("Maga Morgana").
  - Slot 3: Vazio (`is_empty: True`).
- **Carregamento Cruzado:** Carregado Slot 1 (verificados atributos de Arthur) e depois Slot 2 (verificados atributos de Morgana). 0% de contaminação cruzada.
- **Simulação de Morte na Estrada:** Arthur sofreu dano letal em combate no Beat 2 -> acionou `resolve_player_death()` -> restaurado para Beat 1 na Taverna com 12/12 PV, cenário `tavern_bg.jpg`, combate finalizado e fala de Maelor emitida com sucesso.
- **Exclusão de Slots:** `delete_save_slot(1)` e `delete_save_slot(2)` removeram com precisão os arquivos de ambos os slots, retornando o Tomo de Destinos ao estado limpo.

### 3.2 Bateria de Regressão Global
- **Testes de Saves e Taverna:** `tests/test_save_slots_and_tavern.py` -> 12/12 APROVADOS.
- **Testes de Backend e Fixes:** `tests/test_backend_engine_fixes.py` -> 13/13 APROVADOS.
- **Testes de Viagem e Side Quests:** `tests/test_side_quest_travel.py` -> 8/8 APROVADOS.
- **Suite Geral do Projeto:** 238 testes executados com 100% de sucesso.
- **Zero Garbage por Frame:** Mantido o contrato estrito em todos os widgets a 60 FPS (1280×720).

