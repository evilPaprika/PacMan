import time
import tkinter

from game_logic.point import Point


class Portal:
    def __init__(self, x, y, exit_x, exit_y):
        self.location = Point(x, y)
        self.exit_location = Point(exit_x, exit_y)
        self.sprite = tkinter.PhotoImage(file="./sprites/loop_portal.gif", format="gif -index 0")

    def get_sprite(self):
        self.sprite.config(format="gif -index {}".format(int(time.time()*10) % 4))
        return self.sprite

    def action_when_collided_with(self, obj):
        timestamp = time.time()
        if timestamp > obj.last_teleported + 1:
            obj.location = self.exit_location
            obj.last_teleported = timestamp

    def update_position(self):
        pass


