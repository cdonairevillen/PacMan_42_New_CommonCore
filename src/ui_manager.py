
import pygame
from game_manager import GameManager, State
from UI.main_menu import MainMenu
from UI.pause_menu import PauseMenu
from UI.game_over import GameOver
from UI.victory import Victory
from UI.ready import Ready
from UI.leaderboard_menu import UILeader
from UI.instructions import Instructions
from UI.game_screen import GameScreen


class UIManager:
    """
    Routes pygame events and draw calls to the active Screen.

    Observes GameManager.state each frame and activates the matching
    Screen. The visualizer delegates all non-gameplay rendering here.

    Attributes:
        game_manager: Shared game state.
        surface: Pygame surface passed to each screen.
        screens: Mapping of State -> Screen instance.
        current_screen: The screen currently being rendered.
    """

    def __init__(self, game_manager: GameManager,
                 surface: pygame.Surface, visualizer: object) -> None:
        """
        Initialise all screens and set the initial active screen.

        Args:
            game_manager: Shared game state.
            surface: Pygame surface to render onto.
        """
        self.game_manager: GameManager = game_manager
        self.surface: pygame.Surface = surface

        self.screens = {
            State.MENU: MainMenu(game_manager, surface),
            State.PAUSED: PauseMenu(game_manager, surface),
            State.GAME_OVER: GameOver(game_manager, surface),
            State.VICTORY: Victory(game_manager, surface),
            State.READY: Ready(game_manager, surface),
            State.LEADERBOARD: UILeader(game_manager, surface),
            State.INSTRUCTIONS: Instructions(game_manager, surface),
            State.PLAYING: GameScreen(game_manager, surface, visualizer),
            State.LOADING: GameScreen(game_manager, surface, visualizer)
        }

        self.current_screen = self.screens[State.MENU]

    def update(self, dt: float = 0.0) -> None:
        """
        Sync the active screen to the current game state.

        Also forwards dt to the active screen so animations
        like the READY blink can advance independently.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        state = self.game_manager.state

        if state != getattr(self, '_last_state', None):
            if state in (State.GAME_OVER, State.VICTORY):
                self.screens[state].player_name = ""
                self.screens[state].player_timer = 0.0
            self._last_state = state

        if state in self.screens:
            self.current_screen = self.screens[state]
        else:
            self.current_screen = None  # type: ignore[assignment]

        if self.current_screen is not None:
            self.current_screen.update(dt)

    def draw(self) -> None:
        """Delegate drawing to the active screen."""
        if self.current_screen is not None:
            self.current_screen.draw()

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Forward a pygame event to the active screen.

        Args:
            event: Pygame event to process.
        """
        if self.current_screen is not None:
            self.current_screen.handle_events(event)
