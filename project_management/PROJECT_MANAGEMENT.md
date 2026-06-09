# Project Management

## Project Timeline

The project was planned for approximately one month, starting April 26th and targeting delivery around May 26th. The final delivery took place on June 9th, roughly two weeks later than originally estimated.

### Planned vs Actual

| Milestone | Planned | Actual |
|---|---|---|
| Parser, player, enemy base | Week 1 | Apr 26 – May 6 |
| Visualizer + GameManager | Week 1–2 | May 5 – May 13 |
| Enemies in game, Pac-Gums | Week 2 | May 14 – May 20 |
| Menus, cheat mode, sprites | Week 2–3 | May 26 – May 27 |
| Makefile, movement fixes | Week 3 | May 29 – Jun 4 |
| Screens, documentation, polish | Week 3–4 | Jun 4 – Jun 9 |

### Gantt

```
Task                          | Apr 26 | May 5 | May 13 | May 19 | May 26 | May 29 | Jun 4 | Jun 9
------------------------------|--------|-------|--------|--------|--------|--------|-------|------
Parser (roherna2)             |████████|█      |        |        |        |        |       |
Player + Enemy base (roherna2)|████████|███████|        |        |        |        |       |
Visualizer (cdonaire)         |████████|████   |        |        |        |        |       |
GameManager (cdonaire)        |        |       |████████|        |        |        |       |
Enemy variants (roherna2)     |        |       |        |████    |        |        |       |
Pac-Gums (cdonaire)           |        |       |        |████    |        |        |       |
Enemies in game (cdonaire)    |        |       |        |    ████|        |        |       |
Cheat mode (roherna2)         |        |       |        |        |████    |        |       |
Sprites (roherna2)            |        |       |        |        |    ████|        |       |
Makefile (cdonaire)           |        |       |        |        |        |██      |       |
Movement fixes (cdonaire)     |        |       |        |        |        |████████|       |
Visual/sprite fixes (roherna2)|        |       |        |        |        |████████|       |
Screens (cdonaire)            |        |       |        |        |        |        |██████ |
README (roherna2)             |        |       |        |        |        |        |       |██
```

---

## Project Decisions

### Pydantic for configuration validation
**Decision:** Use Pydantic BaseModels to validate the JSON configuration file.

**Alternatives considered:** Manual key checking with `dict.get()` and type assertions.

**Reason:** Pydantic provides cleaner validation with automatic type coercion, descriptive error messages, and reduces boilerplate. The switch from manual parsing to BaseModels was made mid-project after realising the manual approach was fragile.

---

### JSON highscore storage
**Decision:** Store the leaderboard in a local JSON file.

**Alternatives considered:** SQLite database, in-memory only.

**Reason:** Simple, portable, and sufficient for project requirements. No external dependencies. The file can be inspected and backed up easily. Matches the scope of a local arcade-style game.

---

### State-based architecture via GameManager
**Decision:** Centralise all game state transitions in a single `GameManager` class using a `State` enum.

**Alternatives considered:** Distributing state across individual screen classes.

**Reason:** A single source of truth for state avoids synchronisation bugs between components. All transitions (MENU → LOADING → READY → PLAYING → PAUSED → GAME_OVER / VICTORY) are explicit and traceable.

---

### Separation of rendering and logic
**Decision:** Keep `MazeVisualizer` as a pure renderer delegating to `UIManager` and `GameScreen`, with `GameManager` owning all game logic.

**Alternatives considered:** Mixing rendering and logic in a single class.

**Reason:** Easier to test and modify independently. Changes to the UI do not risk breaking game logic.

---

### Pixel-based movement interpolation
**Decision:** Give each entity a logical grid position and a visual pixel position, updated independently each frame.

**Alternatives considered:** Discrete cell-to-cell movement with no interpolation; full free-movement physics.

**Reason:** Discrete movement is jarring visually. Full free-movement requires wall collision in pixel space, which is significantly more complex. Interpolated grid movement gives smooth visuals while keeping collision logic simple.

---

### Cheat mode implementation
**Decision:** Implement a dedicated `CheatMode` dataclass with invincibility, speed boost, noclip, level skip, and score injection.

**Reason:** Facilitates peer review. Reviewers can quickly verify all gameplay mechanics without manually completing every level.

---

## Risk Analysis

### Maze generation performance
**Risk:** Large mazes may require significant generation time, blocking the main thread.

**Likelihood:** Medium (only affects configs with maps > 20×20).

**Mitigation:** Added a warning prompt for maps larger than 20×20. Players can opt to cap all large levels at 19×19.

---

### Collision detection reliability
**Risk:** Incorrect interaction between player and ghosts due to mismatch between logical and visual positions.

**Likelihood:** High during development.

**Mitigation:** Switched from logical cell comparison to visual distance thresholds. Dedicated debugging sessions with position logging.

---

### State management inconsistencies
**Risk:** Inconsistent transitions between game states causing screens to appear at wrong times or logic to run in wrong states.

**Likelihood:** Medium.

**Mitigation:** Centralised all state transitions through `GameManager`. Added `loading_reason` to distinguish death respawn from level transition.

---

### Platform compatibility
**Risk:** Game developed on Windows, evaluated on Linux (42 cluster).

**Likelihood:** Low for core logic, medium for path separators and file access.

**Mitigation:** Used `os.path.join` for all file paths. Tested on cluster before submission. Switched from `pygame` to `pygame-ce` for `pygame.Window` support.

---

## Team Organization

### cdonaire
- GameManager architecture and state machine.
- Visualizer and rendering pipeline.
- UI screens (MainMenu, PauseMenu, GameOver, Victory, Ready, Instructions, Leaderboard).
- HUD system.
- Pac-Gum placement and collection.
- Enemy integration into the game loop.
- Makefile and packaging.
- Pixel-based movement interpolation.
- Fullscreen and window resize support.
- Collision detection fixes.
- Level transition system.

### roherna2
- Configuration parser (Pydantic migration).
- Player class and movement.
- Enemy base class and four ghost variants with individual AI.
- Cheat mode (invincibility, speed boost, noclip, level skip).
- Sprite integration (player and ghost sprite sheets).
- Visual polish and sprite alignment fixes.
- Project documentation and README.

### Collaboration
Most architectural decisions were discussed together before implementation. The GameManager integration, collision fixes, and final bug resolution required active collaboration between both members. The final week was fully collaborative, with both members working together to identify and fix remaining issues.

---

## Blocking Points and Conflicts

### pygame.Window API differences between pygame and pygame-ce
**Description:** `pygame.Window` is not available in standard `pygame`. Discovered when deploying to the 42 cluster.

**Resolution:** Switched the project dependency from `pygame` to `pygame-ce`, which is API-compatible and adds `pygame.Window`.

---

### Ghost double-consumption bug
**Description:** When multiple ghosts occupied the same cell during a power-up, eating one ghost triggered the collision logic for the other in the same frame, causing velocity multiplication.

**Resolution:** Added a per-enemy `eat_cooldown` timer that prevents a ghost from being consumed again within 0.5 seconds of the previous consumption.

---

### Pixel movement interpolation artifacts
**Description:** Transitioning from discrete cell movement to pixel interpolation introduced visual drift when the player was stationary against a wall. The interpolation would animate between the previous and current cell even when no movement occurred.

**Resolution:** Added a check to skip interpolation when the previous and target positions are identical.

---

### State transition ordering
**Description:** The LOADING state needed to distinguish between a death respawn and a level transition, as the two require different setup (reset enemy positions vs rebuild level). Using a single LOADING state for both caused incorrect behaviour.

**Resolution:** Added `loading_reason` attribute (`"death"`, `"level"`, `"start"`) to drive different behaviour inside the LOADING update block.

---

## Acceptance Test Plan

### Features Tested

| Feature | Result |
|---|---|
| Maze generation | ✓ Pass |
| Player movement (WASD + arrows) | ✓ Pass |
| Wall collision | ✓ Pass |
| Pac-Gum collection | ✓ Pass |
| Super Pac-Gum and Power-Up mode | ✓ Pass |
| Ghost AI (Red, Pink, Blue, Orange) | ✓ Pass |
| Ghost fear state | ✓ Pass |
| Ghost consumption during Power-Up | ✓ Pass |
| Level transition | ✓ Pass |
| Victory condition | ✓ Pass |
| Game over condition | ✓ Pass |
| Lives system | ✓ Pass |
| Timer countdown | ✓ Pass |
| Score system | ✓ Pass |
| Highscore persistence | ✓ Pass |
| Leaderboard display | ✓ Pass |
| Main menu navigation | ✓ Pass |
| Pause menu | ✓ Pass |
| Instructions screen | ✓ Pass |
| Cheat mode (C key) | ✓ Pass |
| Invincibility | ✓ Pass |
| Speed boost | ✓ Pass |
| Noclip (V key) | ✓ Pass |
| Level skip (N key) | ✓ Pass |
| Score injection (I key) | ✓ Pass |
| Fullscreen toggle (F11) | ✓ Pass |
| Window resize | ✓ Pass |
| Config file validation | ✓ Pass |

### Bugs Found and Fixed

| Bug | Status |
|---|---|
| Ghost fear state not restored after respawn | Fixed |
| Player trapped inside walls after disabling noclip | Fixed |
| Level skip not rebuilding the maze | Fixed |
| Double ghost consumption in same frame causing speed multiplication | Fixed |
| Movement interpolation drift when stationary | Fixed |
| State transition showing wrong screen between levels | Fixed |
| Mouse click coordinates offset after window resize | Fixed |
| Leaderboard name persisting between games | Fixed |

---

## Project Retrospective

### What worked well
- Modular architecture made it easy to work in parallel without conflicts.
- Separation between game logic and rendering.
- Configuration system allowed quick iteration on level parameters.
- Git version control prevented data loss during refactoring.

### Challenges
- Ghost state transitions required multiple iterations to stabilise.
- Pixel-based movement introduced subtle timing bugs that took significant time to diagnose.
- pygame.Window API compatibility between pygame and pygame-ce was an unexpected blocker.

### Lessons Learned
- Define state machine transitions explicitly before implementation.
- Test on the target platform early.
- Incremental testing after each feature reduces bug accumulation.
- Clear separation of rendering and logic simplifies debugging significantly.
