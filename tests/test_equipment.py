from core.dnd_rules import CharacterCalculator
from core.combat_system import resolve_action

if __name__ == "__main__":
    print("=== TESTE 1: CRIANDO O LADINO ===")
    ladino_stats = CharacterCalculator.calculate_derived_stats(
        {'FOR': 10, 'DES': 16, 'CON': 12, 'INT': 10, 'SAB': 10, 'CAR': 10},
        'Humano', 'Ladino', 'Herói'
    )

    print(f"CA Ladino (Couro + 3 DES): {ladino_stats['ac']} (Esperado: 14)")
    print(f"Inventário: {ladino_stats['equipment']}")

    # Simulando um ataque com Rapieira
    parsed_json_ladino = {
        "tipo_acao": "ataque",
        "arma_usada": "rapieira",
        "alvo": ["alvo_teste"]
    }

    alvo_mock = {"alvo_teste": {"name": "Ogro Teste", "ca": 13, "pv_atual": 30}}

    print("\n--- Ataque do Ladino ---")
    import random
    random.seed(5) # fixar seed
    ladino_stats['attributes'] = {'FOR': 10, 'DES': 16}
    resultado_ladino = resolve_action(parsed_json_ladino, ladino_stats, [alvo_mock["alvo_teste"]], alvo_mock)
    print(resultado_ladino["sys_log"])

    print("\n=== TESTE 2: CRIANDO O GUERREIRO ===")
    guerreiro_stats = CharacterCalculator.calculate_derived_stats(
        {'FOR': 16, 'DES': 10, 'CON': 14, 'INT': 10, 'SAB': 10, 'CAR': 10},
        'Humano', 'Guerreiro', 'Herói'
    )

    print(f"CA Guerreiro (Cota de Malha + Escudo): {guerreiro_stats['ac']} (Esperado: 18)")
    print(f"Inventário: {guerreiro_stats['equipment']}")

    # Simulando um ataque com Espada Longa
    parsed_json_guerreiro = {
        "tipo_acao": "ataque",
        "arma_usada": "espada longa",
        "alvo": ["alvo_teste"]
    }

    alvo_mock2 = {"alvo_teste": {"name": "Dragão Teste", "ca": 15, "pv_atual": 100}}

    print("\n--- Ataque do Guerreiro ---")
    guerreiro_stats['attributes'] = {'FOR': 16, 'DES': 10}
    resultado_guerreiro = resolve_action(parsed_json_guerreiro, guerreiro_stats, [alvo_mock2["alvo_teste"]], alvo_mock2)
    print(resultado_guerreiro["sys_log"])

