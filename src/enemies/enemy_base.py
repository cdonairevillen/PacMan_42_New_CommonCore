from enum import Enum


class EnemyState(Enum):
    INV = "invulnerable"
    NORMAL = "normal"
    FEAR = "fear"


class Enemy:
    """
    Clase base de todos los enemigos. Es muy parecida a la de player
    usaremos esta como pase para luego que los enemigos de colores
    hereden de esta.

    Aqui guardamos:
    - posicion logica (celdas)
    - posicion visual (pixeles)
    - velocidad
    - movimiento
    """

    def __init__(
        self,
        x: int,
        y: int,
        speed: int,
        cell_size: int = 28,
    ) -> None:

        self.x = x
        self.y = y

        self.spawn_x = x
        self.spawn_y = y

        self.speed = speed
        self.cell_size = cell_size
        self.pixels_per_second: float = float(speed * cell_size)

        self.px: float = float(x * cell_size)
        self.py: float = float(y * cell_size)
        self.target_px: float = self.px
        self.target_py: float = self.py

        self.direction_x = 0
        self.direction_y = 0
        self.move_timer: float = 0.0
        self.state = EnemyState.NORMAL
        self.respawn_timer = 0

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
        Cambia la direccion del enemigo.
        """

        self.direction_x = dx
        self.direction_y = dy

    def move(self, maze) -> None:
        """
        Mueve al enemigo si no hay pared.
        Actualiza posicion logica y destino visual.
        """

        cell = maze.get_cell(self.x, self.y)

        if cell is None:
            return

        # Derecha
        if self.direction_x == 1:
            if cell.can_move("E"):
                self.x += 1
                self.target_px = float(self.x * self.cell_size)
                self.target_py = float(self.y * self.cell_size)

        # Izquierda
        elif self.direction_x == -1:
            if cell.can_move("W"):
                self.x -= 1
                self.target_px = float(self.x * self.cell_size)
                self.target_py = float(self.y * self.cell_size)

        # Arriba
        elif self.direction_y == -1:
            if cell.can_move("N"):
                self.y -= 1
                self.target_px = float(self.x * self.cell_size)
                self.target_py = float(self.y * self.cell_size)

        # Abajo
        elif self.direction_y == 1:
            if cell.can_move("S"):
                self.y += 1
                self.target_px = float(self.x * self.cell_size)
                self.target_py = float(self.y * self.cell_size)

    def get_possible_directions(self, maze) -> list[tuple[int, int]]:
        """
        direcciones posibles.
        """

        possible_directions = []

        cell = maze.get_cell(self.x, self.y)

        if cell is None:
            return possible_directions

        if cell.can_move("E"):
            possible_directions.append((1, 0))

        if cell.can_move("W"):
            possible_directions.append((-1, 0))

        if cell.can_move("N"):
            possible_directions.append((0, -1))

        if cell.can_move("S"):
            possible_directions.append((0, 1))

        return possible_directions

    def get_position(self) -> tuple[int, int]:
        """
        Devuelve la posicion actual.
        """

        return (self.x, self.y)
