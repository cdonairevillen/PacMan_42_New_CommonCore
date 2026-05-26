from player.player import PlayerState


class Pacgum():

    def __init__(self, x, y, points):

        self.x = x
        self.y = y
        self.eaten = False
        self.points = points

    def consumed(self, player=None):

        self.eaten = True
        return self.points


class SuperPacgum(Pacgum):

    def __init__(self, x, y, points):
        super().__init__(x, y, points)

    def consumed(self, player):

        player.state = PlayerState.POWER_UP
        player.power_timer = 10
        return super().consumed(player)
