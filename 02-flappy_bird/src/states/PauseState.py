import pygame
from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text

import settings


class PauseState(BaseState):
    def enter(self, **params: dict) ->None :
        self.world = params["world"]
        self.bird = params["bird"]
        self.score = params["score"]
        self.strategy = params["strategy"]


    def render(self, surface: pygame.Surface) ->None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            "Paused",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center = True,
            shadowed = True,
       )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "playing",
                 world=self.world,
                 bird=self.bird,
                 score=self.score,
                 strategy = self.strategy,
                 resume = True
                )


    
