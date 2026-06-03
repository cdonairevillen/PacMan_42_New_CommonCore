from enum import Enum
from maze.maze import Maze
from player.player import Player, PlayerState
from typing import Optional
from consumibles.pac_gum import Pacgum, SuperPacgum
from enemies.enemy_base import Enemy, EnemyState
from enemies.enemy_red import EnemyRed
from enemies.enemy_pink import EnemyPink
from enemies.enemy_blue import EnemyBlue
from enemies.enemy_orange import EnemyOrange
from leaderboard import Leaderboard
from cheat_mode import CheatMode


class State(Enum):
    MENU = "menu"
    LEADERBOARD = "leaderboard"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "gameover"
    VICTORY = "victory"
    LOADING = "loading"
    READY = "ready"
    INSTRUCTIONS = "instructions"


class GameManager():

    def __init__(self, config: dict) -> None:

        self.config = config
        self.leaderboard = Leaderboard(config["highscore_filename"])

        # Game info
        self.points_per_gum = config["points_per_pacgum"]
        self.points_per_supergum = config["points_per_super_pacgum"]
        self.points_per_ghost = config["points_per_ghost"]
        self.loading_timer: float = 0.0
        self.loading_duration: float = 2.0
        self.cell_size: int = 28

        # Game State
        self.state = State.MENU
        self.current_level: int = 0
        self.current_pacgums: list[Pacgum] = []
        self.enemies: list[Enemy] = []
        self.current_maze: Optional[Maze] = None
        self.large_map_warning_shown = False
        self.build_level(seed=config["seed"])

        # Game Conditions
        self.level_max_time = config["level_max_time"]
        self.time_remining = self.level_max_time
        self.move_timer: float = 0.0

        # Player info
        self.player = Player(x=self.current_maze.center[0],
                             y=self.current_maze.center[1],
                             lives=config["lives"], speed=5,
                             cell_size=self.cell_size)
        
        self.cheat_mode = CheatMode()

        self.score = 0

    # Level Management

    def build_level(self, seed: int) -> None:

        level = self.config["levels"][self.current_level]
        width = level["width"]
        height = level["height"]

        print(
            "LEVEL:",
            self.current_level,
            "SIZE:",
            width,
            "x",
            height
        )

        if (
            not self.large_map_warning_shown
            and (width > 20 or height > 20)
        ):
            print(
                "\nMaps larger than 20x20 have been detected."
            )
            answer = input(
                "Do you wish to continue with those sizes? (y/n):"
            ).strip().lower()
            self.large_map_warning_shown = True
            if answer != "s":
                print(
                    "\n19x19 will be used for all large levels."
                )
                for level_cfg in self.config["levels"]:
                    if (
                        level_cfg["width"] > 20
                        or level_cfg["height"] > 20
                    ):
                        level_cfg["width"] = 19
                        level_cfg["height"] = 19
                width = 19
                height = 19

        if self.current_level == 0:
            self.current_maze = Maze.build(
                width=self.config["levels"][self.current_level]["width"],
                height=self.config["levels"][self.current_level]["height"],
                seed=42)

        elif self.config["seed"] == 0 or self.config["seed"] is None:
            self.current_maze = Maze.build(
                width=self.config["levels"][self.current_level]["width"],
                height=self.config["levels"][self.current_level]["height"],
                seed=0)

        else:
            self.current_maze = Maze.build(
                width=self.config["levels"][self.current_level]["width"],
                height=self.config["levels"][self.current_level]["height"],
                seed=self.config["seed"])

        corners = set(self.current_maze.get_corner_cells())
        center = self.current_maze.center
        self.current_pacgums = []
        self.enemies = []

        corners = list(self.current_maze.get_corner_cells())

        self.enemies = [
            EnemyRed(corners[0][0], corners[0][1], speed=3.8,
                     cell_size=self.cell_size),
            EnemyPink(corners[1][0], corners[1][1], speed=3.5,
                      cell_size=self.cell_size),
            EnemyBlue(corners[2][0], corners[2][1], speed=3.2,
                      cell_size=self.cell_size),
            EnemyOrange(corners[3][0], corners[3][1], speed=2.8,
                        cell_size=self.cell_size),
        ]

        for x, y in self.current_maze.get_walkable_cells():

            if (x, y) == center:
                continue

            elif (x, y) in corners:
                self.current_pacgums.append(
                    SuperPacgum(x=x, y=y, points=self.points_per_supergum))

            else:
                self.current_pacgums.append(
                    Pacgum(x=x, y=y, points=self.points_per_gum))

    def reset(self):

        self.score = 0
        self.current_level = 0
        self.time_remining = self.level_max_time
        self.build_level(seed=self.config["seed"])
        self.player.respawn(self.current_maze)
        self.player.lives = self.config["lives"]

    def next_level(self) -> bool:
        """
        Advance to the next level or trigger victory.
        """

        self.current_level += 1
        if self.current_level >= len(self.config["levels"]):
            self.state = State.VICTORY
            return False

        self.build_level(
            seed=self.config["seed"]
        )
        self.player.respawn(
            self.current_maze
        )
        self.time_remining = (
            self.level_max_time
        )
        self.state = State.PLAYING

        return True

    # State Management

    def pause(self):

        if self.state == State.PLAYING:
            self.state = State.PAUSED

    def resume(self):

        if self.state in (State.PAUSED, State.READY):
            self.state = State.PLAYING

    def victory(self):

        self.state = State.VICTORY

    def game_over(self):

        self.state = State.GAME_OVER

    def ready(self):

        self.state = State.READY

    def update(self, dt: float) -> None:
        """
        Advance game logic by one frame.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        if self.state == State.LOADING:
            self.loading_timer += dt
            if self.loading_timer >= self.loading_duration:
                self.player.respawn(self.current_maze)
                self.reset_enemy_positions()
                self.state = State.READY
            return

        if self.state != State.PLAYING:
            return

        if not self.cheat_mode.enabled:
            self.time_remining -= dt

        self.move_timer += dt

        if self.move_timer >= 1.0 / self.player.speed:
            self.player.move(self.current_maze, self.cheat_mode)
            self.move_timer -= 1.0 / self.player.speed

        self.player.update_visual(dt)

        if self.player.state == PlayerState.POWER_UP:
            self.player.power_timer -= dt
            if self.player.power_timer <= 0:
                self.player.state = PlayerState.NORMAL
                for enemy in self.enemies:
                    if enemy.state == EnemyState.FEAR:
                        enemy.state = EnemyState.NORMAL

        player_pos = self.player.get_position()

        for pacgum in self.current_pacgums:
            if not pacgum.eaten and (pacgum.x, pacgum.y) == player_pos:
                self.eat_packgum(pacgum)
                break

        for enemy in self.enemies:
            if enemy.state == EnemyState.INV:
                enemy.respawn_timer -= dt
                if enemy.respawn_timer <= 0:
                    if self.player.state == PlayerState.POWER_UP:
                        enemy.state = EnemyState.FEAR
                    else:
                        enemy.state = EnemyState.NORMAL

            enemy.move_timer += dt

            if enemy.move_timer >= 1.0 / enemy.speed:
                if isinstance(enemy, EnemyOrange):
                    enemy.choose_direction(self.current_maze)
                else:
                    enemy.choose_direction(self.player, self.current_maze)
                enemy.move(self.current_maze)
                enemy.move_timer -= 1.0 / enemy.speed

            enemy.update_visual(dt)

            enemy_pos = enemy.get_position()
            if enemy_pos == player_pos:
                if self.cheat_mode.invincible:
                    continue
                if enemy.state == EnemyState.INV:
                    continue
                if enemy.state == EnemyState.FEAR:
                    self.eat_ghost(enemy)
                else:
                    self.check_life()

            if self.time_remining <= 0:
                self.game_over()

    # Player Management

    def reset_enemy_positions(self) -> None:

        corners = self.current_maze.get_corner_cells()

        if len(corners) < 4:
            return

        self.enemies[0].x, self.enemies[0].y = corners[0]
        self.enemies[1].x, self.enemies[1].y = corners[1]
        self.enemies[2].x, self.enemies[2].y = corners[2]
        self.enemies[3].x, self.enemies[3].y = corners[3]

        for enemy in self.enemies:
            enemy.direction_x = 0
            enemy.direction_y = 0
            enemy.state = EnemyState.NORMAL
            enemy.px = float(enemy.x * enemy.cell_size)
            enemy.py = float(enemy.y * enemy.cell_size)
            enemy.target_px = enemy.px
            enemy.target_py = enemy.py

    def check_life(self) -> None:
        """
        Deduct a life and trigger loading or game over accordingly.

        Respawns the player and resets enemies after losing a life,
        then enters LOADING state before showing the READY screen.
        """
        self.player.lose_life()

        if self.player.lives <= 0:
            self.game_over()
            return

        self.state = State.LOADING
        self.loading_timer = 0.0

    def eat_packgum(self, pacgum):

        self.score += pacgum.consumed(self.player)
        if isinstance(pacgum, SuperPacgum):
            for enemy in self.enemies:
                enemy.state = EnemyState.FEAR
        if not any(not p.eaten for p in self.current_pacgums):
            self.next_level()

    def eat_ghost(self, enemy):

        self.score += self.points_per_ghost
        enemy.state = EnemyState.INV
        enemy.respawn_timer = 1
        enemy.x = enemy.spawn_x
        enemy.y = enemy.spawn_y
        enemy.px = float(enemy.x * enemy.cell_size)
        enemy.py = float(enemy.y * enemy.cell_size)
        enemy.target_px = enemy.px
        enemy.target_py = enemy.py
        enemy.direction_x = 0
        enemy.direction_y = 0

    def toggle_cheat_mode(self):
        self.cheat_mode.toggle()

        if self.cheat_mode.enabled:

            # Invencibilidad
            self.cheat_mode.invincible = True

            # Devilitar fanatsmas
            self.cheat_mode.freeze_ghosts = True

            # Velocidad x2
            self.player.speed = (
                self.player.normal_speed * 2
            )

            self.player.pixels_per_second = (
                self.player.speed * self.player.cell_size
            )

        else:

            self.cheat_mode.invincible = False

            self.cheat_mode.freeze_ghosts = False

            self.player.speed = (
                self.player.normal_speed
            )

            self.player.pixels_per_second = (
                self.player.speed * self.player.cell_size
            )

            print("Cheat mode disabled")

    def skip_level(self) -> None:
        """
        Pasa al siguiente nivel si el cheat mode está activo.
        """

        if not self.cheat_mode.enabled:
            return

        print("Level skipped")

        self.next_level()
