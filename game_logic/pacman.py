from threading import Timer
from game_logic import BOARD_WIDTH
from game_logic import BOARD_HIGHT
from game_logic.food import Food
import game_logic.ghost
from game_logic.point import Point
from game_logic.power_food import PowerFood


class Pacman:
    def __init__(self, x, y, board):
        self.is_dead = False
        self.respawn_location = Point(x, y)
        self.location = self.respawn_location
        self.saved_direction = Point(0, 0)
        self.direction = Point(0, 0)
        self.speed = 0.1
        self.lives = 1
        self.walls = board.walls
        self.score = 0
        self.super_power = False

    def action_when_collided_with(self, obj):
        if isinstance(obj, Food):
            self.score += 10
        if isinstance(obj, PowerFood):
            self.score += 100
            self.super_power += 1
            Timer(5.0, self.reset_super_power).start()
        if isinstance(obj, game_logic.ghost.Ghost):
            if not self.super_power:
                self.location = Point(-1, -1)
                self.lives -= 1
                self.saved_direction = Point(0, 0)
                self.direction = Point(0, 0)
                Timer(1.0, self.respawn).start()

    def move(self, direction):
        new_location = Point(self.location.x + direction.x * self.speed, self.location.y + direction.y * self.speed)
        # хитрая математика для крсивого прохода через края без прыжков
        self.location = Point((new_location.x + 0.5) % BOARD_WIDTH - 0.5,
                              (new_location.y + 0.5) % BOARD_HIGHT - 0.5)

    def decide_direction(self):
        new_location = Point(self.location.x + self.direction.x * self.speed,
                             self.location.y + self.direction.y * self.speed)
        for wall in self.walls:
            if wall.location.distance(new_location) < 0.99:
                new_location = Point(self.location.x + self.saved_direction.x * self.speed,
                                     self.location.y + self.saved_direction.y * self.speed)
                for wall1 in self.walls:
                    if wall1.location.distance(new_location) < 0.99:
                        return Point(0, 0)
                return self.saved_direction
        self.saved_direction = Point(0, 0)
        return self.direction

    def update_position(self):
        self.move(self.decide_direction())

    def get_sprite(self):
        return "./sprites/pacman_0.png"

    def set_new_direction(self, new_direction):
        if new_direction == self.direction:
            return
        self.saved_direction = self.direction
        self.direction = new_direction

    def set_direction_up(self):
        self.set_new_direction(Point(0, -1))

    def set_direction_down(self):
        self.set_new_direction(Point(0, 1))

    def set_direction_left(self):
        self.set_new_direction(Point(-1, 0))

    def set_direction_right(self):
        self.set_new_direction(Point(1, 0))

    def set_direction_stop(self):
        self.saved_direction = Point(0, 0)
        self.direction = Point(0, 0)

    def respawn(self):
        self.location = self.respawn_location

    def reset_super_power(self):
        self.super_power -= 1