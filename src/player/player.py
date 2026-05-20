from enum import Enum


class PlayerState(Enum):

    POWER_UP = "power_up"
    NORMAL = "normal"


class Player:
    """
    Clase de jugador.

    Aqui guardamos:
    - posicion
    - movimiento
    - vidas
    - velocidad
    """

    def __init__(
        self,
        x: int,
        y: int,
        speed: int,
        lives: int
    ) -> None:

        self.x = x
        self.y = y

        self.speed = speed

        self.lives = lives

        self.direction_x = 0
        self.direction_y = 0

        self.state = PlayerState.NORMAL

    def set_direction(self, dx: int, dy: int) -> None:
        """
        Cambia la direccion del jugador.
        """

        self.direction_x = dx
        self.direction_y = dy

    def move(self, maze) -> None:
        """
        Mueve al jugador si no hay pared.
        """

        cell = maze.get_cell(self.x, self.y)

        if cell is None:
            return

        #Derecha
        if self.direction_x == 1:

            if cell.can_move("E"):
                self.x += 1

        #Izquierda
        elif self.direction_x == -1:

            if cell.can_move("W"):
                self.x -= 1

        #arriba
        elif self.direction_y == -1:

            if cell.can_move("N"):
                self.y -= 1

        #abajo
        elif self.direction_y == 1:

            if cell.can_move("S"):
                self.y += 1

    def lose_life(self) -> None:
        """
        Resta una vida al jugador.
        """

        if self.lives > 0:
            self.lives -= 1

    def respawn(self, maze) -> None:
        """
        Devuelve al jugador al centro del mapa.
        """

        self.x = maze.center[0]
        self.y = maze.center[1]

    def get_position(self) -> tuple[int, int]:
        """
        Devuelve la posicion actual.
        """

        return (self.x, self.y)
