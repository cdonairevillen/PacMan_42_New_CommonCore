from enum import Enum
from visualizer.colors import Color
import pygame


class ButtonState(Enum):

    NORMAL = "normal"
    HOVERED = "hovered"
    SELECTED = "selected"


class ButtonForm(Enum):

    SQUARE = "square"
    RECT = "rectangle"
    CIRCLE = "circle"


class Button():

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 text: str, form: ButtonForm = ButtonForm.RECT) -> None:

        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.state: ButtonState = ButtonState.NORMAL
        self.form: ButtonForm = form
        self.text: str = text
        self.font: pygame.font.Font = pygame.font.SysFont("monospace", 20)

    def draw(self, surface: pygame.surface.Surface) -> None:

        if self.state == ButtonState.NORMAL:
            color = Color.BUTTON_NORMAL

        elif self.state == ButtonState.HOVERED:
            color = Color.BUTTON_HOVERED

        elif self.state == ButtonState.SELECTED:
            color = Color.BUTTON_SELECTED

        pygame.draw.rect(surface, color.rgb(), self.rect)

        text_surface = self.font.render(self.text, True, Color.TEXT.rgb())
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:

        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.state = ButtonState.HOVERED

            else:
                self.state = ButtonState.NORMAL

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = ButtonState.SELECTED

    def is_clicked(self, event: pygame.event.Event) -> bool:

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
           and self.rect.collidepoint(event.pos)):
            return True

        if (event.type == pygame.KEYDOWN
           and event.key in (pygame.K_RETURN, pygame.K_SPACE)
           and self.state == ButtonState.SELECTED):
            return True

        return False
