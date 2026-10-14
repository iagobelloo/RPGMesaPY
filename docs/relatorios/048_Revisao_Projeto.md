# Revisão Geral do Projeto: Crônicas da Taverna

Após uma varredura completa realizada pela força-tarefa de subagentes (Core, Combate, UI/UX e Dados), consolidamos um diagnóstico profundo do estado atual do seu projeto. O jogo possui uma base incrivelmente sólida de D&D 5e e Pygame, mas sofre de "desconexão" entre as regras escritas nos dados (JSON) e a execução no código.

Abaixo estão os apontamentos de onde estamos, o que está quebrado e o que precisa ser feito.

---

## 1. Onde Estamos (Estado Atual do Projeto)
O jogo possui a infraestrutura completa de um RPG Textual 2.5D:
- **Narrativa e Dados:** Uma campanha inteira de 15 Beats, um bestiário rico, classes, raças, cutscenes (Loops de Tempo) e sistema de magias estão definidos em JSONs, embora em grande parte desacoplados do motor principal.
- **UI:** A interface foi modernizada para *Knights of Pen & Paper*, com suporte a portraits dinâmicos, barras de HP, painéis de combate e um terminal semântico que não "sequestra" o teclado.
- **Motor (Engine):** O backend tem sistemas avançados de rolagem matemática (DiceEngine), regras de vantagem/desvantagem (ConditionManager) e salvamento de morte.

No entanto, as peças não estão totalmente "conversando" umas com as outras.

---

## 2. Falhas Críticas Encontradas (Bugs)

### 🗡️ Combate (Matemática e Lógica)
1. **O Bug da "Pancada Universal":** No arquivo `combat_system.py`, o turno dos monstros pulou a fila de iniciativa. Pior: ao tentar agir, o código busca inimigos em um dicionário obsoleto em português (ex: `"lacaio goblin"`). Como os IDs reais são `"m_goblin"`, o jogo não acha os ataques do bestiário que geramos (2d10, 6d6). **O resultado?** Do simples Goblin ao Dragão Supremo, **TODO monstro ataca o jogador com o fallback genérico de 1d4 de dano.**
2. **Magia de Dano Inevitável:** Magias de alvo único (ex: Raio de Fogo) pulam a checagem da CA (Armadura) e os Testes de Resistência, aplicando dano 100% garantido e inevitável.
3. **Morte Instantânea:** O código ignora os "Death Saves" (Testes contra a morte). Bater a zero de HP decreta morte direta, o que quebra a mecânica de sobrevivência.

### 🧩 Dados (JSONs Desconectados)
1. **Campanha Travada no Beat 5:** Embora o `campaign.json` tenha 15 Beats perfeitos, o `story_engine.py` tem um dicionário manual travado em 5 Beats. O jogador **nunca passará do Beat 5**.
2. **Tendências e Raças "Fantasmas":** O loader Python tenta ler as Tendências no padrão `"al_lg"` (Lawful Good), mas o JSON usa a chave `"al_lawful_good"`. O resultado é que as descrições de tendência falham em carregar. O mesmo ocorre com "Anão da Colina" e "Elfo da Floresta", que foram esquecidos no mapa de raças.
3. **Poção da Fênix Inexistente:** O código checa se o jogador possui uma `"Pocao da Fenix"` no inventário ao morrer (Beat 15 e Loop), mas esse item não existe em `items.json`.

### 🎨 Interface (Memory Leaks e UI)
1. **Desperdício de Processamento:** Textos longos, modais base (Surfaces do Pygame) e retângulos translúcidos estão sendo recriados do absoluto zero 60 vezes por segundo, em vez de serem "cacheados".
2. **Memory Leak de Imagens:** O `AssetManager` guarda todas as imagens escalonadas na memória. Se o jogador passar horas jogando e gerando portraits/monstros, a RAM vai encher infinitamente sem limpeza.
3. **Estouro de Caixa no Input/Log:** As "caixas de diálogo" estouram as margens se alguma palavra gigante não tiver espaços, ou se houverem mensagens demais no log de combate que passa dos limites.

---

## 3. Melhorias Arquiteturais Propostas

1. **Cortar a I/O Bloqueante:** A IA lê o arquivo `spells.json` e `items.json` direto do Disco Rígido toda vez que processa um ataque de combate. Estes arquivos devem ser carregados uma única vez na RAM na inicialização.
2. **Ativar o `game_cutscenes.json`:** O seu roteiro (Loops Temporais, O Despertar no Beat 1, Entrada Surpresa do Aliado no Boss do Beat 15) está maravilhosamente escrito num JSON raiz, mas o código não os utiliza (o StoryEngine só lê o prólogo).
3. **Data-Driven de Verdade:** Tirar mecânicas "Hardcoded" do motor. Em vez da `GameEngine` checar `if current_beat == 15:` para acionar o fim do jogo, o `StoryEngine` deveria ler no `campaign.json` que aquele Beat tem a flag `"is_climax": true`.
4. **Time Manager vs Descanso Curto:** As curas por descanso em `game_engine.py` são valores chutados no código. O módulo abandonado `time_manager.py` deveria ser usado para processar os "Hit Dice" (Dados de Vida) reais dos jogadores.

---

## 4. Próximos Passos (Plano de Ação)

Dado o levantamento, recomendo atacarmos em etapas ordenadas para não desestabilizar o jogo:

* **PASSO 1: Destravar a Base (JSONs e Loaders):**
  - Corrigir a nomenclatura e chaves em `alignments.json`, `races.json` e `classes.json`.
  - Atualizar o `story_engine.py` para ler de fato a extensão total dos **15 Beats** e carregar o restante da lore a partir de `game_cutscenes.json`.
* **PASSO 2: Consertar o Combate Matemático:**
  - Plugar os monstros de `bestiary.json` de volta na engine para baterem com o dano real (remover o ataque genérico de 1d4).
  - Implementar verificação de CA para danos mágicos diretos.
* **PASSO 3: Otimização da UI e Memória:**
  - Aplicar caching nas Surfaces Pygame que são lidas por frame e implementar limite de caracteres baseado no tamanho (hitbox) real da fonte na criação de personagem.

O que você prefere que ataquemos primeiro? Recomendo fortemente o **Passo 1** ou o **Passo 2** para garantir que o fluxo de jogo e a progressão funcionem corretamente!
