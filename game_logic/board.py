import itertools

from game_logic.food import Food
from game_logic.ghost import Ghost
from game_logic.pacman import Pacman
from game_logic.point import Point
from game_logic.power_food import PowerFood
from game_logic.wall import Wall
import threading


class Board:
    def __init__(self):
        self.food = {}
        self.moving_gameObjects = []
        self.walls = []
        self.pacman = None
        self.generate_level()
        self.game_lost = False
        self.game_won = False
        self.update_board()

    def update_board(self):
        self.check_collisions()
        for obj in self.moving_gameObjects[:]:
            obj.update_position()
        # for obj in self.food[:]:
        #     if obj.is_dead: self.food.remove(obj)
        if len(self.food) == 0:
            self.game_won = True
        elif self.pacman.lives <= 0:
            self.game_lost = True


    def check_collisions(self):
        if round(self.pacman.location) in self.food:
            print("test")
            self.food.pop(round(self.pacman.location))

        # for s_obj in self.food:
        #     if s_obj.location.distance(self.pacman.location) < 0.5:
        #         s_obj.action_when_collided_with(self.pacman)
        #         self.pacman.action_when_collided_with(s_obj)
        for s_obj in self.moving_gameObjects:
            if s_obj != self.pacman and s_obj.location.distance(self.pacman.location) < 0.7:
                s_obj.action_when_collided_with(self.pacman)
                self.pacman.action_when_collided_with(s_obj)

    def generate_level(self):
        for i in range(7):
            self.walls.append(Wall(i, 0))
            self.walls.append(Wall(i, 14))
        for i in range(7):
            self.walls.append(Wall(0, i))
            self.walls.append(Wall(0, i + 8))
        self.walls.append(Wall(1, 6))
        self.walls.append(Wall(1, 8))
        self.walls.append(Wall(2, 2))
        self.walls.append(Wall(2, 4))
        self.walls.append(Wall(2, 10))
        self.walls.append(Wall(2, 11))
        self.walls.append(Wall(2, 12))
        self.walls.append(Wall(3, 2))
        self.walls.append(Wall(3, 6))
        self.walls.append(Wall(3, 8))
        self.walls.append(Wall(4, 4))
        self.walls.append(Wall(4, 5))
        self.walls.append(Wall(4, 6))
        self.walls.append(Wall(4, 8))
        self.walls.append(Wall(4, 9))
        self.walls.append(Wall(4, 10))
        self.walls.append(Wall(4, 12))
        self.walls.append(Wall(5, 2))
        self.walls.append(Wall(5, 4))
        self.walls.append(Wall(5, 12))
        self.walls.append(Wall(6, 2))
        self.walls.append(Wall(6, 6))
        self.walls.append(Wall(6, 7))
        self.walls.append(Wall(6, 8))
        self.walls.append(Wall(6, 10))

        for obj in self.walls[:]:
            # отражение стен
            if isinstance(obj, Wall):
                self.walls.append(Wall(14 - obj.location.x, obj.location.y))

        self.walls.append(Wall(7, 0))
        self.walls.append(Wall(7, 2))
        self.walls.append(Wall(7, 3))
        self.walls.append(Wall(7, 4))
        self.walls.append(Wall(7, 6))
        self.walls.append(Wall(7, 7))
        self.walls.append(Wall(7, 8))
        self.walls.append(Wall(7, 10))
        self.walls.append(Wall(7, 11))
        self.walls.append(Wall(7, 13))
        self.walls.append(Wall(7, 14))

        self.food.update({Point(1, 1): PowerFood(1, 1)})
        self.food.update({Point(13, 12): PowerFood(13, 12)})
        self.food.update({Point(9, 9): PowerFood(9, 9)})

        self.pacman = Pacman(7, 9, self)
        self.moving_gameObjects.append(self.pacman)
        self.moving_gameObjects.append(Ghost(7, 5, self, "./sprites/ghost_red.png"))
        self.moving_gameObjects.append(Ghost(7, 5, self, "./sprites/ghost_blue.png"))
        self.moving_gameObjects.append(Ghost(7, 5, self, "./sprites/ghost_pink.png"))
        self.moving_gameObjects.append(Ghost(7, 5, self, "./sprites/ghost_yellow.png"))

        for i in range(15):
            for j in range(15):
                for obj in itertools.chain(self.walls, self.food.values()):
                    if obj.location == Point(i, j):
                        break
                else:
                    self.food.update({Point(i, j): Food(i, j)})

