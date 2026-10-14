"""Módulo de Sistema de Magias e Espaços de Magia (Spell Slots)."""

class SpellManager:
    """Gerencia os recursos mágicos de um personagem (Spell Slots)."""
    
    def __init__(self, max_slots: dict[int, int]):
        """
        max_slots: Dicionário onde a chave é o nível da magia (1 a 9) 
                   e o valor é a quantidade máxima de slots.
        Exemplo: {1: 4, 2: 2} (4 slots de nível 1, 2 slots de nível 2)
        """
        self.max_slots = max_slots
        # Copia os slots máximos para os slots atuais ao inicializar
        self.current_slots = {level: count for level, count in max_slots.items()}

    def cast_spell(self, spell_level: int) -> bool:
        """
        Tenta consumir um slot de magia do nível especificado.
        Retorna True se houver slot e for consumido, False caso contrário.
        Magias de nível 0 (Truques/Cantrips) não consomem slots.
        """
        if spell_level == 0:
            return True # Cantrips podem ser conjurados infinitamente
            
        if spell_level not in self.current_slots:
            return False
            
        if self.current_slots[spell_level] > 0:
            self.current_slots[spell_level] -= 1
            return True
            
        return False

    def reset_slots(self):
        """
        Restaura todos os slots para o valor máximo.
        Deve ser chamado após um descanso longo (gerenciado pelo RestSystem).
        """
        self.current_slots = {level: count for level, count in self.max_slots.items()}
