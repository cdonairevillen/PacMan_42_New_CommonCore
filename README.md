
El proyecto va a ser probado con el siguiente comando:

$> python3 pac-man.py config.json

mi estructura de carpetas recomendada seria:



# Entrada de Datos

Solo podra coger como argumento un archivo tipo Json.
El programa solo podra coger 1 argumento

Parseo igual que flyin y amazing (lineas empezadas por # no deben ser consideradas
                                    podremos soportar otros estilos de comentarios)
                                    
Estructura de el archivo queda a nuestra eleccion.

Ante elementos no definidos o invalidos, setear a default. Tenemos que mostrar un mensaje
de error y recovery en terminal.

Idea: Este archivo es el base de creacion de el juego. Dependiendo de la escalabilidad
que queramos tener, podemos modificarlo bastante. Supuestamente en el tenemos que tener
la base de nuestro juego (ruta  al archivo de laderboard, los niveles accesibles, el ancho
de cada nivel...) Si queremos que el programa tenga evolucion, tal vez podriamos hacer que
este  archivo de paso a configs especificas para cada nivel, dependiendo de lo que queramos
proyectar (niveles con bajos puntos por cazar fantasmas, niveles con muy pocas monedas, etc.)

Tambien podemos hacerlo matematicamente una vez tengamos el mapa seleccionado, asi que podemos
discutir como manejarlo

# Logica de score*

Tenemos que generar un sistema de scores. Mi idea aqui seria generar un json "nombre": score que solo guarde los 10 primeros jugadores. Con la libreria json es bastante sencillo manipular este archivo.

Cuando se llame al laderboard o al iniciar el juego podemos leer este archivo para tenerlo precomputado y poder modificarlo tras el seteo de una nueva puntuacion. Si el archivo no existe, se generara un archivo nuevo con todas las puntuaciones a 0

Parsearemos el output del jugador a traves de una clase con BaseModel para usar field() y controlar la entrada de datos de manera sencilla. El nombre del jugador debe ser de max 10 caracteres alfanumericos con espacios.

Los scores no pueden ser negativos

Permitir siempre meter el nombre al jugador al ganar o perder(mi forma d ever esto es que llegado el momento el jugador metera sus credenciales y podra chequear la laderboard junto a su score. Si esta entre los 10 primeros, encontrara su score entre la lista, si no, saldra la lista de 10 puntuaciones y su score en la parte inferior. no se registrara en la lista en este caso)

la laderboard debera mostrarse en el main menu (horrible. Tendremos que ver como hacerlo y que no de puto asco.)

# Logica de generacion

La generacion de laberintos sera aleatoria quitando el primer nivel, que tendra semilla fixeada (contradiccion con la explicacion del json de entrada)

Los coins deberan generarse en la mayoria de las casillas

Los poweups deberan generarse en las esquinas de la mazmorra

deberan generarse 4 fantasmas, cada uno en una esquina d ela mazmorra

el jugador empieza en el punto mas centrico de la mazmorra. Como es un punto recurrente, deberiamos forzar que la salida del jugador siempre este en ese punto.


# Player:

La clase d ejugador necesitara un metodo move que chequee si la siguiente celda  es accesible con respecto a las pareces cerradas que haya. Logica muy parecida a la de generacion de laberinto.

Necesitaremos un metodo estilo keyhook para el movimiento con las teclas WASD. 

Empezara con 3 vidas. Necesitara un metodo is_hitted() para registrar los golpes del enemigo

respawnea en su casilla seleccionada (la mas centrica)

deberia tener una flag para cuando se coma un powerup y una gestion de tiempo para su duracion.

## Game Manager

El game manager debera controlar los elementos del mapa. Si el jugador llega a 0 vidas, game over, si se come todos los elementos del mapa, nivel superado. Tambien el game manager debera llevar el control de los puntos alcanzados por el jugador a traves de los valores por token metidos en el config.json (o como hayamos decidido hacerlo).

Tambien debe llevar un registro de los mapas superados. Si se hacen los 10, se dara por vencido el juego. 

# Enemigos:

Podemos hacer que todos se comporten igual o podemos hacer que funcionen como el pacman original. Total libertad en la logica de persecucion. 

Respawnean en su esquina cuando son comidos. No hace falta que encuentren el camino, pueden popear(cutre) despues de x tiempo.

# Consumibles

Mejor que sean una clase a parte, mas sencillos de controlar a traves del game manager. Recomendacion: Herencia. un pacgum base y los powerups que sean lo mismo reinterpretanndo el metodo. 

## Extras

debera haber un cheatmode

# UI

## Menu Manager

Controla los elementos del menu. Debe tener las siguientes posibilidades:

- Start Game
- View Scores
- Instructions
- Exit

## HUD in game

Displayea los elementos visuales ingame (score, vidas, etc.)

- Current Score
- Remaining Lives
- Current Level
- Time

Lee el game manager y displayea sus elementos en el formato y posicion deseada. Una capa superior al render del juego.

## Menu de pausa

Misma idea que el menu manager. Sistema de botones para:

- Resume
- Return to main menu

## Screan de game over

Muestra el final score con la laderboard y permite al jugador introducir su nombre.

## Victory screen 

lo mismo que "game over" pero mas alegre.

* con respecto a esto yo me basaria en arcades actuales para realizarlo. UI sera la clase que recoja todas estas subclases y aplicara y destruira cada una en el momento que deba. Cuanto mas modular realicemos este ejercicio, creo que sera mejor.

# MI VISION:

Necesitamos las siguientes clases logicas si o si:

Game Manager
    - Parser

Menu Manager/UI
    - Main Menu
    - Pause Menu
    - HUD
    - Special Screens

Player

Enemies

Consumables

Visualizer(no se si deberia ser gestionado por el game manager)

Idea de flujo:

player intenta moverse -> game manager registra su nueva posicion -> visualizer lo muestra

player chequea si el movimiento que va a realizar es posible, tambien si ha tocado una moneda o un fantasma, etc. Game manager revisa si eso ha ocurrido y actualiza la informacion acorde

Plantea que cada elemento extra (botones, por ejemplo) seran clases seteadas en utils. Mi idea seria usar herencia para no tener duplicaciones. Si necesitamos un boton de exit, que herede del boton base y reinterpretamos su metodo get_push(). Si tenemos utils bases, podemos reinterpretarlos en los archivos .py que les correspondan, lo cual hace que tengamos el repo mucho ma slimpio y ordenado.

Necesitaremos un monton de recursos. Sprites de fantasmitas, pacman y consumibles para recrear el movimiento y que no de asco, aunque primero haremos la logica y despues el resto.

# MUY IMPORTANTE:

## Empaquetado del proyecto

mismo empaqueado que el amazing.

## CONTROL DEL PROCESO DEL PROYECTO

Necesitamos registros y control de procesos del proyecto. Organizacion del equipo, analisis de riesgos y posibles formas de solventarlo... Necesitamos darle una vuelta extra a este archivo mientras planteamos el proyecto de cara a empezar con buen pie este punto y no tener que inventarnos todo al ultimo momento. 

Esto sera el ultimo punto del readme
