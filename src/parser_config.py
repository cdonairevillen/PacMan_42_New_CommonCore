import json
from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError

"""
Configuración por defecto del jueguito.
"""
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
    Carga el config.json y devuelve la configuración validaada.
    """

    try:
        with open(path, "r") as file:
            lines = []

            for line in file:

                # Eliminamos espacios al principio y final.
                clean_line = line.strip()

                # Ignoramos comentarios y líneas vacías.
                if clean_line.startswith("#") or clean_line == "":
                    continue

                lines.append(line)

            # Convertimos todas las líneas en un único texto.
            json_content = "".join(lines)

            # Convertimos el texto JSON a diccionario Python.
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
    Valida el config usando Pydantic.
    """

    try:

        validated = GameConfig(**config)

        final_config = validated.model_dump()

        for level in final_config["levels"]:

            # Aseguramos centro.
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
