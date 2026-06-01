from .screen import Screen
import pygame
from visualizer.colors import Color


class Ready(Screen):

    def __init__(self, game_manager, surface):
        super().__init__(game_manager, surface)

        self.blink_timer: float = 0
        self.level_font = pygame.font.SysFont("monospace", 32, bold=True)
        self.ready_font = pygame.font.SysFont("monospace", 22, bold=True)

    def handle_events(self, event):

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:

            self.game_manager.resume()

    def draw(self):
        self.screen.fill(Color.BG.rgb())

        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        level = self.level_font.render(f"Level: {self.game_manager.current_level}", True, Color.PACGUM.rgb())
        level_rect = level.get_rect(center=(cx, cy - 150))
        self.screen.blit(level, level_rect)

        ready = self.ready_font.render("READY!", True, Color.PACGUM.rgb())
        ready_rect = ready.get_rect(center=(cx, cy - 70))
        if (self.blink_timer % 1.0) < 0.5:
            self.screen.blit(ready, ready_rect)

    def update(self, dt):
        self.blink_timer += dt
