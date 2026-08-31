import pygame
import settings

class Projectile:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8 
        self.vy = -400
        self.texture = settings.TEXTURES["spritesheet"]

        self.frame = 5
        self.active = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt:float) -> None:
        self.y += self.vy * dt

        if self.y + self.height < 0:
            self.active = False

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(
            self.texture,(self.x, self.y), settings.FRAMES["balls"][self.frame]
        )

        