
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

    Attributes:
        selected_tab: Index of the currently active tab (0 or 1).
        font: Body text font.
        title_font: Tab title font.
        tab_buttons: List of two tab selector buttons.
        back_button: Button to return to the main menu.
        selected_button: Which button has keyboard focus (0-2).
    """

    TABS: list[str] = ["Controls", "Rules"]

    CONTROLS: list[str] = [
        "Movement      WASD  /  Arrow Keys",
        "Pause         P",
        "Cheat mode    C",
        "Quit          ESC",
    ]

    RULES: list[str] = [
        "Eat all pac-gums to complete the level.",
        "Avoid ghosts — they cost you a life.",
        "Eat a super pac-gum to frighten ghosts.",
        "Frightened ghosts can be eaten for bonus points.",
        "The game ends when all lives are lost.",
        "Complete all levels to win.",
        "",
        "Scoring:",
        "  Pac-gum         +10 pts",
        "  Super pac-gum   +50 pts",
        "  Ghost (eaten)  +200 pts",
    ]

    def __init__(
        self,
        game_manager: GameManager,
        surface: pygame.Surface,
    ) -> None:
        """
        Initialise the Instructions screen.

        Args:
            game_manager: Shared game state.
            surface: Pygame surface to draw onto.
        """
        super().__init__(game_manager, surface)

        self.selected_tab: int = 0
        self.selected_button: int = 0

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

    def activate_selected(self) -> None:
        """Activate the currently focused button."""
        if self.selected_button < len(self.tab_buttons):
            self.selected_tab = self.selected_button
        else:
            self.game_manager.state = State.MENU

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Handle keyboard and mouse input.

        Left/Right switch tabs. Up/Down move focus to Back.
        Enter/Space activates the focused button.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selected_tab = (
                    self.selected_tab + 1
                ) % len(self.TABS)
                self.selected_button = self.selected_tab

            elif event.key == pygame.K_LEFT:
                self.selected_tab = (
                    self.selected_tab - 1
                ) % len(self.TABS)
                self.selected_button = self.selected_tab

            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                if self.selected_button < len(self.tab_buttons):
                    self.selected_button = len(self.tab_buttons)
                else:
                    self.selected_button = self.selected_tab

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.activate_selected()

            elif event.key == pygame.K_ESCAPE:
                self.game_manager.state = State.MENU

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, btn in enumerate(self.tab_buttons):
                if btn.is_clicked(event):
                    self.selected_tab = i
                    self.selected_button = i

            if self.back_button.is_clicked(event):
                self.game_manager.state = State.MENU

        elif event.type == pygame.MOUSEMOTION:
            for btn in self.tab_buttons:
                btn.handle_event(event)
            self.back_button.handle_event(event)

    def draw(self) -> None:
        """Render the active tab content and navigation buttons."""
        self.screen.fill(Color.BG.rgb())

        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        tab_spacing = 180
        tab_y = cy - 160
        for i, btn in enumerate(self.tab_buttons):
            btn.rect.center = (
                cx - tab_spacing // 2 + i * tab_spacing,
                tab_y,
            )
            if i == self.selected_tab:
                btn.state = ButtonState.SELECTED
            elif i == self.selected_button:
                btn.state = ButtonState.SELECTED
            else:
                btn.state = ButtonState.NORMAL
            btn.draw(self.screen)

        title_surf = self.title_font.render(
            self.TABS[self.selected_tab],
            True,
            Color.TEXT.rgb(),
        )
        title_rect = title_surf.get_rect(center=(cx, tab_y + 55))
        self.screen.blit(title_surf, title_rect)

        lines = (
            self.CONTROLS
            if self.selected_tab == 0
            else self.RULES
        )
        line_y = tab_y + 90
        for line in lines:
            surf = self.font.render(line, True, Color.TEXT_DIM.rgb())
            rect = surf.get_rect(midleft=(cx - 180, line_y))
            self.screen.blit(surf, rect)
            line_y += 28

        self.back_button.rect.center = (cx, cy + 180)
        if self.selected_button == len(self.tab_buttons):
            self.back_button.state = ButtonState.SELECTED
        else:
            self.back_button.state = ButtonState.NORMAL
        self.back_button.draw(self.screen)
