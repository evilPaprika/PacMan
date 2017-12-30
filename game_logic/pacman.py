import winsound
from threading import Timer

from PIL import ImageTk, Image

import game_logic.ghost
from game_logic import BOARD_HIGHT
from game_logic import BOARD_WIDTH
from game_logic.food import Food
from game_logic.point import Point
from game_logic.power_food import PowerFood
from game_logic.prize import Prize


class Pacman:
    def __init__(self, x, y, board):
        self.is_dead = False
        self.respawn_location = Point(x, y)
        self.location = self.respawn_location
        self.saved_direction = Point(0, 0)
        self.last_direction = Point(1, 0)
        self.direction = Point(0, 0)
        self._directions = []
        self.sprites = {}
        self.speed = 0.2
        self.lives = 3
        self.board = board
        self.score = 0
        self.super_power = 0
        self.last_teleported = 0
        self._configure_sprites()

    def action_when_collided_with(self, obj):
        if isinstance(obj, Food):
            winsound.PlaySound("./audio/pacman_chomp.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.score += 10
            self.board.food_left -= 1
        elif isinstance(obj, PowerFood):
            winsound.PlaySound("./audio/pacman_eatfruit.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.score += 100
            self.super_power += 1
            Timer(5.0, self._reset_super_power).start()
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
        # проход через края
        self.location = Point((new_location.x + 0.5) % BOARD_WIDTH - 0.5,
                              (new_location.y + 0.5) % BOARD_HIGHT - 0.5)

    def decide_direction(self):
        if self.direction.is_opposite(self.saved_direction):
            self.saved_direction = Point(0, 0)
            return self.direction
        if self.location != round(self.location):
            return self.last_direction
        walls = list(self.board.get_neighbour_walls(self.location))
        new_location = self.location + self.direction
        for wall in walls:
            if new_location == wall.location: break
        else:
            self.saved_direction = Point(0, 0)
            return self.direction
        new_location = self.location + self.saved_direction
        for wall in walls:
            if new_location == wall.location: break
        else:
            return self.saved_direction
        self.saved_direction = Point(0, 0)
        return self.saved_direction

    def update_position(self):
        if self.location != Point(-1, -1):
            new_dir = self.decide_direction()
            if new_dir != Point(0, 0):
                self.last_direction = new_dir
            self.move(new_dir)

    def get_sprite(self):
        return self.sprites[self.last_direction][round((self.location.x + self.location.y) * 10) % 3]

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

    def _reset_super_power(self):
        self.super_power -= 1

    def _configure_sprites(self):
        self.sprites = {Point(1, 0) : [ImageTk.PhotoImage(file="./sprites/pacman_1.png"),
                                      ImageTk.PhotoImage(file="./sprites/pacman_2.png") ,
                                    ImageTk.PhotoImage(file="./sprites/pacman_3.png")],
                        Point(0, 1) : [ImageTk.PhotoImage(Image.open("./sprites/pacman_1.png").rotate(270)),
                                      ImageTk.PhotoImage(Image.open("./sprites/pacman_2.png").rotate(270)) ,
                                     ImageTk.PhotoImage(Image.open("./sprites/pacman_3.png").rotate(270))],
                        Point(-1, 0): [ImageTk.PhotoImage(Image.open("./sprites/pacman_1.png").rotate(180)),
                                      ImageTk.PhotoImage(Image.open("./sprites/pacman_2.png").rotate(180)),
                                      ImageTk.PhotoImage(Image.open("./sprites/pacman_3.png").rotate(180))],
                        Point(0, -1): [ImageTk.PhotoImage(Image.open("./sprites/pacman_1.png").rotate(90)),
                                      ImageTk.PhotoImage(Image.open("./sprites/pacman_2.png").rotate(90)),
                                      ImageTk.PhotoImage(Image.open("./sprites/pacman_3.png").rotate(90))]
                        }
