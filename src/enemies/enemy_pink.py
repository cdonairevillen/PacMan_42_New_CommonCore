import random

from enemies.enemy_base import Enemy


class EnemyPink(Enemy):
    """
    Fantasma rosa.
    Intenta alinearse lateralmente primero.
    """

    def choose_direction(self, player, maze) -> None:

        possible_directions = self.get_possible_directions(maze)

        if not possible_directions:
            return

        # Prioriza vertical.

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

        # Evitar quedarse quieto.
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
