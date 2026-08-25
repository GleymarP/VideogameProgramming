import random
import settings
from gale.input_handler import InputData

class NormalStrategy:
    def handle_bird_movement(self, bird, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            bird.jump()

class HardStrategy:
    def handle_bird_movement(self, bird, input_id: str, input_data: InputData) -> None:

        if input_id == "move_left":
            if input_data.pressed:
                bird.vx = -settings.BIRD_SPEED
            elif bird.vx < 0:
                bird.vx = 0

        if input_id == "move_right":
            if input_data.pressed:
                bird.vx = settings.BIRD_SPEED
            elif bird.vx > 0:
                bird.vx = 0

        if input_id == "jump" and input_data.pressed:
                    bird.jump()

    