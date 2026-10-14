# Relatório do Bloco 15 (Motor Matemático de Equipamentos e Atributos)

Diretor, a matemática do "Crônicas da Taverna" acaba de atingir maturidade mecânica oficial (D&D 5e). Erradicamos o improviso da IA no cálculo de armaduras e armas, transformando o inventário em um motor rigoroso.

### 1. Dicionário de Armas (`ARMAS_5E`) e Acuidade
Criei o dicionário oficial `ARMAS_5E` dentro do `core/dnd_rules.py`, contendo armas primárias (Espada Longa, Espada Curta, Rapieira, Adaga, Arcos, Maça, Besta Leve, Bordão, etc.).
- **Regra de Acuidade (Finesse):** O dicionário suporta a chave `"propriedades": ["acuidade"]`. 
- Se a arma usada for, por exemplo, uma *Rapieira*, o motor dinamicamente avalia a `FOR` e a `DES` do jogador e usa o modificador mais alto, como manda a regra do livro.

### 2. Dicionário de Armaduras e Escudos (`ARMADURAS_5E`)
A gambiarra condicional de CA foi aposentada. O `CharacterCalculator` agora varre o inventário do jogador consultando a `ARMADURAS_5E`:
- **Armaduras Pesadas (Cota de Malha):** `ca_base` bruta (16), sem somar destreza (`soma_des = False`).
- **Armaduras Médias (Brunea):** `ca_base` 14, soma destreza com limite (`limite_des = 2`).
- **Armaduras Leves (Couro):** `ca_base` 11, soma destreza total.
- **Escudos:** Se detectado, adiciona `+2` global ao cálculo.
O sistema provou seu valor na simulação: O Guerreiro gerou exatos `18 CA` (16 + 2) e o Ladino gerou `14 CA` (11 + 3 de Destreza).

### 3. Modificação do Prompt (Gatilho da Arma)
O cérebro da IA (Fase 0) recebeu um novo gatilho. Toda vez que o `tipo_acao` for classificado como `"ataque"`, ela é **obrigada** a preencher a nova chave `"arma_usada"` do JSON (deduzida do texto do jogador ou do inventário visível na ficha).

### 4. Refatoração do Round Bilateral
Em `combat_system.py`, quando a ação "ataque" bate na mesa:
1. O Python lê a `"arma_usada"` do JSON. Se a IA falhar ou tentar inventar uma metralhadora, o motor ativa o *Fallback Seguro*: `"ataque desarmado" (1 de dano + Modificador de FOR)`.
2. O Motor carrega a arma do dicionário.
3. Rola o D20 e o Dano verdadeiro, aplicando os modificadores de Força ou Destreza correspondentes.
No script de teste de estresse (Ladino e Guerreiro), vi a máquina rolar um crítico letal de Rapieira puxando bônus corretos de Destreza.

Tudo testado e operante! Qual será o próximo alvo da nossa Arquitetura?
