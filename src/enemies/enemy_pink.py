import random
from enemies.enemy_base import Enemy
from player.player import Player
from maze.maze import Maze


class EnemyPink(Enemy):
    """
    Pink ghost that prioritizes vertical pursuit.
    """

    def choose_direction(self, player: Player, maze: Maze) -> None:
        """
        Choose a direction toward the player.

        Prioritizes vertical movement before horizontal movement and
        falls back to a random valid direction when necessary.
        """
        possible_directions = self.get_possible_directions(maze)
        if not possible_directions:
            return

        if (
            player.y > self.y
            and (0, 1) in possible_directions
        ):

            self.set_direction(0, 1)

        elif (
            player.y < self.y
            and (0, -1) in possible_directions
        ):

            self.set_direction(0, -1)

        elif (
            player.x > self.x
            and (1, 0) in possible_directions
        ):

            self.set_direction(1, 0)

        elif (
            player.x < self.x
            and (-1, 0) in possible_directions
        ):

            self.set_direction(-1, 0)
        current_direction = (
            self.direction_x,
            self.direction_y
        )

        if current_direction not in possible_directions:
            direction = random.choice(possible_directions)
            self.set_direction(
                direction[0],
                direction[1]
            )
