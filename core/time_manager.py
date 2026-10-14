"""Módulo de Sistema de Descanso e Passagem de Tempo."""
import math

class RestSystem:
    """Gerencia as regras de descanso Curto e Longo (D&D 5e)."""

    @staticmethod
    def short_rest(character_state: dict, hit_dice_spent: int, hit_die_type: int = 8, con_modifier: int = 0) -> dict:
        """
        Calcula a cura de um descanso curto.
        Utiliza os dados de vida gastos e atualiza hp_current sem ultrapassar hp_max.
        """
        # Em D&D a média de recuperação de um dado é: floor((Max / 2) + 1)
        average_roll = math.floor((hit_die_type / 2) + 1)
        heal_per_die = max(1, average_roll + con_modifier) # Pelo menos 1 de cura por dado
        
        total_healing = heal_per_die * hit_dice_spent
        
        current_hp = character_state.get("hp_current", 0)
        max_hp = character_state.get("hp_max", 1)
        
        new_hp = min(max_hp, current_hp + total_healing)
        character_state["hp_current"] = new_hp
        
        return character_state

    @staticmethod
    def long_rest(character_state: dict, campaign_state: dict) -> tuple[dict, dict]:
        """
        Descanso longo:
        - Cura HP para o máximo.
        - Restaura recursos diários (ex: MP).
        - Incrementa o current_day da campanha em +1.
        """
        # Cura e Recursos Mágicos
        character_state["hp_current"] = character_state.get("hp_max", 1)
        
        if "mp_max" in character_state:
            character_state["mp_current"] = character_state["mp_max"]
            
        # Passagem de tempo no mundo
        current_day = campaign_state.get("current_day", 1)
        campaign_state["current_day"] = current_day + 1
        
        return character_state, campaign_state