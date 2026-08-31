from typing import TypeVar

from src.powerups.PowerUp import PowerUp

from gale.timer import Timer

import settings

class Cannons(PowerUp):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 2)

    def take(self, play_state:TypeVar("PlayState")) -> None:
        settings.SOUNDS["selected"].stop()
        settings.SOUNDS["selected"].play()

        play_state.paddle.has_cannons = True

        def deactivate_cannons():
            play_state.paddle.has_cannons = False

        Timer.after(8.0, deactivate_cannons)

        self.active = False
        