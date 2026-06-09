import pygame
from game_manager import State, GameManager
from visualizer.colors import Color
from .utils.button import Button, ButtonState
from .screen import Screen


class UILeader(Screen):

    LINE_HEIGHT: int = 35
    SCROLL_WINDOW_H: int = 300
    SCROLL_SPEED: int = 35

    def __init__(self, game_manager: GameManager,
                 surface: pygame.surface.Surface) -> None:
        super().__init__(game_manager, surface)

        self.font = pygame.font.SysFont("monospace", 24, bold=False)
        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)
        self.button = Button(0, 0, 200, 50, "Back")
        self.selected = True
        self.scroll_offset: int = 0

    def max_scroll(self) -> int:
        """Return the maximum scroll offset in pixels."""
        scores = self.game_manager.leaderboard.get_scores()
        total_h = len(scores) * self.LINE_HEIGHT
        return max(0, total_h - self.SCROLL_WINDOW_H)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE,
                             pygame.K_ESCAPE):
                self.game_manager.state = State.MENU

            elif event.key == pygame.K_DOWN:
                if self.scroll_offset < self.max_scroll():
                    self.scroll_offset = min(
                        self.scroll_offset + self.SCROLL_SPEED,
                        self.max_scroll()
                    )
                else:
                    self.selected = True

            elif event.key == pygame.K_UP:
                if self.scroll_offset > 0:
                    self.scroll_offset = max(
                        0, self.scroll_offset - self.SCROLL_SPEED
                    )

        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(
                0,
                min(
                    self.scroll_offset - event.y * self.SCROLL_SPEED,
                    self.max_scroll()
                )
            )

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.is_clicked(event):
                self.game_manager.state = State.MENU

        elif event.type == pygame.MOUSEMOTION:
            self.selected = False
            self.button.handle_event(event)

    def draw(self) -> None:
        self.screen.fill(Color.BG.rgb())

        cx = self.screen.get_width() // 2

        title = self.title_font.render(
            "LEADERBOARD", True, Color.PACGUM.rgb()
        )
        self.screen.blit(title, title.get_rect(center=(cx, 40)))

        # scroll window
        scores = self.game_manager.leaderboard.get_scores()
        content_x = 40
        content_w = self.screen.get_width() - 80
        scroll_y = 100
        scroll_rect = pygame.Rect(
            content_x, scroll_y, content_w, self.SCROLL_WINDOW_H
        )
        pygame.draw.rect(self.screen, (20, 20, 50), scroll_rect)
        pygame.draw.rect(self.screen, Color.WALL.rgb(), scroll_rect, 1)

        if scores:
            total_h = len(scores) * self.LINE_HEIGHT
            list_surf = pygame.Surface(
                (content_w, max(total_h, 1)), pygame.SRCALPHA
            )
            for i, entry in enumerate(scores):
                line = (
                    f"{i + 1:2}.  "
                    f"{entry['name']:<10}  "
                    f"{entry['score']:>6}"
                )
                text = self.font.render(line, True, Color.TEXT.rgb())
                list_surf.blit(text, (10, i * self.LINE_HEIGHT))

            clip_h = min(self.SCROLL_WINDOW_H, total_h)
            self.screen.blit(
                list_surf,
                (content_x, scroll_y),
                area=pygame.Rect(
                    0, self.scroll_offset, content_w, clip_h
                )
            )

            if total_h > self.SCROLL_WINDOW_H:
                bar_h = int(
                    self.SCROLL_WINDOW_H
                    * self.SCROLL_WINDOW_H / total_h
                )
                bar_y = scroll_y + int(
                    self.scroll_offset / total_h * self.SCROLL_WINDOW_H
                )
                pygame.draw.rect(
                    self.screen,
                    Color.TEXT_DIM.rgb(),
                    pygame.Rect(
                        content_x + content_w - 6, bar_y, 4, bar_h
                    )
                )

        # back button
        back_y = scroll_y + self.SCROLL_WINDOW_H + 30
        self.button.rect.center = (cx, back_y)
        if self.selected:
            self.button.state = ButtonState.SELECTED
        else:
            self.button.state = ButtonState.NORMAL
        self.button.draw(self.screen)
