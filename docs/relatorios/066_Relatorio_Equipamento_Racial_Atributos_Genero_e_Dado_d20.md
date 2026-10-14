# Relatório 066: Conclusão do Equipamento Inicial (Classe + Item Único Racial), Standard Array por Classe, Indicativo de Gênero (`♂/♀`) e Animação do Dado d20 Pixel Art

**Projeto:** RPGMesaPY (VTT 2D D&D 5e Dark Fantasy)  
**Data:** 12/10/2026  
**Subagentes Envolvidos:** `dev-backend-dnd` (Regras D&D 5e, Standard Array & Itens Raciais), `dev-frontend-ui` (Ficha de Criação, Badges de Gênero & Frames do Dado d20), `dev-ia-prompt` (Direção de Arte & Prólogo com Herança Racial/Gênero)  
**Status da Suíte de Testes:** 91/91 Testes Aprovados (100% de Sucesso, 0 Falhas)  

---

## 1. Visão Geral das Entregas

1. **Higienização Ortográfica de [`core/dnd_rules.py`](file:///c:/Users/iagob/RPGMesaPY/core/dnd_rules.py):**
   - Correção integral de todos os textos e acentuações nas Raças, Classes, Antecedentes, Tendências e Bestiário (`Sábio`, `Ancestral Dracônico`, `Resistência a Dano`, `Conjuração`, `Médio`, `idiomas`, `Pés Ligeiros`, etc.).
2. **Atributos D&D 5e Corretos na Criação de Personagem (Standard Array por Classe + Bônus Racial):**
   - Implementados [`CLASS_STANDARD_ARRAY`](file:///c:/Users/iagob/RPGMesaPY/core/dnd_rules.py#L18-L25) e [`get_class_base_attributes()`](file:///c:/Users/iagob/RPGMesaPY/core/dnd_rules.py#L27-L39), aplicando automaticamente a distribuição oficial `15, 14, 13, 12, 10, 8` nos atributos principais da Classe selecionada + soma exata dos bônus da Raça (sincronizando `FOR/STR`, `DES/DEX`, `CON`, `INT`, `SAB/WIS`, `CAR/CHA`).
3. **Equipamento Inicial Ajustado (2 da Classe + 1 Item Único da Raça):**
   - Adicionados os **7 Itens Únicos Raciais** em [`data/items.json`](file:///c:/Users/iagob/RPGMesaPY/data/items.json) e [`ITENS_UNICOS_RACIAIS`](file:///c:/Users/iagob/RPGMesaPY/core/dnd_rules.py#L42-L96).
   - Na Ficha de Criação, as 3 linhas de `Equipamento` mostram: (1) Armadura/Traje da Classe, (2) Arma Principal da Classe, e (3) O **Item Único da Raça escolhida**, já aplicando seus bônus mecânicos na ficha!
4. **Indicativo Visual Intuitivo de Gênero (`♂ Masculino` / `♀ Feminino`) sem alterar `char_sheet_bg.png`:**
   - Mapeamento oficial dos 42 arquétipos (`PROT-01` a `PROT-42`) em [`PROTAGONIST_GENDER_MAP`](file:///c:/Users/iagob/RPGMesaPY/core/dnd_rules.py#L99-L128).
   - Selo nativo **`[ ♂ Masculino ]`** / **`[ ♀ Feminino ]`** exibido dentro da caixa de `Raça:` na Ficha, flexão de nome com símbolo na caixa de `Classe:` (`Clériga ♀`, `Maga ♀`, `Patrulheira ♀`, `Ladina ♀`, `Guerreiro ♂`, `Mago ♂`, `Paladino ♂`) e indicadores `(♂)` / `(♀)` nos modais `RaceSelectionPanel` e `ClassSelectionPanel`.
5. **Animação do Dado d20 Pixel Art Girando na Tela (`assets/ui/dice_loading/` e [`LoadingDiceAnimation`](file:///c:/Users/iagob/RPGMesaPY/ui/hud_components.py#L2015)):**
   - Gerados os **12 frames `.png` (`96x96` RGBA)** em `assets/ui/dice_loading/frame_1.png` a `frame_12.png`, reproduzindo fielmente o d20 vermelho-rubi facetado em pixel art da ficha com *ordered dithering*, arestas de ouro velho e fagulhas.
   - Adicionada bandeja gótica de madeira/bronze sob o dado, quique vertical suave durante o giro e modo de impacto [`trigger_roll_result()`](file:///c:/Users/iagob/RPGMesaPY/ui/hud_components.py#L2136) cravando o resultado na tela (com destaque para `★ 20 CRÍTICO! ★` e `1 FALHA CRÍTICA!`).

---

## 2. Tabela dos 7 Itens Únicos Raciais Implementados

| Raça | Item Único Racial (Linha 3 da Ficha) | ID (`data/items.json`) | Bônus Aplicado Automaticamente |
|---|---|---|---|
| **Humano** | `Sinete da Coroa Partida` | `i_racial_human_signet` | `+1` em Testes de Resistência e `+10 PO` iniciais (total 25 PO) |
| **Elfo da Floresta** | `Manto de Folhas Cinzentas` | `i_racial_elf_cloak` | `+1` na Iniciativa e `+2` em Furtividade |
| **Anão da Colina** | `Runa da Pedra-Forja` | `i_racial_dwarf_rune` | `+3` Pontos de Vida Máximos (+1 PV de Tenacidade Anã = +4 PV) |
| **Halfling** | `Moeda da Sorte Antiga` | `i_racial_halfling_coin` | `+1` na Classe de Armadura (CA) e `+2` em Sorte (`LUCK`) |
| **Draconato** | `Escama Ancestral Incandescente` | `i_racial_dragon_scale` | `+1` no Dano de ataques e Arma de Sopro |
| **Meio-Orc** | `Presa de Ferro Sangrento` | `i_racial_orc_tusk` | `+1` no Dano corpo a corpo e `+2` em Intimidação |
| **Tiefling** | `Selo de Brasas Abissais` | `i_racial_tiefling_seal` | `+1` no Acerto e CD de Magias |

---

## 3. Validação e Suíte de Testes (91 Testes)

```text
python -m unittest discover tests
...........................................................................................
----------------------------------------------------------------------
Ran 91 tests in 18.5s

OK (100% de Sucesso - 91 testes aprovados, 0 falhas)
```

