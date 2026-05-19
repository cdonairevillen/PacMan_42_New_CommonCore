from src.enemies.enemy_base import Enemy


class EnemyRed(Enemy):
    """
    Fantasma rojo.
    Persigue directamente al jugador.
    """

    def choose_direction(self, player, maze) -> None:

        possible_directions = self.get_possible_directions(maze)

        # Derecha
        if player.x > self.x and (1, 0) in possible_directions:
            self.set_direction(1, 0)

        # Izquirda
        elif player.x < self.x and (-1, 0) in possible_directions:
            self.set_direction(-1, 0)

        # Abajo
        elif player.y > self.y and (0, 1) in possible_directions:
            self.set_direction(0, 1)

        # Arriba
        elif player.y < self.y and (0, -1) in possible_directions:
            self.set_direction(0, -1)
