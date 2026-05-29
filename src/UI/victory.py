import pygame
from .screen import Screen
from .utils.button import Button, ButtonState
from visualizer.colors import Color
from game_manager import GameManager, State


class Victory(Screen):

    def __init__(self, game_manager, surface):
        super().__init__(game_manager, surface)

        self.player_name = ""
        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)
        self.font = pygame.font.SysFont("monospace", 24)
        self.buttons = [Button(0, 0, 200, 50, "Main Menu")]
        self.selected_index = 0

    def save_score(self):
        self.game_manager.leaderboard.add_score(
            self.player_name,
            self.game_manager.score
        )

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]

            elif event.key == pygame.K_RETURN:
                if self.game_manager.leaderboard.can_enter(self.game_manager.score):
                    self.save_score()
                self.game_manager.state = State.MENU

            elif len(self.player_name) < 10:
                if event.unicode.isalnum() or event.unicode == " ":
                    self.player_name += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    self.selected_index = i
                    if self.game_manager.leaderboard.can_enter(self.game_manager.score):
                        self.save_score()
                    self.game_manager.state = State.MENU

        elif event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.handle_event(event)

    def draw(self):

        self.screen.fill(Color.BG.rgb())

        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        title = self.title_font.render(
            "YOU WIN!!", True, Color.PLAYER_SPAWN.rgb())
        title_rect = title.get_rect(center=(cx, cy - 150))
        self.screen.blit(title, title_rect)

        score_text = self.font.render(
            f"Score: {self.game_manager.score}", True, Color.TEXT.rgb())
        score_rect = score_text.get_rect(center=(cx, cy - 60))
        self.screen.blit(score_text, score_rect)

        can_enter = self.game_manager.leaderboard.can_enter(self.game_manager.score)

        if can_enter:
            name_text = self.font.render(
                f"{self.player_name}_", True, Color.TEXT.rgb())
            name_rect = name_text.get_rect(center=(cx, cy))
            self.screen.blit(name_text, name_rect)
            self.buttons[0].rect.center = (cx, cy + 80)

        else:
            self.buttons[0].rect.center = (cx, cy + 20)

        self.buttons[0].draw(self.screen)
