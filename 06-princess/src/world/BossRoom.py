from src.world.Room import Room
from src.Boss import Boss
import settings
import pygame

from src.world.Doorway import Doorway

class BossRoom(Room):
    def __init__(self, player, on_game_over, dungeon, entry_direction):
        super().__init__(player, on_game_over, dungeon)
        self.dungeon = dungeon

        pygame.mixer.music.load(settings.MUSIC["boss"])
        pygame.mixer.music.play(loops=-1)

        self.entities = []
        self.objects = []
        self.doorways = []
        self._doorways_by_direction = {}

        if entry_direction == "up":
            door_dir = "top"
        elif entry_direction == "down":
            door_dir = "bottom"
        else:
            door_dir = entry_direction
        if entry_direction == "up":
            door_dir = "top"
        elif entry_direction == "down":
            door_dir = "bottom"
        else:
            door_dir = entry_direction

        self.entry_door = Doorway(door_dir, False, self)
        self.doorways.append(self.entry_door)
        self._doorways_by_direction = {door_dir: self.entry_door}
        self.boss_door = self.entry_door
        
        if door_dir == "top":
            boss_x = settings.MAP_RENDER_OFFSET_X + (settings.MAP_WIDTH * settings.TILE_SIZE // 2) - 16
            boss_y = settings.MAP_RENDER_OFFSET_Y + settings.MAP_HEIGHT * settings.TILE_SIZE - settings.TILE_SIZE * 3
        elif door_dir == "bottom":
            boss_x = settings.MAP_RENDER_OFFSET_X + (settings.MAP_WIDTH * settings.TILE_SIZE // 2) - 16
            boss_y = settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE * 2
        elif door_dir == "left":
            boss_x = settings.MAP_RENDER_OFFSET_X + settings.MAP_WIDTH * settings.TILE_SIZE - settings.TILE_SIZE * 3
            boss_y = settings.MAP_RENDER_OFFSET_Y + (settings.MAP_HEIGHT * settings.TILE_SIZE // 2) - 16
        else:  
            boss_x = settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE * 2
            boss_y = settings.MAP_RENDER_OFFSET_Y + (settings.MAP_HEIGHT * settings.TILE_SIZE // 2) - 16

        self.boss = Boss(boss_x, boss_y, self.player, self)
        self.entities.append(self.boss)
        
    def _generate_entities(self):
        pass

    def _generate_objects(self):
        pass
    
    def boss_defeated(self):
        self.boss_door.open = True
        settings.SOUNDS["door"].play()

        pygame.mixer.music.load(settings.MUSIC["dungeon"])
        pygame.mixer.music.play(loops=-1)
       