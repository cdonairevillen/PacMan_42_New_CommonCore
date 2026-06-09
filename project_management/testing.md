# Acceptance Test Plan

## Features Tested

- Maze generation
- Player movement
- Collision detection
- Pac-Gum collection
- Super Pac-Gum behaviour
- Ghost AI
- Level transitions
- Highscore persistence
- Cheat mode

## Bugs Found

### Ghost fear state after respawn

Status: Fixed

Description:
Ghosts respawned incorrectly after being eaten.

---

### Noclip trapped inside walls

Status: Fixed

Description:
Player could become trapped after disabling noclip mode.

---

### Level skip not loading new maze

Status: Fixed

Description:
Level transitions did not rebuild the maze correctly.