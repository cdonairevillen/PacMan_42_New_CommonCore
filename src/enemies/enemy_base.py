from __future__ import annotations

from collections import deque
from enum import Enum


class EnemyState(Enum):
    """Represents the possible states of an enemy."""
    INV = "invulnerable"
    NORMAL = "normal"
    FEAR = "fear"


class Enemy:
    """
    Base class for all enemy types.

    Stores the enemy's logical and visual positions, movement
    information, speed, and state. Specific enemy behaviors are
    implemented by subclasses.
    """

    def __init__(
        self,
        x: int,
        y: int,
        speed: int,
        cell_size: int = 28,
    ) -> None:
        """
        Initialize an enemy instance.

        Args:
            x: Initial horizontal position in grid cells.
            y: Initial vertical position in grid cells.
            speed: Movement speed in cells per second.
            cell_size: Size of a maze cell in pixels.
        """
        self.x = x
        self.y = y

        self.spawn_x = x
        self.spawn_y = y

        self.speed = speed
        self.normal_speed: float = float(speed)
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

        self.return_path: list[tuple[int, int]] = []
        self.blink_timer: float = 0.0

    def find_path_to(self, tx: int, ty: int, maze) -> list[tuple[int, int]]:
        """
        Find shortest path to target using BFS.

        Args:
            tx: Target column index.
            ty: Target row index.
            maze: Current maze instance.

        Returns:
            List of (x, y) cells from next step to target,
            or empty list if no path exists.
        """
        start = (self.x, self.y)
        goal = (tx, ty)

        if start == goal:
            return []

        queue: deque[list[tuple[int, int]]] = deque([[start]])
        visited: set[tuple[int, int]] = {start}

        while queue:
            path = queue.popleft()
            cx, cy = path[-1]

            if (cx, cy) == goal:
                return path[1:]

            cell = maze.get_cell(cx, cy)
            if cell is None:
                continue

            for dx, dy, direction in [
                (1, 0, "E"),
                (-1, 0, "W"),
                (0, -1, "N"),
                (0, 1, "S"),
            ]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) not in visited and cell.can_move(direction):
                    visited.add((nx, ny))
                    queue.append(path + [(nx, ny)])

        return []

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
        Set the enemy's movement direction.
        """

        self.direction_x = dx
        self.direction_y = dy

    def move(self, maze) -> None:
        """
        Move the enemy one cell in the current direction.
        Updates both the logical position and the target visual
        position.
        """

        cell = maze.get_cell(self.x, self.y)

        if cell is None:
            return

        if self.direction_x == 1:
            if cell.can_move("E"):
                self.x += 1
                self.target_px = float(self.x * self.cell_size)
                self.target_py = float(self.y * self.cell_size)

        elif self.direction_x == -1:
            if cell.can_move("W"):
                self.x -= 1
                self.target_px = float(self.x * self.cell_size)
                self.target_py = float(self.y * self.cell_size)

        elif self.direction_y == -1:
            if cell.can_move("N"):
                self.y -= 1
                self.target_px = float(self.x * self.cell_size)
                self.target_py = float(self.y * self.cell_size)

        elif self.direction_y == 1:
            if cell.can_move("S"):
                self.y += 1
                self.target_px = float(self.x * self.cell_size)
                self.target_py = float(self.y * self.cell_size)

    def get_possible_directions(self, maze) -> list[tuple[int, int]]:
        """
        Return all valid movement directions from the current cell.
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
        Return the enemy's current grid position.
        """

        return (self.x, self.y)
