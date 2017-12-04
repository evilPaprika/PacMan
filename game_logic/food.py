from game_logic.point import Point


class Food:
    def __init__(self, x, y):
        self.is_dead = False
        self.location = Point(x, y)

    def get_sprite(self):
        return "./sprites/food.png"

    def action_when_collided_with(self, obj):
        self.is_dead = True
