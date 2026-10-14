import sys
import os

# Adiciona diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.story_engine import StoryManager

def run_test():
    story = StoryManager()
    print("=== TESTE STORY ENGINE (ALIADOS E DÉJÀ VU) ===")
    
    # 1. Prólogo
    story.inject_prologue_data("Anão", "Clérigo", "Soldado")
    story.advance_beat()
    
    # 2. Desbloqueia aliados nas missões
    story.set_beat(2)
    story.unlock_ally("cleric")
    story.unlock_ally("mage")
    story.advance_beat()
    story.unlock_ally("rogue")
    story.unlock_ally("warlock")
    
    # 3. Boss Final (Beat 4)
    story.set_beat(4)
    fake_pc = {"hp": 50, "name": "Herói"}
    fake_targets = {"Boss": {"hp": 100}}
    fake_visuals = {"Boss": "boss_img"}
    
    print("\n[Simulação] Entrando em combate no Beat 4. Injetando aliados...")
    unlocked = story.get_unlocked_allies()
    for ally_id, ally_data in unlocked.items():
        fake_targets[ally_data['name']] = ally_data
        
    print(f"[Simulação] Grupo final para o Boss: {list(fake_targets.keys())}")
    
    story.create_snapshot(fake_pc, fake_targets, fake_visuals)
    
    # Simula perda de HP
    fake_pc["hp"] = 0
    print(f"\n[Simulação] Batalha perdida! HP do Herói caiu para: {fake_pc['hp']}")
    
    # Load Snapshot
    snap = story.load_snapshot()
    if snap:
        restored_pc, restored_targets, restored_visuals = snap
        print(f"[Simulação] HP do Herói após Déjà Vu: {restored_pc['hp']}")
        print(f"[Simulação] Grupo Restaurado Intacto: {list(restored_targets.keys())}")

if __name__ == "__main__":
    run_test()

