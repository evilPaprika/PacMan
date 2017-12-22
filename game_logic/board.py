from game_logic import BOARD_HIGHT, BOARD_WIDTH
from game_logic.food import Food
from game_logic.ghost import Ghost
from game_logic.pacman import Pacman
from game_logic.power_food import PowerFood
from game_logic.wall import Wall


class Board:
    def __init__(self):
        self.moving_gameObjects = []
        self.field = [[None for x in range(BOARD_WIDTH)] for y in range(BOARD_HIGHT)]
        self.pacman = None
        self.generate_level()
        self.game_lost = False
        self.game_won = False
        self.update_board()

    def update_board(self):
        self.check_collisions()
        for obj in self.moving_gameObjects[:]:
            obj.update_position()
        for i in range(15):
            for j in range(15):
                if isinstance(self.field[i][j], Food):
                    break
            else:
                continue
            break
        else:
            self.game_won = True
        if self.pacman.lives <= 0:
            self.game_lost = True



    def check_collisions(self):
        pacman_location = round(self.pacman.location)
        if isinstance(self.field[pacman_location.x][pacman_location.y], Food) \
                or isinstance(self.field[pacman_location.x][pacman_location.y], PowerFood):
            self.pacman.action_when_collided_with(self.field[pacman_location.x][pacman_location.y])
            self.field[pacman_location.x][pacman_location.y] = None
        for s_obj in self.moving_gameObjects:
            if s_obj != self.pacman and s_obj.location.distance(self.pacman.location) < 0.5:
                s_obj.action_when_collided_with(self.pacman)
                self.pacman.action_when_collided_with(s_obj)

    def get_neighbour_walls(self, point):
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    obj = self.field[point.x + i][point.y + j]
                    if isinstance(obj, Wall):
                        yield obj
                except IndexError:
                    pass

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
        self.field[4][4] = (Wall(4, 4))
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

        for i in range(BOARD_HIGHT):
            for j in range(BOARD_WIDTH):
                # отражение стен
                obj = self.field[i][j]
                if isinstance(obj, Wall):
                    self.field[14 - obj.location.x][obj.location.y] = Wall(14 - obj.location.x, obj.location.y)

        self.field[7][0] = (Wall(7, 0))
        self.field[7][2] = (Wall(7, 2))
        self.field[7][3] = (Wall(7, 3))
        self.field[7][4] = (Wall(7, 4))
        self.field[7][6] = (Wall(7, 6))
        self.field[7][7] = (Wall(7, 7))
        self.field[7][8] = (Wall(7, 8))
        self.field[7][10] = (Wall(7, 10))
        self.field[7][11] = (Wall(7, 11))
        self.field[7][13] = (Wall(7, 13))
        self.field[7][14] = (Wall(7, 14))

        self.field[1][1] = PowerFood(1, 1)
        self.field[13][12] = PowerFood(13, 12)
        self.field[9][9] = PowerFood(9, 9)

        self.pacman = Pacman(7, 9, self)
        self.moving_gameObjects.append(self.pacman)
        self.moving_gameObjects.append(Ghost(7, 5, self, "./sprites/ghost_red.png"))
        self.moving_gameObjects.append(Ghost(6, 5, self, "./sprites/ghost_blue.png"))
        self.moving_gameObjects.append(Ghost(8, 5, self, "./sprites/ghost_pink.png"))
        self.moving_gameObjects.append(Ghost(7, 5, self, "./sprites/ghost_yellow.png"))

        for i in range(BOARD_HIGHT):
            for j in range(BOARD_WIDTH):
                if self.field[i][j] is None:
                    self.field[i][j] = Food(i, j)
        self.field[7][9] = None

