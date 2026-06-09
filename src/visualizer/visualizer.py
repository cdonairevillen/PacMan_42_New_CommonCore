from __future__ import annotations
import sys
import pygame
from visualizer.colors import Color
from visualizer.visual_config import VisualConfig
from game_manager import GameManager, State
from ui_manager import UIManager


class MazeVisualizer:

    def __init__(self, game_manager: GameManager,
                 cfg: VisualConfig = None,
                 title: str = "Pac-Man") -> None:
        self.game_manager: GameManager = game_manager
        self.cfg: VisualConfig = cfg if cfg is not None else VisualConfig()
        self.title: str = title

        self.window: pygame.Window
        self.screen: pygame.Surface
        self.base_surface: pygame.Surface
        self.clock: pygame.time.Clock
        self.running: bool = False
        self.is_fullscreen: bool = False
        self.resize_timer: float = 0.0
        self._pre_fullscreen_size: tuple[int, int] = (0, 0)
        self._pending_resize: int = 0

        self.enemy_sprites: dict = {}
        self.enemy_animation_frame: int = 0
        self.enemy_animation_timer: float = 0.0

        self.player_sprites: dict = {}
        self.player_animation_frame: int = 0
        self.player_animation_timer: float = 0.0

    @property
    def cell_size(self) -> int:
        return self.cfg.cell_size

    def base_size(self) -> tuple[int, int]:
        if self.game_manager.state in (State.PLAYING, State.LOADING):
            maze = self.game_manager.current_maze
            w = maze.width * self.cfg.cell_size + self.cfg.margin * 2
            h = (maze.height * self.cfg.cell_size
                 + self.cfg.margin * 2
                 + self.cfg.hud_height)
            return (w, h)
        return (self.cfg.menu_w, self.cfg.menu_h)

    def run(self) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/theme.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()

        bw, bh = self.base_size()
        self.base_surface = pygame.Surface((bw, bh))
        self.window = pygame.Window(self.title, size=(bw, bh))
        self.window.resizable = True
        self.screen = self.window.get_surface()
        self._pre_fullscreen_size = (bw, bh)

        self.load_sprites()

        self.ui_manager = UIManager(
            self.game_manager, self.base_surface, self
        )

        self.running = True
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.resize_timer = max(0.0, self.resize_timer - dt)
            self.handle_events()
            self.game_manager.update(dt)
            self.draw(dt)

        pygame.quit()
        sys.exit(0)

    def update_base_surface(self) -> None:
        bw, bh = self.base_size()
        if (self.base_surface.get_width() != bw
                or self.base_surface.get_height() != bh):
            self.base_surface = pygame.Surface((bw, bh))
            self.ui_manager.surface = self.base_surface

        for screen in self.ui_manager.screens.values():
            screen.screen = self.base_surface
            if hasattr(screen, "hud"):
                screen.hud.surface = self.base_surface

    def cell_rect(self, x: int, y: int) -> pygame.Rect:
        px = self.cfg.margin + x * self.cfg.cell_size
        py = self.cfg.margin + y * self.cfg.cell_size
        return pygame.Rect(px, py, self.cfg.cell_size, self.cfg.cell_size)

    def visual_rect(self, vx: float, vy: float) -> pygame.Rect:
        px = int(self.cfg.margin + vx * self.cfg.cell_size)
        py = int(self.cfg.margin + vy * self.cfg.cell_size)
        return pygame.Rect(px, py, self.cfg.cell_size, self.cfg.cell_size)

    def screen_to_base(self, pos: tuple[int, int]) -> tuple[int, int]:
        "Convert the real screen pixel position to the new proxy screen"

        sw, sh = self.screen.get_size()
        bw, bh = self.base_surface.get_size()
        scale = min(sw / bw, sh / bh)
        scaled_w = int(bw * scale)
        scaled_h = int(bh * scale)
        offset_x = (sw - scaled_w) // 2
        offset_y = (sh - scaled_h) // 2
        x = int((pos[0] - offset_x) / scale)
        y = int((pos[1] - offset_y) / scale)
        return (x, y)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.WINDOWRESIZED:
                if self.resize_timer <= 0:
                    self._pending_resize = 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_F11:
                    self.is_fullscreen = not self.is_fullscreen
                    self.resize_timer = 0.5
                    if self.is_fullscreen:
                        self._pre_fullscreen_size = self.window.size
                        self.window.set_fullscreen(True)
                        self.screen = self.window.get_surface()
                    else:
                        bw, bh = self._pre_fullscreen_size
                        self.window.destroy()
                        self.window = pygame.Window(
                            self.title, size=(bw, bh)
                        )
                        self.window.resizable = True
                        self.screen = self.window.get_surface()
                    self.ui_manager.surface = self.base_surface

            if event.type in (pygame.MOUSEMOTION,
                              pygame.MOUSEBUTTONDOWN,
                              pygame.MOUSEBUTTONUP):
                x, y = self.screen_to_base(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    event = pygame.event.Event(
                        pygame.MOUSEMOTION,
                        pos=(x, y),
                        rel=event.rel,
                        buttons=event.buttons)
                else:
                    event = pygame.event.Event(
                        event.type,
                        pos=(x, y),
                        button=event.button)

            self.ui_manager.handle_event(event)

    def draw(self, dt: float) -> None:
        self.update_base_surface()

        self.base_surface.fill(Color.BG.rgb())
        self.ui_manager.update(dt)
        self.ui_manager.draw()

        sw, sh = self.screen.get_size()
        bw, bh = self.base_surface.get_size()

        scale = min(sw / bw, sh / bh)
        scaled_w = int(bw * scale)
        scaled_h = int(bh * scale)
        offset_x = (sw - scaled_w) // 2
        offset_y = (sh - scaled_h) // 2

        self.screen.fill((0, 0, 0))
        scaled = pygame.transform.scale(
            self.base_surface, (scaled_w, scaled_h)
        )
        self.screen.blit(scaled, (offset_x, offset_y))
        self.window.flip()

        if self._pending_resize > 0:
            self._pending_resize -= 1
            if self._pending_resize == 0:
                self.screen = self.window.get_surface()

    def advance_animations(self) -> None:
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
        self.draw_cell_backgrounds()
        self.draw_pacgums()
        self.draw_walls()

    def draw_entities(self) -> None:
        self.draw_enemies()
        self.draw_player()

    def draw_cell_backgrounds(self) -> None:
        maze = self.game_manager.current_maze
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.cells[y][x]
                color = (
                    Color.BLOCKED if cell.is_blocked else Color.FLOOR
                )
                pygame.draw.rect(
                    self.base_surface, color.rgb(), self.cell_rect(x, y)
                )

    def draw_pacgums(self) -> None:
        from consumibles.pac_gum import SuperPacgum

        for pacgum in self.game_manager.current_pacgums:
            if pacgum.eaten:
                continue

            rect = self.cell_rect(pacgum.x, pacgum.y)

            if isinstance(pacgum, SuperPacgum):
                r = max(4, self.cfg.cell_size // 4)
                pygame.draw.circle(
                    self.base_surface,
                    Color.SUPER_PACGUM.rgb(),
                    rect.center,
                    r,
                )
            else:
                r = max(2, self.cfg.cell_size // 10)
                pygame.draw.circle(
                    self.base_surface,
                    Color.PACGUM.rgb(),
                    rect.center,
                    r,
                )

    def draw_walls(self) -> None:
        maze = self.game_manager.current_maze
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.cells[y][x]
                rect = self.cell_rect(x, y)

                if cell.is_blocked:
                    pygame.draw.rect(
                        self.base_surface,
                        Color.WALL.rgb(),
                        rect,
                        self.cfg.wall_thickness,
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
                          end: tuple[int, int]) -> None:
        pygame.draw.line(
            self.base_surface, Color.WALL.rgb(), start, end,
            self.cfg.wall_thickness
        )
        pygame.draw.line(
            self.base_surface, Color.WALL_GLOW.rgb(), start, end, 1
        )

    def draw_player(self) -> None:
        player = self.game_manager.player
        px, py = player.get_visual_pos()
        x = int(self.cfg.margin + px)
        y = int(self.cfg.margin + py)
        sprite = self.player_sprites[
            player.last_direction
        ][self.player_animation_frame]
        self.base_surface.blit(sprite, (x, y))

    def draw_enemies(self) -> None:
        from enemies.enemy_base import EnemyState
        from enemies.enemy_red import EnemyRed
        from enemies.enemy_pink import EnemyPink
        from enemies.enemy_blue import EnemyBlue
        from enemies.enemy_orange import EnemyOrange

        for enemy in self.game_manager.enemies:
            epx, epy = enemy.get_visual_pos()
            ex = int(self.cfg.margin + epx)
            ey = int(self.cfg.margin + epy)

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

            self.base_surface.blit(sprite, (ex, ey))

    def load_sprites(self) -> None:
        size = (self.cfg.cell_size, self.cfg.cell_size)

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