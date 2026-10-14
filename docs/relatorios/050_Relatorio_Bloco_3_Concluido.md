# Relatório de Conclusão: Bloco 3 (Sistema de Combate e Regras Específicas)

O **Bloco 3** foi implementado com sucesso na base de código. Abaixo estão os detalhes das correções e novas funcionalidades adicionadas:

## 1. Conexão com o Bestiário (Dano e Atributos Reais)
* **Problema Resolvido:** Os monstros estavam ignorando o `bestiary.json` durante o combate e atacando com um soco padrão (1d4 de dano) devido a uma busca falha no dicionário estático `dnd_rules.py`.
* **Solução Aplicada:** O `combat_system.py` foi modificado para ler os ataques, bônus de acerto e dados de dano diretamente da lista de `actions` do inimigo instanciado (que o `story_engine.py` já puxa corretamente do `bestiary.json`). Agora, lobos terríveis e bandidos causam o dano correto.

## 2. Mecânica de Hit-Kill do Dragão Supremo
* **Problema Resolvido:** O dragão precisa de uma habilidade de morte instantânea que leve a party à derrota para acionar o loop de *déjà vu* da história.
* **Solução Aplicada:** A lógica do turno dos inimigos (`process_enemies_turn_batch`) foi atualizada. Quando o Dragão Supremo usa sua magia de sopro, ele agora itera sobre todos os alvos válidos (jogador e aliados), reduzindo o HP de todos a 0 e alterando o status para "morto", incinerando a party inteira.

## 3. Mecânica de Ressurreição (Uso Único)
* **Problema Resolvido:** Era necessário um item/magia para reviver o jogador uma única vez por batalha.
* **Solução Aplicada:** 
  * Criado o item `i_scroll_revive` no `data/items.json` e adicionado ao inventário inicial.
  * Implementada a lógica de reviver no `game_engine.py` (para o item) e no `combat_system.py` (para magias).
  * Criada a trava de uso único no `game_state["meta"]["revive_used"]`, que é resetada ao final de cada combate.
  * O sistema de morte do jogador agora tenta consumir automaticamente o `i_scroll_revive` antes de declarar o Game Over, desde que não tenha sido usado naquela batalha.

---

### Próximos Passos

O Bloco 3 está tecnicamente completo. Você gostaria de **realizar um teste prático (playtest)** para verificar se os monstros estão batendo corretamente e se o pergaminho de reviver funciona, ou prefere **avançar diretamente para o Bloco 4** (onde trataremos a questão da UI do Chat cobrindo a tela e a barra de rolagem)?
