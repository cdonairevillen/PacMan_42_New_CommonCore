import random

from enemies.enemy_base import Enemy


class EnemyOrange(Enemy):
    """
    Orange ghost with random movement behavior.
    """

    def choose_direction(self, maze) -> None:
        """
        Choose a random valid movement direction.

        Keeps the current direction when possible and selects a new
        random direction only when necessary.
        """
        possible_directions = self.get_possible_directions(maze)
        if not possible_directions:
            return

        current_direction = (
            self.direction_x,
            self.direction_y
        )

        if current_direction in possible_directions:

            return

        direction = random.choice(possible_directions)
        self.set_direction(
            direction[0],
            direction[1]
        )
