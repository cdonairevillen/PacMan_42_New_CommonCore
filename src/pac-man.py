import sys
from maze.maze import Maze
from visualizer.visualizer import MazeVisualizer


def main() -> None:

    # Add parser

    maze = Maze.build(width=21, height=21, seed=42)
    print(f"[main] Maze built: {maze.width}x{maze.height}  spawn={maze.center}")

    viz = MazeVisualizer(maze)
    viz.run()


if __name__ == "__main__":
    main()