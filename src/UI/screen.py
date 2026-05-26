from __future__ import annotations
from game_manager import GameManager
from abc import ABC, abstractmethod


class Screen(ABC):

    def __init__(self, game_manager: GameManager, surface):
        self.game_manager: GameManager = game_manager
        self.screen = surface

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_events(self, event):
        pass

    def update(self):          # si queremos meter animaciones
        pass
