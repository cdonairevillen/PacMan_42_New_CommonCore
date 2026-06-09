from player.player import PlayerState, Player


class Pacgum():
    """
    Collectible item that awards points when consumed.
    """
    def __init__(self, x: int, y: int, points: int):

        self.x: int = x
        self.y: int = y
        self.eaten: bool = False
        self.points: int = points

    def consumed(self, player: Player) -> int:
        """
        Mark the pacgum as eaten and return its score value.
        """
        self.eaten = True
        return self.points


class SuperPacgum(Pacgum):
    """
    Special pacgum that grants a temporary power-up.
    """
    def __init__(self, x: int, y: int, points: int) -> None:
        super().__init__(x, y, points)

    def consumed(self, player: Player) -> int:
        """
        Activate the player's power-up state and award points.
        """
        player.state = PlayerState.POWER_UP
        player.power_timer = 10
        return super().consumed(player)
