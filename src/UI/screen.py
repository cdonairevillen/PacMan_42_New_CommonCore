
from game_manager import GameManager
from abc import ABC, abstractmethod
from enum import Enum
import pygame


class ScrollState(Enum):
    WAITING = "waiting"
    SCROLLING = "scrolling"
    FADING = "fading"
    PAUSED = "paused"


class Screen(ABC):

    def __init__(self, game_manager: GameManager,
                 surface: pygame.surface.Surface) -> None:
        self.game_manager: GameManager = game_manager
        self.screen = surface
        self.player_name = ""
        self.player_timer = 0.0

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass
