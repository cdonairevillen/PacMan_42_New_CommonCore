class CheatMode:
    """
    Manage cheat mode features such as invincibility,
    speed boosts, and noclip movement.
    """
    def __init__(self):
        """
        Initialize all cheat options as disabled.
        """
        self.enabled = False
        self.speed_boost = False
        self.invincible = False
        self.noclip = False

    def toggle(self):
        """
        Enable or disable cheat mode and its default effects.
        """
        self.enabled = not self.enabled
        self.speed_boost = self.enabled
        self.invincible = self.enabled
        if not self.enabled:
            self.noclip = False
        print(
            f"Cheat mode: {self.enabled}"
        )

    def toggle_noclip(self):
        """
        Toggle noclip mode when cheat mode is active.
        """
        if not self.enabled:
            print(
                "Activate cheat mode first."
            )
            return
        self.noclip = not self.noclip
        print(
            f"Noclip: {self.noclip}"
        )
