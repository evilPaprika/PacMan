from game_logic.point import Point


class PowerFood:
    def __init__(self, x, y):
        self.is_dead = False
        self.location = Point(x, y)

    def get_sprite(self):
        return "./sprites/power_food.png"

    def action_when_collided_with(self, obj):
        self.is_dead = True
