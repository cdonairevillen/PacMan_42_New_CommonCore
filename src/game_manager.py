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
import random

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
                             lives=config["lives"], speed=5)

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
        self.enemies = []

        corners = list(self.current_maze.get_corner_cells())

        self.enemies = [
            EnemyRed(corners[0][0], corners[0][1], speed=3.8),
            EnemyPink(corners[1][0], corners[1][1], speed=3.5),
            EnemyBlue(corners[2][0], corners[2][1], speed=3.2),
            EnemyOrange(corners[3][0], corners[3][1], speed=2.8),
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

    def next_level(self):

        self.current_level += 1

        if self.current_level >= len(self.config["levels"]):
            self.state = State.VICTORY

            return False

        else:
            self.state = State.LOADING
            self.build_level(seed=0)
            self.time_remining = self.level_max_time
            self.player.respawn(self.current_maze)
            self.state = State.PLAYING

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
            if not self.player.cheat_mode:
                self.time_remining -= dt
            self.move_timer += dt

            if self.move_timer >= 1.0 / self.player.speed:
                self.player.move(self.current_maze)
                self.move_timer = 0
       
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
                        enemy.state = EnemyState.NORMAL
                enemy.move_timer += dt
                if enemy.move_timer >= 1.0 / enemy.speed:
                    if isinstance(enemy, EnemyOrange):
                        enemy.choose_direction(self.current_maze)
                    else:
                        enemy.choose_direction(
                            self.player,
                            self.current_maze
                        )
                    enemy.move(self.current_maze)
                    enemy.move_timer = 0
                enemy_pos = enemy.get_position()
                if enemy_pos == player_pos:
                    if self.player.cheat_mode:
                        continue
                    if enemy.state == EnemyState.INV:
                        continue

                    elif (enemy.state == EnemyState.FEAR
                          and self.player.state == PlayerState.POWER_UP):
                        self.eat_ghost(enemy)

                    elif (enemy.state == EnemyState.NORMAL
                          and self.player.state == PlayerState.NORMAL):
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
        
    def check_life(self) -> None:

        self.player.lose_life()

        if self.player.lives <= 0:

            self.game_over()

            return

        # Respawn player.
        self.player.respawn(self.current_maze)

        # Reset fantasmas.
        self.reset_enemy_positions()

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
        enemy.respawn_timer = 3
        corners = self.current_maze.get_corner_cells()

        if corners:
            enemy.x, enemy.y = random.choice(corners)
        enemy.direction_x = 0
        enemy.direction_y = 0
