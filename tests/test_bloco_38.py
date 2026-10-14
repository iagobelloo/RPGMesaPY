import pygame
import os
from ui.asset_manager import AssetManager

pygame.init()
pygame.display.set_mode((800, 600)) # Needed to init pygame image module fully

print("Teste Background inexistente:")
bg = AssetManager.get_background("nonexistent_bg_123.png")
if bg.get_size() == (800, 600) and bg.get_at((0,0))[:3] == (255, 0, 255):
    print("Background fallback OK")
else:
    print("Background fallback FALHOU", bg.get_size(), bg.get_at((0,0)))

print("Teste Enemy inexistente:")
enemy = AssetManager.get_enemy_sprite("m_fake_monster")
if enemy.get_size() == (64, 64) and enemy.get_at((0,0))[:3] == (255, 0, 255):
    print("Enemy fallback OK")
else:
    print("Enemy fallback FALHOU", enemy.get_size(), enemy.get_at((0,0)))

print("Teste Player inexistente:")
player = AssetManager.get_character_sprite("FakeRace", "FakeClass")
if player.get_size() == (64, 64) and player.get_at((0,0))[:3] == (255, 0, 255):
    print("Player fallback OK")
else:
    print("Player fallback FALHOU", player.get_size(), player.get_at((0,0)))

print("Teste Player existente:")
player_real = AssetManager.get_character_sprite("Humano", "Guerreiro")
if player_real.get_size() != (64, 64) or player_real.get_at((0,0))[:3] != (255, 0, 255):
    print("Player existente OK")
else:
    print("Player existente FALHOU")

print("Todos os testes do Bloco 38 concluiram.")
pygame.quit()
