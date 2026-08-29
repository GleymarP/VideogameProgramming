"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

import pygame
import random
import settings

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.factory import Factory

from src.Bird import Bird
from src.World import World
from src.Strategy import NormalStrategy
from src.Ghost import Ghost


class PlayingState(BaseState):
    def enter(self, **params: dict) -> None:

        if not params.get("resume", False):
            self.strategy = params.get("strategy", NormalStrategy())
            self.world = World()
            self.world.reset(True, self.strategy)
            self.bird = Bird(
                settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
                settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
                settings.BIRD_WIDTH,
                settings.BIRD_HEIGHT,
            )
            self.score = 0
            self.powerups = []
            self.powerup_spawn_timer = 0.0
            self.was_ghost = False

            
        else:
            self.world = params["world"]
            self.bird = params["bird"]
            self.score = params["score"]
            self.strategy = params["strategy"]
            self.powerups = params.get("powerups", [])
            self.powerup_spawn_timer = params.get("powerup_spawn_timer", 0.0)
            self.was_ghost = params.get("was_ghost", False)

        self.powerup_factory = Factory (Ghost)

    def update(self, dt: float) -> None:
        self.bird.update(dt)
        self.world.update(dt)

        self.powerup_spawn_timer += dt

        if self.powerup_spawn_timer >= 10.0:
            self.powerup_spawn_timer = 0.0

            if self.world.logs:
                last_log_pair = self.world.logs[-1]
                center_y = last_log_pair.get_gap_center()
    
                spawn_y = center_y - (settings.POWERUP_HEIGHT / 2)
                spawn_x = last_log_pair.x + (settings.LOG_WIDTH / 2) - (settings.POWERUP_WIDTH / 2)

                powerup = self.strategy.spawn_powerup(self.powerup_factory, spawn_x, spawn_y)

                if powerup is not None:
                    self.powerups.append(powerup)

        for powerup in self.powerups:
            powerup.update(dt)
            if powerup.collides(self.bird):
                powerup.take(self)

        self.powerups = [p for p in self.powerups if p.active]

        if self.was_ghost and not self.bird.is_ghost:
            pygame.mixer.music.load(settings.MUSIC["normal"])
            pygame.mixer.music.play(-1)

        self.was_ghost = self.bird.is_ghost

        
        if self.bird.get_rect().bottom >= settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT:
            settings.SOUNDS["explosion"].play()
            settings.SOUNDS["hurt"].play()

            if self.bird.is_ghost:
                pygame.mixer.music.load(settings.MUSIC["normal"])
                pygame.mixer.music.play(-1)

            self.state_machine.change("count_down", strategy = self.strategy)
            return    

        if not self.bird.is_ghost:
            if self.world.collides(self.bird.get_rect()):
                settings.SOUNDS["explosion"].play()
                settings.SOUNDS["hurt"].play()
                self.state_machine.change("count_down", strategy = self.strategy)
                return

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)

        for powerup in self.powerups:
            powerup.render(surface)

        self.bird.render(surface)
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            settings.COLOR_WHITE,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
      
        self.strategy.handle_bird_movement(self.bird, input_id, input_data)
        if input_id == "pause" and input_data.pressed:
            pygame.mixer.music.pause()

            self.state_machine.change(
                "paused",
                world=self.world,
                bird=self.bird,
                score=self.score,
                strategy = self.strategy,
                powerups = self.powerups,
                powerup_spawn_timer = self.powerup_spawn_timer,
                was_ghost = self.was_ghost,
                )
