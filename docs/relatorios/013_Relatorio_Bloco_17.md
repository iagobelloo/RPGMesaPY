# Relatório do Bloco 17 (Iniciativa e Rodada Fechada)

Diretor, o Motor Matemático (Fase 1) passou por uma evolução profunda. Nós quebramos o paradigma de apenas "receber dano", transformando o script em um simulador de Turno de Combate Completo, sem introduzir nenhum loop assíncrono perigoso ou animações bloqueantes.

### 1. Correção Gráfica do Alpha (Triângulo Opaco)
O triângulo (rabo) da caixa de diálogo estava desenhando pixels sólidos por cima do cenário, quebrando a ilusão do alpha 210.
**Solução:** Criei uma `full_surf` com `pygame.SRCALPHA` que engloba tanto o retângulo do balão quanto o triângulo inferior. Os dois polígonos são desenhados internamente nessa surface com `(15, 15, 15, 210)`. Ao dar o Blit na tela principal, o triângulo compartilha da mesma transparência perfeita de 210, assim como as bordas em bronze.

### 2. O Arsenal do Bestiário Expandido
Os monstros não atacam mais usando "Pancada (1d4)" genérico.
Injetei a chave `"ataques"` com dicionários de armas literais no `BESTIARIO_5E`.
Exemplos em ação:
- O **Lacaio Goblin** puxa sua `"Cimitarra"` (1d6+2).
- O **Ogro** esmaga com sua `"Clava Grande"` (2d8+4).
- O **Kraken** despedaça com seu `"Tentáculo"` (3d6+10) com bônus de acerto +17.

### 3. A Rodada Fechada (Initiative System)
A função `resolve_action` foi reescrita. Em uma única passagem síncrona:
1. Rolamos a **Iniciativa do Jogador** (1d20 + DES).
2. Rolamos a **Iniciativa dos Inimigos Reagentes** (1d20 + DES do bestiário).
3. Colocamos todos numa lista e ordenamos do maior para o menor.
4. Executamos os ataques em sequência.
5. **Permadeath Instantâneo:** Se o jogador matar o Ogro primeiro, a verificação `if monstro.get("pv_atual") <= 0:` impede o Ogro de atacar. Se o Ogro ganhar a iniciativa e matar o jogador, o jogador não ataca.
6. Todos os resultados são concatenados em uma única variável `sys_log`, gerando um relatório tático massivo que será lido pela IA (Fase 2) para descrever a coreografia cinematográfica de golpes e esquivas.

O jogo atingiu um nível de simulação mecânica autônoma digna de um Virtual Tabletop oficial de D&D. Qual é o plano para o Bloco 18?
