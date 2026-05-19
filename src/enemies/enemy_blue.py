import random

from src.enemies.enemy_base import Enemy


class EnemyBlue(Enemy):
    """
    Fantasma azul.

    A veces persigue.
    A veces se mueve random.
    """

    def choose_direction(self, player, maze) -> None:
    
        possible_directions = self.get_possible_directions(maze)

        if not possible_directions:
            return
        # Decide aleatoriamente si perseguir o moverse random.
        random_mode = random.randint(0, 1)

        if random_mode == 0:

            if player.x > self.x:
                self.set_direction(1, 0)

            elif player.x < self.x:
                self.set_direction(-1, 0)

            elif player.y > self.y:
                self.set_direction(0, 1)

            elif player.y < self.y:
                self.set_direction(0, -1)

        else:

            direction = random.choice(possible_directions)

            self.set_direction(direction[0], direction[1])
