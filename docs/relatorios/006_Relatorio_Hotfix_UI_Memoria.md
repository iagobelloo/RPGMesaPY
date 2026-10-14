# Relatório de Hotfix (UI Visual e Memória de IA)

A auditoria solicitada pelo Diretor foi concluída e os patches de código foram aplicados ao sistema. Abaixo estão as correções, validações arquiteturais e análise de impacto.

### 1. Refatoração Visual (ui/asset_manager.py)
**O Bug Original:** Quando o sistema tentava carregar um arquivo inexistente, o `try/except` desabava e a classe criava um `pygame.Surface(150, 300)` gigante que quebrava o grid visual do motor Pygame. Além disso, nomes com espaços ou maiúsculas podiam não dar *match* com o nome do arquivo, causando falsos negativos.

**A Solução Aplicada:** 
- A chave de busca e o processo de salvamento em memória agora utilizam estritamente `.lower().replace(" ", "_")` (Ex: "Lacaio Goblin" vira "lacaio_goblin"), alinhando a string limpa com o sistema de arquivos.
- A Geração do Fallback Visual foi reescrita. Caso a imagem não exista de jeito nenhum (mesmo usando o "Cosplay" adaptativo), o Motor injeta um bloco cinza restrito a `TILE_SIZE = (64, 64)`, que é o tamanho de célula padrão, preservando o alinhamento da janela gráfica do Pygame.
- Mensagens de `print()` foram adicionadas apontando exatamente o path que falhou, permitindo debugar artes faltando.

### 2. Memória Narrativa (Histórico em ai_client.py)
**O Bug Original:** A Fase 2 (Narrador) recebia apenas os 3 blocos fixos do turno atual. Para a IA, era como se o mundo tivesse começado naquele segundo, repetindo eternamente a descrição do cenário base.

**A Solução Aplicada:**
- Criei a propriedade `self.chat_history = []` no inicializador do `AIGameMaster`.
- Implementei o sistema de **Sliding Window (Janela Deslizante)** de 5 interações: Ao fim de cada turno, o motor guarda o comando exato que o Jogador digitou e a narrativa que o Mestre retornou.
- A Fase 2 agora injeta uma chave extra no Prompt: `[HISTÓRICO RECENTE]`, contendo as últimas linhas conversacionais. A IA agora sabe o que acabou de acontecer!

### 3. Reescrita do Prompt do Narrador (Avanço de Plot)
O Prompt da Fase 2 (Tradutor Narrativo) recebeu suas ordens marciais de **não repetir cenário**. O comando inserido foi:
> *"Você é um Mestre de Jogo de D&D 5e (Dark Fantasy). REGRA DE OURO: NUNCA repita a descrição do cenário. O jogador já sabe onde está. O seu papel é AVANÇAR o enredo."*

**A Blindagem do Parser (Fase 0):** A injeção dessas regras foi feita restritamente no escopo da função `generate_narrative_from_log` (Fase 2). A função que extrai a intenção mecânica (Fase 0) roda com `temperature=0.0` e um prompt completamente diferente, mantendo-se imaculada e gerando apenas o JSON puro, sem misturar prosas narrativas nas chaves do dicionário.

### Análise de Risco (Possíveis Falhas)
1. **Janela Deslizante e Tokens:** O uso das 5 últimas interações adiciona texto ao LLM. Como estamos usando o `gemini-3.5-flash-lite`, ele suporta um milhão de tokens, portanto não causará crash de tamanho, mas o aumento do contexto pode aumentar levemente o tempo de inferência (cerca de +200ms na Fila Assíncrona). 
2. **Nomenclatura Cruzada:** Agora que o `get_character_sprite` usa nomes totalmente minúsculos e com *underline* (`_`), os nomes das pastas no disco rígido do usuário precisam respeitar o padrão ou o sistema vai imprimir o `[WARNING]` no terminal e usar o fallback cinza de 64x64. O jogo **não vai crashar**, mas o erro gráfico ficará visualizável até a arte correta ser inserida na pasta `assets`.

O motor continua assíncrono, operando em Threads seguras, sem engasgar o Pygame! Missão cumprida.
