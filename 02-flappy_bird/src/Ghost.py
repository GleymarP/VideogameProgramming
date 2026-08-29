import pygame
import settings
from typing import TypeVar
from src.PowerUp import PowerUp

PlayState = TypeVar("PlayState")

class Ghost(PowerUp):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, "power")

    def take(self, play_state: PlayState) -> None:
        play_state.bird.active_ghost_mode(duration = 8.0)

        pygame.mixer.music.load(settings.MUSIC["ghost"])
        pygame.mixer.music.play(-1)

        self.active = False