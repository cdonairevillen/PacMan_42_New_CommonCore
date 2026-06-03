from enum import Enum


class PlayerState(Enum):

    POWER_UP = "power_up"
    NORMAL = "normal"


class Player:
    """
    Clase de jugador.

    Aqui guardamos:
    - posicion logica (celdas)
    - posicion visual (pixeles)
    - movimiento
    - vidas
    - velocidad
    """

    def __init__(self, x: int, y: int, speed: int,
                 lives: int, cell_size: int = 28) -> None:

        self.x = x
        self.y = y

        self.speed = speed
        self.normal_speed = speed
        self.cell_size = cell_size
        self.pixels_per_second: float = float(speed * cell_size)

        self.px: float = float(x * cell_size)
        self.py: float = float(y * cell_size)
        self.target_px: float = self.px
        self.target_py: float = self.py

        self.lives = lives
        self.hit = False

        self.direction_x = 0
        self.direction_y = 0

        self.state = PlayerState.NORMAL
        self.power_timer = 0

        self.last_direction = "right"

    def update_visual(self, dt: float) -> None:
        """
        Move the visual position toward the target pixel position.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        step = self.pixels_per_second * dt

        dx = self.target_px - self.px
        dy = self.target_py - self.py

        if abs(dx) <= step:
            self.px = self.target_px
        else:
            self.px += step if dx > 0 else -step

        if abs(dy) <= step:
            self.py = self.target_py
        else:
            self.py += step if dy > 0 else -step

    def get_visual_pos(self) -> tuple[float, float]:
        """
        Return the current visual pixel position.

        Returns:
            (px, py) float tuple for rendering.
        """
        return (self.px, self.py)

    def set_direction(self, dx: int, dy: int) -> None:
        """
        Cambia la direccion del jugador.
        """

        self.direction_x = dx
        self.direction_y = dy

    def move(self, maze, cheat_mode=None) -> None:
        """
        Mueve al jugador si no hay pared.
        Actualiza posicion logica y destino visual.
        """

        cell = maze.get_cell(self.x, self.y)

        if cell is None:
            return

        noclip = (
            cheat_mode is not None
            and cheat_mode.noclip
        )

        # Derecha
        if self.direction_x == 1:
            self.last_direction = "right"

            if noclip:

                if self.x < maze.width - 1:
                    self.x += 1

            elif cell.can_move("E"):

                self.x += 1

            self.target_px = float(self.x * self.cell_size)
            self.target_py = float(self.y * self.cell_size)

        # Izquierda
        elif self.direction_x == -1:
            self.last_direction = "left"

            if noclip:

                if self.x > 0:
                    self.x -= 1

            elif cell.can_move("W"):

                self.x -= 1

            self.target_px = float(self.x * self.cell_size)
            self.target_py = float(self.y * self.cell_size)

        # Arriba
        elif self.direction_y == -1:
            self.last_direction = "up"

            if noclip:

                if self.y > 0:
                    self.y -= 1

            elif cell.can_move("N"):

                self.y -= 1

            self.target_px = float(self.x * self.cell_size)
            self.target_py = float(self.y * self.cell_size)

        # Abajo
        elif self.direction_y == 1:
            self.last_direction = "down"

            if noclip:

                if self.y < maze.height - 1:
                    self.y += 1

            elif cell.can_move("S"):

                self.y += 1

            self.target_px = float(self.x * self.cell_size)
            self.target_py = float(self.y * self.cell_size)

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

        self.px = float(self.x * self.cell_size)
        self.py = float(self.y * self.cell_size)
        self.target_px = self.px
        self.target_py = self.py
        self.hit = False

        self.direction_x = 0
        self.direction_y = 0

        self.last_direction = "right"

    def get_position(self) -> tuple[int, int]:
        """
        Devuelve la posicion actual.
        """

        return (self.x, self.y)
