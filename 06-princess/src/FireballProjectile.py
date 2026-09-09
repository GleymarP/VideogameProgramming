import math
import pygame
import settings

from src.GameObject import GameObject
from src.Projectile import Projectile

class FireballProjectile(Projectile):
    def __init__(self, obj, dx, dy, speed):
        super().__init__(obj, "right") 
        self.vx = dx
        self.vy = dy
      
        length = math.hypot(dx, dy)
        if length != 0:
            self.vx = dx / length * speed
            self.vy = dy / length * speed
        else:
            self.vx = speed
            self.vy = 0

        self.speed = speed
        self.damage = 1  
        self.owner = None 
  
   
    def update(self, dt: float):
        if self.dead:
            return
    
        self.obj.x += self.vx * dt
        self.obj.y += self.vy * dt

        margin = 32
        if (self.obj.x < -margin or self.obj.x > settings.VIRTUAL_WIDTH + margin or
            self.obj.y < -margin or self.obj.y > settings.VIRTUAL_HEIGHT + margin):
            self.dead = True

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        if self.obj:
            self.obj.render(surface, offset_x, offset_y)



class FireballFactory:
    @staticmethod
    def create_fireball(x: float, y: float, dx: float, dy: float, speed: float, owner) -> FireballProjectile:
        fire_def = {
            "type": "fireball",
            "texture": "fireball", 
            "frame": 1,
            "width": 16,
            "height": 16,
            "solid": False,
            "default_state": "default",
            "states": {"default": {"frame": 1}},
        }

        fire_obj = GameObject(fire_def, x, y)
        fireball = FireballProjectile(fire_obj, dx, dy, speed)
        fireball.owner = owner

        texture = settings.TEXTURES[fire_obj.texture_id]
        rect = settings.frame(fire_obj.texture_id, fire_obj.frame_index)
        original = texture.subsurface(rect)
        
        angle = math.degrees(math.atan2(fireball.vy, fireball.vx))
        fireball.image = pygame.transform.rotate(original, -angle)

        fireball.image_offset_x = (fireball.image.get_width() - fire_obj.width) / 2
        fireball.image_offset_y = (fireball.image.get_height() - fire_obj.height) / 2

        return fireball