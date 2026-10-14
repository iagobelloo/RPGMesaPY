"""Módulo de rolagem de dados."""
import random
import math

class DiceEngine:
    # pylint: disable=missing-function-docstring
    @staticmethod
    def calculate_modifier(base_stat: int) -> int:
        """Calcula o modificador de D&D 5e a partir de um atributo base."""
        return math.floor((base_stat - 10) / 2)

    @staticmethod
    def roll_d20() -> int:
        return random.randint(1, 20)

    @staticmethod
    def roll_d12() -> int:
        return random.randint(1, 12)

    @staticmethod
    def roll_d10() -> int:
        return random.randint(1, 10)

    @staticmethod
    def roll_d8() -> int:
        return random.randint(1, 8)

    @staticmethod
    def roll_d6() -> int:
        return random.randint(1, 6)

    @staticmethod
    def roll_d4() -> int:
        return random.randint(1, 4)

    @staticmethod
    def roll_d100() -> int:
        return random.randint(1, 100)

    @staticmethod
    def roll_with_advantage() -> int:
        """Rola 2d20 e retorna o maior valor (Vantagem)."""
        return max(DiceEngine.roll_d20(), DiceEngine.roll_d20())

    @staticmethod
    def roll_with_disadvantage() -> int:
        """Rola 2d20 e retorna o menor valor (Desvantagem)."""
        return min(DiceEngine.roll_d20(), DiceEngine.roll_d20())

    @staticmethod
    def skill_check(d20_roll: int, modifier: int, dc: int) -> bool:
        """
        Valida se um teste passou na Classe de Dificuldade (DC).
        Trata sucessos e falhas simples matematicamente.
        """
        return (d20_roll + modifier) >= dc

    @staticmethod
    def parse_and_roll_dice(dice_string: str) -> int:
        """
        Lê textos como '2d4+2', '1d8', '3d6-1' e retorna o valor inteiro final rolado.
        """
        import re
        dice_string = str(dice_string).lower().strip()
        match = re.match(r'^(\d+)d(\d+)(?:([+-])(\d+))?$', dice_string)
        if not match:
            # Fallback seguro
            return 1
            
        num_dice = int(match.group(1))
        sides = int(match.group(2))
        op = match.group(3)
        mod = int(match.group(4)) if match.group(4) else 0
        
        total = sum(random.randint(1, sides) for _ in range(num_dice))
        if op == '+':
            total += mod
        elif op == '-':
            total -= mod
            
        return max(0, total)