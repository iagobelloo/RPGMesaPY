from core.dnd_rules import CharacterCalculator
from core.combat_system import resolve_action
import random

random.seed(12) # Fixed seed

if __name__ == "__main__":
    ladino_stats = CharacterCalculator.calculate_derived_stats(
        {'FOR': 10, 'DES': 16, 'CON': 12, 'INT': 10, 'SAB': 10, 'CAR': 10},
        'Humano', 'Ladino', 'Herói'
    )
    ladino_stats['hp_current'] = ladino_stats.get('hp_max', 10)

    # Simulando uma rodada de combate
    parsed_json = {
        "tipo_acao": "ataque",
        "arma_usada": "rapieira",
        "alvo": ["Goblin Feio"],
        "reacao_inimigos": [
            {"id_narrativo": "Goblin Feio", "tipo_acao": "ataque"}
        ]
    }

    alvos_ativos = {
        "Goblin Feio": {"name": "Goblin Feio", "ca": 13, "pv_atual": 7, "tipo_bestiario": "Lacaio Goblin"}
    }

    ladino_stats['attributes'] = {'FOR': 10, 'DES': 16}

    print("=== RODADA DE COMBATE ===")
    resultado = resolve_action(parsed_json, ladino_stats, [alvos_ativos["Goblin Feio"]], alvos_ativos)
    print(resultado["sys_log"])
    print(f"Status do jogador: {resultado['status']}")
    print(f"HP do jogador: {ladino_stats.get('hp_current', 'Erro')}")
    print(f"HP do Goblin: {alvos_ativos['Goblin Feio']['pv_atual']}")

