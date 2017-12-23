import itertools
import time
import tkinter as tk
import winsound

from PIL import ImageTk

import game_logic.board as board
from game_logic import BOARD_HIGHT
from game_logic import BOARD_WIDTH
from game_logic.wall import Wall
from gui import CELL_SIZE
from gui.game_lost import GameLost
from gui.game_won import GameWon


class Game(tk.Frame):
    def __init__(self, parent):
        winsound.PlaySound("./audio/pacman_end.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.board = board.Board()
        self.canvas = tk.Canvas(self, width=BOARD_WIDTH * CELL_SIZE, height=(BOARD_HIGHT * CELL_SIZE) + CELL_SIZE / 2,
                                background="black")
        self.canvas.pack()
        self.initialise_canvas()

    def frame_update_loop(self):
        self.canvas.itemconfig(self.score_canvas, text="score: " + str(self.board.pacman.score))
        self.canvas.itemconfig(self.lives_canvas, text="lives left: " + "●" * self.board.pacman.lives)
        for m_obj in self.board.moving_gameObjects:
            self.canvas.itemconfig(m_obj.canvas, image=m_obj.get_sprite())
            self.update_moving_object_position(m_obj)
        self.initialise_new_objects()
        if self.board.game_won:
            time.sleep(1)
            self.parent.change_frame(GameWon(self.parent, self.board.pacman.score))
            return
        if self.board.game_lost:
            time.sleep(1)
            self.parent.change_frame(GameLost(self.parent, self.board.pacman.score))
            return
        self.board.update_board()
        self.after(50, self.frame_update_loop)

    def update_moving_object_position(self, m_obj):
        self.canvas.coords(m_obj.canvas, m_obj.location.x * CELL_SIZE,
                           m_obj.location.y * CELL_SIZE)

    def initialise_new_objects(self):
        for obj in self.board.new_objects:
            obj.canvas = self.canvas.create_image(obj.location.x * CELL_SIZE, obj.location.y * CELL_SIZE,
                                                  image=obj.get_sprite(), anchor="nw")
        self.board.new_objects = []

    def initialise_canvas(self):
        self.bg = ImageTk.PhotoImage(file="./sprites/map40_3.png")
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.canvas.focus_set()
        self.score_canvas = self.canvas.create_text(100, BOARD_HIGHT * CELL_SIZE, fill="yellow",
                                                    font=("MV Boli", 17, "bold"), anchor='w')
        self.lives_canvas = self.canvas.create_text(340, BOARD_HIGHT * CELL_SIZE, fill="yellow",
                                                    font=("MV Boli", 17, "bold"), anchor='w')
        for obj in itertools.chain(filter(lambda x: not isinstance(x, Wall) and not x is None,
                                          itertools.chain.from_iterable(zip(*self.board.field))), self.board.moving_gameObjects):
            obj.canvas = self.canvas.create_image(obj.location.x * CELL_SIZE, obj.location.y * CELL_SIZE,
                                                  image=obj.get_sprite(), anchor="nw")

        self.canvas.bind('<Up>', lambda e: self.board.pacman.set_direction_up())
        self.canvas.bind('<Down>', lambda e: self.board.pacman.set_direction_down())
        self.canvas.bind('<Left>', lambda e: self.board.pacman.set_direction_left())
        self.canvas.bind('<Right>', lambda e: self.board.pacman.set_direction_right())
        self.after(1000, self.frame_update_loop)



