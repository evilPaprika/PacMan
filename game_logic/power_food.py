from PIL import ImageTk

from game_logic.point import Point


class PowerFood:
    def __init__(self, x, y):
        self.location = Point(x, y)
        self.sprite = ImageTk.PhotoImage(file="./sprites/power_food.png")

    def get_sprite(self):
        return self.sprite

