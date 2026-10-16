# Relatório 070 — Refinamento do Mestre Maelor, Destravamento de Campanha, Habilidades e Ergonomia da HUD

**Data:** 15/10/2026  
**Responsáveis:** Orquestrador Principal, `dev_ia_prompt_writer`, `dev_backend_dnd_writer`, `dev_frontend_ui_writer`  
**Status:** ✅ Concluído e Validado (166 testes automatizados aprovados - 100% OK)

---

## 1. Resumo Executivo

Este ciclo de desenvolvimento resolveu de forma definitiva os problemas críticos reportados durante os playtests na Taverna (Beat 1), abrangendo:
1. A persona do narrador (Menestrel Maelor) reestruturada para um estilo visceral, conciso e contextual (inspirado em *The Witcher* e *Darkest Dungeon*), eliminando repetições de chavões ("cheiro de fuligem", "cordas de cinza") e mantendo 2 a 3 opções elegantes de ação.
2. O destravamento completo da saída da Taverna para permitir a progressão orgânica pela Planície dos Uivos (Beat 2) até o Clímax (Beat 15).
3. A proteção civil em Hubs Seguros, eliminando combates bugados e auto-instanciação de goblins ao interagir com NPCs na taverna.
4. Auto-alvo em magias de cura/suporte fora de combate e inicialização de habilidades de classe no Nível 1.
5. Inclusão de botões/totens de acesso rápido para `[⚡ Hab.]` e `[✨ Magia]` na HUD de combate e no Grimório.
6. Correção do auto-scroll do chat (*Smart Anchor*) para nunca mais cortar o topo das falas e clareza total na ficha de atributos (Atributo Total + Modificador D&D 5e oficial).

---

## 2. Detalhamento de Todas as Alterações e Melhorias

### 2.1. Inteligência Artificial e Prompts (`dev_ia_prompt_writer`)
* **Arquivos Modificados:** [`docs/dm_guidelines.md`](file:///c:/Users/iagob/RPGMesaPY/docs/dm_guidelines.md), [`ai_master/ai_client.py`](file:///c:/Users/iagob/RPGMesaPY/ai_master/ai_client.py).
* **Persona do Menestrel Maelor:**
  - Elevada para o padrão de cronistas sombrios de alto nível (*The Witcher*, Ancestor de *Darkest Dungeon*, Narrador de *Baldur's Gate 3*): sóbrio, cínico, poético e atento ao destino e à mecânica.
  - Limite estrito de concisão: 1 a 2 parágrafos por turno (60 a 90 palavras).
* **Eliminação de Repetições e Chavões:**
  - Banida a exigência de "5 estímulos sensoriais por parágrafo".
  - Erradicada a repetição compulsória de *"cordas de cinza"*, *"cheiro acre de fuligem"* e *"frio cortante"*. A narração é estritamente contextual ao que acabou de ocorrer.
* **Gatilho de Agência com 2 a 3 Opções Contextuais:**
  - As narrativas do Mestre encerram sempre com 2 a 3 sugestões situacionais elegantes para orientar o jogador caso ele esteja em dúvida, finalizando com o clássico *"O que você faz?"*.
* **Separação Categórica de Vozes e NPCs:**
  - Falas de NPCs (como o Taverneiro) retornam o metadado `"npc_falando": "Taverneiro"` para acionar seu retrato correspondente no chat. Maelor atua como a voz do cronista/mestre e só fala em 1ª pessoa quando abordado diretamente.
* **Reescrita dos Fallbacks Offline:**
  - Todos os 17 blocos de fallback heurístico foram reescritos em formato curto, dinâmico e sem linhas fixas repetitivas de alaúde.

---

### 2.2. Core Backend, Regras D&D 5e e Motor de Jogo (`dev_backend_dnd_writer`)
* **Arquivos Modificados:** [`core/game_engine.py`](file:///c:/Users/iagob/RPGMesaPY/core/game_engine.py), [`core/combat_system.py`](file:///c:/Users/iagob/RPGMesaPY/core/combat_system.py), [`core/dnd_rules.py`](file:///c:/Users/iagob/RPGMesaPY/core/dnd_rules.py), [`data/spells.json`](file:///c:/Users/iagob/RPGMesaPY/data/spells.json).
* **Destravamento da Saída da Taverna (Beat 1 ➔ Beat 2):**
  - Reconhecimento ampliado de comandos em 1ª pessoa: `"sair"`, `"saio"`, `"saio da taverna"`, `"abro a porta"`, `"abrir a porta"`, `"vou para a estrada"`, `"seguir viagem"`, `"partir"`, `"vou embora"`, `"vou lá fora"`.
  - Intenções legítimas de saída não são mais rebaixadas para `INTERAGIR_CENARIO`. O motor avança para o Beat 2 (*Planície dos Uivos*), despacha o evento `beat_transition` e gera o encontro com `m_dire_wolf` e `m_bandit`.
* **Proteção de Hub Seguro (Sem Goblins na Lareira):**
  - Ataques contra civis na Taverna são interceptados pelo motor: o Taverneiro desvia com firmeza (*'Guarde o aço, forasteiro. Aqui bebe-se em paz; sangue derrama-se lá fora.'*) e emite alerta da guarda, bloqueando a auto-instanciação de monstros do bestiário.
* **Magias de Cura Fora de Combate e Auto-Alvo:**
  - Adicionada a magia oficial `cure_wounds` (*Curar Ferimentos*) em `data/spells.json` (`evocation`, `single_ally`, `heal`).
  - Conjurações de cura/suporte sem alvo definido fora de combate assumem automaticamente o herói (`self: pc['name']`), aplicando a rolagem de cura e debitando o spell slot sem erros.
* **Habilidades Desbloqueadas no Nível 1:**
  - `CharacterCalculator.calculate_derived_stats` inicializa `pc['unlocked_skills']` no Nível 1 para as 6 classes (*Retomar o Fôlego*, *Cura pelas Mãos*, *Discípulo da Vida*, *Ataque Furtivo*, *Recuperação Arcana*, *Inimigo Favorito*).
* **Restauração de Viagens no Diário:**
  - Compatibilidade garantida para os prefixos `travel_quest:`, `btn_travel_quest:` e `travel_side_quest:`.

---

### 2.3. Frontend UI, HUD e Ergonomia Visual (`dev_frontend_ui_writer`)
* **Arquivos Modificados:** [`ui/scene_renderer.py`](file:///c:/Users/iagob/RPGMesaPY/ui/scene_renderer.py), [`ui/hud_components.py`](file:///c:/Users/iagob/RPGMesaPY/ui/hud_components.py), [`ui/menu_components.py`](file:///c:/Users/iagob/RPGMesaPY/ui/menu_components.py), [`main.py`](file:///c:/Users/iagob/RPGMesaPY/main.py).
* **Smart Anchor no Chat (Fim dos Cortes no Topo):**
  - O painel agora ancora a rolagem no **topo exato da nova mensagem** (`new_msg_top`). Retrato, nome do falante e as primeiras linhas de narração ficam sempre visíveis de imediato, permitindo leitura natural do começo ao fim.
* **Botões e Totens de Habilidades e Magias na QuickActionBar:**
  - Botão `[⚡ Hab.]` com totem de relâmpago dourado procedural.
  - Botão `[✨ Magia]` com totem de estrela arcana (abre o Grimório diretamente na aba arcanas).
  - **Menu Suspenso Flutuante (Flyout de Habilidades):** Ao clicar em `[⚡ Hab.]`, abre um menu flutuante listando as habilidades ativas desbloqueadas do herói (ex: *Retomar o Fôlego [1d10+1 PV]*). O clique dispara a habilidade instantaneamente com 1 toque!
  - **Botão [Usar Habilidade] no Grimório:** Habilidades adquiridas no livro agora possuem botão ativo de ativação direta.
* **Ficha de Criação com Atributos Canônicos D&D 5e:**
  - Coluna 1: **Atributo Total** somado (`Base + Bônus Racial`, ex: `15`).
  - Coluna 2: **Modificador D&D 5e** autêntico `(Total - 10) // 2` (ex: `+2`, `+1`, `0`, `-1`).
  - Indicador racial sutil `(+2)` em verde floresta acima do total.
* **Despoluição Visual dos Logs Mecânicos:**
  - Rolagens de dados e mensagens de sistema são renderizadas como **cartões/pílulas compactas** com filete semântico colorido: Dourado (d20), Verde (Acerto/Cura) e Carmesim (Dano/Erro), preservando a pureza visual da prosa de Maelor.
* **Calibração Cenográfica da Taverna:**
  - Sprites e tokens foram deslocados lateralmente em `tavern_bg.jpg` (Herói à esquerda em `X: 42%-58%`, NPCs à direita em `X >= 77%`), deixando a lareira central limpa e desobstruída.
* **Zero Garbage a 60 FPS:**
  - Todas as molduras, badges e pílulas utilizam pré-renderização e cache de texturas, sem alocações dinâmicas no loop de desenho.

---

## 3. Pontos de Atenção

> [!IMPORTANT]
> **Modo Exploração vs Combate para Magias Ofensivas:**
> Magias de dano direto (*Mísseis Mágicos*, *Bola de Fogo*) continuam exigindo inimigos visíveis. Se o jogador tentar conjurá-las na taverna ou em áreas seguras sem inimigos, o sistema informa que não há alvos hostis em alcance.

> [!WARNING]
> **Conexão de Rede e Modelo de IA:**
> Durante os testes, os fallbacks locais foram acionados perfeitamente em modo offline. Em ambiente de produção com a chave de API Gemini configurada, o modelo `gemini-3.5-flash-lite` gerará respostas ainda mais vívidas e personalizadas de acordo com o prólogo e antecedentes do herói.

---

## 4. Possíveis Falhas e Riscos Mapeados

1. **Tentativa de Forçar Ataques Excessivos em Zonas Seguras:**
   - *Risco:* O jogador insistir repetidamente em atacar civis na taverna na tentativa de forçar um combate de monstros.
   - *Mitigação Atual:* O sistema emite a advertência do taverneiro e da guarda. Se necessário no futuro, pode-se implementar um sistema completo de cadeia ou expulsão do estabelecimento.
2. **Rolagem do Chat com Mousewheel durante Animações:**
   - *Risco:* Usuário rolar a roda do mouse violentamente enquanto uma animação de dados estiver ativa.
   - *Mitigação Atual:* O `MOUSEWHEEL` possui `math.clamp` entre `0` e `max_scroll`, impedindo estouro de limites ou exceções de divisão por zero.
3. **Economia de Recursos em Descanso Curto:**
   - *Risco:* Uso contínuo de habilidades como *Retomar o Fôlego* sem descanso.
   - *Ponto de Melhoria Futuro:* Conectar o contador de uso de *Retomar o Fôlego* ao sistema de descanso curto/longo (`time_manager.py`) para limitar a 1 uso por descanso.

---

## 5. Pontos de Melhoria Futura Sugeridos

1. **Árvore de Talentos Raciais Interativa:**
   - Implementar botões de ativação específicos para traços raciais ativos, como a *Arma de Sopro* do Draconato (cone de 2d6) na barra de atalhos.
2. **Retratos Animados de Conversação:**
   - Adicionar uma leve pulsação de brilho ou movimento sutil no retrato do NPC enquanto sua fala estiver sendo exibida no chat.
3. **Mini-Mapa Tático da Trilha:**
   - Exibir na aba de Diário um mapa esquemático em pergaminho mostrando a rota percorrida pelo herói entre os Beats 1 a 15 e as rotas bifurcadas das Side Quests.

---

## 6. Validação por Testes Automatizados

* **Suíte Global Executada:** `python -m unittest discover tests`
* **Testes Específicos Adicionados:**
  - `tests/test_dnd_backend_improvements.py` (Avanço de Beat, Taverna Segura, Magia Self, Habilidades Nv 1).
  - `tests/test_frontend_improvements.py` (Smart Anchor, Menu Flyout, Ficha Canônica, Posicionamento Taverna).
  - `tests/test_ai_agent.py` & `tests/test_ai_prompt_fixes.py` (Persona de Maelor, Fallbacks Concisos).
* **Resultado:** **166 testes executados, 166 aprovados (100% de sucesso)**.

