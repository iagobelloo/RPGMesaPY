# 🧠 DIRETRIZES DO AGENTE DE IA (LLM & PROMPT ENGINEERING)
**Cargo:** Especialista em Integração de LLM, Engenharia de Prompts, Parser Estruturado e Mestre Narrativo.  
**Objetivo:** Garantir a sinergia perfeita entre o jogador e o sistema através do ciclo de duas fases: Fase 0 (Parser Mecânico estrito em JSON) e Fase 2 (Mestre Narrador imersivo, dinâmico e contextual), com zero alucinação matemática e blindagem total contra falhas de API.

---

## 1. Isolamento de Domínio (Regra de Ouro)
Você tem permissão EXCLUSIVA para ler e editar os seguintes arquivos:
* `ai_master/ai_client.py` (Conexão com a API via SDK google-genai, injeção de prompts de sistema, estruturação de payloads, controle de sliding window)
* `docs/dm_guidelines.md` (Diretrizes narrativas mestras, tom Grounded Dark Fantasy, regras de oráculo e anatomia do turno)
* `data/campaign.json` e `data/side_quests.json` (Descrições ambientais de beats e diálogos de introdução de missões)

**É ESTRITAMENTE PROIBIDO:**
* Alterar o motor gráfico Pygame (`ui/scene_renderer.py`, etc.) ou a física/matemática de combate (`core/combat_system.py`, `core/dnd_rules.py`).
* A IA **NUNCA** decide valores numéricos de dano, sucesso de testes de resistência ou PVs dos personagens; a narrativa deve espelhar fielmente o `sys_log` do motor.

---

## 2. A Fase 0: O Parser Mecânico (JSON Estrito & Anti-Crash)
A primeira chamada do ciclo converte a ação livre do jogador em uma intenção acionável para o motor D&D:
1. **JSON Puro:** O modelo deve retornar exclusivamente uma string JSON válida, sem blocos de código markdown adicionais (sem triplas crases ```json) e sem mensagens introdutórias ou conclusivas.
2. **Campos Obrigatórios Padronizados:**
   - `"tipo_acao"`: (ex: `"ataque"`, `"magia"`, `"usar_item"`, `"exploracao"`, `"descansar"`, `"avancar_historia"`)
   - `"recurso_utilizado"`: nome exato da arma, magia ou item
   - `"alvo"`: lista com o(s) nome(s) do(s) alvo(s)
   - `"intencao_cena"`: (ex: `"iniciar_combate"`, `"fugir"`, `"manter"`, `"investigar"`)
3. **Resiliência Absoluta:** Toda chamada à API deve estar envolvida em blocos `try/except` robustos. Em caso de timeout, falha de conexão ou resposta malformada, a função deve retornar imediatamente um dicionário seguro de *fallback*, garantindo que a thread assíncrona nunca congele o jogo.

---

## 3. A Fase 2: O Mestre Narrador (Imersão, Lore & Memória)
A segunda chamada recebe o resultado matemático do backend (`sys_log`) e a intenção da cena, transformando dados brutos em narrativa épica de fantasia sombria:
1. **Fidelidade aos Dados Numéricos:** Se o log indicar que o goblin sofreu 4 de dano e sobreviveu com 3 PV, a narrativa deve descrever um golpe que feriu mas não matou a criatura. Se o Dragão Supremo estiver carregando seu ataque devastador sofrendo 1% de dano, a narrativa deve descrever as escamas de obsidiana repelindo os ataques enquanto o magma brilha no peito.
2. **Proibição de Repetição Estéril:** O System Prompt deve instruir a IA a **sempre avançar a narrativa** (diálogos, reações, pistas do mistério, consequências imediatas), proibindo explicitamente a repetição estática de descrições de cenários ("as paredes de pedra fria", "o vento uivante") a cada turno.
3. **Contexto de Criação (Prólogo & Beats):** A IA deve injetar ativamente a raça, classe, tendência e antecedentes do herói na narrativa do prólogo e nas interações ao longo da jornada, proporcionando uma experiência de RPG de mesa autêntica.
4. **Acionamento de Retratos (Portraits):** Sempre que um NPC falar diretamente com o jogador, o retorno deve incluir o metadado `"npc_falando": "Nome do NPC"` para que a interface carregue o retrato correspondente.
5. **Controle de Janela Deslizante (Sliding Window):** Manter no `chat_history` apenas as últimas 5 a 6 interações relevantes, garantindo memória de curto prazo sem estourar o limite de tokens da API nem causar lentidão na resposta.
6. **SDK & Modelo:** Execução padronizada no SDK `google-genai` com o modelo `gemini-3.5-flash-lite`, operando com sessões de chat estruturadas para evitar alertas de AFC e assegurar JSON determinístico.