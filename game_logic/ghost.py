import threading
from math import floor

import time

from game_logic import BOARD_WIDTH, BOARD_HIGHT
from game_logic.pacman import Pacman
from game_logic.point import Point
import random


class Ghost:
    def __init__(self, x, y, board, sprite):
        self.sprite = sprite
        self.is_dead = False
        self.location = Point(x, y)
        self.speed = 0.1
        self.walls = board.walls
        self.board = board
        self.direction = Point(0, 0)
        self.movement_marker = None

    def move(self, speed):
        new_location = Point(self.location.x + self.direction.x * speed, self.location.y + self.direction.y * speed)
        if self.movement_marker and self.location.distance(self.movement_marker[0]) + self.movement_marker[0].distance(
                new_location) == self.location.distance(new_location):
            new_location = self.movement_marker[0] + Point(self.movement_marker[1].x * speed,
                                                           self.movement_marker[1].y * speed)
            self.direction = self.movement_marker[1]
            self.movement_marker = None
        # хитрая математика для крсивого прохода через края без прыжков
        self.location = Point((new_location.x + 0.5) % BOARD_WIDTH - 0.5,
                              (new_location.y + 0.5) % BOARD_HIGHT - 0.5)

    def make_marker(self):
        flored_location = Point(floor(self.location.x + 0.5), floor(self.location.y + 0.5))
        directions = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]
        random.shuffle(directions)
        for direction in directions:
            if (direction * -1) == self.direction: continue
            for wall in self.board.walls:
                if (flored_location + direction) == wall.location:
                    break
            else:
                self.movement_marker = (flored_location, direction)
                break

    def update_position(self):
        self.make_marker()
        if self.board.pacman.super_power:
            self.move(self.speed / 2)
        else:
            self.move(self.speed)

    def get_sprite(self):
        if self.board.pacman.super_power:
            return "./sprites/ghost_scared.png"
        else:
            return self.sprite

    def action_when_collided_with(self, obj):
        if isinstance(obj, Pacman):
            if obj.super_power:
                threading.Thread(target=self.respawn).start()

                obj.score += 100

    def respawn(self):
        # запускать в отдельном потоке
        self.direction = Point(0, 0)
        self.location = Point(7, 7)
        time.sleep(3)
        self.direction = Point(0, -1)
        self.speed = self.speed / 2
        time.sleep(1)
        self.speed = self.speed * 2
