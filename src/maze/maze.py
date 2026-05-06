from dataclasses import dataclass
from typing import Optional
from maze.cell import Cell
from mazegenerator.mazegenerator import MazeGenerator


class Maze:
    def __init__(self, cells: list[list[Cell]],
                 entry: tuple[int, int],
                 exit_pos: tuple[int, int],) -> None:
        self.cells: list[list[Cell]] = cells
        self.height: int = len(cells)
        self.width: int = len(cells[0]) if self.height > 0 else 0
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_pos
        self.center: tuple[int, int] = self.find_center()

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def get_walkable_cells(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.cells[y][x].is_walkable]

    def get_corner_cells(self) -> list[tuple[int, int]]:
        targets = [
            (1, 1),
            (self.width - 2, 1),
            (1, self.height - 2),
            (self.width - 2, self.height - 2),
        ]
        result: list[tuple[int, int]] = []
        for tx, ty in targets:
            nearest = self.find_nearest_walkable(tx, ty)
            if nearest is not None:
                result.append(nearest)
        return result

    def find_center(self) -> tuple[int, int]:
        cx = self.width // 2
        cy = self.height // 2
        return self.find_nearest_walkable(cx, cy) or (cx, cy)

    def find_nearest_walkable(
        self, tx: int, ty: int
    ) -> Optional[tuple[int, int]]:
        for radius in range(max(self.width, self.height)):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    x, y = tx + dx, ty + dy
                    if (
                        0 <= x < self.width
                        and 0 <= y < self.height
                        and self.cells[y][x].is_walkable
                    ):
                        return (x, y)
        return None

    @staticmethod
    def from_generator(generator: MazeGenerator) -> Maze:
        raw: list[list[int]] = generator.maze
        cells: list[list[Cell]] = [
            [Cell(x=x, y=y, walls=raw[y][x]) for x in range(len(raw[y]))]
            for y in range(len(raw))
        ]
        return Maze(
            cells=cells,
            entry=generator.maze_entry,
            exit_pos=generator.maze_exit,
        )

    @staticmethod
    def build(
        width: int = 21,
        height: int = 21,
        seed: int = 0,
        perfect: bool = False,
    ) -> Maze:
        generator = MazeGenerator(
            size=(width, height),
            perfect=perfect,
            seed=seed,
        )
        return Maze.from_generator(generator)