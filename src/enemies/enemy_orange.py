import random

from src.enemies.enemy_base import Enemy


class EnemyOrange(Enemy):
    """
    Fantasma naranja.
    random.
    """

    def choose_direction(self, maze) -> None:

        possible_directions = self.get_possible_directions(maze)

        if not possible_directions:
            return

        direction = random.choice(possible_directions)

        self.set_direction(direction[0], direction[1])
