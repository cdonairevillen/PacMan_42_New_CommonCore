from __future__ import annotations
import sys
import pygame
from visualizer.colors import Color
from game_manager import GameManager
from ui_manager import UIManager


WALL_THICKNESS: int = 3
CELL_SIZE_DEFAULT: int = 28
MARGIN: int = 40
HUD_HEIGHT: int = 56


class MazeVisualizer:
    """
    Pygame renderer for the Pac-Man game.

    Owns the pygame window, the event loop, and sprite assets.
    All game-logic rendering is delegated to GameScreen (via
    UIManager); this class exposes draw_maze(), draw_entities(),
    and advance_animations() so GameScreen can call them directly.

    Attributes:
        game_manager: Shared game state.
        cell_size: Pixel dimension of each cell square.
        title: Window caption string.
    """

    def __init__(self, game_manager: GameManager,
                 cell_size: int = CELL_SIZE_DEFAULT,
                 title: str = "Pac-Man") -> None:
        """
        Initialise the visualizer without starting pygame yet.

        Args:
            game_manager: Shared game state.
            cell_size: Initial pixel size per cell.
            title: Window caption string.
        """
        self.game_manager: GameManager = game_manager
        self.cell_size: int = cell_size
        self.title: str = title

        self.screen: pygame.Surface
        self.clock: pygame.time.Clock
        self.running: bool = False

        self.enemy_sprites: dict = {}
        self.enemy_animation_frame: int = 0
        self.enemy_animation_timer: float = 0.0

        self.player_sprites: dict = {}
        self.player_animation_frame: int = 0
        self.player_animation_timer: float = 0.0

    def run(self) -> None:
        """Initialise pygame, open the window, and start the event loop."""
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/theme.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()
        self.resize_window()
        pygame.display.set_caption(self.title)
        self.load_sprites()

        self.ui_manager = UIManager(
            self.game_manager, self.screen, self
        )

        self.running = True
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.game_manager.update(dt)
            self.draw(dt)

        pygame.quit()
        sys.exit(0)

    def resize_window(self) -> None:
        """Recalculate and apply window dimensions for the current maze."""
        maze = self.game_manager.current_maze
        w = maze.width * self.cell_size + MARGIN * 2
        h = (
            maze.height * self.cell_size
            + MARGIN * 2
            + HUD_HEIGHT
        )
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

    def visual_rect(self, vx: float, vy: float) -> pygame.Rect:
        """
        Return the pixel Rect for interpolated visual coordinates.

        Args:
            vx: Interpolated column position (float).
            vy: Interpolated row position (float).

        Returns:
            pygame.Rect covering that position on screen.
        """
        px = int(MARGIN + vx * self.cell_size)
        py = int(MARGIN + vy * self.cell_size)
        return pygame.Rect(px, py, self.cell_size, self.cell_size)

    def handle_events(self) -> None:
        """Process all pending pygame events for this frame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            self.ui_manager.handle_event(event)

    def draw(self, dt: float) -> None:
        """
        Execute a full render pass for the current frame.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        maze = self.game_manager.current_maze

        if (
            maze.width * self.cell_size + MARGIN * 2
            != self.screen.get_width()
        ):
            self.resize_window()
            self.ui_manager.surface = self.screen

        self.screen.fill(Color.BG.rgb())
        self.ui_manager.update(dt)
        self.ui_manager.draw()
        pygame.display.flip()

    def advance_animations(self) -> None:
        """Advance player and enemy animation frame counters."""
        self.player_animation_timer += 1 / 60
        if self.player_animation_timer >= 0.1:
            self.player_animation_frame = (
                self.player_animation_frame + 1
            ) % 3
            self.player_animation_timer = 0.0

        self.enemy_animation_timer += 1 / 60
        if self.enemy_animation_timer >= 0.15:
            self.enemy_animation_frame = (
                self.enemy_animation_frame + 1
            ) % 2
            self.enemy_animation_timer = 0.0

    def draw_maze(self) -> None:
        """Draw cell backgrounds, pac-gums, and walls."""
        self.draw_cell_backgrounds()
        self.draw_pacgums()
        self.draw_walls()

    def draw_entities(self) -> None:
        """Draw enemies then the player on top."""
        self.draw_enemies()
        self.draw_player()

    def draw_cell_backgrounds(self) -> None:
        """Fill each cell with its background colour."""
        maze = self.game_manager.current_maze
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.cells[y][x]
                color = (
                    Color.BLOCKED if cell.is_blocked else Color.FLOOR
                )
                pygame.draw.rect(
                    self.screen, color.rgb(), self.cell_rect(x, y)
                )

    def draw_pacgums(self) -> None:
        """Draw all uneaten pac-gums and super pac-gums."""
        from consumibles.pac_gum import SuperPacgum

        for pacgum in self.game_manager.current_pacgums:
            if pacgum.eaten:
                continue

            rect = self.cell_rect(pacgum.x, pacgum.y)

            if isinstance(pacgum, SuperPacgum):
                r = max(4, self.cell_size // 4)
                pygame.draw.circle(
                    self.screen,
                    Color.SUPER_PACGUM.rgb(),
                    rect.center,
                    r,
                )
            else:
                r = max(2, self.cell_size // 10)
                pygame.draw.circle(
                    self.screen,
                    Color.PACGUM.rgb(),
                    rect.center,
                    r,
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
                        self.screen,
                        Color.WALL.rgb(),
                        rect,
                        WALL_THICKNESS,
                    )
                    continue

                if cell.wall_north:
                    self.draw_wall_segment(
                        rect.topleft, rect.topright
                    )
                if cell.wall_south:
                    self.draw_wall_segment(
                        rect.bottomleft, rect.bottomright
                    )
                if cell.wall_west:
                    self.draw_wall_segment(
                        rect.topleft, rect.bottomleft
                    )
                if cell.wall_east:
                    self.draw_wall_segment(
                        rect.topright, rect.bottomright
                    )

    def draw_wall_segment(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> None:
        """
        Draw a wall segment with a one-pixel glow line.

        Args:
            start: Pixel start coordinate.
            end: Pixel end coordinate.
        """
        pygame.draw.line(
            self.screen, Color.WALL.rgb(), start, end, WALL_THICKNESS
        )
        pygame.draw.line(
            self.screen, Color.WALL_GLOW.rgb(), start, end, 1
        )

    def draw_player(self) -> None:
        """Draw the player sprite using pixel visual position."""
        player = self.game_manager.player
        px, py = player.get_visual_pos()
        x = int(MARGIN + px)
        y = int(MARGIN + py)
        sprite = self.player_sprites[
            player.last_direction
        ][self.player_animation_frame]
        self.screen.blit(sprite, (x, y))

    def draw_enemies(self) -> None:
        """Draw each enemy sprite using interpolated visual position."""
        from enemies.enemy_base import EnemyState
        from enemies.enemy_red import EnemyRed
        from enemies.enemy_pink import EnemyPink
        from enemies.enemy_blue import EnemyBlue
        from enemies.enemy_orange import EnemyOrange

        for enemy in self.game_manager.enemies:
            epx, epy = enemy.get_visual_pos()
            ex = int(MARGIN + epx)
            ey = int(MARGIN + epy)

            if enemy.direction_x == 1:
                direction = "right"
            elif enemy.direction_x == -1:
                direction = "left"
            elif enemy.direction_y == -1:
                direction = "up"
            else:
                direction = "down"

            if enemy.state == EnemyState.FEAR:
                sprite = self.enemy_sprites["fear"][
                    self.enemy_animation_frame
                ]
            elif isinstance(enemy, EnemyRed):
                sprite = self.enemy_sprites["red"][direction][
                    self.enemy_animation_frame
                ]
            elif isinstance(enemy, EnemyPink):
                sprite = self.enemy_sprites["pink"][direction][
                    self.enemy_animation_frame
                ]
            elif isinstance(enemy, EnemyBlue):
                sprite = self.enemy_sprites["blue"][direction][
                    self.enemy_animation_frame
                ]
            elif isinstance(enemy, EnemyOrange):
                sprite = self.enemy_sprites["orange"][direction][
                    self.enemy_animation_frame
                ]
            else:
                continue

            self.screen.blit(sprite, (ex, ey))

    def load_sprites(self) -> None:
        """Load and scale all enemy and player sprite sheets."""
        size = (self.cell_size, self.cell_size)

        def scaled(path: str) -> pygame.Surface:
            return pygame.transform.scale(
                pygame.image.load(path).convert_alpha(), size
            )

        self.enemy_sprites = {
            "red": {
                d: [scaled(f"assets/ghosts/red/red_{d}_1.png"),
                    scaled(f"assets/ghosts/red/red_{d}_2.png")]
                for d in ("right", "left", "up", "down")
            },
            "pink": {
                d: [scaled(f"assets/ghosts/pink/pink_{d}_1.png"),
                    scaled(f"assets/ghosts/pink/pink_{d}_2.png")]
                for d in ("right", "left", "up", "down")
            },
            "blue": {
                d: [scaled(f"assets/ghosts/blue/blue_{d}_1.png"),
                    scaled(f"assets/ghosts/blue/blue_{d}_2.png")]
                for d in ("right", "left", "up", "down")
            },
            "orange": {
                d: [scaled(f"assets/ghosts/orange/orange_{d}_1.png"),
                    scaled(f"assets/ghosts/orange/orange_{d}_2.png")]
                for d in ("right", "left", "up", "down")
            },
            "fear": [
                scaled("assets/ghosts/fear/fear_1.png"),
                scaled("assets/ghosts/fear/fear_2.png"),
            ],
        }

        self.player_sprites = {
            d: [
                scaled(f"assets/player/pacman_{d}_1.png"),
                scaled(f"assets/player/pacman_{d}_2.png"),
                scaled(f"assets/player/pacman_{d}_3.png"),
            ]
            for d in ("right", "left", "up", "down")
        }
