import sys
import os
from visualizer.visualizer import MazeVisualizer
from game_manager import GameManager
import parser_config


def main() -> None:

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
    path = "../config.json"
    if len(sys.argv) == 2:
        path = sys.argv[1]

    config = parser_config.load_config(path)
    manager = GameManager(config)
    viz = MazeVisualizer(manager)
    viz.run()


if __name__ == "__main__":
    main()
