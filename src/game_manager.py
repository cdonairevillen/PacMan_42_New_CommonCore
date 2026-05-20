from enum import Enum
from maze.maze import Maze
from player.player import Player, PlayerState
from typing import Optional
from consumibles.pac_gum import Pacgum, SuperPacgum
from enemies.enemy_base import Enemy, EnemyState


class State(Enum):

    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "gameover"
    VICTORY = "victory"
    LOADING = "loading"


class GameManager():

    def __init__(self, config: dict) -> None:

        self.config = config

        # Game info
        self.points_per_gum = config["points_per_pacgum"]
        self.points_per_supergum = config["points_per_super_pacgum"]
        self.points_per_ghost = config["points_per_ghost"]

        # Game State
        self.state = State.PAUSED
        self.current_level: int = 0
        self.current_pacgums: list[Pacgum] = []
        self.enemies: list[Enemy] = []
        self.current_maze: Optional[Maze] = None
        self.build_level(seed=config["seed"])

        # Game Conditions
        self.level_max_time = config["level_max_time"]
        self.time_remining = self.level_max_time
        self.move_timer: float = 0.0

        # Player info
        self.player = Player(x=self.current_maze.center[0],
                             y=self.current_maze.center[1],
                             lives=config["lives"], speed=10)

        self.score = 0

    # Level Management

    def build_level(self, seed: int) -> None:

        if self.current_level == 0:
            self.current_maze = Maze.build(
                width=self.config["levels"][self.current_level]["width"],
                height=self.config["levels"][self.current_level]["height"],
                seed=42)

        else:

            self.current_maze = Maze.build(
                width=self.config["levels"][self.current_level]["width"],
                height=self.config["levels"][self.current_level]["height"],
                seed=0)

        corners = set(self.current_maze.get_corner_cells())
        center = self.current_maze.center
        self.current_pacgums = []

        for x, y in self.current_maze.get_walkable_cells():

            if (x, y) == center:
                continue

            elif (x, y) in corners:
                self.current_pacgums.append(
                    SuperPacgum(x=x, y=y, points=self.points_per_supergum))

            else:
                self.current_pacgums.append(
                    Pacgum(x=x, y=y, points=self.points_per_gum))

    def next_level(self):

        self.current_level += 1

        if self.current_level >= len(self.config["levels"]):
            self.state = State.VICTORY

            return False

        else:
            self.state = State.LOADING
            self.build_level(seed=0)
            self.time_remining = self.level_max_time

            return True

    # State Management

    def pause(self):

        if self.state == State.PLAYING:
            self.state = State.PAUSED

    def resume(self):

        if self.state == State.PAUSED:
            self.state = State.PLAYING

    def victory(self):

        self.state = State.VICTORY

    def game_over(self):
        self.state = State.GAME_OVER

    def update(self, dt):

        if self.state == State.PLAYING:
            self.time_remining -= dt
            self.move_timer += dt
            player_pos = self.player.get_position()
            if self.move_timer >= 1.0 / self.player.speed: # El parametro de speed iria aqui en caso de que lo hicisesemos
                self.player.move(self.current_maze)
                self.move_timer = 0

            for pacgum in self.current_pacgums:
                if not pacgum.eaten and (pacgum.x, pacgum.y) == player_pos:
                    self.eat_packgum(pacgum)
                    break

            for enemy in self.enemies:
                enemy_pos = enemy.get_position()
                if enemy_pos == player_pos:
                    if enemy.state == EnemyState.FEAR:
                        continue

                    elif (enemy.state == EnemyState.FEAR
                          and self.player.state == PlayerState.POWER_UP):
                        self.eat_ghost(enemy)

                    elif (enemy.state == EnemyState.NORMAL
                          and self.player.state == PlayerState.NORMAL):
                        self.player.lose_life()

            if self.time_remining <= 0:
                self.game_over()

    # Player Management

    def check_life(self):

        self.player.lose_life()

        if self.player.lives <= 0:
            self.game_over()

    def eat_packgum(self, pacgum):

        self.score += pacgum.consumed(self.player)

        if not any(not p.eaten for p in self.current_pacgums):
            self.next_level()

    def eat_ghost(self, enemy):

        self.score += self.points_per_ghost
        enemy.state = EnemyState.FEAR
