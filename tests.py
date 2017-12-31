import unittest
from tkinter import Tk

from game_logic.board import Board
from game_logic.food import Food
from game_logic.pacman import Pacman
from game_logic.point import Point
from game_logic.power_food import PowerFood
from game_logic.wall import Wall


class TestPacman(unittest.TestCase):
    def create_test_board(self, width, height, pacman_location, static_objects=None):
        root = Tk()
        board = Board()
        board.field = [[None for x in range(width)] for y in range(height)]
        if static_objects is not None:
            for object in static_objects:
                board.field[object.location.x][object.location.y] = object
        board.pacman = Pacman(pacman_location.x, pacman_location.y, board, 1)
        board.moving_gameObjects = [board.pacman]
        return board

    def test_movement(self):
        board = self.create_test_board(5, 5, Point(3, 3))
        board.pacman.set_new_direction(Point(1, 0))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(4, 3))
        board.pacman.set_new_direction(Point(0, 1))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(4, 4))
        board.pacman.set_new_direction(Point(-1, 0))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(3, 4))
        board.pacman.set_new_direction(Point(0, -1))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(3, 3))

    def test_long_movement(self):
        board = self.create_test_board(5, 5, Point(1, 1))
        board.pacman.set_new_direction(Point(1, 0))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(2, 1))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(3, 1))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(4, 1))

    def test_walls_stop_movement(self):
        board = self.create_test_board(5, 5, Point(1, 1), [Wall(3, 1), Wall(2, 4)])
        board.pacman.set_new_direction(Point(1, 0))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(2, 1))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(2, 1))
        board.pacman.set_new_direction(Point(0, 1))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(2, 2))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(2, 3))
        board.update_board()
        self.assertEqual(board.pacman.location, Point(2, 3))

    def test_eat_food(self):
        root = Tk()
        board = self.create_test_board(5, 5, Point(1, 1), [Food(2, 1), PowerFood(3, 1)])
        board.pacman.set_new_direction(Point(1, 0))
        board.update_board()
        board.update_board()
        self.assertEqual(board.field[2][1], None)
        self.assertEqual(board.pacman.score, 10)
        board.update_board()
        self.assertEqual(board.field[3][1], None)
        self.assertEqual(board.pacman.score, 110)
        self.assertEqual(board.pacman.super_power, 1)

class TestGhost(unittest.TestCase):
    def test_movement(self):
        pass

    def test_wall_stops_movement(self):
        pass

    def test_dont_eat_food(self):
        pass
