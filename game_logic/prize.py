import random

from PIL import ImageTk

from game_logic.point import Point


class Prize:
    def __init__(self, x, y):
        self.location = Point(x, y)
        s_names = ["./sprites/prize_apple.png", "./sprites/prize_cherry.png", "./sprites/prize_srawberry.png"]
        self.sprite = ImageTk.PhotoImage(file=random.choice(s_names))

    def get_sprite(self):
        return self.sprite

