import json
from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError

DEFAULT_CONFIG = {
    "lives": 3,
    "seed": 42,
    "level_max_time": 90,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "highscore_filename": "high_score/leaderboard.json",
    "levels": [
        {
            "width": 3,
            "height": 3
        }
    ]
}


class LevelConfig(BaseModel):
    """
    Represents the configuration settings for a game level.

    Attributes:
        width: Width of the level grid.
        height: Height of the level grid.
    """
    width: int = Field(
        default=15,
        ge=3,
        le=99
    )

    height: int = Field(
        default=15,
        ge=3,
        le=99
    )


class GameConfig(BaseModel):
    """
    Represents the complete game configuration.

    Attributes:
        lives: Number of lives available to the player.
        seed: Random seed used for procedural generation.
        level_max_time: Maximum duration of a level in seconds.
        points_per_pacgum: Points awarded for collecting a pacgum.
        points_per_super_pacgum: Points awarded for collecting a super pacgum.
        points_per_ghost: Points awarded for defeating a ghost.
        highscore_filename: Path to the high score file.
        levels: List of level configurations.
    """

    lives: int = Field(default=3, ge=1)

    seed: int = Field(default=42, ge=0)

    level_max_time: int = Field(default=90, ge=1)

    points_per_pacgum: int = Field(
        default=10,
        ge=0
    )

    points_per_super_pacgum: int = Field(
        default=50,
        ge=0
    )

    points_per_ghost: int = Field(
        default=200,
        ge=0
    )

    highscore_filename: str = (
        "high_score/leaderboard.json"
    )

    levels: list[LevelConfig] = [
        LevelConfig(width=3, height=3)
        ]


def load_config(path: str) -> dict:
    """
    Load a configuration file and validate its contents.

    The function reads a JSON configuration file while ignoring
    blank lines and lines starting with '#'. If the file cannot
    be read or parsed, the default configuration is returned.

    Args:
        path: Path to the configuration file.

    Returns:
        A validated configuration dictionary. If loading fails,
        the default configuration is returned.
    """

    try:
        with open(path, "r") as file:
            lines = []

            for line in file:
                clean_line = line.strip()
                if clean_line.startswith("#") or clean_line == "":
                    continue
                lines.append(line)

            json_content = "".join(lines)
            config = json.loads(json_content)

    except FileNotFoundError:
        print("Config file not found. Using default config.")
        return DEFAULT_CONFIG

    except Exception as error:
        print(f"Error reading config: {error}")
        return DEFAULT_CONFIG

    return validate_config(config)


def validate_config(config: dict) -> dict:
    """
    Validate and normalize a game configuration.

    The configuration is validated against the GameConfig schema.
    Level dimensions are adjusted to ensure they are odd numbers,
    which may be required by the game's map generation logic.

    Args:
        config: Configuration dictionary to validate.

    Returns:
        A validated and normalized configuration dictionary.

    Raises:
        ValidationError: Internally handled when the configuration
            does not match the expected schema.
    """

    try:

        validated = GameConfig(**config)

        final_config = validated.model_dump()

        for level in final_config["levels"]:
            if level["width"] % 2 == 0:
                level["width"] += 1

            if level["height"] % 2 == 0:
                level["height"] += 1

        return final_config

    except ValidationError as error:
        print(
            "Invalid config. Using default config."
        )
        print(error)

        return DEFAULT_CONFIG.copy()
