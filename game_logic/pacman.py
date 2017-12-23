from threading import Timer

import winsound
from PIL import ImageTk
from game_logic import BOARD_WIDTH
from game_logic import BOARD_HIGHT
from game_logic.food import Food
import game_logic.ghost
from game_logic.point import Point
from game_logic.power_food import PowerFood
from game_logic.prize import Prize


class Pacman:
    def __init__(self, x, y, board):
        self.is_dead = False
        self.respawn_location = Point(x, y)
        self.location = self.respawn_location
        self.saved_direction = Point(0, 0)
        self.direction = Point(0, 0)
        self._directions = []
        self.speed = 0.2
        self.lives = 3
        self.board = board
        self.score = 0
        self.super_power = False
        self.sprites = [ImageTk.PhotoImage(file="./sprites/pacman_0.png")]

    def action_when_collided_with(self, obj):
        if isinstance(obj, Food):
            winsound.PlaySound("./audio/pacman_chomp.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.score += 10
            self.board.food_left -= 1
        elif isinstance(obj, PowerFood):
            winsound.PlaySound("./audio/pacman_eatfruit.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.score += 100
            self.super_power += 1
            Timer(5.0, self.reset_super_power).start()
        elif isinstance(obj, game_logic.ghost.Ghost):
            if not self.super_power:
                winsound.PlaySound("./audio/pacman_death.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                self.location = Point(-1, -1)
                self.lives -= 1
                self.saved_direction = Point(0, 0)
                self.direction = Point(0, 0)
                Timer(1.0, self.respawn).start()
        elif isinstance(obj, Prize):
            winsound.PlaySound("./audio/pacman_eatfruit.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.score += 200

    def move(self, direction):
        new_location = Point(self.location.x + direction.x * self.speed, self.location.y + direction.y * self.speed)
        # проход через края без прыжков
        if self.location.x - round(self.location.x) < 0.02:
            self.location.x = round(self.location.x)
        if self.location.y - round(self.location.y) < 0.02:
            self.location.y = round(self.location.y)
        self.location = Point((new_location.x + 0.5) % BOARD_WIDTH - 0.5,
                              (new_location.y + 0.5) % BOARD_HIGHT - 0.5)

    def decide_direction(self):
        walls = list(self.board.get_neighbour_walls(round(self.location)))
        new_location = self.location + self.direction * self.speed
        for wall in walls:
            if new_location.distance(wall.location) < 0.99:
                break
        else:
            self.saved_direction = Point(0, 0)
            return self.direction
        new_location = self.location + self.saved_direction * self.speed
        for wall in walls:
            if new_location.distance(wall.location) < 0.99:
                break
        else:
            return self.saved_direction
        self.saved_direction = Point(0, 0)
        return self.saved_direction

    def update_position(self):
        if self.location != Point(-1, -1):
            self.move(self.decide_direction())

    def get_sprite(self):
        return self.sprites[0]

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
