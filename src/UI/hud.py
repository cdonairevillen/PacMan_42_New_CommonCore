
import pygame
from game_manager import GameManager
from visualizer.colors import Color


HUD_HEIGHT: int = 56
HEART_SIZE: tuple[int, int] = (24, 24)
HEART_SPACING: int = 30


class HUD:
    """
    In-game heads-up display rendered below the maze.

    Draws three zones on a dark bar:
      Left   — heart sprites for remaining lives.
      Centre — digital-style MM:SS countdown timer in green.
      Right  — current score.

    Attributes:
        game_manager: Shared game state.
        surface: Pygame surface to draw onto.
        font_score: Font for score and level labels.
        font_clock: Larger monospace font for the digital timer.
        heart_full: Sprite for a remaining life.
        heart_empty: Sprite for a lost life.
    """

    def __init__(self, game_manager: GameManager,
                 surface: pygame.Surface) -> None:
        """
        Initialise the HUD and load heart sprites.

        Args:
            game_manager: Shared game state.
            surface: Pygame surface to draw onto.
        """
        self.game_manager: GameManager = game_manager
        self.surface: pygame.Surface = surface

        self.font_score: pygame.font.Font = pygame.font.SysFont(
            "monospace", 16, bold=True
        )
        self.font_clock: pygame.font.Font = pygame.font.SysFont(
            "monospace", 28, bold=True
        )

        sheet = pygame.image.load(
            "assets/lifes.png"
        ).convert_alpha()
        w = sheet.get_width() // 3
        h = sheet.get_height()

        self.heart_full: pygame.Surface = pygame.transform.scale(
            sheet.subsurface(pygame.Rect(0, 0, w, h)),
            HEART_SIZE,
        )
        self.heart_empty: pygame.Surface = pygame.transform.scale(
            sheet.subsurface(pygame.Rect(w * 2, 0, w, h)),
            HEART_SIZE,
        )

    def draw(self, y_base: int) -> None:
        """
        Render the HUD bar at the given vertical offset.

        Args:
            y_base: Y pixel coordinate of the top of the HUD bar.
        """
        gm = self.game_manager
        sw = self.surface.get_width()
        bar_rect = pygame.Rect(0, y_base, sw, HUD_HEIGHT)
        pygame.draw.rect(self.surface, (15, 15, 40), bar_rect)
        pygame.draw.line(
            self.surface,
            Color.WALL.rgb(),
            (0, y_base),
            (sw, y_base),
            1,
        )

        cy = y_base + HUD_HEIGHT // 2

        max_lives: int = min(gm.config["lives"], 10)
        lives: int = gm.player.lives
        heart_x = 16
        heart_y_top = cy - HEART_SIZE[1] - 2
        heart_y_bottom = cy + 2

        for i in range(max_lives):
            sprite = self.heart_full if i < lives else self.heart_empty
            row = i // 5
            col = i % 5
            x = heart_x + col * HEART_SPACING
            y = heart_y_top if row == 0 else heart_y_bottom
            self.surface.blit(sprite, (x, y))

        secs = max(0, int(gm.time_remining))
        mm, ss = divmod(secs, 60)
        clock_str = f"{mm:02d}:{ss:02d}"
        clock_color = (
            (255, 80, 80) if secs <= 10 else (80, 255, 120)
        )
        clock_surf = self.font_clock.render(clock_str, True, clock_color)
        clock_rect = clock_surf.get_rect(center=(sw // 2, cy))
        self.surface.blit(clock_surf, clock_rect)

        score_str = f"SCORE  {gm.score:06d}"
        score_surf = self.font_score.render(
            score_str, True, Color.TEXT.rgb()
        )
        score_rect = score_surf.get_rect(
            midright=(sw - 16, cy - 10)
        )
        self.surface.blit(score_surf, score_rect)

        level_str = f"LEVEL  {gm.current_level + 1}"
        level_surf = self.font_score.render(
            level_str, True, Color.TEXT_DIM.rgb()
        )
        level_rect = level_surf.get_rect(
            midright=(sw - 16, cy + 10)
        )
        self.surface.blit(level_surf, level_rect)
