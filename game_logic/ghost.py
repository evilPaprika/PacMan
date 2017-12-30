import threading
import time
import winsound
from PIL import ImageTk
from game_logic import BOARD_WIDTH, BOARD_HIGHT
from game_logic.pacman import Pacman
from game_logic.point import Point
import random


class Ghost:
    def __init__(self, x, y, board, sprite):
        self.sprite = ImageTk.PhotoImage(file=sprite)
        self.scared_sprite = ImageTk.PhotoImage(file="./sprites/ghost_scared.png")
        self.is_dead = False
        self.location = Point(x, y)
        self.speed = 0.19
        self.board = board
        self.direction = Point(0, 0)
        self.movement_marker = None
        self.teleport_delay = False
        self.last_teleported = 0

    def move(self, speed):
        new_location = Point(self.location.x + self.direction.x * speed, self.location.y + self.direction.y * speed)
        if self.movement_marker and self.location.distance(self.movement_marker[0]) + self.movement_marker[0].distance(
                new_location) == self.location.distance(new_location):
            new_location = self.movement_marker[0] + Point(self.movement_marker[1].x * speed,
                                                           self.movement_marker[1].y * speed)
            self.direction = self.movement_marker[1]
            self.movement_marker = None
        # проход через края
        self.location = Point((new_location.x + 0.5) % BOARD_WIDTH - 0.5,
                              (new_location.y + 0.5) % BOARD_HIGHT - 0.5)

    def _get_prefered_directions(self):
        directions = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]
        random.shuffle(directions)
        return directions

    def _make_marker(self):
        location = round(self.location)
        directions = self._get_prefered_directions()
        for direction in directions:
            if direction.is_opposite(self.direction):
                continue
            new_location = location + direction
            walls = self.board.get_neighbour_walls(location)
            for wall in walls:
                if new_location == wall.location:
                    break
            else:
                self.movement_marker = (location, direction)
                break


    def update_position(self):
        self._make_marker()
        if self.board.pacman.super_power:
            self.move(self.speed / 2)
        else:
            self.move(self.speed)

    def get_sprite(self):
        if self.board.pacman.super_power:
            return self.scared_sprite
        else:
            return self.sprite

    def action_when_collided_with(self, obj):
        if isinstance(obj, Pacman):
            if obj.super_power:
                threading.Thread(target=self.respawn).start()
                winsound.PlaySound("./audio/pacman_eatghost.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                obj.score += 200

    def respawn(self):
        # запускать в отдельном потоке
        self.direction = Point(0, 0)
        self.location = Point(7, 7)
        time.sleep(7)
        self.direction = Point(0, -1)
        self.speed = self.speed / 2
        time.sleep(1)
        self.speed = self.speed * 2
