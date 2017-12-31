import threading
import time
import winsound
from PIL import ImageTk
from game_logic import BOARD_WIDTH, BOARD_HEIGHT, make_location_in_borders
from game_logic.pacman import Pacman
from game_logic.point import Point
import random

from game_logic.wall import Wall


class Ghost:
    def __init__(self, x, y, board, speed, sprite="./sprites/ghost_red.png"):
        self.sprite = ImageTk.PhotoImage(file=sprite)
        self.scared_sprite = ImageTk.PhotoImage(file="./sprites/ghost_scared.png")
        self.location = Point(x, y)
        self.speed = speed
        self.board = board
        self.direction = Point(0, 0)
        self._movement_marker = None
        self.last_teleported = 0
        self.destination = Point(14, 1)

    def move(self, speed, direction):
        new_location = Point(self.location.x + direction.x * speed, self.location.y + direction.y * speed)
        if self._movement_marker and self.location.distance(self._movement_marker[0]) +\
                self._movement_marker[0].distance(new_location) == self.location.distance(new_location):
            new_location = self._movement_marker[0] + Point(self._movement_marker[1].x * speed,
                                                            self._movement_marker[1].y * speed)
            self.direction = self._movement_marker[1]
            self._movement_marker = None
        self.location = make_location_in_borders(new_location)

    def _get_prefered_directions(self):
        if self.board.game_state == 'frightened':
            directions = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]
            random.shuffle(directions)
            return directions
        else:
            self._update_destination()
            directions = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]
            course = self.location - self.destination
            directions.sort(key=lambda x: (x + course).length())
            return directions

    def _make_marker(self):
        location = round(self.location)
        directions = self._get_prefered_directions()
        for direction in directions:
            if direction.is_opposite(self.direction):
                continue
            new_location = round(make_location_in_borders(location + direction))
            if not isinstance(self.board.field[new_location.x][new_location.y], Wall):
                self._movement_marker = (location, direction)
                break

    def _update_destination(self):
        self.destination = self.board.pacman.location

    def _account_portals(self, dest):
        # возвращает расположение портала входа, если ближе пройти по нему
        straight_distance = self.location.distance(dest)
        for portal in self.board.portals:
            if straight_distance > self.location.distance(portal.location) + portal.exit_location.distance(dest):
                return portal.location
        return dest

    def update_position(self):
        self._make_marker()
        if self.board.pacman.super_power:
            self.move(self.speed / 2, self.direction)
        else:
            self.move(self.speed, self.direction)

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
