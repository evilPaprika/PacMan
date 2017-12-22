from PIL import ImageTk

from game_logic.point import Point


class Food:
    def __init__(self, x, y):
        self.location = Point(x, y)
        self.sprite = ImageTk.PhotoImage(file="./sprites/food.png")

    def get_sprite(self):
        return self.sprite
