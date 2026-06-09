from dataclasses import dataclass


@dataclass
class VisualConfig():

    wall_thickness: int = 3
    cell_size: int = 28
    margin: int = 40
    hud_height: int = 56
    menu_w: int = 600
    menu_h: int = 500
