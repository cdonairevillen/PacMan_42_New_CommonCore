from src.parser_config import load_config


config = load_config("config.json")

print(config)

"""
Si hay valores invalidos en el .json usamos los por defecto y mostramos el mensaje de error
ya que el subject pone: On missing or invalid values, clamp to safe defaults, log a clear message, and continue.
"""