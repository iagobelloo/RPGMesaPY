# Relatório 067 — Auditoria Geral, Limpeza de Código Obsoleto e Conexão Total (End-to-End)

**Data:** 12/10/2026  
**Responsáveis:** Orquestrador Principal, `dev-frontend-ui`, `dev-backend-dnd`  
**Status:** ✅ Concluído e Validado (103 Testes Automatizados — 100% OK)

---

## 1. Diagnóstico e Correção do Crash na Inicialização do `main.py`

### 1.1. Causa Raiz (`UnboundLocalError`)
Ao executar `python main.py`, o interpretador Python lançava imediatamente:
```text
UnboundLocalError: cannot access local variable 'SessionManager' where it is not associated with a value
```
- **Por que ocorria:** Na linha 41 de [`main.py`](file:///c:/Users/iagob/RPGMesaPY/main.py), `def main()` instanciava `session = SessionManager(ai_master)` usando a importação global da linha 10. Porém, na linha 161 (dentro do bloco `elif cmd == "delete_slot":` da mesma função `main()`), havia um `from core.game_engine import SessionManager` local. Em Python, qualquer declaração `import` dentro do corpo de uma função torna aquele identificador uma variável local em todo o escopo da função, sombreando o import global e gerando `UnboundLocalError` antes da linha 161 ser alcançada.
- **Correção Aplicada:** Todos os imports locais redundantes dentro de `def main()` (`SessionManager`, `AssetManager`, `BESTIARIO_5E`, `BackpackModal`, `ChatBox`, `LoadingDiceAnimation`, `QuickActionBar`, `SceneRenderer`, `BeatTransitionScene`, `queue`, `re`) foram removidos do interior do loop e consolidados de forma limpa no cabeçalho de [`main.py`](file:///c:/Users/iagob/RPGMesaPY/main.py#L1-L36). Validado via análise de AST em `tests/test_main_startup_and_integration.py`.

---

## 2. Remoção de Arquivos e Códigos Obsoletos

1. **Diretórios e Arquivos Temporários Removidos do Repositório:**
   - `scratch_enemy_classification.json` (arquivo temporário na raiz).
   - `scratch/` (`create_all_playable_pcs.py`, `patch_bestiary.py`, `test_api_key.py`).
   - `database/` (`connection.py`, `rpg_mesa.db` — módulo SQLite legado substituído pelo sistema de 3 slots JSON em `saves/slot_1..3.json`).
   - **58 scripts temporários** `scripts/fix_*.py` e `scripts/patch_*.py` (mantidos apenas os 5 utilitários canônicos: `load_jsons.py`, `refactor_backgrounds.py`, `refactor_bestiary.py`, `srd_importer.py`, `standardize_assets.py`).
2. **Remoção de Código Morto em [`main.py`](file:///c:/Users/iagob/RPGMesaPY/main.py):**
   - Removida a instanciação órfã de `SessionZeroPanel` (`session_zero_panel`, `sz_question_index`, `sz_history`, `sz_questions`), já que a criação de personagem flui diretamente para o Prólogo (`BEAT_TRANSITION` $\to$ `IN_GAME`).

---

## 3. Declaração Completa dos 42 Protagonistas e 24 Skills no `AssetManager` e `dnd_rules`

1. **Correção do Slug `"ladino"` em [`ui/asset_manager.py`](file:///c:/Users/iagob/RPGMesaPY/ui/asset_manager.py):**
   - Anteriormente, `CLASS_SLUGS["ladino"]` apontava para `"rogue"`, impedindo que `resolve_hero_candidates("Humano", "Ladino", "male")` buscasse `humano_ladino_male.png`.
   - Agora `"ladino"` mapeia para `"ladino"`, com alias bidirecional `["ladino", "rogue"]` em `CLASS_FILE_ALIASES`.
2. **Manifesto Explícito dos 42 Protagonistas (`PROTAGONIST_SPRITE_MANIFEST`):**
   - Declarado em [`ui/asset_manager.py`](file:///c:/Users/iagob/RPGMesaPY/ui/asset_manager.py#L70-L129) e [`core/dnd_rules.py`](file:///c:/Users/iagob/RPGMesaPY/core/dnd_rules.py#L264-L305) para todos os 42 pares `(raça, classe)` (`PROT-01` a `PROT-42`):
     - Sprite de Corpo Inteiro: `assets/sprites/heroes/{raca_slug}_{classe_slug}_{genero}.png` (ex.: `humano_clerigo_female.png`, `humano_ladino_male.png`).
     - Retrato 1:1: `assets/sprites/heroes/icones/{raca_slug}_{classe_slug}_{genero}.png`.
   - **Fallback Inteligente Sem Quadrado Ciano (`ALLY_HERO_FALLBACK_BY_RACE_CLASS`):** Enquanto o usuário gera manualmente os 42 arquivos `.png` dos protagonistas e os adiciona à pasta `assets/sprites/heroes/`, o `AssetManager` verifica primeiro o arquivo `{raca}_{classe}_{genero}.png`; caso ainda não esteja em disco, carrega automaticamente o sprite/retrato do herói aliado correspondente da mesma raça e classe que já existe em `assets/sprites/heroes/` (e assim que o arquivo `{raca}_{classe}_{genero}.png` for colocado na pasta, ele passa a ter prioridade automática!).
3. **Manifesto dos 24 Ícones da Árvore de Habilidades (`SKILL_ICON_MANIFEST`):**
   - Declarado em [`ui/asset_manager.py`](file:///c:/Users/iagob/RPGMesaPY/ui/asset_manager.py#L180-L236) com o método `AssetManager.get_skill_icon(skill_id_or_dict, size=(36, 36))`, carregando os ícones em `assets/ui/skills/*.png` (ou renderizando a moldura + glifo procedural no `GrimoireModal` enquanto o `.png` não estiver em disco).

---

## 4. Conexão de Pontas Soltas (Frontend $\leftrightarrow$ Backend)

1. **Equipamento via Mochila (`BackpackModal` $\to$ `SessionManager.equip_item`):**
   - Em [`main.py`](file:///c:/Users/iagob/RPGMesaPY/main.py#L209-L221), clicar em "Empunhar/Equipar" na mochila agora invoca `session.equip_item(item_name)`, equipando armas, armaduras ou escudos, recalculando a CA (AC) em tempo real e registrando a confirmação no log.
2. **Diário no Menu de Pausa (`PauseMenuPanel` $\to$ `GrimoireModal`):**
   - Clicar em "Diário de Aventuras" no menu de pausa agora abre diretamente o `GrimoireModal` na aba `"diario"` com todas as missões principais, secundárias e aliados recrutados.
3. **Jornada Solo nos Beats 1 a 14 vs Grupo Completo no Clímax (Beat 15):**
   - Em [`ui/scene_renderer.py`](file:///c:/Users/iagob/RPGMesaPY/ui/scene_renderer.py#L228-L255), aliados recrutados nas side quests não aparecem mais ao lado do jogador nos Beats 1 a 14; eles aguardam no Grimório e entram no tabuleiro apenas no Clímax (Beat 15 — `session.story.is_climax()`) ou quando em `combat_allies`, usando seus próprios sprites (`sprite_key`).
4. **Sincronização Bilíngue de Atributos (`PT` $\leftrightarrow$ `EN`) e IDs de Habilidades (`sk_*` $\leftrightarrow$ Canônicos):**
   - `GrimoireModal._apply_level_up_choices` e `SessionManager.apply_level_up` sincronizam automaticamente `STR/FOR`, `DEX/DES`, `CON/CON`, `INT/INT`, `WIS/SAB`, `CHA/CAR` e desbloqueiam simultaneamente os IDs de UI (`sk_warrior_1`) e canônicos (`second_wind`).
5. **Correção de `teste_pericia`, `actions` dos 42 Aliados e Habilidades Ativas (`USAR_HABILIDADE`) em [`core/combat_system.py`](file:///c:/Users/iagob/RPGMesaPY/core/combat_system.py):**
   - Corrigido o `NameError: name 'prof' is not defined` nos testes de perícia em combate.
   - Conectadas as `actions` reais D&D 5e (`name`, `hit_bonus`, `damage_dice`) dos 42 aliados de `data/heroes_lore.json` no turno dos aliados (eliminando o fallback genérico `"Pancada" 1d4`).
   - Implementada a resolução mecânica de habilidades ativas (`second_wind`, `action_surge`, `lay_on_hands`, `channel_divinity_preserve_life`, `spiritual_weapon`, `destroy_undead`, `arcane_recovery`, `cunning_action`, `uncanny_dodge`) tanto em combate quanto em exploração.

---

## 5. Validação e Testes Automatizados

- [`tests/test_main_startup_and_integration.py`](file:///c:/Users/iagob/RPGMesaPY/tests/test_main_startup_and_integration.py): 6 novos testes cobrindo inicialização do `main.py`, manifesto dos 42 protagonistas, jornada solo vs Beat 15, Level Up no Grimório e equipamento na Mochila.
- [`tests/test_backend_integration_audit.py`](file:///c:/Users/iagob/RPGMesaPY/tests/test_backend_integration_audit.py): 6 novos testes cobrindo `teste_pericia`, ações reais dos 42 aliados, habilidades ativas/passivas e metadados dos 42 protagonistas.
- **Total da Suíte Global:** **103 testes executados — 100% OK (0 erros, 0 falhas)**.

