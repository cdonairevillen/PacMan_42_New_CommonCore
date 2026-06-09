
import pygame
from game_manager import GameManager
from visualizer.colors import Color
from .screen import Screen


class Ready(Screen):
    """
    Interstitial screen displayed after the player loses a life.

    Shows the current level, remaining lives as heart sprites,
    and a blinking 'READY!' prompt. Input is blocked for the first
    0.5 seconds to prevent accidental skips.

    Attributes:
        blink_timer: Accumulates dt to drive the blink effect.
        level_font: Font for the level indicator.
        ready_font: Font for the 'READY!' text.
        heart_full: Sprite for a remaining life.
        heart_empty: Sprite for a lost life.
    """

    HEART_SIZE: tuple[int, int] = (28, 28)
    HEART_SPACING: int = 34
    INPUT_BLOCK_DURATION: float = 0.5

    def __init__(self, game_manager: GameManager,
                 surface: pygame.Surface) -> None:
        """
        Initialise the Ready screen and load heart sprites.

        Args:
            game_manager: Shared game state.
            surface: Pygame surface to draw onto.
        """
        super().__init__(game_manager, surface)

        self.blink_timer: float = 0.0
        self.level_font: pygame.font.Font = pygame.font.SysFont(
            "monospace", 32, bold=True
        )
        self.ready_font: pygame.font.Font = pygame.font.SysFont(
            "monospace", 48, bold=True
        )

        sheet = pygame.image.load(
            "assets/lifes.png"
        ).convert_alpha()
        w = sheet.get_width() // 3
        h = sheet.get_height()

        self.heart_full: pygame.Surface = pygame.transform.scale(
            sheet.subsurface(pygame.Rect(0, 0, w, h)),
            self.HEART_SIZE,
        )
        self.heart_empty: pygame.Surface = pygame.transform.scale(
            sheet.subsurface(pygame.Rect(w * 2, 0, w, h)),
            self.HEART_SIZE,
        )

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Resume play on any key press or mouse click.

        Input is ignored for the first INPUT_BLOCK_DURATION seconds
        to prevent accidental skips right after a death.

        Args:
            event: Pygame event to process.
        """
        if self.blink_timer < self.INPUT_BLOCK_DURATION:
            return

        if (
            event.type == pygame.KEYDOWN
            or event.type == pygame.MOUSEBUTTONDOWN
        ):
            self.blink_timer = 0.0
            self.game_manager.resume()

    def update(self, dt: float) -> None:
        """
        Advance the blink timer.

        Args:
            dt: Delta time in seconds since last frame.
        """
        self.blink_timer += dt

    def draw(self) -> None:

        """Render level indicator, heart sprites, and blinking READY!."""
        self.screen.fill(Color.BG.rgb())

        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        level_text = f"Level: {self.game_manager.current_level + 1}"
        level_surf = self.level_font.render(
            level_text, True, Color.PACGUM.rgb()
        )
        level_rect = level_surf.get_rect(center=(cx, cy - 100))
        self.screen.blit(level_surf, level_rect)

        max_lives: int = min(self.game_manager.config["lives"], 18)
        lives: int = self.game_manager.player.lives
        per_row = 9
        spacing = self.HEART_SPACING
        total_rows = (max_lives + per_row - 1) // per_row

        for i in range(max_lives):
            sprite = self.heart_full if i < lives else self.heart_empty
            row = i // per_row
            col = i % per_row
            row_width = min(per_row, max_lives - row * per_row) * spacing
            start_x = cx - row_width // 2
            x = start_x + col * spacing
            y = (cy + row * (self.HEART_SIZE[1] + 4)
                 - (total_rows * (self.HEART_SIZE[1] + 4)) // 2)
            self.screen.blit(sprite, (x, y))

        if (self.blink_timer % 1.0) < 0.5:
            ready_surf = self.ready_font.render(
                "READY!", True, Color.PLAYER_SPAWN.rgb()
            )
            ready_rect = ready_surf.get_rect(center=(cx, cy + 80))
            self.screen.blit(ready_surf, ready_rect)
