"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List, Optional, Tuple

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

from src.Tile import Tile

import settings


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        self.dragging = False
        self.dragged_tile = None
        self.start_i = -1
        self.start_j = -1
        self.start_x = -1
        self.start_y = -1

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

        if self.active and self.dragging and self.dragged_tile:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x = mouse_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            mouse_y = mouse_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            self.dragged_tile.x = (mouse_x - self.board.x) - settings.TILE_SIZE // 2
            self.dragged_tile.y = (mouse_y - self.board.y) - settings.TILE_SIZE // 2

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        if self.dragging and self.dragged_tile:
            self.dragged_tile.render(surface, self.board.x, self.board.y)

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        if input_id == "click":
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            if input_data.pressed:
                i = (pos_y - self.board.y) // settings.TILE_SIZE
                j = (pos_x - self.board.x) // settings.TILE_SIZE

                if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH and self.board.tiles[i][j] is not None:
                    clicked_tile = self.board.tiles[i][j]

                    if clicked_tile.power_up is not None:
                        self.active = False
                        self.board.matches = [[clicked_tile]]
                        self._calculate_matches([clicked_tile])
                        return

                    self.dragging = True
                    self.start_i = i
                    self.start_j = j
                    self.dragged_tile = self.board.tiles[i][j]
                    self.start_x = self.dragged_tile.x
                    self.start_y = self.dragged_tile.y

            elif not input_data.pressed and self.dragging:
                self.dragging = False

                target_i = (pos_y - self.board.y) // settings.TILE_SIZE
                target_j = (pos_x - self.board.x) // settings.TILE_SIZE

                if 0 <= target_i < settings.BOARD_HEIGHT and 0 <= target_j < settings.BOARD_WIDTH:
                    di = abs(target_i - self.start_i)
                    dj = abs(target_j - self.start_j)

                    if di <= 1 and dj <= 1 and di != dj:
                        self.active = False
                        tile1 = self.dragged_tile
                        tile2 = self.board.tiles[target_i][target_j]

                        target_x1 = target_j * settings.TILE_SIZE
                        target_y1 = target_i * settings.TILE_SIZE
                        target_x2 = self.start_x
                        target_y2 = self.start_y


                        def arrive():
                            (
                                self.board.tiles[self.start_i][self.start_j],
                                self.board.tiles[target_i][target_j],
                            ) = (
                                self.board.tiles[target_i][target_j],
                                self.board.tiles[self.start_i][self.start_j],
                            )
                            tile1.i, tile1.j, tile2.i, tile2.j = (
                                target_i,
                                target_j,
                                self.start_i,
                                self.start_j,
                            )
                            self._calculate_matches([tile1, tile2], swapped_tiles=(tile1, tile2), spawn_pos=(target_i, target_j))

                        # Swap tiles
                        Timer.tween(
                            0.25,
                            [
                                (tile1, {"x": target_x1, "y": target_y1}),
                                (tile2, {"x": target_x2, "y": target_y2}),
                            ],
                            on_finish=arrive,
                        )

                        self.dragged_tile = None
                        return

                Timer.tween(
                    0.15,
                    [(self.dragged_tile, {"x": self.start_x, "y": self.start_y})]

                )
                self.dragged_tile = None

    def _calculate_matches(self, tiles: List, swapped_tiles: Optional[Tuple[Tile, Tile]] = None, spawn_pos :  Optional[Tuple[int, int]] = None) -> None:
        matches = self.board.calculate_matches_for(tiles)

        if matches is None:
            if swapped_tiles is not None:
                tile1, tile2 = swapped_tiles

                settings.SOUNDS["error"].stop()
                settings.SOUNDS["error"].play()

                def revert_logic():
                    (
                        self.board.tiles[tile1.i][tile1.j],
                        self.board.tiles[tile2.i][tile2.j],
                    ) = (
                        self.board.tiles[tile2.i][tile2.j],
                        self.board.tiles[tile1.i][tile1.j],
                    )
                    tile1.i, tile1.j, tile2.i, tile2.j = (
                        tile2.i,
                        tile2.j,
                        tile1.i,
                        tile1.j,
                    )

                    self.active = True
                Timer.tween(
                    0.25,
                    [
                        (tile1, {"x": tile2.x, "y":tile2.y}),
                        (tile2, {"x": tile1.x, "y": tile1.y}),
                    ],
                    on_finish=revert_logic,
                ) 
                return
            else:
                self.active = True

                has_powerup = any(
                    tile is not None and tile.power_up is not None
                    for row in self.board.tiles
                    for tile in row
                )

                if not self.board.has_possible_matches() and not has_powerup:
                    self.board.recreate_board()
                return
            
        self.board.expand_powerup_matches()

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        for match in matches:
            self.score += len(match) * 50

        self.board.remove_matches(spawn_pos = spawn_pos)

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles],
                swapped_tiles=None,
                spawn_pos = None
            ),
        )
