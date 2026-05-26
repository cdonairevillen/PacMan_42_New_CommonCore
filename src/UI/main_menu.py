import pygame
import sys
from .screen import Screen
from .utils.button import Button, ButtonState
from visualizer.colors import Color
from game_manager import GameManager, State


class MainMenu(Screen):

    def __init__(self, game_manager, surface):
        super().__init__(game_manager, surface)

        self.selected_index = 0
        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)
        self.buttons = [Button(0, 0, 200, 50, "Start Game"),
                        Button(0, 0, 200, 50, "High Scores"),
                        Button(0, 0, 200, 50, "Instructions"),
                        Button(0, 0, 200, 50, "Exit")]

    def activate_selected(self):
        if self.selected_index == 0:
            self.game_manager.reset()
            self.game_manager.state = State.PLAYING

        elif self.selected_index == 3:
            pygame.quit()
            sys.exit(0)

    def handle_events(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)

            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.activate_selected()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    self.selected_index = i
                    self.activate_selected()

        elif event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.handle_event(event)

    def draw(self):
        self.screen.fill(Color.BG.rgb())

        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        title = self.title_font.render("PAC-MAN", True, Color.PACGUM.rgb())
        title_rect = title.get_rect(center=(cx, cy - 150))
        self.screen.blit(title, title_rect)

        button_spacing = 70

        for i, button in enumerate(self.buttons):
            button.rect.center = (cx, cy + i * button_spacing)

            if i == self.selected_index:
                button.state = ButtonState.SELECTED

            button.draw(self.screen)
