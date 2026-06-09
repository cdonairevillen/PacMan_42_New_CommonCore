import pygame
from .screen import Screen
from .utils.button import Button, ButtonState
from visualizer.colors import Color
from game_manager import GameManager, State


class PauseMenu(Screen):

    def __init__(self, game_manager: GameManager, surface: pygame.Surface):
        super().__init__(game_manager, surface)

        self.selected_index = 0
        self.panel_width = 300
        self.panel_height = 200
        self.font = pygame.font.SysFont("monospace", 24, bold=True)
        self.buttons = [Button(0, 0, 200, 50, "Resume"),
                        Button(0, 0, 200, 50, "Main Menu")]

    def activate_selected(self) -> None:
        if self.selected_index == 0:
            self.game_manager.state = State.PLAYING

        elif self.selected_index == 1:
            self.game_manager.state = State.MENU

    def handle_events(self, event: pygame.event.Event) -> None:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (
                    self.selected_index + 1) % len(self.buttons)

            elif event.key == pygame.K_UP:
                self.selected_index = (
                    self.selected_index - 1) % len(self.buttons)

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

    def draw(self) -> None:
        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(0, 0, self.panel_width, self.panel_height)
        panel_rect.center = (cx, cy)
        pygame.draw.rect(self.screen, Color.BLOCKED.rgb(), panel_rect)
        pygame.draw.rect(self.screen, Color.WALL.rgb(), panel_rect, 2)

        title = self.font.render("PAUSED", True, Color.TEXT.rgb())
        title_rect = title.get_rect(center=(cx, cy - 60))
        self.screen.blit(title, title_rect)

        for i, button in enumerate(self.buttons):
            button.rect.center = (cx, cy + i * 60)

            if i == self.selected_index:
                button.state = ButtonState.SELECTED

            else:
                button.state = ButtonState.NORMAL

            button.draw(self.screen)
