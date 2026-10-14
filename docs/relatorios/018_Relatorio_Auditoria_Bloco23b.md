# Relatório de Auditoria Matemática (Bloco 23b) - Backend D&D 5e
**Status:** Concluído
**Analista:** Dev Backend D&D (Antigravity)
**Alvo da Auditoria:** `core/game_engine.py` e `core/dnd_rules.py` (Referência: Draconato Mago Lvl 1)

## 1. Geração de Atributos Base
Após inspecionar as entranhas do módulo de orquestração (`core/game_engine.py`), identifiquei que o motor está utilizando o método **Aleatório (Roll for Stats)**, especificamente a variante RAW "4d6, descarta o menor".

**Trecho do Código Responsável (`CharacterBuilder`):**
```python
@staticmethod
def roll_stats_4d6_drop_lowest() -> int:
    rolls = [DiceEngine.roll_d6() for _ in range(4)]
    rolls.remove(min(rolls))
    return sum(rolls)
```
Este método é acionado 6 vezes na inicialização do painel de ficha em `CharacterCreationPanel` (`ui/menu_components.py`). Portanto, os atributos são genuinamente aleatórios a cada nova ficha.

## 2. Validação de Bônus Raciais
O processamento ocorre na função `CharacterCalculator.calculate_derived_stats` dentro de `core/dnd_rules.py`. O loop mapeia a estrutura de bônus raciais e os injeta nos atributos base rolados:

- **Draconato (Regra 5e):** Concede `+2 Força` e `+1 Carisma`.
- **Análise da Imagem (Resultado: FOR 12, DES 10, CON 15, INT 12, SAB 10, CAR 11):**
  - **Força (12):** O valor rolado pelo algoritmo `4d6 drop lowest` foi **10**, que após o bônus racial de +2 atingiu 12.
  - **Carisma (11):** O valor rolado foi **10**, que com o bônus de +1 atingiu 11.
  - Todos os demais atributos (DES 10, CON 15, INT 12, SAB 10) mantiveram os valores exatos originados pela rolagem, pois a raça não fornece modificadores para eles.
  - **Veredito:** A matemática racial do backend está perfeitamente sincronizada com o *Player's Handbook* (RAW).

## 3. Verificação de Atributos Derivados
O cálculo final obedece as regras mecânicas de cruzamento de Classe, Equipamento e Modificadores:

- **Modificadores Utilizados:**
  - `CON 15` -> Modificador de `+2`
  - `DES 10` -> Modificador de `+0`

- **HP Máximo (Resultado 8):**
  O `pv_base` atrelado à classe "Mago" no dicionário `CLASSES` é **6** (Dado de Vida d6). A regra define: `HP Base + Modificador de Constituição`. A fórmula implementada no backend (`hp_base + con_mod`) processa `6 + 2 = 8`. **Cálculo exato.**

- **Classe de Armadura / CA (Resultado 10):**
  O equipamento inicial listado para a classe "Mago" contém apenas `["Roupas Comuns", "Bordão", "Grimório", "Pacote de Estudioso"]`. Não há escudo e "Roupas Comuns" não concede CA base especial. A lógica recai para o padrão desarmado: `10 + Modificador de Destreza`. Sendo a DES 10 (+0), temos `10 + 0 = 10`. **Cálculo exato.**

- **Iniciativa (Resultado 0):**
  A iniciativa baseia-se exclusivamente no Modificador de Destreza. Sem talentos aplicáveis para a raça/classe neste nível, ela é fixada em `+0`. **Cálculo exato.**

## Conclusão da Auditoria
Não há nenhuma discrepância matemática ou de arquitetura lógica no modelo atual da Criação de Personagem. O backend aplica rigorosamente o modelo "4d6 Drop Lowest" com processamento *Fail-Proof* dos dicionários raciais e das classes do D&D 5e SRD. O *Model* (M) está blindado e não requer intervenções técnicas neste momento.
