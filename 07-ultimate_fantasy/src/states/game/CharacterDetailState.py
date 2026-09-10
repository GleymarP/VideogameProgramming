from typing import Any, List
import pygame

from gale.state import BaseState

import settings
from src.entity.Character import Character
from src.gui.Panel import Panel

class CharacterDetailState(BaseState):
    def enter(self, party: Any, character: Character) -> None:
        self.party = party
        self.character = character
        self.selected_action_index = 0

        self.panel_left = Panel(20, 30, 150, 190)
        self.panel_right = Panel(180, 30, 130, 90)

        self.font_small = settings.FONTS["small"]
        self.font_medium = settings.FONTS["medium"]
        self.selecting_target = False
        self.active_action = None
        self.target_index = 0

        self.message = None
        self.message_timer = 0.0

    def on_input(self, input_id: str, input_data: Any) -> None:
        if not input_data.pressed:
            return

        if self.selecting_target:
            chars = [c for c in self.party.characters.values() if not c.dead]
            if not chars:
                self.selecting_target = False
                self.active_action = None
                return

            if input_id == "move_up" or input_id == "move_left":
                self.target_index = (self.target_index - 1) % len(chars)
            elif input_id == "move_down" or input_id == "move_right":
                self.target_index = (self.target_index + 1) % len(chars)
            elif input_id == "confirm" or input_id == "enter":
                target = chars[self.target_index]
                settings.SOUNDS["powerup"].stop()
                settings.SOUNDS["powerup"].play()
                amount = self.active_action["func"](self.character, target, self.active_action.get("strength", 1))

                if hasattr(target, 'energy_bar') and target.energy_bar:
                    target.energy_bar.value = target.current_hp
            
                self.message = f"{self.character.name} healed {target.name} for {amount} HP"
                self.message_timer = 2.0
                self.selecting_target = False
                self.active_action = None

            elif input_id == "status" or input_id == "quit":
                self.selecting_target = False
                self.active_action = None
            return

        if input_id == "status" or input_id == "quit":
            self.state_machine.pop()
            return

        actions = self.character.actions
        if input_id == "move_up":
            self.selected_action_index = (self.selected_action_index - 1) % (len(actions) + 1)
        elif input_id == "move_down":
            self.selected_action_index = (self.selected_action_index + 1) % (len(actions) + 1)
        elif input_id == "confirm" or input_id == "enter":
            settings.SOUNDS["blip"].stop()
            settings.SOUNDS["blip"].play()

            if self.selected_action_index == len(actions):
                self.state_machine.pop()
            else:
                action = actions[self.selected_action_index]
                is_heal = action.get("target_type") == "character"

                if is_heal:
                    self.active_action = action
                    if action.get("require_target", True):
                        self.selecting_target = True
                        self.target_index = 0
                    else:
                        settings.SOUNDS["powerup"].stop()
                        settings.SOUNDS["powerup"].play()
                        living_chars = [c for c in self.party.characters.values() if not c.dead]
                        if living_chars:
                            amount = action["func"](self.character, living_chars, action.get("strength", 1))
                            for target in living_chars:
                                if hasattr(target, 'energy_bar') and target.energy_bar:
                                    target.energy_bar.value = target.current_hp
                            self.message = f"{self.character.name} used {action['name']} (global) for {amount} HP each"
                            self.message_timer = 2.0
               

    def update(self, dt: float) -> None:
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = None

    def render(self, surface: pygame.Surface) -> None: 
        overlay = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        self.panel_left.render(surface)
        self.panel_right.render(surface)

        x_left = self.panel_left.x + 10
        y = self.panel_left.y + 8

        status_text = "Alive" if not self.character.dead else "Dead"
        line = f"Name: {self.character.name} - {status_text}"
        text = self.font_small.render(line, True, (255, 255, 255))
        surface.blit(text, (x_left, y))
        y += 18

        line = f"Level: {self.character.level}"
        text = self.font_small.render(line, True, (255, 255, 255))
        surface.blit(text, (x_left, y))
        y += 18

        exp_str = f"EXP: {int(self.character.current_exp)} / {int(self.character.exp_to_level)}"
        text = self.font_small.render(exp_str, True, (255, 255, 255))
        surface.blit(text, (x_left, y))
        y += 18

        hp_str = f"HP: {int(self.character.current_hp)} / {int(self.character.hp)}"
        text = self.font_small.render(hp_str, True, (255, 255, 255))
        surface.blit(text, (x_left, y))
        y += 18

        rest = getattr(self.character, 'rest_time', 0)
        text = self.font_small.render(f"Rest Time: {rest}", True, (255, 255, 255))
        surface.blit(text, (x_left, y))
        y += 18

        text = self.font_small.render(f"Attack: {int(self.character.attack)}", True, (255, 255, 255))
        surface.blit(text, (x_left, y))
        y += 18

        text = self.font_small.render(f"Defense: {int(self.character.defense)}", True, (255, 255, 255))
        surface.blit(text, (x_left, y))
        y += 18

        text = self.font_small.render(f"Magic: {int(self.character.magic)}", True, (255, 255, 255))
        surface.blit(text, (x_left, y))

        x_right = self.panel_right.x + 12
        y_right = self.panel_right.y + 8

        actions = self.character.actions
        for i, action in enumerate(actions):
            action_name = action["name"]
            is_heal = action.get("target_type") == "character"
            alpha = 255 if is_heal else 100

            text_surf = self.font_small.render(action_name, True, (255, 255, 255))
            text_surf.set_alpha(alpha)
            surface.blit(text_surf, (x_right + 10, y_right))

            if i == self.selected_action_index and not self.selecting_target:
                cursor = settings.TEXTURES["cursor-right"]
                cursor_rect = cursor.get_rect(midleft=(x_right, y_right + 6))
                surface.blit(cursor, cursor_rect)

            y_right += 20

        close_surf = self.font_small.render("Close", True, (255, 255, 255))
        surface.blit(close_surf, (x_right + 10, y_right))
        if self.selected_action_index == len(actions) and not self.selecting_target:
            cursor = settings.TEXTURES["cursor-right"]
            cursor_rect = cursor.get_rect(midleft=(x_right, y_right + 6))
            surface.blit(cursor, cursor_rect)

        if self.selecting_target:
            chars = [c for c in self.party.characters.values() if not c.dead]
            if chars:
                target = chars[self.target_index]
            
                msg = f"Select target: {target.name}"
                text = self.font_small.render(msg, True, (255, 255, 0))
                rect = text.get_rect(center=(settings.VIRTUAL_WIDTH/2, settings.VIRTUAL_HEIGHT - 30))
                surface.blit(text, rect)

        if self.message:
            msg_surf = self.font_small.render(self.message, True, (255, 255, 0))
            msg_rect = msg_surf.get_rect(center=(settings.VIRTUAL_WIDTH/2, settings.VIRTUAL_HEIGHT - 60))
            surface.blit(msg_surf, msg_rect)




        
        