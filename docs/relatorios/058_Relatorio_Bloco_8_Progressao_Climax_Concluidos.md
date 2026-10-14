# Relatório 058 - Bloco 8 (Opções 3 e 4 Concluídas: Progressão D&D 5e & Simulação do Clímax Déjà Vu)

## 1. Resumo Executivo
Concluímos com sucesso a implementação conjunta das **Opções 3 e 4**:
1. **Opção 3 (Progressão & Level Up D&D 5e e Distribuição de Loot / Recompensas):** Sistema oficial de evolução de nível, cálculo de Dado de Vida (Hit Die), bônus de proficiência, expansão de Spell Slots para classes conjuradoras, economia de ouro (PO), saque de monstros dinâmico e integração transparente com o HUD e o Grimório.
2. **Opção 4 (Simulação e Balanceamento do Clímax com Déjà Vu):** Validação e simulação completa dos Beats 1 ao 15, mecânica de snapshot da party completa na entrada do covil, wipeout no Loop 0 acionando o retorno temporal idêntico do Déjà Vu, quebra de armadura do Tirano das Cinzas e vitória definitiva da party no Loop 1 com transição limpa para o modo Epílogo.

> [!IMPORTANT]
> **Isolamento de Direção de Arte Respeitado:** Conforme solicitação expressa do usuário, todo o escopo visual e de direção de arte (novos cenários, sprites e objetos) permaneceu estritamente isolado para blocos dedicados futuros. Foco exclusivo em regras, backend, UI funcional e estabilidade.

---

## 2. Detalhamento da Opção 3: Sistema de Progressão & Level Up D&D 5e

### A) Matemática e Regras Oficiais (`core/dnd_rules.py`)
- **Fórmula Oficial de PV por Nível:**
  $$\text{PV Ganho} = \left(\left\lfloor \frac{\text{Dado de Vida}}{2} \right\rfloor + 1\right) + \text{Modificador de CON}$$
  Garantindo ganho justo sem randomicidade punitiva (ex: Guerreiro d10 ganha $6 + \text{CON}$; Mago d6 ganha $4 + \text{CON}$).
- **Escalonamento de Bônus de Proficiência:**
  - Níveis 1 a 4: $+2$
  - Níveis 5+: $+3$
- **Expansão de Magias (Spell Slots):**
  - Mago: ganha slots de 2º nível ao atingir Nível 3 (`{"1": 4, "2": 2}`).
  - Clérigo e Paladino: expansão progressiva dos círculos divinos.
- **Tabela de Experiência (XP Thresholds):**
  - Nível 1: 0 a 300 XP
  - Nível 2: 300 a 900 XP
  - Nível 3: 900 a 2.700 XP
  - Nível 4: 2.700 a 6.500 XP
  - Nível 5: 6.500 a 14.000 XP
- **Saque de Monstros (`calculate_monster_loot`):**
  - Geração ponderada de Moedas de Ouro (PO) com base no CR do monstro e chance equilibrada de consumíveis pertinentes.

### B) Motor de Jogo (`core/game_engine.py`)
- **Ação `SUBIR_NIVEL` / `LEVEL_UP`:** Adicionado despachador dedicado que aplica `CharacterCalculator.apply_level_up(pc)` e atualiza o estado do herói.
- **Recompensas ao Abater Inimigos:**
  - Concessão de XP real da ficha do monstro e moedas de ouro diretamente na morte do inimigo.
  - Alerta de evolução `🌟 [EVOLUÇÃO] XP suficiente para SUBIR DE NÍVEL!` quando o limiar for alcançado.
  - Bônus de encontro ao vencer combate (+100 XP e bônus em ouro).
- **Tratamento Seguro de Alvos e Aliados:**
  - O motor agora distingue estritamente entre facções `enemy` e `ally` ao verificar a resolução do combate. Aliados vivos em campo não bloqueiam mais a vitória quando todos os inimigos são abatidos.

### C) Interface Visual & HUD (`ui/hud_components.py` e `main.py`)
- **TopHeroHUD:**
  - Exibição de ouro em tempo real: `OURO: {gold} PO`.
  - Indicador pulsante em destaque no cabeçalho quando há evolução disponível: `★ SUBIR DE NÍVEL!`.
- **GrimoireModal (Aba Status):**
  - Exibição do ouro acumulado.
  - Botão interativo `Subir de Nível` (habilitado e destacado quando o jogador acumulou XP suficiente), despachando a ação assíncrona ao motor.

---

## 3. Detalhamento da Opção 4: Simulação do Clímax e Déjà Vu

### A) Entrada no Beat 15 e Snapshot da Party
- Ao entrar no Beat 15 (Covil do Tirano das Cinzas), todos os aliados recrutados pelo jogador entram em campo com ele contra o dragão.
- É gerado um **Snapshot Profundo** contendo:
  - Estado completo do herói (HP atual, HP máximo, XP, Nível, Spell Slots, Inventário).
  - Estado de todos os aliados ativos.
  - Configuração visual da cena.

### B) Mecânica do Loop 0 (Wipeout & Déjà Vu)
- No Loop 0, o dragão possui escama impenetrável (CA 99, 999 PV).
- Ao sofrer a morte da party pelo sopro vulcânico:
  - O Déjà Vu é ativado.
  - O snapshot é integralmente restaurado: o jogador e todos os seus aliados retornam exatamente como entraram no covil (mesmo HP, itens e habilidades).
  - O cenário transiciona para `deja_vu_bg.jpg`.
  - A cutscene dramática do tempo se estilhaçando é exibida.
  - O segredo do dragão é ativado (`segredo_tirano = True`, `loop_count = 1`), quebrando a armadura do monstro (CA 14, 100 PV).

### C) Derrota do Tirano e Epílogo Definitivo
- Ao derrotar o Tirano das Cinzas no Loop 1:
  - O modo de jogo transiciona para `EPILOGO`.
  - A lista de alvos hostis é limpa.
  - O AI Game Master narra o fim épico da batalha e encerra a demo com a mensagem oficial da vitória.

---

## 4. Blindagem NLP e Fallback Inteligente (`ai_master/ai_client.py`)
- Adicionada heurística offline e contra esgotamento de cota (HTTP 429) no `parse_player_intent`:
  - Se a API estiver offline ou em rate-limit, palavras-chave canônicas (`descansar`, `subir nivel`, `atacar`, `sair/viajar`, `usar item`) são mapeadas com segurança de tipo, evitando interrupções em testes ou partidas locais.

---

## 5. Validação e Testes Automatizados

Foi criada a suíte dedicada `tests/test_bloco_8_progressao_climax.py` contendo 5 testes de integração:
1. `test_level_up_fighter_math`: Validação matemática de subida de nível de classe marcial (Guerreiro d10, CON, proficiência e limiar de XP).
2. `test_level_up_wizard_spell_slots`: Validação de subida de nível de conjurador (Mago d6 e expansão de Spell Slots).
3. `test_monster_loot_generation`: Validação estatística de ouro por CR e chances de drops de consumíveis.
4. `test_async_monster_kill_rewards`: Validação do fluxo assíncrono de abate de monstro, concessão de XP/PO e remoção limpa do alvo abatido.
5. `test_climax_allies_and_deja_vu_flow`: Simulação ponta a ponta dos Beats 1 ao 15, wipeout no Loop 0, ativação do Déjà Vu com restauração idêntica da party e vitória no Loop 1.

Todas as suítes de teste de regressão (`test_bloco_40.py`, `test_bloco_6_backend.py`, `test_bloco_6_frontend.py`, `test_bloco_6_ia_prologo.py`, `test_bloco_7_backend.py`, `test_bloco_7_frontend.py`, `test_parser.py`, `test_turn_lock.py`) foram executadas e aprovadas com sucesso.

