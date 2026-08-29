"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Bird.
"""

import pygame
import settings

class Bird:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.vx: float = 0.0
        self.jumping: bool = False

        self.is_ghost = False
        self.ghost_timer = 0.0
      
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)
    
    def jump(self) -> None:
        self.jumping = True

    def active_ghost_mode (self, duration: float) -> None:
        self.is_ghost = True
        self.ghost_timer = duration

    def update(self, dt: float) -> None:
        self.vy += settings.GRAVITY * dt

        if self.jumping:
            settings.SOUNDS["jump"].play()
            self.vy = -settings.JUMP_TAKEOFF_SPEED
            self.jumping = False

        self.y += self.vy * dt

        self.x += self.vx * dt
        self.x = max(0, min(self.x, settings.VIRTUAL_WIDTH - self.width))

        if self.is_ghost:
            self.ghost_timer -= dt
            if self.ghost_timer <= 0:
                self.is_ghost = False
                self.ghost_timer = 0.0

    def render(self, surface: pygame.Surface) -> None:
        if self.is_ghost:
            surface.blit(settings.TEXTURES["ghost"], self.get_rect())   
        else:
            surface.blit(settings.TEXTURES["bird"], self.get_rect())   

       
             