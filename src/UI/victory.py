from __future__ import annotations
import pygame
from .screen import Screen, ScrollState
from .utils.button import Button
from visualizer.colors import Color
from game_manager import State


class Victory(Screen):
    from game_manager import GameManager

    def __init__(self, game_manager: GameManager,
                 surface: pygame.surface.Surface) -> None:
        super().__init__(game_manager, surface)

        self.player_name = ""
        self.buttons = [Button(0, 0, 200, 50, "Main Menu")]
        self.selected_index = 0

        # AUTOSCROLL
        self.scroll_state: ScrollState = ScrollState.WAITING
        self.scroll_timer: float = 0.0
        self.scroll_offset: float = 0.0
        self.scroll_alpha: int = 255

        # UI
        self.cursor_timer: float = 0.0
        self.cursor_visible: bool = True

        # Fonts
        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)
        self.font = pygame.font.SysFont("monospace", 24)
        self.small_font = pygame.font.SysFont("monospace", 20, bold=True)

        # Layout constants
        self.SCROLL_WINDOW_H: int = 180
        self.LINE_HEIGHT: int = 32
        self.WAIT_DURATION: float = 1.0
        self.FADE_DURATION: float = 1.0
        self.PAUSE_DURATION: float = 1.0
        self.SCROLL_SPEED: float = 50.0

    def save_score(self) -> None:
        self.game_manager.leaderboard.add_score(
            self.player_name,
            self.game_manager.score)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]

            elif event.key == pygame.K_RETURN:
                if (self.game_manager.leaderboard.can_enter(
                        self.game_manager.score)):
                    self.save_score()
                self.game_manager.state = State.MENU

            elif len(self.player_name) < 10:
                if event.unicode.isalnum() or event.unicode == " ":
                    self.player_name += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    self.selected_index = i
                    if (self.game_manager.leaderboard.can_enter(
                            self.game_manager.score)):
                        self.save_score()
                    self.game_manager.state = State.MENU

        elif event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.handle_event(event)

    def update(self, dt: float) -> None:

        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0.0

        scores = self.game_manager.leaderboard.get_scores()
        total_h = max(len(scores) * self.LINE_HEIGHT, self.SCROLL_WINDOW_H + 1)

        if self.scroll_state == ScrollState.WAITING:
            self.scroll_timer += dt
            if self.scroll_timer >= self.WAIT_DURATION:
                self.scroll_state = ScrollState.SCROLLING
                self.scroll_timer = 0.0

        elif self.scroll_state == ScrollState.SCROLLING:
            self.scroll_offset += self.SCROLL_SPEED * dt
            if self.scroll_offset >= total_h - self.SCROLL_WINDOW_H:
                self.scroll_state = ScrollState.FADING
                self.scroll_timer = 0.0

        elif self.scroll_state == ScrollState.FADING:
            self.scroll_timer += dt
            self.scroll_alpha = max(
                0,
                int(255 * (1.0 - self.scroll_timer / self.FADE_DURATION))
            )
            if self.scroll_timer >= self.FADE_DURATION:
                self.scroll_state = ScrollState.PAUSED
                self.scroll_timer = 0.0
                self.scroll_offset = 0.0

        elif self.scroll_state == ScrollState.PAUSED:
            self.scroll_timer += dt
            if self.scroll_timer >= self.PAUSE_DURATION:
                self.scroll_state = ScrollState.WAITING
                self.scroll_timer = 0.0
                self.scroll_alpha = 255

    def draw(self) -> None:

        self.screen.fill(Color.BG.rgb())

        sw = self.screen.get_width()
        cx = sw // 2

        title = self.title_font.render(
            "YOU WIN!.", True, Color.PLAYER_SPAWN.rgb())
        self.screen.blit(title, title.get_rect(center=(cx, 40)))

        # Scrore
        score_text = self.font.render(
            f"Score: {self.game_manager.score}", True, Color.TEXT.rgb())
        self.screen.blit(score_text, score_text.get_rect(center=(cx, 100)))

        # Scroll Laderboard
        scroll_x = cx - 150
        scroll_y = 140
        scroll_w = 300
        scroll_rect = pygame.Rect(scroll_x, scroll_y,
                                  scroll_w, self.SCROLL_WINDOW_H)
        pygame.draw.rect(self.screen, (20, 20, 50), scroll_rect)
        pygame.draw.rect(self.screen, Color.WALL.rgb(), scroll_rect, 1)

        scores = self.game_manager.leaderboard.get_scores()
        if scores:
            list_h = len(scores) * self.LINE_HEIGHT
            list_surf = pygame.Surface(
                (scroll_w, list_h), pygame.SRCALPHA
            )
            for i, entry in enumerate(scores):
                line = (
                    f"{i + 1:2}. "
                    f"{entry['name']:<10} "
                    f"{entry['score']:>6}"
                )
                text = self.small_font.render(
                    line, True, Color.TEXT.rgb()
                )
                text.set_alpha(self.scroll_alpha)
                list_surf.blit(text, (10, i * self.LINE_HEIGHT))

            clip_h = min(self.SCROLL_WINDOW_H, list_h)
            self.screen.blit(
                list_surf,
                (scroll_x, scroll_y),
                area=pygame.Rect(
                    0, int(self.scroll_offset), scroll_w, clip_h
                )
            )

        # Input Name
        input_y = scroll_y + self.SCROLL_WINDOW_H + 24
        can_enter = self.game_manager.leaderboard.can_enter(
            self.game_manager.score
        )

        if can_enter:
            cursor = "_" if self.cursor_visible else " "
            label = self.small_font.render(
                f"{self.player_name}{cursor}",
                True, Color.TEXT.rgb()
            )
        else:
            label = self.small_font.render(
                "Score too low for leaderboard",
                True, Color.TEXT_DIM.rgb()
            )
        self.screen.blit(label, label.get_rect(center=(cx, input_y)))

        # Button
        self.buttons[0].rect.center = (cx, input_y + 50)
        self.buttons[0].draw(self.screen)
