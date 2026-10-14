# Relatório: Correção Bloco 38 - Blindagem do Padrão Inglês e Tratamento de Erros de Asset

## 1. Visão Geral
Nesta fase, modernizamos todo o sistema de carregamento de texturas e imagens do jogo para torná-lo resistente a erros e para usar os identificadores estruturais rígidos em vez de strings narrativas em português, em preparação ao grande expurgo de nomenclaturas irregulares e à padronização do código fonte.

## 2. Refatoração do AssetManager
O coração da UI visual, a classe `AssetManager`, foi inteiramente reescrita e limpa de código de fallback desatualizado:
- **Heróis:** O antigo sistema de chaves baseadas em (Raça + Classe + Gênero) foi substituído por uma busca explícita no banco de dados (`classes.json`). Agora a classe do jogador informa nativamente a chave `sprite_path` exata a ser procurada em `assets/sprites/heroes`.
- **Cenários:** A engine gráfica agora exige que o Motor Narrativo (`scene_renderer.py` lendo de `campaign.json`) especifique o arquivo visual do fundo através da chave `bg_image` de cada Beat, em vez de depender da correspondência pelo nome em inglês traduzido do Beat.
- **Inimigos:** O parser já procurava com segurança limpando o prefixo `"m_"`. Ele foi mantido mas adicionado às proteções globais abaixo.

## 3. Segurança Anti-Crash (Failsafe)
- **Tolerância a falhas FileNotFoundError:** Todos os blocos onde a UI engata e tenta executar o carregamento I/O no disco físico usando `pygame.image.load()` foram envolvidos com um `try/except`.
- Caso o ficheiro se encontre corrompido, bloqueado pelo sistema operacional, com extensão diferente, ou com nomenclatura errada, a UI exibirá imediatamente no terminal:
`[ERRO UI] Ficheiro 'X' não encontrado. Usando placeholder.`
- **Placeholder Visuais:** A UI gera quadros com a cor magenta (`(255, 0, 255)`) e os injeta transparentemente na renderização em vez das superfícies ausentes. Foram aplicados dois padrões de tamanho que correspondem rigorosamente ao requisitado:
  - Backgrounds: Superfície de `800x600`.
  - Entidades: Superfície de `64x64`.

## 4. Teste e Validação
A script automatizada validou com sucesso todos os fluxos ao forçar a inicialização sem as texturas necessárias, comprovando o isolamento perfeito do core sem crashes em tempo de execução. Tudo funciona perfeitamente!
