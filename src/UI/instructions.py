from __future__ import annotations
import pygame
from game_manager import GameManager, State
from visualizer.colors import Color
from .screen import Screen
from .utils.button import Button, ButtonState


class Instructions(Screen):
    """
    Two-tab instructions screen accessible from the main menu.

    Tab 0 shows game controls, tab 1 shows rules and scoring.
    Left/Right arrows or tab buttons switch between tabs.
    Up/Down arrows or the Back button return to the main menu.
    Both tabs support keyboard and mouse wheel scrolling.

    Attributes:
        selected_tab: Index of the currently active tab (0 or 1).
        font: Body text font.
        title_font: Tab title font.
        tab_buttons: List of two tab selector buttons.
        back_button: Button to return to the main menu.
        selected_button: Which button has keyboard focus (0-2).
        scroll_offset: Current vertical scroll offset in pixels.
    """

    TABS: list[str] = ["Controls", "Rules"]

    CONTROLS: list[str] = [
        "Movement      WASD  /  Arrow Keys",
        "Pause         P",
        "Cheat mode    C",
        "  Skip level    N  (cheat only)",
        "  Noclip        V  (cheat only)",
        "  +1000 pts     I  (cheat only)",
        "Quit          ESC",
    ]

    LINE_HEIGHT: int = 30
    SCROLL_SPEED: int = 30
    SCROLL_WINDOW_H: int = 260

    def __init__(self, game_manager: GameManager,
                 surface: pygame.Surface) -> None:
        """
        Initialise the Instructions screen.

        Args:
            game_manager: Shared game state.
            surface: Pygame surface to draw onto.
        """
        super().__init__(game_manager, surface)

        self.selected_tab: int = 0
        self.selected_button: int = 0
        self.scroll_offset: int = 0

        self.font: pygame.font.Font = pygame.font.SysFont(
            "monospace", 18
        )
        self.title_font: pygame.font.Font = pygame.font.SysFont(
            "monospace", 28, bold=True
        )

        self.tab_buttons: list[Button] = [
            Button(0, 0, 160, 40, tab) for tab in self.TABS
        ]
        self.back_button: Button = Button(0, 0, 160, 40, "Back")

    def rules(self) -> list[str]:
        """
        Build the rules list dynamically from config values.

        Returns:
            List of strings for the Rules tab.
        """
        cfg = self.game_manager.config
        ppg = cfg.get("points_per_pacgum", 10)
        pps = cfg.get("points_per_super_pacgum", 50)
        ppgh = cfg.get("points_per_ghost", 200)
        lives = cfg.get("lives", 3)
        max_time = cfg.get("level_max_time", 90)
        levels = len(cfg.get("levels", []))

        return [
            "Eat all pac-gums to complete a level.",
            "Avoid ghosts — each hit costs one life.",
            "Eat a super pac-gum to frighten ghosts.",
            "Frightened ghosts can be eaten for points.",
            "The game ends when all lives are lost.",
            "Complete all levels to win.",
            "",
            f"Starting lives:   {lives}",
            f"Levels:           {levels}",
            f"Time per level:   {max_time}s",
            "",
            "Scoring:",
            f"  Pac-gum         +{ppg} pts",
            f"  Super pac-gum   +{pps} pts",
            f"  Ghost (eaten)   +{ppgh} pts",
        ]

    def activate_selected(self) -> None:
        """Activate the currently focused button."""
        if self.selected_button < len(self.tab_buttons):
            self.selected_tab = self.selected_button
            self.scroll_offset = 0
        else:
            self.game_manager.state = State.MENU

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Handle keyboard and mouse input.

        Left/Right switch tabs. Up/Down scroll content or move
        focus to Back. Mouse wheel scrolls content.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selected_tab = (
                    self.selected_tab + 1
                ) % len(self.TABS)
                self.selected_button = self.selected_tab
                self.scroll_offset = 0

            elif event.key == pygame.K_LEFT:
                self.selected_tab = (
                    self.selected_tab - 1
                ) % len(self.TABS)
                self.selected_button = self.selected_tab
                self.scroll_offset = 0

            elif event.key == pygame.K_DOWN:
                if self.scroll_offset < self.max_scroll():
                    self.scroll_offset = min(
                        self.scroll_offset + self.SCROLL_SPEED,
                        self.max_scroll())
                else:
                    self.selected_button = len(self.tab_buttons)

            elif event.key == pygame.K_UP:
                if self.selected_button == len(self.tab_buttons):
                    self.selected_button = self.selected_tab
                else:
                    self.scroll_offset = max(0,
                                             self.scroll_offset
                                             - self.SCROLL_SPEED)

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.activate_selected()

            elif event.key == pygame.K_ESCAPE:
                self.game_manager.state = State.MENU

        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(
                0,
                min(
                    self.scroll_offset - event.y * self.SCROLL_SPEED,
                    self.max_scroll()
                )
            )

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, btn in enumerate(self.tab_buttons):
                if btn.is_clicked(event):
                    self.selected_tab = i
                    self.selected_button = i
                    self.scroll_offset = 0

            if self.back_button.is_clicked(event):
                self.game_manager.state = State.MENU

        elif event.type == pygame.MOUSEMOTION:
            for btn in self.tab_buttons:
                btn.handle_event(event)
            self.back_button.handle_event(event)

    def update(self, dt: float) -> None:
        """No animation needed for this screen."""
        pass

    def max_scroll(self) -> int:
        """
        Calculate the maximum scroll offset for the active tab.

        Returns:
            Maximum scroll offset in pixels, floored at 0.
        """
        lines = (self.CONTROLS
                 if self.selected_tab == 0
                 else self.rules())
        total_h = len(lines) * self.LINE_HEIGHT
        return max(0, total_h - self.SCROLL_WINDOW_H)

    def draw(self) -> None:
        """Render the active tab content and navigation buttons."""
        self.screen.fill(Color.BG.rgb())

        cx = self.screen.get_width() // 2
        sw = self.screen.get_width()

        tab_spacing = 180
        tab_y = 40

        for i, btn in enumerate(self.tab_buttons):
            btn.rect.center = (
                cx - tab_spacing // 2 + i * tab_spacing,
                tab_y,
            )
            if i in (self.selected_tab, self.selected_button):
                btn.state = ButtonState.SELECTED
            else:
                btn.state = ButtonState.NORMAL
            btn.draw(self.screen)

        title_surf = self.title_font.render(
            self.TABS[self.selected_tab], True, Color.TEXT.rgb()
        )
        self.screen.blit(
            title_surf, title_surf.get_rect(center=(cx, tab_y + 50))
        )

        lines = (
            self.CONTROLS
            if self.selected_tab == 0
            else self.rules()
        )

        content_x = 40
        content_w = sw - 80
        content_y = tab_y + 80
        scroll_rect = pygame.Rect(
            content_x, content_y, content_w, self.SCROLL_WINDOW_H
        )
        pygame.draw.rect(self.screen, (20, 20, 50), scroll_rect)
        pygame.draw.rect(
            self.screen, Color.WALL.rgb(), scroll_rect, 1
        )

        total_h = len(lines) * self.LINE_HEIGHT
        list_surf = pygame.Surface(
            (content_w, max(total_h, 1)), pygame.SRCALPHA
        )

        for i, line in enumerate(lines):
            color = (
                Color.TEXT.rgb() if line and not line.startswith(" ")
                else Color.TEXT_DIM.rgb()
            )
            surf = self.font.render(line, True, color)
            list_surf.blit(surf, (10, i * self.LINE_HEIGHT))

        clip_h = min(self.SCROLL_WINDOW_H, total_h)
        self.screen.blit(
            list_surf,
            (content_x, content_y),
            area=pygame.Rect(0, self.scroll_offset, content_w, clip_h)
        )

        # scroll indicator
        if total_h > self.SCROLL_WINDOW_H:
            bar_h = int(
                self.SCROLL_WINDOW_H
                * self.SCROLL_WINDOW_H / total_h
            )
            bar_y = content_y + int(
                self.scroll_offset
                / total_h
                * self.SCROLL_WINDOW_H
            )
            pygame.draw.rect(
                self.screen,
                Color.TEXT_DIM.rgb(),
                pygame.Rect(
                    content_x + content_w - 6,
                    bar_y, 4, bar_h
                )
            )

        back_y = content_y + self.SCROLL_WINDOW_H + 30
        self.back_button.rect.center = (cx, back_y)
        if self.selected_button == len(self.tab_buttons):
            self.back_button.state = ButtonState.SELECTED
        else:
            self.back_button.state = ButtonState.NORMAL
        self.back_button.draw(self.screen)
