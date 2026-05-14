from src.enemies.enemy_base import Enemy


class EnemyPink(Enemy):
    """
    Fantasma rosa.
    """

    def choose_direction(self, player) -> None:
        """
        Es solo de prueba luego que hay que ver exactamente el patron
        de cada enemigo dependiendo de su color.
        Este de moemnto solo intenta acercarse al jugador.
        """

        if player.x > self.x:
            self.set_direction(1, 0)

        elif player.x < self.x:
            self.set_direction(-1, 0)

        elif player.y > self.y:
            self.set_direction(0, 1)

        elif player.y < self.y:
            self.set_direction(0, -1)
