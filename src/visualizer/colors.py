from enum import Enum


class Color(Enum):
    """
    RGB color palette for the maze visualizer.

    Each member is a (R, G, B) tuple ready to be passed to pygame draw
    calls. Add new entries here to extend the palette without touching
    any renderer code.
    """

    BG = (10, 10, 30)
    FLOOR = (0, 0, 0)
    BLOCKED = (5, 5, 60)

    WALL = (33, 33, 222)
    WALL_GLOW = (80, 80, 255)

    ENTRY = (0, 255, 100)
    EXIT = (255, 80, 0)
    PLAYER_SPAWN = (255, 220, 0)
    GHOST_CORNER = (200, 0, 200)

    PACGUM = (255, 220, 180)
    SUPER_PACGUM = (255, 255, 255)

    TEXT = (255, 255, 255)
    TEXT_DIM = (140, 140, 180)

    def rgb(self) -> tuple[int, int, int]:
        """
        Return the colour as a plain (R, G, B) tuple.

        Convenience wrapper so callers never need to access .value directly.

        Returns:
            (R, G, B) integer tuple.
        """
        return self.value
