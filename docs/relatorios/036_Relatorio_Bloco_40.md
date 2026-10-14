# Relatório de Implementação: Bloco 40 - Parser Gráfico, Lixeiro de Cadáveres e Gatilhos de Vitória

## 1. Visão Geral
Esta missão finalizou o polimento visual de campo de batalha (removendo a complexidade desnecessária dos tokens) e sedimentou o loop principal de game design. A transição de Combate para Exploração está automática, e a condição absoluta de Fim de Jogo ("Epílogo") foi codificada contra o dragão final.

## 2. Ações Executadas

### 2.1. O Parser Gráfico UUID (`ui/asset_manager.py` e `ui/scene_renderer.py`)
- O método `get_enemy_sprite` foi refatorado para ser determinístico. A renderização agora desacopla a chave descritiva na tela (`npc_id` gerada pelo uuid4, que o player vê na barra de vida) da chave física do asset (`tipo_bestiario`). 
- **Filtro Aplicado**: `tipo_bestiario.replace("m_", "") + ".png"` é o novo padrão rígido. 
- **Failsafe Visual Inquebrável**: Se a pipeline gráfica requisitar um inimigo cujo `.png` não exista na pasta, o Pygame não irá travar (crash). O engine irá desenhar programaticamente um Placeholder *(um quadrado vermelho sólido com a string 'ERR' inscrita em texto)*, permitindo que a sessão prossiga.

### 2.2. Lixeiro de Cadáveres Dinâmico (`core/game_engine.py`)
- A verificação de ciclo ao fim de cada Loop (`_async_turn_processor`) ganhou uma camada rigorosa de verificação de HP.
- Agora, imediatamente após o jogador *ou* a horda de inimigos finalizarem suas ações, uma varredura instantânea checa a lista `active_combat_targets`.
- Qualquer entidade (aliado ou inimigo) que caia a `0` HP é deletada das instâncias visuais e mecânicas, sendo apagada do tabuleiro antes do próximo _tick_ de UI. Isso também impede "Ataques Fantasmas" contra alvos que já morreram.

### 2.3. Os Gatilhos do Diretor (Vitória e Epílogo)
O método `check_combat_resolution` foi criado para avaliar o encerramento do encontro:
- **Vitória Normal**: Se a mesa é limpa no Beat 1 a 14, o estado do jogo destrava para `"EXPLORACAO"`. O LLM do Mestre de Jogo é silenciosamente ativado por baixo dos panos (via `generate_narrative_from_math`) recebendo um prompt de [SISTEMA] para narrar o recolhimento de despojos, o som ambiente após a batalha e encorajar o jogador a seguir a trilha.
- **Epílogo**: Ao executar e varrer os alvos no *Beat 15*, a engine entra em sobrecarga narrativa. Ela declara o encerramento e não destrava as portas. A inteligência artificial é notificada da queda do *Tirano das Cinzas* e compila o fechamento poético da aventura ("FIM DA DEMO").

## 3. Testes Executados
Os testes automatizados construídos (`test_bloco_40.py`) atestam com sucesso os resultados lógicos do Motor:
1. `Matar 1 de 2`: O HP de 1 Goblin zera. O loop confirma o apagamento exclusivo de 1 índice e sustenta o Game State = COMBATE.
2. `Vitória Limpa`: O último HP zera no Beat 1. Game State passa livremente para EXPLORACAO.
3. `Triunfo Absoluto`: HP do Boss zera no Beat 15. Game State trava imutável em EPILOGO.
