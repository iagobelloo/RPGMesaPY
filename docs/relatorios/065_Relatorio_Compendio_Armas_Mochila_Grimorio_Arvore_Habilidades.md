# Relatório 065: Conclusão do Compêndio de Armas Balanceadas, Limite de Carga da Mochila, Redesign do Grimório (Herói em Pé) & Árvore de Habilidades das 6 Classes

**Projeto:** RPGMesaPY (VTT 2D D&D 5e Dark Fantasy)  
**Data:** 12/10/2026  
**Subagentes Envolvidos:** `dev-backend-dnd` (Regras & Engine), `dev-frontend-ui` (Interface Pygame & Grimório), `dev-ia-prompt` (Direção de Arte de Ícones & Voz de Maelor)  
**Status da Suíte de Testes:** 84/84 Testes Aprovados (100% de Sucesso, 0 Falhas)  

---

## 1. Visão Geral das Entregas

Conforme aprovado na proposta arquitetural, executamos a reformulação completa dos sistemas de equipamento, inventário, evolução de nível e habilidades de classe:

1. **Compêndio de Armas Balanceadas (7 Famílias = 21 Armas):**
   - Cada família de armas conta agora com **2 variações táticas base + 1 versão aprimorada no ferreiro (+1)** em [`data/items.json`](file:///c:/Users/iagob/RPGMesaPY/data/items.json).
2. **Raridade da Ressurreição e Kit Inicial:**
   - O `Pergaminho de Ressurreição` (`i_scroll_revive`) foi removido do kit inicial, reclassificado como item **Lendário** (`price_gold: 200`). O herói inicia a campanha com 1 Poção de Cura (`2d4+2`) e 2 Rações de Viagem.
3. **Limite de Carga da Mochila:**
   - Sistema determinístico de capacidade: **10 slots base + Modificador de Força** (mínimo 10, máximo 14 slots).
   - Empilhamento inteligente: Armas/Armaduras (1/slot), Poções/Elixires (até 3/slot), Rações (até 5/slot), Acessórios (até 2/slot).
4. **Redesign da Ficha do Herói no Grimório Aberto (`GrimoireModal`):**
   - **Página Esquerda:** O **personagem em pé** (sprite 2.5D de corpo inteiro sobre pedestal de pedra com sombra elíptica e anel rúnico), 4 slots visuais interativos (`⚔ ARMA`, `🛡 ARMADURA`, `❖ ESCUDO`, `✧ ACESSÓRIO`), barra segmentada de carga da bolsa (`Carga: X / Y Slots`) e botão rápido para abrir a Mochila.
   - **Página Direita:** Grid 3x2 de Atributos D&D 5e (`FOR`, `DES`, `CON`, `INT`, `SAB`, `CAR`) com modificadores, barras de PV e XP, CA, Iniciativa, Deslocamento, Proficiência e botão **`Subir de Nível ★`**.
   - **Modal Interativo de Level Up:** Alocação de +2 pontos de atributo (`+2 em 1` ou `+1 em 2`), ganho automático de PV e desbloqueio da habilidade do tier correspondente.
5. **Árvore de Habilidades Simplificada das 6 Classes (24 Habilidades):**
   - 4 Tiers (Níveis 1, 2, 3 e 5) para **Guerreiro, Clérigo, Mago, Paladino, Patrulheiro e Ladino** em [`data/class_skills.json`](file:///c:/Users/iagob/RPGMesaPY/data/class_skills.json).
   - Ícones quadrados de **40x40 pixels** com moldura chanfrada de bronze/ouro nos 3 estados (`Adquirida ✓`, `Disponível ★`, `Bloqueada 🔒`).
   - Especificação estética e prompts de geração documentados em [`docs/prompts_skills_art_direction.md`](file:///c:/Users/iagob/RPGMesaPY/docs/prompts_skills_art_direction.md).

---

## 2. Compêndio de Armas (7 Famílias x 3 Variações)

| Família | Variação Base 1 | Variação Base 2 | Versão Aprimorada (+1 Ferreiro / Rúnica) |
|---|---|---|---|
| **1. Espadas** | `i_shortsword` — Espada Curta (`1d6`, acuidade, leve) | `i_longsword` — Espada Longa (`1d8`/`1d10`, versátil) | `i_forged_longsword` — Espada Longa de Aço Forjado +1 (`1d8+1`, +1 acerto/dano) |
| **2. Armas Pesadas** | `i_greatsword` — Montante (`2d6`, pesada, 2 mãos) | `i_greataxe` — Machado de Guerra (`1d12`, pesada, 2 mãos) | `i_adamantine_greatsword` — Montante de Adamante das Cinzas +1 (`2d6+1`, +1 acerto/dano) |
| **3. Lâminas Ágeis** | `i_dagger` — Adaga de Caça (`1d4`, acuidade, leve) | `i_rapier` — Rapieira de Duelo (`1d8`, acuidade) | `i_serrated_dagger` — Adaga de Mithral Serrilhada +1 (`1d4+1`, crítico 19-20) |
| **4. Impacto / Sagradas** | `i_mace` — Maça Flangeada (`1d6`, simples) | `i_warhammer` — Martelo de Guerra (`1d8`/`1d10`, versátil) | `i_blessed_hammer` — Martelo Abençoado do Alvorecer +1 (`1d8+1`, +1 acerto/dano) |
| **5. Arcos** | `i_shortbow` — Arco Curto (`1d6`, 2 mãos) | `i_longbow` — Arco Longo de Teixo (`1d8`, pesada, 2 mãos) | `i_elven_longbow` — Arco Élfico de Madeira-Cinza +1 (`1d8+1`, +1 acerto/dano) |
| **6. Bestas** | `i_light_crossbow` — Besta Leve (`1d8`, recarga) | `i_hand_crossbow` — Besta de Mão (`1d6`, leve, recarga) | `i_reinforced_crossbow` — Besta Mecânica Reforçada +1 (`1d8+1`, +1 acerto/dano) |
| **7. Focos / Bastões** | `i_wand` — Varinha de Freixo (foco arcano, leve) | `i_quarterstaff` — Bordão de Carvalho (`1d6`/`1d8`, foco) | `i_arcane_staff` — Cajado Arcano do Vácuo +1 (`1d6+1`, +1 CD e acerto mágico) |

---

## 3. Árvore de Habilidades das 6 Classes

| Classe | Nível 1 (Tier 1) | Nível 2 (Tier 2) | Nível 3 (Tier 3) | Nível 5 (Tier 4) |
|---|---|---|---|---|
| **Guerreiro** | Retomar o Fôlego (`1d10+Nv` PV) | Surto de Ação (+1 ação no turno) | Foco do Campeão (Crítico 19-20) | Ataque Extra (2 ataques/turno) |
| **Clérigo** | Bênção da Cura (`+2+Nv` PV cura) | Preservar a Vida (`5xNv` PV em área) | Escudo da Fé (`+2 CA` sagrado) | Fogo Radiante (`+1d8` radiante) |
| **Mago** | Recuperação Arcana (+1 slot Nv 1) | Evocação Potente (`+INT` no dano) | Escudo Arcano (`+5 CA` reação) | Mestre dos Elementos (`+1 CD` magias) |
| **Paladino** | Cura pelas Mãos (`5xNv` PV toque) | Destruição Divina (`+2d8` radiante) | Aura de Coragem (Imune a medo, `+1` Saves) | Golpe Abençoado Extra (2 ataques) |
| **Patrulheiro** | Marca do Caçador (`+1d6` dano) | Estilo Arquearia (`+2` acerto distância) | Matador de Colossos (`+1d8` em feridos) | Rajada de Flechas (2 disparos) |
| **Ladino** | Ataque Furtivo (`+1d6` vantagem) | Ação Ardilosa (Esquiva/Disparada bônus) | Emboscada Mortal (`+2d6` furtivo, crítico) | Esquiva Sobrenatural (Metade do dano) |

---

## 4. Validação e Suíte de Testes (84 Testes)

Foram adicionadas duas novas suítes completas:
* [`tests/test_items_capacity_and_skills.py`](file:///c:/Users/iagob/RPGMesaPY/tests/test_items_capacity_and_skills.py) (7 testes de backend para armas, limite de carga, raridade de reviver e árvore de habilidades).
* [`tests/test_grimoire_character_sheet_ui.py`](file:///c:/Users/iagob/RPGMesaPY/tests/test_grimoire_character_sheet_ui.py) (5 testes de UI para o herói em pé no pedestal, slots de equipamento, árvore de habilidades visual e modal de Level Up).

```text
python -m unittest discover tests
....................................................................................
----------------------------------------------------------------------
Ran 84 tests in 27.6s

OK (100% de Sucesso - 84 testes aprovados, 0 falhas)
```

