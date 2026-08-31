from typing import TypeVar
from src.powerups.PowerUp import PowerUp

from gale.timer import Timer

import settings

class BallCapture(PowerUp):
    def __init__(self, x : int, y: int):
        super().__init__(x, y, 6)

    def take (self, play_state: TypeVar("PlayState")) -> None:

        settings.SOUNDS["selected"].stop()
        settings.SOUNDS["selected"].play()

        play_state.paddle.sticky = True

        def desactive_glue():
            play_state.paddle.sticky = False

        Timer.after(6.0, desactive_glue)

        self.active = False

   




    

        
