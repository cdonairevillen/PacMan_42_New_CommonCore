class CheatMode:

    def __init__(self):

        self.enabled = False

        self.speed_boost = False

        self.invincible = False

        self.noclip = False

    def toggle(self):

        self.enabled = not self.enabled

        self.speed_boost = self.enabled

        self.invincible = self.enabled

        if not self.enabled:
            self.noclip = False

        print(
            f"Cheat mode: {self.enabled}"
        )

    def toggle_noclip(self):
        if not self.enabled:

            print(
                "Activate cheat mode first."
            )
            return
        self.noclip = not self.noclip

        print(
            f"Noclip: {self.noclip}"
        )
