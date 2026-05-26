import random

from enemies.enemy_base import Enemy


class EnemyBlue(Enemy):
    """
    Fantasma azul.
    Semi-random.
    """

    def choose_direction(self, player, maze) -> None:

        possible_directions = self.get_possible_directions(maze)

        if not possible_directions:
            return

        random_mode = random.randint(0, 1)

        if random_mode == 0:

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

        else:

            direction = random.choice(possible_directions)

            self.set_direction(
                direction[0],
                direction[1]
            )

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
