from game_logic.point import Point


class Wall:
    def __init__(self, x, y):
        self.location = Point(x, y)
