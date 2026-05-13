import sys
from maze.maze import Maze
from visualizer.visualizer import MazeVisualizer
import parser_config


def main() -> None:

    path = "../config.json"

    if len(sys.argv) == 2:
        path = sys.argv[1]

    # Add parser
    config = parser_config.load_config(path)

    maze = Maze.build(width=30, height=21, seed=42)
    print(f"[main] Maze built: {maze.width}x{maze.height}  spawn={maze.center}")

    viz = MazeVisualizer(maze)
    viz.run()


if __name__ == "__main__":
    main()