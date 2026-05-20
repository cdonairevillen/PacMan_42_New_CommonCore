from dataclasses import dataclass


WALL_NORTH: int = 1
WALL_EAST: int = 2
WALL_SOUTH: int = 4
WALL_WEST: int = 8
CELL_BLOCKED: int = 15


@dataclass
class Cell:

    x: int
    y: int
    walls: int

    @property
    def wall_north(self) -> bool:
        return bool(self.walls & WALL_NORTH)

    @property
    def wall_east(self) -> bool:
        return bool(self.walls & WALL_EAST)

    @property
    def wall_south(self) -> bool:
        return bool(self.walls & WALL_SOUTH)

    @property
    def wall_west(self) -> bool:
        return bool(self.walls & WALL_WEST)

    @property
    def is_blocked(self) -> bool:
        return self.walls == CELL_BLOCKED

    @property
    def is_walkable(self) -> bool:
        return not self.is_blocked

    def can_move(self, direction: str) -> bool:
        mapping: dict[str, bool] = {
            'N': self.wall_north,
            'S': self.wall_south,
            'E': self.wall_east,
            'W': self.wall_west,
        }
        return not mapping.get(direction, True)
