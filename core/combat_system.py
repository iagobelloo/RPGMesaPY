"""Módulo de Sistema de Combate e Economia de Ação."""

class TurnManager:
    """Gerencia a economia de ação de um personagem durante seu turno."""
    
    def __init__(self, base_movement: int = 30):
        self.base_movement = base_movement
        self.has_action: bool = True
        self.has_bonus_action: bool = True
        self.has_reaction: bool = True
        self.movement_left: int = base_movement

    def reset_turn(self):
        """Reseta todos os recursos no início de um novo turno."""
        self.has_action = True
        self.has_bonus_action = True
        self.has_reaction = True
        self.movement_left = self.base_movement

    def use_action(self) -> bool:
        """Tenta consumir a ação principal. Retorna False se não tiver."""
        if self.has_action:
            self.has_action = False
            return True
        return False

    def use_bonus_action(self) -> bool:
        """Tenta consumir a ação bônus. Retorna False se não tiver."""
        if self.has_bonus_action:
            self.has_bonus_action = False
            return True
        return False

    def use_reaction(self) -> bool:
        """Tenta consumir a reação. Retorna False se não tiver."""
        if self.has_reaction:
            self.has_reaction = False
            return True
        return False

    def move(self, feet: int) -> bool:
        """Consome movimento. Retorna False se não houver o suficiente."""
        if self.movement_left >= feet:
            self.movement_left -= feet
            return True
        return False


class DeathSaveTracker:
    """Gerencia os Testes de Resistência contra a Morte (Death Saves) quando o HP chega a 0."""
    
    def __init__(self):
        self.successes: int = 0
        self.failures: int = 0

    def roll_death_save(self, d20_result: int) -> str:
        """
        Processa o resultado de um D20 para o Death Save.
        Retorna uma string descritiva do estado atual.
        """
        if d20_result == 1:
            self.failures += 2
            return "Falha Crítica! 2 falhas marcadas."
        elif d20_result == 20:
            self.successes = 0
            self.failures = 0
            return "Sucesso Crítico! Você acorda com 1 HP."
        elif d20_result >= 10:
            self.successes += 1
            return "Sucesso no Teste de Morte."
        else:
            self.failures += 1
            return "Falha no Teste de Morte."

    def is_dead(self) -> bool:
        """Retorna True se o personagem acumulou 3 ou mais falhas."""
        return self.failures >= 3

    def is_stable(self) -> bool:
        """Retorna True se o personagem acumulou 3 ou mais sucessos."""
        return self.successes >= 3

    def reset(self):
        """Zera os contadores (usado quando curado)."""
        self.successes = 0
        self.failures = 0


class ConditionManager:
    """Gerencia Status Effects permanentemente até que sejam curados/removidos."""
    def __init__(self):
        self.active_conditions: set[str] = set()

    def apply_condition(self, condition_name: str):
        """Aplica uma nova condição de forma binária."""
        self.active_conditions.add(condition_name.lower().strip())

    def remove_condition(self, condition_name: str):
        """Remove a condição diretamente."""
        self.active_conditions.discard(condition_name.lower().strip())

    def evaluate_conditions(self) -> dict:
        """
        Retorna os modificadores sistêmicos baseados nas condições ativas para o Motor de Regras aplicar.
        """
        modifiers = {
            "disadvantage_on_attacks": False,
            "attacks_against_have_advantage": False,
            "movement_speed_multiplier": 1.0,
            "cant_take_actions": False
        }
        
        if "poisoned" in self.active_conditions:
            modifiers["disadvantage_on_attacks"] = True
            
        if "prone" in self.active_conditions:
            modifiers["disadvantage_on_attacks"] = True
            modifiers["attacks_against_have_advantage"] = True 
            modifiers["movement_speed_multiplier"] = 0.5
            
        if "unconscious" in self.active_conditions or "paralyzed" in self.active_conditions:
            modifiers["cant_take_actions"] = True
            modifiers["attacks_against_have_advantage"] = True
            modifiers["movement_speed_multiplier"] = 0.0

        return modifiers


import random
import re
from core.dice_engine import DiceEngine
from core.dnd_rules import MATRIZ_DE_PERICIAS, get_modifier, expand_unlocked_skills, normalize_skill_id


def _get_player_attr_value(player_sheet: dict, attr_pt: str, default: int = 10) -> int:
    """Obtém valor de atributo da ficha aceitando tanto chaves PT (FOR..CAR) quanto EN (STR..CHA)."""
    if not player_sheet or not isinstance(player_sheet, dict):
        return default
    attrs = player_sheet.get("attributes") or player_sheet.get("atributos") or {}
    if not isinstance(attrs, dict):
        return default
    pt_to_en = {"FOR": "STR", "DES": "DEX", "CON": "CON", "INT": "INT", "SAB": "WIS", "CAR": "CHA"}
    en_to_pt = {v: k for k, v in pt_to_en.items()}
    key_up = str(attr_pt).upper().strip()
    pt_key = en_to_pt.get(key_up, key_up)
    en_key = pt_to_en.get(pt_key, key_up)
    if pt_key in attrs and en_key in attrs:
        if attrs[pt_key] != attrs[en_key]:
            return attrs[pt_key] if attrs[en_key] == 10 else (attrs[en_key] if attrs[pt_key] == 10 else max(attrs[pt_key], attrs[en_key]))
        return attrs[pt_key]
    return attrs.get(pt_key, attrs.get(en_key, default))


def resolve_skill_effect(parsed_json: dict, player_sheet: dict, target_entities: list, active_combat_targets: dict, game_state: dict = None) -> str:
    """Resolve mecanicamente habilidades ativas de classe (tanto IDs sk_* quanto canônicos ou nomes PT)."""
    if not player_sheet or not isinstance(player_sheet, dict):
        player_sheet = {}
    raw_ref = (
        parsed_json.get("recurso_utilizado")
        or parsed_json.get("habilidade")
        or parsed_json.get("skill_id")
        or ""
    )
    if not raw_ref or str(raw_ref).lower() == "nenhum":
        intencao_txt = str(parsed_json.get("intencao_cena") or "").lower()
        for candidate in [
            "retomar o fôlego", "retomar o folego", "second_wind", "sk_warrior_1",
            "surto de ação", "surto de acao", "action_surge", "sk_warrior_2",
            "cura pelas mãos", "cura pelas maos", "lay_on_hands", "sk_paladin_1",
            "preservar a vida", "channel_divinity_preserve_life", "sk_cleric_2",
            "arma espiritual", "spiritual_weapon",
            "destruir mortos-vivos", "destroy_undead", "sk_cleric_3",
            "golpe divino", "divine_strike", "sk_cleric_4",
            "recuperação arcana", "recuperacao arcana", "arcane_recovery", "sk_mage_1",
            "ação ardilosa", "ação astuta", "cunning_action", "sk_rogue_2",
            "esquiva sobrenatural", "uncanny_dodge", "sk_rogue_3"
        ]:
            if candidate in intencao_txt:
                raw_ref = candidate
                break
        if (not raw_ref or str(raw_ref).lower() == "nenhum") and player_sheet.get("unlocked_skills"):
            raw_ref = player_sheet["unlocked_skills"][0]

    canonical_id = normalize_skill_id(raw_ref)
    raw_low = str(raw_ref).lower().strip()
    level = max(1, int(player_sheet.get("level", 1)))
    hp_max = max(1, int(player_sheet.get("hp_max", 10)))

    # 1. Habilidades de Cura (Retomar o Fôlego, Cura pelas Mãos, Preservar a Vida)
    if canonical_id == "second_wind" or "retomar" in raw_low:
        cura = DiceEngine.parse_and_roll_dice("1d10") + level
        player_sheet["hp_current"] = min(hp_max, player_sheet.get("hp_current", hp_max) + cura)
        return f"🎲 [HABILIDADE - CURA] Retomar o Fôlego: recuperou +{cura} PV (1d10 + Nv {level}) ➔ PV: {player_sheet['hp_current']}/{hp_max}!\n"

    elif canonical_id == "lay_on_hands" or "cura pelas m" in raw_low:
        cura = level * 5
        player_sheet["hp_current"] = min(hp_max, player_sheet.get("hp_current", hp_max) + cura)
        return f"🎲 [HABILIDADE - CURA] Cura pelas Mãos: restaurou +{cura} PV (5x Nv {level}) ➔ PV: {player_sheet['hp_current']}/{hp_max}!\n"

    elif canonical_id == "channel_divinity_preserve_life" or "preservar a vida" in raw_low or "canalizar divindade" in raw_low:
        cura = level * 5
        player_sheet["hp_current"] = min(hp_max, player_sheet.get("hp_current", hp_max) + cura)
        for t_data in (active_combat_targets or {}).values():
            if t_data.get("faction") == "ally" and t_data.get("status") != "morto" and t_data.get("pv_atual", 0) > 0:
                t_max = t_data.get("pv_max", 10)
                t_data["pv_atual"] = min(t_max, t_data.get("pv_atual", t_max) + cura)
        return f"🎲 [HABILIDADE - CURA] Canalizar Divindade (Preservar a Vida): restaurou +{cura} PV (5x Nv {level}) ➔ PV: {player_sheet['hp_current']}/{hp_max}!\n"

    # 2. Recuperação Arcana (Restaura 1 slot de magia Nv 1)
    elif canonical_id == "arcane_recovery" or "recupera" in raw_low:
        slots = player_sheet.setdefault("spell_slots", {"1": 2})
        slots["1"] = int(slots.get("1", 0)) + 1
        return f"✨ [HABILIDADE - ARCANO] Recuperação Arcana: +1 Espaço de Magia de Nível 1 restaurado (Total Nv 1: {slots['1']})!\n"

    # 3. Habilidades Ofensivas (Surto de Ação, Arma Espiritual, Destruir Mortos-Vivos, Golpe Divino)
    elif canonical_id in ["action_surge", "spiritual_weapon", "destroy_undead", "divine_strike"] or any(
        k in raw_low for k in ["surto", "arma espiritual", "destruir mortos", "golpe divino"]
    ):
        enemies = [t for t in (target_entities or []) if isinstance(t, dict) and t.get("status") != "morto" and t.get("pv_atual", 0) > 0]
        if not enemies and active_combat_targets:
            enemies = [
                t for t in active_combat_targets.values()
                if isinstance(t, dict) and t.get("faction", "enemy") == "enemy" and t.get("status") != "morto" and t.get("pv_atual", 0) > 0
            ]

        if canonical_id == "action_surge" or "surto" in raw_low:
            mod_for = get_modifier(_get_player_attr_value(player_sheet, "FOR", 10))
            dano = max(1, DiceEngine.parse_and_roll_dice("1d8") + max(0, mod_for))
            hab_nome = "Surto de Ação"
        elif canonical_id == "spiritual_weapon" or "arma espiritual" in raw_low:
            mod_sab = get_modifier(_get_player_attr_value(player_sheet, "SAB", 10))
            dano = max(1, DiceEngine.parse_and_roll_dice("1d8") + max(0, mod_sab))
            hab_nome = "Arma Espiritual"
        elif canonical_id == "divine_strike" or "golpe divino" in raw_low:
            dano = DiceEngine.parse_and_roll_dice("2d8")
            hab_nome = "Golpe Divino"
        else:
            dano = DiceEngine.parse_and_roll_dice("4d6")
            hab_nome = "Destruir Mortos-Vivos"

        if enemies:
            alvo = enemies[0]
            if alvo.get("tipo_bestiario") == "m_supreme_dragon" and alvo.get("charge_turn", 0) > 0 and not (game_state and game_state.get("meta", {}).get("segredo_tirano", False)):
                dano = max(0, int(dano * 0.01))
            alvo["pv_atual"] = max(0, alvo.get("pv_atual", 10) - dano)
            if alvo["pv_atual"] <= 0:
                alvo["status"] = "morto"
            alvo_nome = alvo.get("name", "Inimigo")
            pv_max_a = alvo.get("pv_max", 10)
            return f"⚔️ [HABILIDADE - {hab_nome}] Desferiu {dano} de dano em {alvo_nome} (PV: {alvo['pv_atual']}/{pv_max_a})!\n"
        return f"⚔️ [HABILIDADE - {hab_nome}] Energia combativa canalizada (+{dano} de poder ofensivo)!\n"

    # 4. Habilidades Táticas / Defensivas (Ação Ardilosa / Astuta, Esquiva Sobrenatural)
    elif canonical_id in ["cunning_action", "uncanny_dodge"] or any(
        k in raw_low for k in ["ardilosa", "astuta", "esquiva sobrenatural"]
    ):
        hab_nome = "Esquiva Sobrenatural" if (canonical_id == "uncanny_dodge" or "esquiva" in raw_low) else "Ação Ardilosa"
        cur_ac = int(player_sheet.get("ac", player_sheet.get("ca", 14)))
        if not player_sheet.get("_tactical_ac_applied"):
            player_sheet["ac"] = cur_ac + 2
            player_sheet["ca"] = player_sheet["ac"]
            player_sheet["_tactical_ac_applied"] = True
        return f"🛡️ [HABILIDADE - {hab_nome}] Postura evasiva ativada (+2 CA tática, CA Atual: {player_sheet.get('ac', cur_ac)})!\n"

    return f"⚡ [HABILIDADE] Técnica '{raw_ref or canonical_id}' ativada com sucesso!\n"


def resolve_action(parsed_json: dict, player_sheet: dict, target_entities: list = None, active_combat_targets: dict = None, game_state: dict = None) -> dict:
    if player_sheet is None or not isinstance(player_sheet, dict):
        player_sheet = {}
    if active_combat_targets is None or not isinstance(active_combat_targets, dict):
        active_combat_targets = {}
    if target_entities is None or not isinstance(target_entities, list):
        target_entities = []
    if parsed_json is None or not isinstance(parsed_json, dict):
        parsed_json = {}
        
    raw_tipo = str(parsed_json.get("tipo_acao") or "").strip()
    if raw_tipo.upper() in ["USAR_HABILIDADE", "ACAO_TATICA_5E", "HABILIDADE"]:
        tipo_acao = "habilidade"
    elif raw_tipo.upper() == "TESTE_PERICIA":
        tipo_acao = "teste_pericia"
    elif raw_tipo.upper() in ["USO_ITEM", "USAR_ITEM"]:
        tipo_acao = "uso_item"
    elif raw_tipo.upper() in ["ATAQUE", "ATACAR", "ATAQUE_FISICO"]:
        tipo_acao = "ataque"
    elif raw_tipo.upper() in ["MAGIA", "CONJURAR_MAGIA"]:
        tipo_acao = "magia"
    else:
        tipo_acao = raw_tipo

    estado_tatico = parsed_json.get("estado_tatico", "normal")
    flavor = parsed_json.get("flavor_text", "")
    
    from core.dice_engine import DiceEngine
    from core.dnd_rules import MATRIZ_DE_PERICIAS, get_modifier, BESTIARIO_5E, ARMAS_5E
    import random
    
    sys_log = ""
    
    # 1. Definir Participantes e Iniciativas
    participants = []
    
    # Player init (suporta chaves PT e EN)
    mod_des_player = get_modifier(_get_player_attr_value(player_sheet, "DES", 10))
    init_player = DiceEngine.roll_d20() + mod_des_player
    participants.append({"type": "player", "init": init_player})
    
    # Monsters and Allies init
    reacoes = parsed_json.get("reacao_inimigos", [])
    reacoes_map = {r.get("id_narrativo", "").lower(): r for r in reacoes}
    
    for t_id, t_data in active_combat_targets.items():
        if t_data.get("status") == "morto": continue
        
        faction = t_data.get("faction", "enemy")
        tipo_best = t_data.get("tipo_bestiario", "lacaio goblin").lower().strip()
        
        best_data = {}
        for bk, bv in BESTIARIO_5E.items():
            if bk.lower().strip() == tipo_best:
                best_data = bv
                break
                
        mod_des = best_data.get("mods", {}).get("DES", 0)
        if not mod_des and isinstance(t_data.get("attributes"), dict):
            mod_des = get_modifier(_get_player_attr_value(t_data, "DES", 10))
        init_roll = DiceEngine.roll_d20() + mod_des
        
        if faction == "enemy":
            reacao = None
            for k, r in reacoes_map.items():
                if k in t_id.lower() or t_id.lower() in k:
                    reacao = r
                    break
            if not reacao: reacao = {"tipo_acao": "ataque"}
            participants.append({"type": "monster", "init": init_roll, "id": t_id, "data": t_data, "reacao": reacao, "best_data": best_data})
        elif faction == "ally":
            participants.append({"type": "ally", "init": init_roll, "id": t_id, "data": t_data, "best_data": best_data})
            
    participants.sort(key=lambda x: x["init"], reverse=True)
    
    for p in participants:
        # Pula se jogador morreu
        if player_sheet.get("hp_current", 10) <= 0 or player_sheet.get("status") == "morto":
            break
            
        if p["type"] == "player":
            dado = DiceEngine.roll_with_advantage() if estado_tatico == "vantagem" else DiceEngine.roll_with_disadvantage() if estado_tatico == "desvantagem" else DiceEngine.roll_d20()
            
            if tipo_acao == "teste_pericia":
                prof = player_sheet.get("proficiency_bonus", 2)
                pericia = parsed_json.get("pericia_sugerida") or parsed_json.get("recurso_utilizado") or "nenhum"
                cd = parsed_json.get("cd_sugerida", 10)
                attr_key = MATRIZ_DE_PERICIAS.get(pericia, "nenhum")
                if attr_key == "nenhum" and pericia:
                    for mk, mv in MATRIZ_DE_PERICIAS.items():
                        if mk.lower() == str(pericia).lower().strip():
                            attr_key = mv
                            break
                mod = 0
                if attr_key != "nenhum" and ("attributes" in player_sheet or "atributos" in player_sheet):
                    val_attr = _get_player_attr_value(player_sheet, attr_key, 10)
                    mod = get_modifier(val_attr)
                tot = dado + mod + prof
                resultado_str = "SUCESSO" if tot >= cd else "FALHA"
                sys_log += f"🎲 [DADO - TESTE] {str(pericia).title()}: d20 ({dado}) + Mod (+{mod}) + Prof (+{prof}) [+{mod+prof}] = {tot} vs CD {cd} ➔ {resultado_str}!\n"
                
            elif tipo_acao == "uso_item":
                sys_log += f"{parsed_json.get('log_precalculado', f'[SISTEMA] Iniciativa {init_player} | Item utilizado.')}\n"

            elif tipo_acao == "habilidade":
                sys_log += resolve_skill_effect(parsed_json, player_sheet, target_entities, active_combat_targets, game_state)
                
            elif tipo_acao in ["ataque", "magia"] and target_entities:
                recurso = parsed_json.get("recurso_utilizado", "")
                unlocked_skills = expand_unlocked_skills(player_sheet.get("unlocked_skills", []))
                raw_unlocked = {str(s).lower().strip() for s in player_sheet.get("unlocked_skills", [])}
                
                # Handling for AoE spells to avoid multiple hits for multiple target_entities
                is_aoe = False
                if tipo_acao == "magia":
                    spell_data = parsed_json.get("spell_data", {})
                    if spell_data and spell_data.get("target_type") == "aoe":
                        is_aoe = True
                        magia = spell_data.get("name", "Magia")
                        m_action = spell_data.get("mechanical_action", "damage")
                        if m_action == "damage":
                            save_stat = spell_data.get("saving_throw", "DES")
                            damage_dice = spell_data.get("damage_dice", "1d4")
                            
                            dano_base = DiceEngine.parse_and_roll_dice(damage_dice)
                            if "potent_cantrip" in unlocked_skills or "potent_spellcasting" in unlocked_skills:
                                dano_base += 2
                            if "empowered_evocation" in unlocked_skills or "arcane_overload" in unlocked_skills:
                                dano_base += DiceEngine.parse_and_roll_dice("1d6")
                            spell_dc = player_sheet.get("spell_save_dc", 14) + (1 if "sculpt_spells" in unlocked_skills else 0)
                            sys_log += f"🎲 [DADO - MAGIA] {magia.title()} (Área de Efeito)! Dano base rolado: {dano_base} (CD {spell_dc} {save_stat}).\n"
                            
                            for t_id, t_data in active_combat_targets.items():
                                if t_data.get("faction", "enemy") == "enemy" and t_data.get("pv_atual", 0) > 0:
                                    tipo_best = t_data.get("tipo_bestiario", "goblin").lower().strip()
                                    best_data = BESTIARIO_5E.get(tipo_best, {})
                                    if not best_data:
                                        for bk, bv in BESTIARIO_5E.items():
                                            if bk.lower().strip() == tipo_best:
                                                best_data = bv
                                                break
                                    mod_save = best_data.get("mods", {}).get(save_stat, 0)
                                    save_roll = DiceEngine.roll_d20() + mod_save
                                    
                                    if save_roll >= spell_dc:
                                        dano_final = dano_base // 2
                                        res = "Passou"
                                    else:
                                        dano_final = dano_base
                                        res = "Falhou"
                                        
                                    if t_data.get("tipo_bestiario") == "m_supreme_dragon" and t_data.get("charge_turn", 0) > 0 and not (game_state and game_state.get('meta', {}).get('segredo_tirano', False)):
                                        dano_final = max(0, int(dano_final * 0.01))
                                        sys_log += f"\n[SISTEMA] O ataque reflete nas escamas de obsidiana! Causou apenas {dano_final} de dano."
                                    t_data["pv_atual"] = max(0, t_data.get("pv_atual", 10) - dano_final)
                                    if t_data["pv_atual"] == 0: t_data["status"] = "morto"
                                    pv_max = t_data.get("pv_max", 10)
                                    res_tr = "SUCESSO" if res == "Passou" else "FALHA"
                                    sys_log += f"  🎲 [DADO - TR {save_stat}] {t_data.get('name', t_id).title()}: d20 ({save_roll-mod_save}) + Mod (+{mod_save}) = {save_roll} vs CD {spell_dc} ➔ {res_tr}! Dano: {dano_final} (PV: {t_data.get('pv_atual')}/{pv_max}).\n"
                
                if not is_aoe:
                    for t_entity in target_entities:
                        if t_entity.get("status") == "morto": continue
                        alvo_nome = t_entity.get("name", "Desconhecido")
                        
                        if tipo_acao == "ataque":
                            arma_nome = str(parsed_json.get("arma_usada") or parsed_json.get("recurso_utilizado") or "").lower().strip()
                            if not arma_nome or arma_nome == "nenhum":
                                eq_w = player_sheet.get("equipped_weapon") or (player_sheet.get("equipment", {}).get("weapon") if isinstance(player_sheet.get("equipment"), dict) else "")
                                arma_nome = str(eq_w).lower().strip() if eq_w else "ataque desarmado"
                            
                            mod_for = get_modifier(_get_player_attr_value(player_sheet, "FOR", 10))
                            mod_des_p = get_modifier(_get_player_attr_value(player_sheet, "DES", 10))
                            prof_bonus = player_sheet.get("proficiency_bonus", 2)
                            
                            crit_threshold = 20
                            weapon_bonus_hit = 0
                            weapon_bonus_dmg = 0
                            is_ranged_weapon = False

                            if arma_nome in ARMAS_5E:
                                w_info = ARMAS_5E[arma_nome]
                                dano_dado = w_info["dano"]
                                props = w_info.get("propriedades", [])
                                is_ranged_weapon = "distancia" in props or "arco" in arma_nome or "besta" in arma_nome
                                mod = max(mod_for, mod_des_p) if "acuidade" in props else (mod_des_p if w_info.get("atributo") == "DES" else mod_for)
                                weapon_bonus_hit = w_info.get("bonus_hit", 0)
                                weapon_bonus_dmg = w_info.get("bonus_damage", 0)
                                if w_info.get("crit_threshold"):
                                    crit_threshold = min(crit_threshold, w_info["crit_threshold"])
                            else:
                                dano_dado = "1d1"
                                mod = mod_for
                                arma_nome = "ataque desarmado"

                            # Passivas da Árvore de Habilidades (Unificadas sk_* e canônicas)
                            skill_bonus_hit = 0
                            skill_bonus_dmg = 0
                            extra_dice_list = []
                            passive_tags = []

                            if "champion_focus" in unlocked_skills or "assassinate" in unlocked_skills:
                                crit_threshold = min(crit_threshold, 19)
                            if "archery_style" in unlocked_skills and is_ranged_weapon:
                                skill_bonus_hit += 2
                            if "sacred_oath_devotion" in unlocked_skills or "aura_of_protection" in unlocked_skills:
                                skill_bonus_hit += 2
                                skill_bonus_dmg += 2
                            if "favored_enemy" in unlocked_skills:
                                skill_bonus_dmg += 2
                            if "divine_smite" in unlocked_skills or "divine_smite_passive" in unlocked_skills:
                                extra_dice_list.append("2d8")
                                passive_tags.append("Destruição Divina")
                            if "improved_divine_smite" in raw_unlocked or "sk_paladin_4" in raw_unlocked:
                                extra_dice_list.append("1d8")
                            if "divine_strike" in unlocked_skills:
                                extra_dice_list.append("1d8")
                                passive_tags.append("Golpe Divino")
                            if "sneak_attack" in unlocked_skills:
                                extra_dice_list.append("1d6")
                                passive_tags.append("Ataque Furtivo")
                            if "colossus_slayer" in unlocked_skills:
                                extra_dice_list.append("1d8")
                                passive_tags.append("Assassino de Colossos")
                            if "hunters_mark_passive" in raw_unlocked or "sk_ranger_2" in raw_unlocked:
                                extra_dice_list.append("1d6")
                                passive_tags.append("Marca do Caçador")
                            if any(ea in unlocked_skills for ea in ["extra_attack_fighter", "extra_attack_paladin", "extra_attack_ranger", "multiattack_volley"]):
                                extra_dice_list.append("1d8")
                                passive_tags.append("Ataque Extra")

                            total_hit_mod = mod + prof_bonus + weapon_bonus_hit + skill_bonus_hit
                            tot_atk = dado + total_hit_mod
                            ca_alvo = t_entity.get("ca", 10)
                            res = "Acerto Crítico" if dado >= crit_threshold else "Falha Crítica" if dado == 1 else "Acerto" if tot_atk >= ca_alvo else "Erro"
                            
                            dano_total = 0
                            if res in ["Acerto", "Acerto Crítico"]:
                                if dano_dado == "1d1":
                                    dano_total = max(1, 1 + mod + skill_bonus_dmg) + (1 if res == "Acerto Crítico" else 0)
                                else:
                                    base_dice_str = dano_dado.split("+")[0].strip()
                                    try: n, t = map(int, base_dice_str.split('d'))
                                    except: n, t = 1, 4
                                    if res == "Acerto Crítico": n *= 2
                                    dano_total = max(0, sum(random.randint(1, t) for _ in range(n)) + mod + weapon_bonus_dmg + skill_bonus_dmg)
                                
                                for ed in extra_dice_list:
                                    dano_total += DiceEngine.parse_and_roll_dice(ed)

                                if t_entity.get("tipo_bestiario") == "m_supreme_dragon" and t_entity.get("charge_turn", 0) > 0 and not (game_state and game_state.get('meta', {}).get('segredo_tirano', False)):
                                    dano_total = max(0, int(dano_total * 0.01))
                                    sys_log += f"\n[SISTEMA] O ataque reflete nas escamas de obsidiana! Causou apenas {dano_total} de dano."
                                t_entity["pv_atual"] = max(0, t_entity.get("pv_atual", 10) - dano_total)
                                if t_entity["pv_atual"] == 0:
                                    t_entity["status"] = "morto"
                            pv_max = t_entity.get("pv_max", 10)
                            passives_str = f" [{', '.join(passive_tags)}]" if (passive_tags and dano_total > 0) else ""
                            sys_log += f"🎲 [DADO - ATAQUE] {arma_nome.title()}: d20 ({dado}) + Mod/Prof (+{total_hit_mod}) = {tot_atk} vs CA {ca_alvo} ➔ {res.upper()}!\n"
                            if dano_total > 0:
                                sys_log += f"🎲 [DADO - DANO]{passives_str} {dano_total} de dano em {alvo_nome.title()} (PV: {t_entity.get('pv_atual')}/{pv_max})!\n"
                        
                        elif tipo_acao == "magia":
                            spell_data = parsed_json.get("spell_data", {})
                            if spell_data:
                                magia = spell_data.get("name", "Magia")
                                m_action = spell_data.get("mechanical_action", "damage")
                                t_type = spell_data.get("target_type", "direct")
                                
                                if m_action == "damage":
                                    damage_dice = spell_data.get("damage_dice", "1d4")
                                    
                                    if t_type == "direct":
                                        dano_total = DiceEngine.parse_and_roll_dice(damage_dice)
                                        if "potent_cantrip" in unlocked_skills or "potent_spellcasting" in unlocked_skills:
                                            dano_total += 2
                                        if "empowered_evocation" in unlocked_skills or "arcane_overload" in unlocked_skills:
                                            dano_total += DiceEngine.parse_and_roll_dice("1d6")
                                        if t_entity.get("tipo_bestiario") == "m_supreme_dragon" and t_entity.get("charge_turn", 0) > 0 and not (game_state and game_state.get('meta', {}).get('segredo_tirano', False)):
                                            dano_total = max(0, int(dano_total * 0.01))
                                            sys_log += f"\n[SISTEMA] O ataque reflete nas escamas de obsidiana! Causou apenas {dano_total} de dano."
                                        t_entity["pv_atual"] = max(0, t_entity.get("pv_atual", 10) - dano_total)
                                        if t_entity["pv_atual"] == 0:
                                            t_entity["status"] = "morto"
                                        pv_max = t_entity.get("pv_max", 10)
                                        sys_log += f"🎲 [DADO - MAGIA] {magia.title()}: Dano direto {dano_total} em {alvo_nome.title()} (PV: {t_entity.get('pv_atual')}/{pv_max})!\n"
                                elif m_action == "heal":
                                    dice_val = spell_data.get("dice_value", spell_data.get("damage_dice", "1d8"))
                                    cura = DiceEngine.parse_and_roll_dice(dice_val)
                                    if "disciple_of_life" in unlocked_skills:
                                        cura += 3
                                    hp_max_p = player_sheet.get("hp_max", 10)
                                    player_sheet["hp_current"] = min(hp_max_p, player_sheet.get("hp_current", hp_max_p) + cura)
                                    sys_log += f"🎲 [DADO - MAGIA CURA] {magia.title()}: +{cura} PV restaurados (PV: {player_sheet['hp_current']}/{hp_max_p})!\n"
                                elif m_action == "revive":
                                    if game_state and game_state.setdefault("meta", {}).get("revive_used", False):
                                        sys_log += f"[SISTEMA] Magia {magia.title()} falhou! Ressurreição só pode ser usada UMA vez por batalha.\n"
                                    elif t_entity.get("status") != "morto" and t_entity.get("pv_atual", 1) > 0:
                                        sys_log += f"[SISTEMA] Magia {magia.title()} falhou. {alvo_nome.title()} já está vivo.\n"
                                    else:
                                        if game_state is not None:
                                            game_state.setdefault("meta", {})["revive_used"] = True
                                        hp_max = t_entity.get("pv_max", 10)
                                        t_entity["pv_atual"] = max(1, hp_max // 2)
                                        t_entity["status"] = "vivo"
                                        sys_log += f"[SISTEMA] Magia {magia.title()} brilhante! {alvo_nome.title()} foi REVIVIDO com {t_entity['pv_atual']} PV!\n"
                            else:
                                sys_log += f"[SISTEMA] Magia não especificada.\n"
            else:
                if tipo_acao not in ["ataque", "magia"]:
                    sys_log += f"[SISTEMA] Iniciativa {init_player} | Ação '{tipo_acao}' confirmada.\n"
        
        elif p["type"] == "monster":
            # BLOCO 30: Escopo de Teste. Contra-ataque de monstros desabilitado temporariamente.
            pass

        elif p["type"] == "ally":
            aliado = p["data"]
            # Aliado caído (flag fantasma ou PV zerado) não age
            if aliado.get("status") == "morto" or aliado.get("pv_atual", 1) <= 0:
                continue
            
            # Filtro de Targeting (Bloco 40): só inimigos vivos e não-fantasmas
            enemies = [t for t in active_combat_targets.values()
                       if t.get("faction", "enemy") == "enemy"
                       and t.get("status") != "morto"
                       and t.get("pv_atual", 0) > 0]
            if not enemies:
                continue
            # IA de foco: concentra o golpe no inimigo mais ferido
            alvo = min(enemies, key=lambda e: e.get("pv_atual", 0))
            
            best = p.get("best_data") or {}
            ataque_padrao = {"nome": "Pancada", "bonus_acerto": 2, "dano": "1d4"}
            if aliado.get("actions") and isinstance(aliado.get("actions"), list) and len(aliado["actions"]) > 0:
                act = random.choice(aliado["actions"])
                atk = {
                    "nome": act.get("name", act.get("nome", "Ataque")),
                    "bonus_acerto": act.get("hit_bonus", act.get("bonus_acerto", 4)),
                    "dano": act.get("damage_dice", act.get("dano", "1d8+2"))
                }
            else:
                ataques = best.get("ataques") or [ataque_padrao]
                atk = random.choice(ataques)
            atk_nome = atk.get("nome", ataque_padrao["nome"])
            atk_bonus = int(atk.get("bonus_acerto", ataque_padrao["bonus_acerto"]))
            atk_dano = str(atk.get("dano", ataque_padrao["dano"]))
            
            d20_ini = DiceEngine.roll_d20()
            tot_atk = d20_ini + atk_bonus
            ca_alvo = alvo.get("ca", 10)
            
            res = ("Acerto Crítico" if d20_ini == 20
                   else "Falha Crítica" if d20_ini == 1
                   else "Acerto" if tot_atk >= ca_alvo
                   else "Erro")
            
            dano_aliado = 0
            if res in ["Acerto", "Acerto Crítico"]:
                dice_matches = re.findall(r"(\d+)d(\d+)", atk_dano)
                if dice_matches:
                    total_rolled = 0
                    for q_str, f_str in dice_matches:
                        qtd = int(q_str) * (2 if res == "Acerto Crítico" else 1)
                        fac = int(f_str)
                        total_rolled += sum(random.randint(1, fac) for _ in range(qtd))
                    # Bônus fixo numérico no final (ex: +3 ou +4)
                    cleaned = re.sub(r"\d+d\d+", "", atk_dano)
                    bonus_matches = re.findall(r"[+-]\s*\d+", cleaned)
                    fixo = sum(int(b.replace(" ", "")) for b in bonus_matches)
                    dano_aliado = max(1, total_rolled + fixo)
                else:
                    dano_aliado = 1
                
                # Bloco 37: Armadura Absoluta do Tirano (99% de redução sem o Orbe)
                if alvo.get("tipo_bestiario") == "m_supreme_dragon" and alvo.get("charge_turn", 0) > 0 and not (game_state and game_state.get('meta', {}).get('segredo_tirano', False)):
                    dano_aliado = max(0, int(dano_aliado * 0.01))
                    sys_log += f"\n[SISTEMA] O ataque reflete nas escamas de obsidiana! Causou apenas {dano_aliado} de dano."
                
                alvo["pv_atual"] = max(0, alvo.get("pv_atual", 10) - dano_aliado)
                # Bloco 40: flag fantasma (o Lixeiro remove após a narrativa)
                if alvo["pv_atual"] <= 0:
                    alvo["status"] = "morto"
            
            pv_max_alvo = alvo.get("pv_max", 10)
            sys_log += (f"🎲 [DADO - ALIADO] {p['id']} usou {atk_nome} em {alvo.get('name', 'Desconhecido')}: "
                        f"d20 ({d20_ini}) + Mod (+{atk_bonus}) = {tot_atk} vs CA {ca_alvo} ➔ {res.upper()}!\n")
            if dano_aliado > 0:
                sys_log += f"🎲 [DADO - DANO] {dano_aliado} de dano em {alvo.get('name', 'Alvo')} (PV: {alvo.get('pv_atual')}/{pv_max_alvo})!\n"
            if alvo.get("status") == "morto":
                sys_log += f"[SISTEMA] 💀 {alvo.get('name', 'O alvo')} foi abatido por {p['id']}.\n"

    return {
        "sys_log": sys_log,
        "log_mecanico": sys_log,
        "status": "player_dead" if player_sheet.get("hp_current", 10) <= 0 or player_sheet.get("status") == "morto" else "alive"
    }


class ArmorClassCalculator:
    """Calcula a Classe de Armadura (AC) seguindo as regras restritas do D&D 5e."""
    
    @staticmethod
    def calculate_ac(base_ac: int, dex_modifier: int, equipped_armor_type: str, has_shield: bool) -> int:
        """
        Calcula a AC baseada no tipo de armadura, modificador de destreza e uso de escudo.
        Tipos suportados: 'none', 'light', 'medium', 'heavy'.
        """
        armor_type = equipped_armor_type.lower().strip()
        final_ac = 10
        
        if armor_type == "none" or not armor_type:
            final_ac = 10 + dex_modifier
        elif armor_type == "light":
            final_ac = base_ac + dex_modifier
        elif armor_type == "medium":
            # Destreza máxima permitida na AC para armadura média é +2
            effective_dex = min(2, dex_modifier)
            final_ac = base_ac + effective_dex
        elif armor_type == "heavy":
            # Armadura pesada ignora bônus de destreza na AC
            final_ac = base_ac
        else:
            # Fallback se o tipo de armadura for desconhecido
            final_ac = base_ac
            
        if has_shield:
            final_ac += 2
            
        return final_ac

def process_enemies_turn_batch(active_combat_targets: dict, player_character: dict, game_state: dict = None) -> str:
    """
    Bloco 31: O Turno dos Inimigos em Lote (Batch Processing & Predatory AI).
    Itera sobre os inimigos vivos, escolhe o alvo mais fraco, e retorna o log concatenado.
    """
    if player_character is None or not isinstance(player_character, dict):
        player_character = {}
    if active_combat_targets is None or not isinstance(active_combat_targets, dict):
        active_combat_targets = {}
    from core.dice_engine import DiceEngine
    from core.dnd_rules import BESTIARIO_5E
    import random
    import re
    
    batch_log = ""
    
    # Prepara lista de possíveis alvos vivos (Jogador + Aliados)
    valid_targets = []
    
    if player_character.get("hp_current", 10) > 0:
        valid_targets.append({
            "id": "Jogador",
            "is_player": True,
            "ref": player_character,
            "hp": player_character.get("hp_current", 10),
            "ca": player_character.get("ca", 10)
        })
        
    for t_id, t_data in active_combat_targets.items():
        if t_data.get("faction", "enemy") == "ally" and t_data.get("pv_atual", 0) > 0:
            valid_targets.append({
                "id": t_id,
                "is_player": False,
                "ref": t_data,
                "hp": t_data.get("pv_atual", 0),
                "ca": t_data.get("ca", 10)
            })
            
    if not valid_targets:
        return ""
        
    for t_id, t_data in active_combat_targets.items():
        if t_data.get("faction", "enemy") == "enemy" and t_data.get("pv_atual", 0) > 0:
            
            # Bloco 37: Charge-Up do Dragão Supremo
            if t_data.get("tipo_bestiario") == "m_supreme_dragon":
                charge_turn = t_data.get("charge_turn", 0)
                if charge_turn < 2:
                    t_data["charge_turn"] = charge_turn + 1
                    batch_log += f"\n[SISTEMA] O Tirano das Cinzas inala profundamente. O magma no seu peito brilha como um sol moribundo. Ele está a carregar um ataque devastador! (Turno {t_data['charge_turn']}/2)\n"
                    continue
                else:
                    t_data["charge_turn"] = 0
                    # Ataca!
                    loop_count = game_state.get('meta', {}).get('loop_count', 0) if game_state else 0
                    if loop_count == 0:
                        # 999 fixed damage to player and allies
                        player_character["hp_current"] = 0
                        player_character["status"] = "morto"
                        for tgt in valid_targets:
                            if tgt["is_player"]:
                                tgt["ref"]["hp_current"] = 0
                                tgt["ref"]["status"] = "morto"
                            else:
                                tgt["ref"]["pv_atual"] = 0
                                tgt["ref"]["status"] = "morto"
                        batch_log += f"\n[SISTEMA] O Tirano das Cinzas usa SOPRO DO FIM DO MUNDO! Dano Inevitável: 999. Toda a party foi incinerada.\n"
                        continue
                    else:
                        # Substitui as actions temporariamente para um sopro massivo
                        t_data["actions"] = [{"name": "Sopro de Cinzas", "hit_bonus": 15, "damage_dice": "8d8"}]

            # Anti-Overkill: reavalia quem está vivo
            vivos = [t for t in valid_targets if t["hp"] > 0 and t["ref"].get("status") != "morto"]
            if not vivos:
                break
                
            # Menor HP, empate vai pro player (is_player True fica primeiro na ordenação estável se negarmos)
            vivos.sort(key=lambda x: (x["hp"], not x["is_player"]))
            target = vivos[0]
            
            ataques = t_data.get("actions", [])
            if not ataques:
                ataques = [{"name": "Pancada", "hit_bonus": 2, "damage_dice": "1d4"}]
                
            atk = random.choice(ataques)
            
            d20 = DiceEngine.roll_d20()
            tot_atk = d20 + atk.get("hit_bonus", 2)
            ca_alvo = target["ca"]
            
            res = "Acerto Crítico" if d20 == 20 else "Falha Crítica" if d20 == 1 else "Acerto" if tot_atk >= ca_alvo else "Erro"
            
            dano_inimigo = 0
            if res in ["Acerto", "Acerto Crítico"]:
                dano_str = str(atk.get("damage_dice", "1d4"))
                m = re.search(r"(\d+)d(\d+)\+?(\d+)?", dano_str)
                if m:
                    qtd = int(m.group(1))
                    fac = int(m.group(2))
                    fixo = int(m.group(3)) if m.group(3) else 0
                    if res == "Acerto Crítico": qtd *= 2
                    dano_inimigo = max(1, sum(random.randint(1, fac) for _ in range(qtd)) + fixo)
                else:
                    dano_inimigo = 1
                    
                target["hp"] = max(0, target["hp"] - dano_inimigo)
                
                if target["is_player"]:
                    target["ref"]["hp_current"] = target["hp"]
                    if target["hp"] <= 0: target["ref"]["status"] = "morto"
                else:
                    target["ref"]["pv_atual"] = target["hp"]
                    if target["hp"] <= 0: target["ref"]["status"] = "morto" 
                    
            batch_log += f"🎲 [DADO - INIMIGO] {t_id.title()} ataca {target['id'].title()} com {atk.get('name', 'Ataque')}: d20 ({d20}) + Mod (+{atk.get('hit_bonus', 2)}) = {tot_atk} vs CA {ca_alvo} ➔ {res.upper()}!\n"
            if dano_inimigo > 0:
                batch_log += f"🎲 [DADO - DANO] {dano_inimigo} de dano em {target['id'].title()} (PV: {target['hp']})!\n"

    return batch_log


class CombatManager:
    """Fachada estática para resolução de ações de combate, perícias, habilidades e turnos de inimigos."""
    resolve_action = staticmethod(resolve_action)
    resolve_skill_effect = staticmethod(resolve_skill_effect)
    process_enemies_turn_batch = staticmethod(process_enemies_turn_batch)

