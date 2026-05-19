from src.enemies.enemy_base import Enemy


class EnemyPink(Enemy):
    """
    Fantasma rosa.
    Intenta alinearse lateralmente primero.
    Da sensacion de rodear al jugador.
    """

    def choose_direction(self, player, maze) -> None:

        possible_directions = self.get_possible_directions(maze)

        # Prioriza vertical primero.

        if player.y > self.y and (0, 1) in possible_directions:
            self.set_direction(0, 1)

        elif player.y < self.y and (0, -1) in possible_directions:
            self.set_direction(0, -1)

        elif player.x > self.x and (1, 0) in possible_directions:
            self.set_direction(1, 0)

        elif player.x < self.x and (-1, 0) in possible_directions:
            self.set_direction(-1, 0)
