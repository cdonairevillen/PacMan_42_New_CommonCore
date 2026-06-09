from enum import Enum
from maze.maze import Maze
from cheat_mode import CheatMode


class PlayerState(Enum):
    """Represents the possible states of the player."""
    POWER_UP = "power_up"
    NORMAL = "normal"


class Player:
    """
    Represents the player character.

    Stores the player's logical position on the maze grid,
    visual position in pixels, movement data, lives, and speed.
    """

    def __init__(self, x: int, y: int, speed: int,
                 lives: int, cell_size: int = 28) -> None:
        """
        Initialize a player instance.

        Args:
            x: Initial horizontal position in grid cells.
            y: Initial vertical position in grid cells.
            speed: Player movement speed in cells per second.
            lives: Initial number of lives.
            cell_size: Size of a maze cell in pixels.
        """
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
        self.power_timer = 0.0

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
        Set the player's movement direction.

        Updates both the current direction and the last facing direction.
        """

        self.direction_x = dx
        self.direction_y = dy

    def move(self, maze: Maze, cheat_mode: CheatMode | None = None) -> None:
        """
        Move the player within the maze.

        Updates the player's logical position and visual target position.
        Movement is restricted by maze walls unless noclip mode is enabled.
        """

        cell = maze.get_cell(self.x, self.y)

        if cell is None:
            return

        noclip = (
            cheat_mode is not None
            and cheat_mode.noclip
        )
        if self.direction_x == 1:
            self.last_direction = "right"
            if noclip:
                if self.x < maze.width - 1:
                    self.x += 1

            elif cell.can_move("E"):

                self.x += 1
            self.target_px = float(self.x * self.cell_size)
            self.target_py = float(self.y * self.cell_size)

        elif self.direction_x == -1:
            self.last_direction = "left"
            if noclip:
                if self.x > 0:
                    self.x -= 1
            elif cell.can_move("W"):
                self.x -= 1

            self.target_px = float(self.x * self.cell_size)
            self.target_py = float(self.y * self.cell_size)

        elif self.direction_y == -1:
            self.last_direction = "up"
            if noclip:
                if self.y > 0:
                    self.y -= 1
            elif cell.can_move("N"):
                self.y -= 1
            self.target_px = float(self.x * self.cell_size)
            self.target_py = float(self.y * self.cell_size)

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
        Decrease the player's remaining lives by one.
        """

        if self.lives > 0:
            self.lives -= 1

    def respawn(self, maze: Maze) -> None:
        """
        Reset the player to the center of the maze.

        Restores the player's position and movement state.
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
        Return the player's current grid position.
        """

        return (self.x, self.y)
