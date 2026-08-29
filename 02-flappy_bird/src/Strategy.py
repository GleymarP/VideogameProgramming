import random
import settings
from gale.input_handler import InputData
from gale.factory import Factory
from src.LogPair import LogPair

class NormalStrategy:
    def handle_bird_movement(self, bird, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            bird.jump()

    def get_spawn_interval(self) -> float:
         return settings.TIME_TO_SPAWN_LOGS

    def calculate_log_y(self, last_y: float) -> float:
         return max(
                    -settings.LOG_HEIGHT + 10,
                        min(
                            last_y + random.randint(-20, 20),
                            settings.VIRTUAL_HEIGHT + 90 - settings.LOG_HEIGHT,
                    ),
                )

    def create_log_pair(self, factory: Factory, x: float, y: float) -> LogPair:
         return factory.create(x, y, properties={ "moving": False })

    def spawn_powerup(self, factory:Factory, x: float, y: float):
         return None

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

    def get_spawn_interval(self) -> float:
         return random.uniform(1 , 30)

    def calculate_log_y(self, last_y: float) -> float:
         target_y = last_y + random.randint(-50, 50)

         min_y = -settings.LOG_HEIGHT + 20
         max_y = settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT - settings.LOG_HEIGHT - 20

         return max(min_y, min(target_y, max_y))

    def create_log_pair(self, factory:Factory, x: float, y:float) -> LogPair:
        is_moving = random.choice([True, False])

        return factory.create(x, y, properties={"moving": is_moving})

    def spawn_powerup(self, factory: Factory, x: float, y: float):
         if random.random() < 0.5:
              return factory.create(x, y)
         return None