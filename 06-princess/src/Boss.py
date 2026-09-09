import pygame
from src.Entity import Entity
from src.FireballProjectile import  FireballFactory
import settings
from src.states.entity.EntityWalkState import EntityWalkState
from src.states.entity.EntityIdleState import EntityIdleState
from src.definitions.entity import ENTITY_DEFS

class Boss(Entity):
    def __init__(self, x, y, player, room):
        boss_def = ENTITY_DEFS["boss"]
        super().__init__(
            x=x,
            y=y,
            width=32,  
            height=32,
            walk_speed=30, 
            health=5,  
            animation_defs=boss_def["animations"],
            states={}
        )
        self.player = player
        self.room = room
        self.offset_x = 0
        self.offset_y = 0
        self.max_health = 5
        
        self.inmune = True  
        self.inmunidad_timer = 0.0
        self.inmunidad_duracion = 2.0 
        
        self.shoot_timer = 0.0
        self.shoot_interval = 3.0  
        self.projectile_speed = 60  
               
        self.state_machine.states = {
            "walk": lambda sm: EntityWalkState(self, sm),
            "idle": lambda sm: EntityIdleState(self, sm),
        }
        self.change_state("idle")
        
    def take_damage_from_sword(self, damage):
        if not self.inmune and not self.invulnerable:
            self.damage(damage)
            self.go_invulnerable(0.3)
            settings.SOUNDS["hit-enemy"].play()
            if self.health <= 0:
                self.dead = True
                self.room.boss_defeated()
        
    def hit_by_arrow(self):
        if not self.dead and not self.invulnerable:
            self.inmune = False
            self.inmunidad_timer = 0.0
            self.go_invulnerable(0.3)

            settings.SOUNDS["hit-enemy"].play()
    
    def update(self, dt):
        super().update(dt)
        
        if not self.inmune:
            self.inmunidad_timer += dt
            if self.inmunidad_timer >= self.inmunidad_duracion:
                self.inmune = True
                self.inmunidad_timer = 0.0
   
        if not self.dead:
            self.shoot_timer += dt
            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0.0
                self.shoot_fireball()
    
    def shoot_fireball(self):
     
        dx = self.player.x + self.player.width/2 - (self.x + self.width/2)
        dy = self.player.y + self.player.height/2 - (self.y + self.height/2)
       
        fireball = FireballFactory.create_fireball(
            self.x + self.width / 2 -8,
            self.y + self.height / 2 - 8,
            dx,
            dy,
            self.projectile_speed,
            self
        )

        self.room.projectiles.append(fireball)
        settings.SOUNDS["sword"].play()

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
  
        super().render(surface, offset_x, offset_y)

        if self.dead:
            return
    
        health_ratio = self.health / self.max_health

        bar_width = 40
        bar_height = 5
        bar_x = self.x + self.width/2 - bar_width/2 + offset_x
        bar_y = self.y - 12 + offset_y

        pygame.draw.rect(surface, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))

        if health_ratio > 0.5:
            color = (0, 255, 0)        
        elif health_ratio > 0.25:
            color = (255, 255, 0)      
        else:
            color = (255, 0, 0)        

        pygame.draw.rect(surface, color, (bar_x, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)