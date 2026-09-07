from src.Projectile import Projectile
import settings
from src.GameObject import GameObject

import pygame

class Bow:
    @staticmethod
    def fire(x: float, y:float, direction: str, owner) -> Projectile:
        return ArrowFactory.create_arrow(x, y, direction, owner)

class ArrowFactory:
    @staticmethod
    def create_arrow(x: float, y: float, direction: str, owner) ->Projectile:
        speed = 150

        arrow_def = {
            "type": "arrow",
            "texture" : "bow-arrows",
            "frame": 3,
            "width" : 16,
            "height": 16,
            "solid" : False,
            "default_state" : "default",
            "states": {"default": {"frame": 3}},
        }

        arrow_obj = GameObject(arrow_def, x, y)

        projectile = Projectile(arrow_obj, direction)
        projectile.speed = speed
        projectile.damage = 1
        projectile.owner = owner

        texture = settings.TEXTURES[arrow_obj.texture_id]
        rect = settings.frame(arrow_obj.texture_id, arrow_obj.frame_index)
        original = texture.subsurface(rect)
        angle = 0
        if direction == "right":
            angle = 0
        elif direction == "down":
            angle =  270
        elif direction == "left":
            angle = 180
        elif direction == "up":
            angle = 90

        projectile.image = pygame.transform.rotate(original, angle)

        projectile.image_offset_x = (projectile.image.get_width() - arrow_obj.width) / 2
        projectile.image_offset_y = (projectile.image.get_height() - arrow_obj.height) / 2


        return projectile

    