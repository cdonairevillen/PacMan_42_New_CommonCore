from src.maze.maze import Maze
from src.player.player import Player
from src.enemies.enemy_pink import EnemyPink


def main() -> None:
    """
    Archivo temporal:
    - Generacion del maze
    - Movimiento del player
    - Movimiento del enemigo
    - Colisiones
    """

    #maze.
    maze = Maze.build(
        width=20,
        height=25,
        seed=42
    )

    print("\nLaberito generado")
    print(f"Size: {maze.width}x{maze.height}")
    print(f"Center: {maze.center}")

    #jugador.
    player = Player(
        x=maze.center[0],
        y=maze.center[1],
        speed=1,
        lives=3
    )

    print("\nJugador crwado")
    print(f"Position: {player.get_position()}")
    print(f"Lives: {player.lives}")

    #enemigo.
    enemy = EnemyPink(
        x=1,
        y=1,
        speed=1
    )

    print("\nEnemigo creado")
    print(f"Position: {enemy.get_position()}")

    #enemigo persiga al jugador.
    enemy.choose_direction(player)

    #Movemos enemigo.
    enemy.move(maze)

    print("\nMovimiento del enemigo")
    print(f"New position: {enemy.get_position()}")

    #ccolision.
    if player.get_position() == enemy.get_position():

        player.lose_life()

        print("\nPlayer hit")
        print(f"Lives left: {player.lives}")

    else:
        print("\nNo hay colision")


if __name__ == "__main__":
    main()
