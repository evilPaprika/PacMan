import random

import time

from game_logic import BOARD_HEIGHT, BOARD_WIDTH
from game_logic.food import Food
from game_logic.ghost import Ghost
from game_logic.pacman import Pacman
from game_logic.portal import Portal
from game_logic.power_food import PowerFood
from game_logic.prize import Prize
from game_logic.wall import Wall


class Board:
    def __init__(self):
        self.food_left = 0
        self.moving_gameObjects = []
        self.new_objects = []
        self.field = [[None for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
        self.pacman = None
        self.portals = []
        self.generate_level()
        self.game_lost = False
        self.game_won = False
        self.game_state = 'scatter' # scatter, chase или frightened
        self.update_board()

    def update_board(self):
        self.check_collisions()
        for obj in self.moving_gameObjects[:]:
            obj.update_position()
        if self.food_left == 80 or self.food_left == 50 or self.food_left == 20:
            self.spawn_prize()
        if self.food_left < 1:
            self.game_won = True
        if self.pacman.lives <= 0:
            self.game_lost = True
        self.update_game_state()


    def update_game_state(self):
        if self.pacman.super_power:
            self.game_state = "frightened"
            return
        timer = time.time() % 15
        if timer < 5:
            self.game_state = 'scatter'
        else:
            self.game_state = 'chase'

    def check_collisions(self):
        pacman_location = round(self.pacman.location)
        if not isinstance(self.field[pacman_location.x][pacman_location.y], Wall):
            self.pacman.action_when_collided_with(self.field[pacman_location.x][pacman_location.y])
            self.field[pacman_location.x][pacman_location.y] = None
        for i in range(len(self.moving_gameObjects)):
            for j in range(i + 1, len(self.moving_gameObjects)):
                if self.moving_gameObjects[i].location.distance(self.moving_gameObjects[j].location) < 0.5:
                    self.moving_gameObjects[i].action_when_collided_with(self.moving_gameObjects[j])
                    self.moving_gameObjects[j].action_when_collided_with(self.moving_gameObjects[i])

    def get_neighbour_walls(self, point):
        for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            try:
                obj = self.field[round(point.x + dir[0])][round(point.y + dir[1])]
                if isinstance(obj, Wall):
                    yield obj
            except IndexError:
                pass

    def spawn_prize(self):
        i = random.randrange(15)
        j = random.randrange(15)
        if isinstance(self.field[i][j], Food):
            self.field[i][j] = Prize(i, j)
            self.food_left -= 1
            self.new_objects.append(self.field[i][j])
        else: self.spawn_prize()

    def generate_level(self):
        for i in range(7):
            self.field[i][0] = Wall(i, 0)
            self.field[i][14] = (Wall(i, 14))
        for i in range(7):
            self.field[0][i] = (Wall(0, i))
            self.field[0][i + 8] = (Wall(0, i + 8))
        self.field[1][6] = (Wall(1, 6))
        self.field[1][8] = (Wall(1, 8))
        self.field[2][2] = (Wall(2, 2))
        self.field[2][4] = (Wall(2, 4))
        self.field[2][10] = (Wall(2, 10))
        self.field[2][11] = (Wall(2, 11))
        self.field[2][12] = (Wall(2, 12))
        self.field[3][2] = (Wall(3, 2))
        self.field[3][6] = (Wall(3, 6))
        self.field[3][8] = (Wall(3, 8))
        # self.field[4][4] = (Wall(4, 4))
        self.field[4][5] = (Wall(4, 5))
        self.field[4][6] = (Wall(4, 6))
        self.field[4][8] = (Wall(4, 8))
        self.field[4][9] = (Wall(4, 9))
        self.field[4][10] = (Wall(4, 10))
        self.field[4][12] = (Wall(4, 12))
        self.field[5][2] = (Wall(5, 2))
        self.field[5][4] = (Wall(5, 4))
        self.field[5][12] = (Wall(5, 12))
        self.field[6][2] = (Wall(6, 2))
        self.field[6][6] = (Wall(6, 6))
        self.field[6][7] = (Wall(6, 7))
        self.field[6][8] = (Wall(6, 8))
        self.field[6][10] = (Wall(6, 10))

        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                # отражение стен
                obj = self.field[i][j]
                if isinstance(obj, Wall):
                    self.field[14 - obj.location.x][obj.location.y] = Wall(14 - obj.location.x, obj.location.y)

        self.field[7][0] = (Wall(7, 0))
        self.field[7][2] = (Wall(7, 2))

        self.field[7][3] = (Wall(7, 3)) #

        self.field[7][4] = (Wall(7, 4))
        self.field[7][6] = (Wall(7, 6))
        self.field[7][7] = (Wall(7, 7))
        self.field[7][8] = (Wall(7, 8))
        self.field[7][10] = (Wall(7, 10))
        self.field[7][11] = (Wall(7, 11))
        # self.field[7][13] = (Wall(7, 13))
        self.field[7][14] = (Wall(7, 14))
        self.field[10][4] = (Wall(10, 4)) #

        self.field[1][1] = PowerFood(1, 1)
        self.field[13][13] = PowerFood(13, 13)
        self.field[1][13] = PowerFood(1, 13)
        self.field[13][1] = PowerFood(13, 1)


        self.pacman = Pacman(7, 9, self, 0.2)
        self.portals.append(Portal(7, 13, 4, 4))
        self.portals.append(Portal(4, 4, 7, 13))
        self.moving_gameObjects.append(self.portals[0])
        self.moving_gameObjects.append(self.portals[1])
        self.moving_gameObjects.append(self.pacman)
        self.moving_gameObjects.append(Ghost(7, 5, self, "./sprites/ghost_red.png", 0.19))
        self.moving_gameObjects.append(Ghost(6, 5, self, "./sprites/ghost_blue.png", 0.19))
        self.moving_gameObjects.append(Ghost(8, 5, self, "./sprites/ghost_pink.png", 0.19))
        self.moving_gameObjects.append(Ghost(7, 5, self, "./sprites/ghost_yellow.png", 0.19))

        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if self.field[i][j] is None:
                    self.field[i][j] = Food(i, j)
                    self.food_left += 1
        self.field[7][9] = None
        self.food_left -= 1

