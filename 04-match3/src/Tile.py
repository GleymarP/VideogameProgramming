"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Tile.
"""
from typing import Optional

import pygame

import settings


class Tile:
    def __init__(self, i: int, j: int, color: int, variety: int, power_up: Optional[str] = None) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.color = color
        self.variety = variety
        self.alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        self.power_up = power_up
        
    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        self.alpha_surface.blit(
            settings.TEXTURES["tiles"],
            (0, 0),
            settings.FRAMES["tiles"][self.color][self.variety],
        )
        pygame.draw.rect(
            self.alpha_surface,
            (34, 32, 52, 200),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )
        surface.blit(self.alpha_surface, (self.x + 2 + offset_x, self.y + 2 + offset_y))
        surface.blit(
            settings.TEXTURES["tiles"],
            (self.x + offset_x, self.y + offset_y),
            settings.FRAMES["tiles"][self.color][self.variety],
        )

        if self.power_up is not None:
            center_x = self.x + offset_x + (settings.TILE_SIZE - settings.POWER_SIZE) // 2
            center_y = self.y + offset_y + (settings.TILE_SIZE - settings.POWER_SIZE) // 2

            if self.power_up == "line": 
               surface.blit(settings.TEXTURES["line"], (center_x, center_y))

            elif self.power_up == "color":
                surface.blit(settings.TEXTURES["color"], (center_x, center_y))