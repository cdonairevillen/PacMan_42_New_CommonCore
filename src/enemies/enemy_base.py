class Enemy:
    """
    Clase base de todos los enemigos. Es muy parecida a la de player
    usaremos esta como pase para luego que los enemigos de colores 
    hereden de esta.

    Aqui guardamos:
    - posicion
    - velocidad
    - movimiento
    """

    def __init__(
        self,
        x: int,
        y: int,
        speed: int
    ) -> None:

        self.x = x
        self.y = y

        self.speed = speed

        self.direction_x = 0
        self.direction_y = 0

    def set_direction(self, dx: int, dy: int) -> None:
        """
        Cambia la direccion del enemigo.
        """

        self.direction_x = dx
        self.direction_y = dy

    def move(self, maze) -> None:
        """
        Mueve al enemigo si no hay pared.
        """

        cell = maze.get_cell(self.x, self.y)

        if cell is None:
            return

        #derecha
        if self.direction_x == 1:

            if cell.can_move("E"):
                self.x += 1

        #Izquierda
        elif self.direction_x == -1:

            if cell.can_move("W"):
                self.x -= 1

        #Arriba
        elif self.direction_y == -1:

            if cell.can_move("N"):
                self.y -= 1

        #Abajo
        elif self.direction_y == 1:

            if cell.can_move("S"):
                self.y += 1

    def get_position(self) -> tuple[int, int]:
        """
        Devuelve la posicion actual.
        """

        return (self.x, self.y)
