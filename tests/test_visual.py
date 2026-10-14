import pygame
import sys
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
screen = pygame.display.set_mode((1280, 720))

from ui.scene_renderer import SceneRenderer
from ui.asset_manager import AssetManager

AssetManager.load_backgrounds()
AssetManager.load_enemies()

renderer = SceneRenderer(1280, 720)
renderer.add_floating_text("-14 HP", 600, 300, (255, 0, 0))

# Moca uma mensagem de NPC
message = {
    "text": "Seu tolo! Você acha que pode me derrotar com esta espada enferrujada?!",
    "npc_falando": "Lacaio Goblin"
}

# Run a few frames
for _ in range(30):
    renderer.draw_bottom_dialog_box(screen, message)
    
    for ft in renderer.floating_texts[:]:
        ft["y"] -= 1
        ft["timer"] -= 1
        
        if ft["timer"] <= 0:
            renderer.floating_texts.remove(ft)
        else:
            alpha = min(255, ft["timer"] * 5)
            txt_surf = renderer.font_dmg.render(ft["text"], True, ft["color"])
            txt_surf.set_alpha(alpha)
            outline = renderer.font_dmg.render(ft["text"], True, (0, 0, 0))
            outline.set_alpha(alpha)
            screen.blit(outline, (ft["x"] - outline.get_width()//2 + 2, ft["y"] + 2))
            screen.blit(txt_surf, (ft["x"] - txt_surf.get_width()//2, ft["y"]))

print("Render test completed successfully! Floating texts left:", len(renderer.floating_texts))
