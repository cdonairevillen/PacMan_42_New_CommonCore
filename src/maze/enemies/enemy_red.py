import random

from enemies.enemy_base import Enemy


class EnemyRed(Enemy):
    """
    Fantasma rojo.
    Persigue directamente al jugador.
    """

    def choose_direction(self, player, maze) -> None:

        possible_directions = self.get_possible_directions(maze)

        if not possible_directions:
            return

        # Distancia al jugador.
        distance = abs(player.x - self.x) + abs(player.y - self.y)

        # Si esta lejos no persigue constantemente.
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

        # Derecha
        if (
            player.x > self.x
            and (1, 0) in possible_directions
        ):

            self.set_direction(1, 0)

        # Izquierda
        elif (
            player.x < self.x
            and (-1, 0) in possible_directions
        ):

            self.set_direction(-1, 0)

        # Abajo
        elif (
            player.y > self.y
            and (0, 1) in possible_directions
        ):

            self.set_direction(0, 1)

        # Arriba
        elif (
            player.y < self.y
            and (0, -1) in possible_directions
        ):

            self.set_direction(0, -1)

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
