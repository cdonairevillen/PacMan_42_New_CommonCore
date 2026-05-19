from src.maze.maze import Maze
from src.player.player import Player

from src.enemies.enemy_pink import EnemyPink
from src.enemies.enemy_blue import EnemyBlue
from src.enemies.enemy_orange import EnemyOrange
from src.enemies.enemy_red import EnemyRed


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
        width=15,
        height=15,
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

    #enemigos.
    enemies = [
        EnemyRed(
            x=1,
            y=1,
            speed=1
        ),

        EnemyPink(
            x=13,
            y=1,
            speed=1
        ),

        EnemyBlue(
            x=1,
            y=13,
            speed=1
        ),

        EnemyOrange(
            x=13,
            y=13,
            speed=1
        )
    ]

    #enemigos persigan al jugador.
    for enemy in enemies:

        print(f"\n{enemy.__class__.__name__}")
        print(f"Position: {enemy.get_position()}")

        print("Possible directions:")
        print(enemy.get_possible_directions(maze))

        if isinstance(enemy, EnemyOrange):

            enemy.choose_direction(maze)

        else:

            enemy.choose_direction(player, maze)

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
