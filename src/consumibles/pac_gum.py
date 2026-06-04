from player.player import PlayerState


class Pacgum():
    """
    Collectible item that awards points when consumed.
    """
    def __init__(self, x, y, points):

        self.x = x
        self.y = y
        self.eaten = False
        self.points = points

    def consumed(self, player=None):
        """
        Mark the pacgum as eaten and return its score value.
        """
        self.eaten = True
        return self.points


class SuperPacgum(Pacgum):
    """
    Special pacgum that grants a temporary power-up.
    """
    def __init__(self, x, y, points):
        super().__init__(x, y, points)

    def consumed(self, player):
        """
        Activate the player's power-up state and award points.
        """
        player.state = PlayerState.POWER_UP
        player.power_timer = 10
        return super().consumed(player)
