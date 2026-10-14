# Relatório de Combate Bilateral e Mortalidade (Fase de Resposta)

O Módulo de Combate Bilateral foi implementado e testado. O RPGMesaPY deixou de ser um simulador de "saco de pancadas" e se tornou um motor letal e responsivo.

### 1. Injeção de Atributos Defensivos do Jogador
Os dados vitais (`pv_max`, `pv_atual`, `ca`, `mods`) foram firmemente atrelados à inicialização da Ficha de Personagem (no `main.py`). O jogador agora possui AC 16 e 30 HP, permitindo que a matemática opere contra ele.

### 2. Intenção de Resposta (A Mente Tática da IA)
O `ai_client.py` na **Fase 0 (Parser)** agora exige a matriz `"reacao_inimigos"`. Se houver 4 Goblins na sala e o jogador atacar 1 deles, o LLM decidirá simultaneamente como os 4 reagirão àquele estímulo logo em seguida.

### 3. O Árbitro de Rounds (Matemática Bilateral)
No `combat_system.py`, reescrevi o método `resolve_action` para que ele não resolva apenas um golpe, mas o **Round Completo**:
- **Ato 1**: O dado do Jogador é rolado contra a `ca` do monstro. Dano é aplicado e o Lixeiro é preparado.
- **Ato 2**: O motor varre os monstros sobreviventes. Se eles optaram por atacar na intenção do LLM, o Python extrai os atributos deles diretos do *Bestiário Oficial* (`+4` para acertar, `1d6+2` de dano), e rola o **d20 interno do motor** contra a CA 16 do jogador.
- **Ato 3**: Se o jogador recebe dano, a chave `pv_atual` cai em tempo real. Se chegar a 0, injetamos a infame flag `[SISTEMA FATAL]`.

### 4. A Narração de Game Over
O *Tradutor Narrativo* (Fase 2) agora atua não apenas como mediador, mas como o ceifador. Ele narra a sua investida, logo em seguida narra as contra-investidas (tudo em um fluxo de texto brutal). Se ele detecta a flag de morte no log de máquina, a regra manda ele ser seco, imersivo e declarar que "a jornada chegou ao fim" — fechando a história permanentemente.

---

### Prova de Fogo (Teste Unitário)
No nosso teste interno, o *Bardo Bob* com `HP 10` e `CA 10` (mock enfraquecido) atacou um ninho de goblins. Ele errou o teste contra CA 15.
Imediatamente, o Motor rolou D20s para os dois Goblins reagindo. Ambos acertaram. A Narrativa traduzida da IA foi:

> *"Você avança pelas sombras da caverna e tenta cravar sua espada... mas a lâmina raspa inofensiva. O erro custa caro: o lacaio ri esganiçadamente e revida, cravando uma adaga enferrujada profundamente na sua costela... Antes que você possa se desvencilhar, o segundo goblin salta, enfiando uma lança rudimentar direto no seu abdômen. O frio da lâmina perfura suas entranhas... Sua jornada termina aqui, esquecida na poeira e no sangue. Game Over."*

### Falhas Conhecidas / Próximas Melhorias
A estrutura base está sublime. 
- **Conclusão / Vitória:** Já temos o "Game Over" de combate, e eu incluí regras implícitas para respeitar desmaios, mas precisamos em breve de um "Game Over de Vitória" quando a "Quest" (Módulo de Missões, talvez?) for concluída.
- **Tempo/Idade:** O sistema não passa "Anos". Ele roda "Turnos". O jogador não morrerá de velhice antes de terminarmos um sistema estruturado de "Time Skip" global (Dias passados ao acampar ou viajar no Mapa-Múndi).

Missão concluída. O combate agora é visceral, rápido, puramente matemático por debaixo dos panos, e belíssimo em prosa.
