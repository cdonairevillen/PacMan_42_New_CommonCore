import json

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
            "width": 15,
            "height": 15
        }
    ]
}



def load_config(path: str) -> dict:
    """
    Carga el config.json y devuelve la configuración validaada.
    """

    try:
        with open(path, "r") as file:
            lines = []

            for line in file:

                #Eliminamos espacios al principio y final.
                clean_line = line.strip()

                #Ignoramos comentarios y líneas vacías.
                if clean_line.startswith("#") or clean_line == "":
                    continue

                lines.append(line)

            #Convertimos todas las líneas en un único texto.
            json_content = "".join(lines)

            #Convertimos el texto JSON a diccionario Python.
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
    Comprueba que los valores del config esten bien.
    Con esto evitamos payasadas como:
    {
        "lives": -400,
        "seed": "hola",
        "levels": "patata"
    }
    Usamos .copy para no modificar el original y luego el resto fucnionaria por ejemplo:
    if isinstance(config.get("lives"), int):
        final_config["lives"] = max(1, config["lives"])
    Buscaria lives en el JASOOOOOON y si este es igual a 5 hacemos config.get y devolvemos
    ese 5, con el isinstance comprobamos si es un int y devuelve True(Ya que si nos pasan por ejemplo "alpaca"
    devolveremos False)
    Luego estuve mirando para que no nos acepte ni vidas negativas o a 0 y por eso el uso de max
    ya que nos va a devolver el mayor valor.
    
    """

    final_config = DEFAULT_CONFIG.copy()

    if isinstance(config.get("lives"), int):
        final_config["lives"] = max(1, config["lives"])
    else:
        print("Invalid lives value. Using default.")

    if isinstance(config.get("seed"), int):
        final_config["seed"] = max(0, config["seed"])
    else:
        print("Invalid seed value. Using default.")

    if isinstance(config.get("level_max_time"), int):
        final_config["level_max_time"] = max(1, config["level_max_time"])
    else:
        print("Invalid level_max_time value. Using default.")

    if isinstance(config.get("points_per_pacgum"), int):
        final_config["points_per_pacgum"] = max(0, config["points_per_pacgum"])
    else:
        print("Invalid points_per_pacgum value. Using default.")

    if isinstance(config.get("points_per_super_pacgum"), int):
        final_config["points_per_super_pacgum"] = max(0, config["points_per_super_pacgum"])
    else:
        print("Invalid points_per_super_pacgum value. Using default.")

    if isinstance(config.get("points_per_ghost"), int):
        final_config["points_per_ghost"] = max(0, config["points_per_ghost"])
    else:
        print("Invalid points_per_ghost value. Using default.")

    if isinstance(config.get("highscore_filename"), str):
        final_config["highscore_filename"] = (config["highscore_filename"])
    else:
        print("Invalid highscore_filename value. Using default.")

    if isinstance(config.get("levels"), list):

        levels = []

        for level in config["levels"]:
            """
            Ponemos por defecto a 15 por si en el config faltan los datos de width y height,
            y Luego usamos % 2 para comprobar si el numero es par. Si es par sumamos 1 
            y lo convertimos en impar para asegurar un centro.
            Ya que en el subject pone "The player starts in the middle of the maze".
            """
            if "width" not in level:
                print("Width missing. Using default value 15.")

            if "height" not in level:
                print("Height missing. Using default value 15.")

            width = level.get("width", 15)
            height = level.get("height", 15)

            if width % 2 == 0:
                width += 1

            if height % 2 == 0:
                height += 1

            levels.append({
                "width": width,
                "height": height
            })

        if levels:
            final_config["levels"] = levels
    else:
        print("Invalid levels list. Using default.")

    return final_config
