from typing import TypeVar

from src.powerups.PowerUp import PowerUp

from gale.timer import Timer

import settings


class HeavyBall(PowerUp):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 5)

    def take(self, play_state:TypeVar("PlayState")) -> None:
        settings.SOUNDS["selected"].stop()
        settings.SOUNDS["selected"].play()

        for ball in play_state.balls:
            ball.heavy = True

        def deactivate_heavy():
            for ball in play_state.balls:
                if ball.active:
                    ball.heavy = False

        Timer.after(8.0, deactivate_heavy)
        self.active = False

        

