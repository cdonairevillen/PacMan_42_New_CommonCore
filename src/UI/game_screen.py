
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from visualizer.visualizer import MazeVisualizer
import pygame
from game_manager import GameManager, State
from .screen import Screen
from .utils.floating_text import FloatingText


class GameScreen(Screen):

    """
    Orchestrates all in-game rendering.

    Delegates maze and entity drawing to the MazeVisualizer, renders
    the HUD bar, and manages floating score texts. Lives as a Screen
    so the UIManager can route State.PLAYING and State.LOADING here.

    Attributes:
        visualizer: MazeVisualizer instance for maze/entity rendering.
        hud: HUD instance for the bottom bar.
        floating_texts: Active FloatingText instances this frame.
        font_float: Font used for floating score labels.
    """

    def __init__(self, game_manager: GameManager, surface: pygame.Surface,
                 visualizer: "MazeVisualizer") -> None:
        """
        Initialise the GameScreen.

        Args:
            game_manager: Shared game state.
            surface: Pygame surface to draw onto.
            visualizer: MazeVisualizer instance (typed as object to
                avoid a circular import; duck-typed at call sites).
        """
        super().__init__(game_manager, surface)

        self.visualizer: MazeVisualizer = visualizer
        self.floating_texts: list[FloatingText] = []
        self.font_float: pygame.font.Font = pygame.font.SysFont(
            "monospace", 20, bold=True
        )

        from .hud import HUD
        self.hud: HUD = HUD(game_manager, surface)

    def add_float(self, text: str, x: float, y: float,
                  color: tuple[int, int, int],) -> None:
        """
        Spawn a new floating score label.

        Args:
            text: Text to display (e.g. '+200').
            x: Horizontal pixel centre of the label.
            y: Vertical pixel top of the label.
            color: RGB colour tuple.
        """
        self.floating_texts.append(FloatingText(text, x, y, color))

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Handle in-game input.

        Movement and cheat keys are processed here so the visualizer
        does not need to import Screen or UIManager.

        Args:
            event: Pygame event to process.
        """
        if event.type != pygame.KEYDOWN:
            return

        state = self.game_manager.state

        if event.key == pygame.K_p and state == State.PLAYING:
            self.game_manager.pause()

        elif event.key == pygame.K_c:
            self.game_manager.toggle_cheat_mode()

        elif (
            event.key == pygame.K_n
            and self.game_manager.cheat_mode.enabled
        ):
            self.game_manager.skip_level()

        elif (event.key == pygame.K_i
              and self.game_manager.cheat_mode.enabled):
            self.game_manager.score += 1000

        elif event.key == pygame.K_v:
            was_noclip = (
                self.game_manager.cheat_mode.noclip
            )
            self.game_manager.cheat_mode.toggle_noclip()
            if was_noclip:
                self.game_manager.player.respawn(
                    self.game_manager.current_maze
                )

        elif event.key in (pygame.K_UP, pygame.K_w):
            self.game_manager.player.set_direction(0, -1)

        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.game_manager.player.set_direction(0, 1)

        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.game_manager.player.set_direction(-1, 0)

        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.game_manager.player.set_direction(1, 0)

    def update(self, dt: float) -> None:
        """
        Advance floating texts and cull expired ones.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        for ft in self.floating_texts:
            ft.update(dt)
        self.floating_texts = [
            ft for ft in self.floating_texts if ft.alive]

    def draw(self) -> None:
        """Render maze, entities, HUD, and floating texts."""
        viz = self.visualizer
        state = self.game_manager.state

        if state == State.PLAYING:
            viz.advance_animations()

        viz.draw_maze()
        viz.draw_entities()

        assert self.game_manager.current_maze is not None
        maze = self.game_manager.current_maze
        y_base = (40 + maze.height * viz.cell_size)
        self.hud.draw(y_base)

        self.draw_floating_texts()

    def draw_floating_texts(self) -> None:
        """Render all active floating score labels with fade-out."""
        for ft in self.floating_texts:
            surf = self.font_float.render(ft.text, True, ft.color)
            surf.set_alpha(ft.alpha)
            rect = surf.get_rect(center=(int(ft.x), int(ft.y)))
            self.screen.blit(surf, rect)
