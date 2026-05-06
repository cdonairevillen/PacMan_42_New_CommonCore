import random
import sys
import pygame
from maze.maze import Maze
from visualizer.colors import Color


WALL_THICKNESS: int = 3
CELL_SIZE_DEFAULT: int = 28
MIN_CELL_SIZE: int = 12
MAX_CELL_SIZE: int = 56
MARGIN: int = 40


class MazeVisualizer:

    def __init__(
        self,
        maze: Maze,
        cell_size: int = CELL_SIZE_DEFAULT,
        title: str = "Pac-Man - Maze Visualizer",
    ) -> None:
        self.maze: Maze = maze
        self.cell_size: int = cell_size
        self.title: str = title
        self.show_info: bool = True

        self.screen: pygame.Surface
        self.clock: pygame.time.Clock
        self.font_small: pygame.font.Font
        self.font_dim: pygame.font.Font
        self.running: bool = False

    def run(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("monospace", 14)
        self.font_dim = pygame.font.SysFont("monospace", 14)
        self.resize_window()
        pygame.display.set_caption(self.title)

        self.running = True
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit(0)

    def update_maze(self, maze: Maze) -> None:
        self.maze = maze
        self.resize_window()

    def resize_window(self) -> None:
        w = self.maze.width * self.cell_size + MARGIN * 2
        h = self.maze.height * self.cell_size + MARGIN * 2 + 60
        self.screen = pygame.display.set_mode((w, h))

    def cell_rect(self, x: int, y: int) -> pygame.Rect:
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

                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info

                elif event.key in (
                    pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS
                ):
                    self.cell_size = min(self.cell_size + 4, MAX_CELL_SIZE)
                    self.resize_window()

                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self.cell_size = max(self.cell_size - 4, MIN_CELL_SIZE)
                    self.resize_window()

                elif event.key == pygame.K_r:
                    new_seed = random.randint(1, 99_999)
                    self.update_maze(
                        Maze.build(
                            width=self.maze.width,
                            height=self.maze.height,
                            seed=new_seed,
                        )
                    )

    def draw(self) -> None:
        self.screen.fill(Color.BG.rgb())
        self.draw_cell_backgrounds()
        self.draw_pacgum_dots()
        self.draw_special_markers()
        self.draw_walls()
        pygame.display.flip()

    def draw_cell_backgrounds(self) -> None:
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.cells[y][x]
                color = Color.BLOCKED if cell.is_blocked else Color.FLOOR
                pygame.draw.rect(self.screen, color.rgb(), self.cell_rect(x, y))

    def draw_pacgum_dots(self) -> None:
        special = {
            self.maze.entry,
            self.maze.exit,
            self.maze.center,
            *self.maze.get_corner_cells(),
        }
        dot_r = max(2, self.cell_size // 10)
        for x, y in self.maze.get_walkable_cells():
            if (x, y) not in special:
                rect = self.cell_rect(x, y)
                pygame.draw.circle(
                    self.screen, Color.PACGUM.rgb(), rect.center, dot_r
                )

    def draw_special_markers(self) -> None:
        markers: list[tuple[int, int, Color]] = [
            (*self.maze.entry, Color.ENTRY),
            (*self.maze.exit, Color.EXIT),
            (*self.maze.center, Color.PLAYER_SPAWN),
        ]
        for gx, gy in self.maze.get_corner_cells():
            markers.append((gx, gy, Color.GHOST_CORNER))

        for mx, my, color in markers:
            rect = self.cell_rect(mx, my)
            r = max(4, self.cell_size // 4)
            pygame.draw.circle(self.screen, color.rgb(), rect.center, r)

    def draw_walls(self) -> None:
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.cells[y][x]
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

    def draw_wall_segment(self, start: tuple[int, int],
                          end: tuple[int, int],) -> None:
        pygame.draw.line(
            self.screen, Color.WALL.rgb(), start, end, WALL_THICKNESS
        )
        pygame.draw.line(
            self.screen, Color.WALL_GLOW.rgb(), start, end, 1
        )
