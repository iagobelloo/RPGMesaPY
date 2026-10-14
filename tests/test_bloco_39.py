import sys
from core.dnd_rules import RACAS_5E, CLASSES, ANTECEDENTES_5E, TENDENCIAS_5E

def test_loading():
    print("Test RACAS_5E Humano:")
    print(RACAS_5E["Humano"]["descricao_ui"])
    print("Test CLASSES Guerreiro:")
    print(CLASSES["Guerreiro"]["descricao_ui"])
    print("Test ANTECEDENTES_5E Herói:")
    print(ANTECEDENTES_5E["Herói"]["descricao_ui"])
    print("Test TENDENCIAS_5E Caótico e Bom:")
    print(TENDENCIAS_5E["Caótico e Bom"]["descricao_ui"])
    print("All loaded successfully!")

if __name__ == "__main__":
    test_loading()

