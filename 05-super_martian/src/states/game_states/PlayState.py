"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any

import pygame

from gale.camera import Camera
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Clock import Clock
from src.GameLevel import GameLevel
from src.Player import Player


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.game_level = enter_params.get("game_level")
        if self.game_level is None:
            self.game_level = GameLevel(self.level)
            if self.level == 2:
                pygame.mixer.music.load(
                    settings.BASE_DIR / "assets" / "sounds" / "rom_hack.mp3"
                )
            else:
                pygame.mixer.music.load(
                    settings.BASE_DIR / "assets" / "sounds" / "music_grassland.ogg"
                )
            pygame.mixer.music.play(loops=-1)

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        if self.player is None:
            # Resting exactly on the ground tile's surface (row 9, one tile
            # below the platform's top edge) rather than a few pixels into
            # it, so gale.tilemap's one-way platform collision (which
            # requires the entity to already be at/above the surface) picks
            # it up on the very first frame instead of falling through.
            spawn_y = 9 * self.tilemap.tile_height - 20
            self.player = Player(0, spawn_y, self.game_level)
            self.player.change_state("idle")

        self.camera = enter_params.get("camera")

        if self.camera is None:
            self.camera = Camera(settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
            self.camera.follow(self.player, rate=settings.CAMERA_FOLLOW_RATE)
            self.camera.bounds = self.game_level.get_rect()
            self.camera.x, self.camera.y = self.player.x, self.player.y
            self.camera.update(0)

        self.clock = enter_params.get("clock")

        if self.clock is None:
            self.clock = Clock(30)

            def countdown_timer():
                self.clock.count_down()

                if 0 < self.clock.time <= 5:
                    settings.SOUNDS["timer"].play()

                if self.clock.time == 0:
                    self.player.change_state("dead")
      
            self.timer_event = Timer.every(1, countdown_timer)
        else:
            Timer.resume()

        self.fade_alpha = 255
        Timer.tween(0.5, [(self, {"fade_alpha": 0})])

    def update(self, dt: float) -> None:
        if self.player.is_dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            Timer.clear()
            self.state_machine.change("game_over", self.player)

        self.player.update(dt)

        if self.player.y >= self.tilemap.pixel_height:
            self.player.change_state("dead")

        self.camera.update(dt)
        self.game_level.update(dt)

        for creature in self.game_level.creatures:
            if self.player.collides(creature):
                self.player.change_state("dead")

        if getattr(self.game_level, "is_completed", False):
            self.next_level()
            self.game_level.is_completed = False

        for item in self.game_level.items:
            if not item.active:
                continue
            
            if self.player.collides(item):
                if not item.consumable and item.collidable:
                    if self.player.vy < 0:
                        self.player.vy = 0

                    item.on_collide(self.player)    
                    
                elif item.consumable and not getattr(self.game_level, "is_completed", False):
                    item.on_collide(self.player)
                    item.on_consume(self.player)

        if self.player.score >= 200 and not getattr(self.game_level, "block_spawned", False):
            pygame.mixer.music.stop()
            settings.SOUNDS["next_level"].play()

            self.game_level.add_item({
                "item_name": "special_block",
                "frame_index": 49,
                "x": 650,
                "y" :20,
                "width":16,
                "height": 16
            })

            self.game_level.block_spawned = True
            if hasattr(self, "timer_event"):
                self.timer_event.remove()

            self.game_level.items = [
            item for item in self.game_level.items 
            if not getattr(item, "consumable", False)
            ]
            

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(surface, self.camera)
        self.player.render(surface, self.camera)

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.clock.time}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        if getattr(self, "fade_alpha", 0) > 0:
            fade_surface = pygame.Surface(
                (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT),
                pygame.SRCALPHA
            )
            fade_surface.fill((0, 0, 0, int(self.fade_alpha)))
            surface.blit(fade_surface, (0, 0))
        
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            Timer.pause()
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                clock=self.clock,
            )
        else:
            self.player.on_input(input_id, input_data)

    def next_level(self):
        self.fade_alpha = 0

        def do_fade():
            if self.level < settings.NUM_LEVELS:
                
                self.state_machine.change(
                    "play",
                    level = self.level + 1,
                )
            else:
                self.state_machine.change("start")

        Timer.tween(0.9, [(self, {"fade_alpha": 255})], on_finish=do_fade)
