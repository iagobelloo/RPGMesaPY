# Relatório da "Grande Cirurgia" (Módulo 2 Assíncrono Completo)

A Grande Cirurgia foi executada com precisão. O Motor do RPGMesaPY agora é totalmente assíncrono, operando no pipeline **Fase 0 -> Fase 1 -> Fase 2**, sem qualquer engasgo na interface do VTT.

### 1. Desacoplamento Assíncrono (`queue.Queue`)
No `core/game_engine.py`, criamos a variável `session.ui_queue`. Quando o jogador pressiona *Enter*, disparamos o método `process_action_async`, que isola o pensamento do LLM em uma Thread Daemon.
Enquanto o `ai_client` está rodando chamadas pesadas, o Pygame (no arquivo `main.py`) continua batendo seus gloriosos 60 quadros por segundo, animando a tela e escutando os cliques, limitando-se apenas a checar se a `ui_queue` possui uma nova narrativa terminada.
**Impacto:** "Crash" do tipo "Não Respondendo" foi eliminado. A UI agora desenha imediatamente o que ocorre nos bastidores de forma responsiva.

### 2. O Estado Persistente de Batalha (HP)
Para resolver o problema crônico dos inimigos invencíveis da Fase 1, criei a variável global `self.active_combat_targets` no `SessionManager`. 
**Como funciona?** 
1. A Fase 0 do LLM avisa: *"O Orc Brutal entrou em cena."*
2. A Thread cria o mock persistente na memória da classe: `{"name": "Orc Brutal", "pv_atual": 20, "pv_max": 20, "ca": 12}`.
3. No turno 1, a matemática da Fase 1 subtrai do HP e altera a chave `"pv_atual"`. 
4. No turno 2, o orc **ainda tem o mesmo objeto alocado na memória**, o que permite que ele caia gradualmente até o 0 HP, sem resetar a cada "Enter".

*Log de Prova Coletado no Motor:*
```text
=== TURNO 1 ===
Narrativa: A lâmina de aço corta o ar e acerta o peito da criatura...
Status HP: {'Orc Brutal': {'name': 'Orc Brutal', 'pv_atual': 8, 'pv_max': 20, 'ca': 12}}

=== TURNO 2 ===
Narrativa: Com um estalo seco, a ponta da sua espada acha a carne grossa...
Status HP: {'Orc Brutal': {'name': 'Orc Brutal', 'pv_atual': 6, 'pv_max': 20, 'ca': 12}}
```

### 3. A Nova Renderização UI (`scene_renderer.py`)
Erradiquei o antigo `AssetManager.get_image()` que causava quebra se a string não existisse. Agora o renderizador se conecta diretamente às listas `session.active_visual_npcs` e `session.current_background_key` manipuladas pela Thread. 
- Ele puxa as `Health Bars` olhando não mais pro antigo `active_entities`, mas pro novíssimo e contínuo `active_combat_targets`.
- Ele aplica um Offset no Eixo X (multiplicado por 150 pixels) para alinhar múltiplos goblins, esqueletos ou NPCs pacíficos ombro a ombro na direita do cenário, sem se sobreporem, sempre renderizados como as imponentes silhuetas de Cosplay (150x300).

---

### Diagnóstico & Próximas Melhorias
A estrutura basilar do VTT agora é nível de produção.
- **Falha Conhecida (Melhoria Futura):** Nossos inimigos inseridos no `active_combat_targets` sempre assumem um perfil MOCK Genérico `(CA 12, HP 20)`. No futuro (Módulo 3 ou similar), a Thread deverá cruzar a "raça_visual" com aquele nosso dicionário espetacular `BESTIARIO_5E` do arquivo `dnd_rules.py` para puxar os Atributos e AC oficiais de um Goblin ou Quimera quando ele surgir.
- **Ajuste de Câmera:** Os `Tokens` dos personagens no fundo da tela também passaram a utilizar o `AssetManager.get_character_sprite`, garantindo blindagem aos arquivos e gerando consistência visual em todo o app.

Projeto integrado com sucesso. O motor assíncrono dita as regras agora!
