from game_manager import GameManager, State
from UI.main_menu import MainMenu
from UI.pause_menu import PauseMenu
from UI.game_over import GameOver
from UI.victory import Victory
from UI.leaderboard_menu import UILeader
import pygame


class UIManager():

    def __init__(self, game_manager: GameManager, surface: pygame.Surface):

        self.game_manager = game_manager
        self.surface = surface
        self.screens = {
            State.MENU: MainMenu(game_manager, surface),
            State.PAUSED: PauseMenu(game_manager, surface),
            State.GAME_OVER: GameOver(game_manager, surface),
            State.VICTORY: Victory(game_manager, surface),
            State.LEADERBOARD: UILeader(game_manager, surface)
        }
        self.current_screen = self.screens[State.MENU]

    def update(self):
        state = self.game_manager.state

        if state in self.screens:
            self.current_screen = self.screens[state]

        else:
            self.current_screen = None

    def draw(self):
        if self.current_screen is not None:
            self.current_screen.draw()

    def handle_event(self, event):
        if self.current_screen is not None:
            self.current_screen.handle_events(event)
