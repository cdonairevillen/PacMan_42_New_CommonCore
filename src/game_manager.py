from enum import Enum
from maze.maze import Maze


class State(Enum):

    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "gameover"
    VICTORY = "Victory"

class GameManager():

    def __init__(self, config: dict[str][list]) -> None:
        
        # Player info
        self.lives = config["lives"]
        self.score = 0

        # Game info
        self.points_per_gum = config["points_per_pacgum"]
        self.points_per_supergum = config["points_per_super_pacgum"]
        self.points_per_ghost = config["points_per_ghost"]

        # Game State
        self.state = State.PAUSED
        self.current_level = 0
        self.current_maze = Maze.build(width=config["levels"][self.current_level]["width"],
                                       height=["levels"][self.current_level]["height"],
                                       seed=42 if self.current_level is 0)
        
        # Game Conditions
        self.level_max_time = config["level_max_time"]
        self.time_remining = self.level_max_time

    def build_level()
