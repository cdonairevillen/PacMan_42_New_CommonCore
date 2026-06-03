import pygame
from game_manager import State
from visualizer.colors import Color
from .utils.button import Button, ButtonState
from .screen import Screen


class UILeader(Screen):
    def __init__(self, game_manager, surface):
        super().__init__(game_manager, surface)

        self.font = pygame.font.SysFont("monospace", 24, bold=False)
        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)
        self.button = Button(0, 0, 200, 50, "Back")
        self.selected = True

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.is_clicked(event):
                self.game_manager.state = State.MENU
        elif event.type == pygame.KEYDOWN:
            self.selected = True
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.game_manager.state = State.MENU
        elif event.type == pygame.MOUSEMOTION:
            self.selected = False
            self.button.handle_event(event)

    def draw(self):

        self.screen.fill(Color.BG.rgb())

        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        title = self.title_font.render("LEADERBOARD", True, Color.PACGUM.rgb())
        title_rect = title.get_rect(center=(cx, cy - 150))
        self.screen.blit(title, title_rect)

        for i, entry in enumerate(self.game_manager.leaderboard.get_scores()):
            line = f"{i + 1}.  {entry['name']:<10}  {entry['score']}"
            text = self.font.render(line, True, Color.TEXT.rgb())
            self.screen.blit(text, (cx - 150, cy - 80 + i * 35))

        if self.selected:
            self.button.state = ButtonState.SELECTED

        else:
            self.button.state = ButtonState.NORMAL

        self.button.rect.center = (cx, cy + 210)
        self.button.draw(self.screen)
