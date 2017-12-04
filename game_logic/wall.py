from game_logic.point import Point


class Wall:
    def __init__(self, x, y):
        self.is_dead = False
        self.location = Point(x, y)

    def action_when_collided_with(self, obj):
        pass
