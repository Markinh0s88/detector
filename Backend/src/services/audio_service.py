# backend/src/services/audio_service.py
import pygame
import os
from typing import Optional

class AudioService:
    def __init__(self):
        # Inicializar o mixer do pygame
        pygame.mixer.init()
        
        # Configurações padrão
        self.settings = {
            'enable_sound': True,
            'success_volume': 0.8,
            'error_volume': 0.7
        }
        
        # Carregar os sons
        self.sounds = {
            'success': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'success.wav')),
            'error': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'error.wav'))
        }

    def update_settings(self, settings: dict):
        """Atualiza as configurações de áudio"""
        self.settings.update(settings)
        
        # Atualizar volumes
        if 'success_volume' in settings:
            self.sounds['success'].set_volume(settings['success_volume'] / 100)
        if 'error_volume' in settings:
            self.sounds['error'].set_volume(settings['error_volume'] / 100)

    def play_success(self):
        """Toca o som de sucesso"""
        if self.settings['enable_sound']:
            self.sounds['success'].play()

    def play_error(self):
        """Toca o som de erro"""
        if self.settings['enable_sound']:
            self.sounds['error'].play()

    def test_sound(self, sound_type: str) -> bool:
        """Testa um som específico"""
        if sound_type in self.sounds:
            if self.settings['enable_sound']:
                self.sounds[sound_type].play()
                return True
        return False

    def cleanup(self):
        """Limpa os recursos de áudio"""
        pygame.mixer.quit()
