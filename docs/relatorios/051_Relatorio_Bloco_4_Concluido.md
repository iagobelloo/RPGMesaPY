# Relatório de Correções do Bloco 4 (UI Gráfica)

Foi concluída a manutenção e o polimento da interface requisitados no Bloco 4.

## 1. Caixa de Input (Chat inferior cobrindo a tela)
- **Problema:** A caixa de texto de digitação (`ChatBox`) estava com largura 100%, atravessando a área visual do jogo e cortando a visão de personagens/cenários.
- **Solução:** A largura da caixa de chat foi cortada para exatamente 40% da tela (`panel_w`), alinhando-se perfeitamente debaixo do painel de histórico à esquerda. A área da direita (jogo) agora fica livre até o chão.

## 2. Histórico de Conversa e Prólogo (Não aparecia direito)
- **Problema:** Como o prólogo era muito longo e a rolagem renderizava de baixo pra cima de forma bruta, partes sumiam e era difícil ler o contexto.
- **Solução:** O `draw_side_dialog_panel` foi reescrito do zero.
  - Agora ele renderiza de cima para baixo corretamente (Top-to-Bottom).
  - Foi **adicionada uma barra de rolagem (Scrollbar) visual e interativa** no canto direito do painel de chat.
  - A direção da rodinha do mouse (Mousewheel) foi consertada para ser natural.
  - Sempre que uma mensagem nova chega, a barra dá scroll automático para baixo.
  - Assim, o prólogo vai aparecer inteirinho e o jogador pode rolar para o começo dele.

## 3. Imagem da Taverna (Background incorreto)
- **Problema:** O jogo buscava a imagem `tavern_bg.jpg` na pasta de `Fases`, mas a imagem real da taverna se chamava `tavern.jpg` e ficava na pasta anterior.
- **Solução:** A imagem oficial da Taverna foi copiada e renomeada corretamente para dentro da pasta `Fases` usada pelo Asset Manager. Agora a Taverna aparece perfeitamente.

---

### Próximos Passos
As pendências visuais cruciais (HUD estourando e rolagem do chat) foram resolvidas. O motor narrativo/batalha também já foi fixado no Bloco 3.

Gostaria de fazer o **Playtest final** agora e jogar um pouco para conferir o visual e o combate, ou há mais algum ajuste em mente que você gostaria de colocar num Bloco 5?
