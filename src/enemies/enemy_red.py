import random
from enemies.enemy_base import Enemy
from player.player import Player
from maze.maze import Maze


class EnemyRed(Enemy):
    """
    Red ghost that actively pursues nearby players.
    """

    def choose_direction(self, player: Player, maze: Maze) -> None:
        """
        Choose a direction based on the player's position.

        Chases the player when nearby and otherwise continues moving
        or selects a valid random direction.
        """
        possible_directions = self.get_possible_directions(maze)
        if not possible_directions:
            return
        distance = abs(player.x - self.x) + abs(player.y - self.y)

        if distance > 5:

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
            return

        if (
            player.x > self.x
            and (1, 0) in possible_directions
        ):

            self.set_direction(1, 0)

        elif (
            player.x < self.x
            and (-1, 0) in possible_directions
        ):

            self.set_direction(-1, 0)

        elif (
            player.y > self.y
            and (0, 1) in possible_directions
        ):

            self.set_direction(0, 1)

        elif (
            player.y < self.y
            and (0, -1) in possible_directions
        ):

            self.set_direction(0, -1)

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
