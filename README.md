*This project has been created as part of the 42 curriculum by roherna2, cdonaire*

# Pacman Ghosts! More ghosts!

## Description

This project is a modern reimplementation of the classic Pac-Man game developed in Python using Pygame.

The objective is to navigate through procedurally generated mazes, collect Pac-Gums, avoid ghosts, use Super Pac-Gums to enter Power-Up mode, and complete multiple levels before running out of lives or time.

The project combines gameplay mechanics, procedural maze generation, configurable settings, score persistence, sprite-based rendering, and a cheat mode designed to facilitate peer review.

---

# Instructions

## Requirements

* Python 3.13+
* Pygame 2.x

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd PacMan
```

Install dependencies:

```bash
pip install pygame pydantic
```

## Execution

Run the game using:

```bash
python src/pac-man.py config.json
```

# Features

* Procedural maze generation.
* Multiple configurable levels.
* Four ghost types with different behaviours.
* Pac-Gums and Super Pac-Gums.
* Power-Up mode.
* Score system.
* Persistent highscores.
* Sprite-based rendering.
* Background music support.
* Cheat mode for peer review.

---

# Configuration

The game uses a JSON configuration file.

Example:

```json
{
    "lives": 3,
    "seed": 42,
    "level_max_time": 90,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "highscore_filename": "high_score/leaderboard.json",
    "levels": [
        {
            "width": 13,
            "height": 13
        }
    ]
}
```

## Configuration Parameters

| Parameter               | Description                       | Default                     |
| ----------------------- | --------------------------------- | --------------------------- |
| lives                   | Initial player lives              | 3                           |
| seed                    | Maze generation seed              | 42                          |
| level_max_time          | Maximum time per level            | 90                          |
| points_per_pacgum       | Points awarded for Pac-Gums       | 10                          |
| points_per_super_pacgum | Points awarded for Super Pac-Gums | 50                          |
| points_per_ghost        | Points awarded for eating ghosts  | 200                         |
| highscore_filename      | Highscore file location           | high_score/leaderboard.json |
| levels                  | Maze dimensions for each level    | See config                  |

Even maze dimensions are automatically converted to odd values to ensure a valid maze center.

Large maps above 20x20 trigger a warning because maze generation may take significantly longer.

---

# Highscore

The game stores highscores in a JSON file.

The leaderboard persists between executions and records the highest scores achieved by players.

This approach was chosen because:

* It is simple and portable.
* No external database is required.
* The file can be easily inspected and backed up.
* It matches the scope of a local arcade-style game.

The leaderboard is loaded during startup and updated whenever a new highscore is achieved.

---

# Maze Generation

Maze generation is implemented using the A-Maze-ing package provided by the project.

For each level:

1. The configured dimensions are loaded.
2. A maze is generated using the selected seed.
3. Walkable cells are extracted.
4. The player is spawned at the maze center.
5. Ghosts are spawned at corner positions.
6. Pac-Gums and Super Pac-Gums are distributed across walkable cells.

The maze generator guarantees a connected and playable maze while preserving procedural variability between levels.

---

# Cheat Mode

The project includes a cheat mode intended to facilitate evaluation.

Available features include:

* Invincibility.
* Increased movement speed.
* Level skipping.
* Noclip mode (wall traversal).
* Fast navigation through large mazes.

These tools allow reviewers to quickly verify gameplay mechanics without manually completing every level.

---

# Implementation

The game is implemented using an object-oriented architecture.

Main systems include:

* Game state management.
* Player movement and collision detection.
* Ghost AI behaviours.
* Maze generation.
* Score management.
* Highscore persistence.
* Rendering and UI management.
* Configuration validation through Pydantic.

Pygame is responsible for rendering, event handling, audio playback, and timing.

Pydantic is used to validate configuration files and ensure safe runtime parameters.

---

# General Software Architecture

The project is organized into several independent modules.

## Core Components

### GameManager

Central controller responsible for:

* Game states.
* Level transitions.
* Collision handling.
* Scoring.
* Win/loss conditions.

### Maze

Stores the maze structure and provides cell access and path information.

### Player

Handles:

* Movement.
* Lives.
* Power-Up state.
* Respawn logic.

### Enemies

Ghost classes inherit from a common base class and implement individual movement strategies.

### Visualizer

Responsible for:

* Sprite rendering.
* Animation updates.
* HUD drawing.
* UI integration.

### UI System

Provides:

* Main menu.
* Pause menu.
* Victory screen.
* Game over screen.
* Leaderboard screen.
* Instructions screen.

---

# Resources

## Documentation

* Python Documentation
* Pygame Documentation
* Pydantic Documentation

## Tutorials and References

* Pac-Man gameplay analysis
* Procedural maze generation algorithms
* Object-oriented game architecture patterns

## AI Usage

Artificial Intelligence tools were used as development assistants for:

* Code reviews.
* Refactoring suggestions.
* Architecture discussions.
* Documentation drafting.
* Debugging support.
* Pydantic migration guidance.

All design decisions, implementation choices, testing, and final code integration were performed by the project authors.

---

# Project Management

The project was developed incrementally using Git version control.

Development was divided into several milestones:

1. Maze generation.
2. Player implementation.
3. Ghost implementation.
4. Rendering system.
5. Game state management.
6. Highscore persistence.
7. Cheat mode.
8. Final testing and polishing.

Project management resources can be found in:

```text
<project_management_directory>
```
