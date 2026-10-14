# Relatório do Bloco 13 (Máquina de Estados de Combate Híbrida)

O **Ciclo de Aventura** foi totalmente desacoplado da visão rígida do combate por turnos ininterrupto. O "Crônicas da Taverna" agora compreende quando o jogador está apenas caminhando e quando o sangue começa a jorrar, tudo de forma orgânica e protegendo o Pygame contra _Thread Crashes_.

### 1. A Nova Inteligência Espacial (game_engine.py e ai_client.py)
**Gatilhos de Fase 0 (Parser):** Instilei o LLM a decidir a `intencao_cena`. Se o jogador explorar, ele envia `"manter"`. Se o jogador sacar a espada, ele grita `"iniciar_combate"`. Se o jogador quiser fugir das mecânicas, ele diz `"fugir"`.
**Modos Híbridos:** 
- **`EXPLORACAO`**: Ninguém ataca e ninguém recebe dano, a não ser que o jogador use cura ou sofra dano ambiental (teste de perícia).
- **`COMBATE`**: O motor assume, o lixeiro de cadáveres liga e o XP rola.

### 2. A Fuga e a Vitória (combat_system.py)
**Fuga:** Se a IA permitir a intenção `"fugir"`, o motor descarrega os monstros e destrava o modo para `EXPLORACAO`. O jogador escapa com a vida que lhe restou.
**Vitória e Exp:** Se o motor matar todos (Garbage Collector esvaziar a lista), ele mesmo anuncia vitória, concede +50 XP por monstro e destrava a aventura.

### 3. A Regra de Ouro (Segurança SDL/OpenGL do Pygame)
**Vazamento Interrompido:** Como você sabiamente alertou, renderizar um arquivo `.png` no meio de uma Thead Assíncrona corromperia a interface do Pygame ou travaria o cache SDL da placa de vídeo.
**Solução Aplicada:** O código do `game_engine.py` (que roda em Thread) foi modificado para injetar **apenas uma string** (ex: `"lacaio goblin"`) no banco de dados. O arquivo da interface gráfica real (`ui/scene_renderer.py`), que roda seguro na Thread Principal do PC, é quem usa essa string para "pescar" e desenhar a imagem instanciada pelo `AssetManager` no tempo certo (FPS).

### Teste de Mesa (Sucesso e Permadeath)
Realizei o laboratório no console injetando o personagem na Estrada e com apenas 2 PV.
1. Em Exploração, o Motor rodou suave.
2. O jogador iniciou a luta; o Parser detectou `"iniciar_combate"` e mudou a flag do motor na hora.
3. O jogador **Errou** o ataque.
4. O Goblin **Acertou** o ataque (3 de dano) — o Motor matou o jogador e engatilhou o `[SISTEMA FATAL]`.
5. Mesmo tentando usar o comando de fuga no passo 3 (o motor acatou e voltou para Exploração), a vida do jogador era 0 e a narrativa decretou `Game Over`. 

A estrutura é sólida. Qual o nosso próximo passo?
