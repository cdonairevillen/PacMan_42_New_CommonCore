
from dataclasses import dataclass, field


@dataclass
class FloatingText:
    """
    A short-lived text label that drifts upward on screen.

    Spawn one whenever the player earns points. The owner
    (GameScreen) updates and culls these every frame.

    Attributes:
        text: String to display.
        x: Horizontal pixel position (centre of text).
        y: Vertical pixel position (top of text), modified each frame.
        color: RGB tuple for the text colour.
        lifetime: Total seconds this text lives before being removed.
        vy: Vertical drift speed in pixels per second (negative = up).
        age: Seconds elapsed since creation.
    """

    text: str
    x: float
    y: float
    color: tuple[int, int, int]
    lifetime: float = 1.2
    vy: float = -45.0
    age: float = field(default=0.0, init=False)

    @property
    def alive(self) -> bool:
        """Return True while the text has remaining lifetime."""
        return self.age < self.lifetime

    @property
    def alpha(self) -> int:
        """
        Fade out in the last third of the lifetime.

        Returns:
            Integer alpha value between 0 and 255.
        """
        fade_start = self.lifetime * 0.65
        if self.age < fade_start:
            return 255
        progress = (self.age - fade_start) / (self.lifetime - fade_start)
        return max(0, int(255 * (1.0 - progress)))

    def update(self, dt: float) -> None:
        """
        Advance the text position and age by one frame.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        self.y += self.vy * dt
        self.age += dt