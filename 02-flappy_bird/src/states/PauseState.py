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
        self.powerups = params.get("powerups", [])
        self.powerup_spawn_timer = params.get("powerup_spawn_timer", 0.0)
        self.was_ghost = params.get("was_ghost", False)


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
        render_text(
            surface,
            "Press M to change the game mode",
                    settings.FONTS["medium"],
                    settings.VIRTUAL_WIDTH / 2,
                    settings.VIRTUAL_HEIGHT / 2 + 30,
                    settings.COLOR_WHITE,
                    center = True,
                    shadowed = True,
               )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            pygame.mixer.music.unpause()
            self.state_machine.change(
                "playing",
                 world=self.world,
                 bird=self.bird,
                 score=self.score,
                 strategy = self.strategy,
                 powerups = self.powerups,
                 powerup_spawn_timer = self.powerup_spawn_timer,
                 was_ghost = self.was_ghost,
                 resume = True
                )
        elif input_id == "menu_select" and input_data.pressed:
            pygame.mixer.music.load(settings.MUSIC["normal"])
            pygame.mixer.music.play(-1)
            self.state_machine.change("title")


    
