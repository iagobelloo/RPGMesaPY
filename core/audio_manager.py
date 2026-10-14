import pygame
import os

class AudioManager:
    """Gerenciador de áudio simples e seguro para Pygame."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AudioManager()
        return cls._instance
        
    def __init__(self):
        self._music_playing = None
        try:
            pygame.mixer.init()
            self.enabled = True
        except:
            self.enabled = False
            
    def play_bgm(self, track_name: str):
        if not self.enabled: return
        if self._music_playing == track_name: return
        
        filepath = os.path.join("assets", "audio", f"{track_name}.mp3")
        if os.path.exists(filepath):
            try:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play(-1) # Loop infinito
                self._music_playing = track_name
            except Exception as e:
                print(f"[Áudio] Falha ao tocar BGM {track_name}: {e}")
                
    def play_sfx(self, effect_name: str):
        if not self.enabled: return
        
        filepath = os.path.join("assets", "audio", f"{effect_name}.wav")
        if not os.path.exists(filepath):
            filepath = os.path.join("assets", "audio", f"{effect_name}.mp3")
            
        if os.path.exists(filepath):
            try:
                sound = pygame.mixer.Sound(filepath)
                sound.play()
            except Exception as e:
                print(f"[Áudio] Falha ao tocar SFX {effect_name}: {e}")

