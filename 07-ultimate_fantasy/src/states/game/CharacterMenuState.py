from typing import Any, List
import pygame
from gale.state import BaseState
import settings
from src.gui.Panel import Panel
from src.entity.Character import Character
from src.states.game.CharacterDetailState import CharacterDetailState
from src.gui.Menu import Menu

class CharacterMenuState(BaseState):
    def enter(self, party: Any) -> None:
        self.party = party
        self.characters: List[Character] = list(party.characters.values())
       
        items = []
        for ch in self.characters:
            items.append((ch.name, self._make_character_callback(ch)))

        items.append(("Close Menu", self._close_menu))

        self.menu = Menu(
            settings.VIRTUAL_WIDTH // 2 - 80,
            settings.VIRTUAL_HEIGHT // 2 - 100,
            160,
            200,
            items=items,
            font=settings.FONTS["medium"],
        )

    def _make_character_callback(self, character):
        def callback():
            self.state_machine.push(CharacterDetailState(self.state_machine),
                                    party = self.party,
                                    character = character)

        return callback

    def _close_menu(self):
        self.state_machine.pop()

    def update(self, dt):
        self.menu.update(dt)

    def on_input(self, input_id, input_data):
        if not input_data.pressed:
            return
        
        if input_id == "status":
            self.state_machine.pop()
            return

        if input_id == "move_up":
            self.menu.navigate((0, -1))

        if input_id == "move_down":
            self.menu.navigate((0, 1))

        if input_id == "enter" or input_id == "confirm":
            self.menu.confirm()

    def render(self, surface):
        overlay = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        self.menu.render(surface)

    
     

