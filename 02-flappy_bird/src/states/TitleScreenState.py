"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.World import World
from src.Strategy import HardStrategy, NormalStrategy


class TitleScreenState(BaseState):
    def enter(self) -> None:
        self.world = World()

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Flappy Bird",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "Press N for normal mode",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center= True,
            shadowed=True,
        )
        render_text(
            surface,
            "Press H for hard mode",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 + 30,
            settings.COLOR_WHITE,
            center = True,
            shadowed= True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        
        if input_id == "normal_mode":
            self.state_machine.change("count_down", strategy = NormalStrategy())
        elif input_id == "hard_mode" :
            self.state_machine.change("count_down", strategy = HardStrategy())
