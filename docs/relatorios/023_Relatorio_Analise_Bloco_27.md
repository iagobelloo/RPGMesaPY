# Relatório de Auditoria: Bloco 27 - Arquitetura Modular Sistêmica e Gerenciamento de Aliados

> [!WARNING] Risco Crítico de Integridade Mecânica
> A auditoria na camada de Modelo (M) e Controller (C) (`core/game_engine.py`, `core/story_engine.py` e sistemas relacionados) identificou falhas graves na integração de aliados ao fluxo de combate e na persistência de estado. O jogo entrará em soft-lock (loop infinito) no momento em que um aliado for instanciado no combate.

## 1. O Soft-Lock do Fim de Combate (Combat End Condition Lock)
**Falha:** O método que decreta o fim do combate avalia a condição `len(self.active_combat_targets) == 0`. Como os novos aliados estão sendo injetados diretamente neste mesmo dicionário `active_combat_targets` (ex: no Beat 4), o motor matemático passa a tratar aliados como se fossem inimigos sobreviventes.
**Consequência:** O combate *nunca* vai acabar até que o jogador assassine seus próprios aliados (ou que eles morram). 

## 2. Processamento Bizarro de Morte de Aliados (Corpse Cleaner)
**Falha:** O "Lixeiro de Cadáveres" (corpse cleaner) que varre a lista de entidades não faz distinção entre facções (aliado vs inimigo). 
**Consequência:** Se o HP de um aliado chegar a 0, o motor irá tratá-lo como um monstro abatido, imprimindo `[SISTEMA] O inimigo morreu...` e recompensando o jogador com pontos de experiência (XP) pela morte do seu próprio companheiro.

## 3. Dessincronização de Save/Load (State Serialization Desync)
**Falha:** As funções de serialização (o salvamento e carregamento de arquivos JSON/pickle) não foram atualizadas para incluir o novo estado narrativo sistêmico gerado pelo `StoryManager` (`current_beat`, `flags_aliados`).
**Consequência:** Ao salvar e carregar o jogo, o motor esquecerá em qual `beat` a campanha estava e perderá todas as marcações de aliados. O jogador sofrerá um dessincronismo narrativo maciço, corrompendo a persistência do RPG.

## 4. Cegueira da IA e Gestão de Turnos Inexistente
**Falha:** Na Fase 0 da jogada, a IA faz o parsing da intenção do jogador *antes* que os aliados sejam corretamente injetados e comunicados ao estado de combate. Além disso, a máquina atual assume que o jogador é o único ator aliado em cena.
**Consequência:** Não existe infraestrutura para que aliados rolem Iniciativa própria, joguem turnos independentes ou para que a IA dite as ações deles em combate embasada na mecânica de D&D 5e. No atual momento, eles são "peso morto" mecânico na resolução de rodadas.

---

### Recomendações Estratégicas para o Backend
- **Refatorar as Estruturas de Entidades:** Separar as estruturas em memória (usar `active_enemies` vs `active_allies`) ou injetar uma propriedade `faction` ("enemy" / "ally") nos objetos matemáticos para filtrar corretamente as condições de vitória (`if not any(t.faction == 'enemy' for t in targets)`).
- **Patch no Save/Load:** Garantir que o snapshot do jogo recupere o `StoryManager` inteiro, persistindo fatos crus independentes da transcrição do chat.
- **Expansão do Loop de Iniciativa:** Atualizar o core de combate para iterar não apenas monstros, mas a Inteligência Artificial controlando as rolagens e ações dos NPCs aliados na fila de combate RAW.

*Auditoria finalizada. Nenhuma linha de código foi adulterada durante este processo.*
