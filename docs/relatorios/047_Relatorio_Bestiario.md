# Relatório de Operação: Sincronização do Bestiário (Missing Data)

**Diagnóstico da Falha:**
Ao analisar os logs e cruzar os dados, identifiquei o **Cenário B (Dados Faltantes)**. O motor do jogo (`core/story_engine.py`) estava lendo as chaves corretas (ex: `"m_dire_wolf"`, `"m_bandit"`) da lista `enemies` do `campaign.json`, mas o arquivo `data/bestiary.json` estava praticamente vazio, contendo apenas o `boss_final`. Isso forçava o motor a gerar entidades genéricas de *fallback* com 1 de HP.

**A Solução Aplicada:**
Para não correr o risco de truncar a saída do JSON ou corromper a formatação (já que a lista de inimigos era longa, com cerca de 25 monstros espalhados pelos 15 Beats da campanha), criei e executei um script Python temporário. 

O script realizou as seguintes ações:
1. Carregou o `data/bestiary.json` existente via `json.load()` com `utf-8`.
2. Injetou programaticamente um dicionário com os status balanceados no formato D&D 5e (Nome, HP, AC e Actions) para todos os monstros referenciados na campanha (incluindo `m_dire_wolf`, `m_bandit`, `m_goblin`, `m_skeleton`, `m_supreme_dragon`, etc.), preservando os prefixos `m_` para dar o *"match"* exato com a engine.
3. Salvou o arquivo de volta via `json.dump()`.

**Status Final:**
Operação concluída. O JSON foi atualizado e re-escrito com sucesso. A `StoryEngine` agora vai spawnar os inimigos reais (Lobo Atroz, Bandido, etc.) com Vida, CA e Danos balanceados para o combate.
