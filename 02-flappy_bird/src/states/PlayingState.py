"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World
from src.Strategy import NormalStrategy


class PlayingState(BaseState):
    def enter(self, **params: dict) -> None:

        if not params.get("resume", False):
            self.world = World()
            self.world.reset(True)
            self.bird = Bird(
                settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
                settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
                settings.BIRD_WIDTH,
                settings.BIRD_HEIGHT,
            )
            self.score = 0
            self.strategy = params.get("strategy", NormalStrategy())
        else:
            self.world = params["world"]
            self.bird = params["bird"]
            self.score = params["score"]
            self.strategy = params["strategy"]


    def update(self, dt: float) -> None:
        self.bird.update(dt)
        self.world.update(dt)

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
            self.state_machine.change(
                "paused",
                world=self.world,
                bird=self.bird,
                score=self.score,
                strategy = self.strategy,
                )
