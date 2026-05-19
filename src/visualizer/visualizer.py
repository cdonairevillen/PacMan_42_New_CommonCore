from __future__ import annotations

import sys

import pygame

from visualizer.colors import Color
from game_manager import GameManager, State


WALL_THICKNESS: int = 3
CELL_SIZE_DEFAULT: int = 28
MIN_CELL_SIZE: int = 12
MAX_CELL_SIZE: int = 56
MARGIN: int = 40


class MazeVisualizer:
    """
    Pygame renderer for the Pac-Man game.

    Receives a GameManager and reads its state every frame to render
    the maze, pacgums, player and enemies. Never modifies game state —
    only reads and draws.

    Attributes:
        game_manager: The active GameManager instance.
        cell_size: Pixel dimension of each cell square.
        title: Window caption string.
    """

    def __init__(self, game_manager: GameManager,
                 cell_size: int = CELL_SIZE_DEFAULT,
                 title: str = "Pac-Man") -> None:
        """
        Initialise the visualizer without starting pygame yet.

        Args:
            game_manager: The GameManager to read state from.
            cell_size: Initial pixel size per cell.
            title: Window title string.
        """
        self.game_manager: GameManager = game_manager
        self.cell_size: int = cell_size
        self.title: str = title

        self.screen: pygame.Surface
        self.clock: pygame.time.Clock
        self.font_small: pygame.font.Font
        self.running: bool = False

    def run(self) -> None:
        """Initialise pygame, open the window, and start the event loop."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("monospace", 14)
        self.resize_window()
        pygame.display.set_caption(self.title)

        self.running = True
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.game_manager.update(dt)
            self.draw()

        pygame.quit()
        sys.exit(0)

    def resize_window(self) -> None:
        """Recalculate and apply window dimensions for the current maze."""
        maze = self.game_manager.current_maze
        w = maze.width * self.cell_size + MARGIN * 2
        h = maze.height * self.cell_size + MARGIN * 2 + 60
        self.screen = pygame.display.set_mode((w, h))

    def cell_rect(self, x: int, y: int) -> pygame.Rect:
        """
        Return the pixel Rect for a given cell coordinate.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            pygame.Rect covering that cell on screen.
        """
        px = MARGIN + x * self.cell_size
        py = MARGIN + y * self.cell_size
        return pygame.Rect(px, py, self.cell_size, self.cell_size)

    def handle_events(self) -> None:
        """Process all pending pygame events for this frame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False

                elif event.key == pygame.K_p:
                    if self.game_manager.state == State.PLAYING:
                        self.game_manager.pause()
                    elif self.game_manager.state == State.PAUSED:
                        self.game_manager.resume()

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.game_manager.player.set_direction(0, -1)

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.game_manager.player.set_direction(0, 1)

                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.game_manager.player.set_direction(-1, 0)

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.game_manager.player.set_direction(1, 0)

    def draw(self) -> None:
        """Execute a full render pass for the current frame."""
        self.screen.fill(Color.BG.rgb())
        self.draw_cell_backgrounds()
        self.draw_pacgums()
        self.draw_walls()
        self.draw_player()
        self.draw_hud()
        pygame.display.flip()

    def draw_cell_backgrounds(self) -> None:
        """Fill each cell with its background colour (floor or blocked)."""
        maze = self.game_manager.current_maze
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.cells[y][x]
                color = Color.BLOCKED if cell.is_blocked else Color.FLOOR
                pygame.draw.rect(self.screen, color.rgb(), self.cell_rect(x, y))

    def draw_pacgums(self) -> None:
        """Draw all pacgums and superpacgums that have not been eaten yet."""
        from consumibles.pac_gum import SuperPacgum

        for pacgum in self.game_manager.current_pacgums:
            if pacgum.eaten:
                continue

            rect = self.cell_rect(pacgum.x, pacgum.y)

            if isinstance(pacgum, SuperPacgum):
                r = max(4, self.cell_size // 4)
                pygame.draw.circle(
                    self.screen, Color.SUPER_PACGUM.rgb(), rect.center, r
                )
            else:
                r = max(2, self.cell_size // 10)
                pygame.draw.circle(
                    self.screen, Color.PACGUM.rgb(), rect.center, r
                )

    def draw_walls(self) -> None:
        """Draw wall segments for every cell using bitmask flags."""
        maze = self.game_manager.current_maze
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.cells[y][x]
                rect = self.cell_rect(x, y)

                if cell.is_blocked:
                    pygame.draw.rect(
                        self.screen, Color.WALL.rgb(), rect, WALL_THICKNESS
                    )
                    continue

                if cell.wall_north:
                    self.draw_wall_segment(rect.topleft, rect.topright)
                if cell.wall_south:
                    self.draw_wall_segment(rect.bottomleft, rect.bottomright)
                if cell.wall_west:
                    self.draw_wall_segment(rect.topleft, rect.bottomleft)
                if cell.wall_east:
                    self.draw_wall_segment(rect.topright, rect.bottomright)

    def draw_wall_segment(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> None:
        """
        Draw a single wall segment with a one-pixel glow line.

        Args:
            start: Pixel coordinate of the segment start.
            end: Pixel coordinate of the segment end.
        """
        pygame.draw.line(
            self.screen, Color.WALL.rgb(), start, end, WALL_THICKNESS
        )
        pygame.draw.line(
            self.screen, Color.WALL_GLOW.rgb(), start, end, 1
        )

    def draw_player(self) -> None:
        """Draw the player as a circle at their current cell position."""
        px, py = self.game_manager.player.get_position()
        rect = self.cell_rect(px, py)
        r = max(4, self.cell_size // 3)
        pygame.draw.circle(
            self.screen, Color.PLAYER_SPAWN.rgb(), rect.center, r
        )

    def draw_hud(self) -> None:
        """Render the HUD bar below the maze with score, lives and time."""
        gm = self.game_manager
        maze = gm.current_maze
        y_base = MARGIN + maze.height * self.cell_size + 8

        lines: list[tuple[str, Color]] = [
            (
                f"Score: {gm.score}   "
                f"Lives: {gm.player.lives}   "
                f"Level: {gm.current_level + 1}   "
                f"Time: {max(0, int(gm.time_remining))}s   "
                f"State: {gm.state.value}",
                Color.TEXT,
            ),
            (
                "[ WASD / Arrows ] move   [ P ] pause   [ ESC ] quit",
                Color.TEXT_DIM,
            ),
        ]

        for i, (text, color) in enumerate(lines):
            surf = self.font_small.render(text, True, color.rgb())
            self.screen.blit(surf, (MARGIN, y_base + i * 18))