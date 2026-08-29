from typing import Any, TypeVar
import pygame
import settings

PlayState = TypeVar("PlayState")

class PowerUp:
    def __init__(self, x: float, y: float, texture: str ) -> None:
        self.x = x
        self.y = y
        self.vx = settings.MAIN_SCROLL_SPEED
        self.active = True
        self.texture = texture

    def get_collision_rect(self) -> pygame.Rect :
        return pygame.Rect(
            round(self.x), round(self.y), settings.POWERUP_WIDTH, settings.POWERUP_HEIGHT 
        )

    def collides(self, obj: Any) -> bool:
        return self.get_collision_rect().colliderect(obj.get_rect())

    def update(self, dt: float) -> None:
        self.x -= self.vx * dt
        if self.x < -settings.POWERUP_WIDTH:
            self.active = False

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(
            settings.TEXTURES[self.texture], 
            (round(self.x), round(self.y)),
        )

    def take(self, play_state: PlayState) -> None:
        raise NotImplementedError