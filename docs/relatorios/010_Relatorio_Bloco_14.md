# Relatório do Bloco 14 (Grid e Softlock)

Diretor, completei a cirurgia tática com sucesso no "Crônicas da Taverna". A arquitetura subjacente está agora mais robusta contra mortes em combate e a escala visual finalmente reflete o tamanho das criaturas do D&D.

### 1. Prevenção de Softlock de Morte
**A Causa:** Antes, a matemática alterava a vida para `0` e escrevia "Você morreu", mas a fase não era cancelada estruturalmente. A IA poderia tentar atacar de novo num turno seguinte e bugar o motor.
**O Polimento:** Modifiquei a função `resolve_action` em `combat_system.py` para devolver um dicionário estrito: `{"sys_log": ..., "status": ...}`. Agora, se o `pv_atual` do jogador cair para `<= 0`, ela retorna o status `"player_dead"`.
O `game_engine.py` (Worker da Thread) enxerga isso instantaneamente, trava a máquina de estados em `GAME_OVER`, expulsa os inimigos ativos da RAM e força a IA a descrever a morte em definitivo, sem margem para travar a tela ou bugar o Pygame.

### 2. Escalonamento e Proporção Épica (Grid Tático)
**O Motor de Tamanho:**
- Injetei a chave `"tamanho": int` (1 a 3) em toda a biblioteca matemática do `BESTIARIO_5E`. Um monstro médio tem tamanho 1, Ogros têm 2 e o temível Kraken recebeu tamanho 3.
- No `ui/asset_manager.py`, modifiquei a busca pelo inimigo: agora ele consulta o `BESTIARIO_5E` em tempo real. Se o Kraken for puxado, o `AssetManager` multiplica o tile padrão de `64px` por `3`, devolvendo à interface gráfica uma `pygame.Surface` imponente de `192x192` píxeis!

### 3. Portraits de Diálogo (Estilo JRPG)
**O Filtro:** Para separar as artes de Token (que vão pro combate) das artes de Rosto (que vão pro diálogo), ensinei a função `load_enemies()` do `AssetManager` a ignorar completamente qualquer arquivo com a palavra `icone` no nome. 
**A Inteligência:** Ensinei a Fase 0 do Parser (Prompt do LLM) a enviar a chave `npc_falando` caso um monstro insulte ou dialogue com o jogador (ex: `"npc_falando": "Lich"`).
**A Tela:** Na hora de desenhar (`scene_renderer.py`), adicionei um verificador. Se a bolha narrativa tiver um `npc_falando` ativo, ele puxa esse portrait separadamente do HD (pela nova função `get_portrait_sprite`) e estampa no canto inferior esquerdo da tela, mantendo a escala de 100x100px.

A máquina está fluida e muito mais cinemática. Quais são as suas ordens para o Bloco 15?
