import tkinter as tk
import gui.game as game
from game_logic import BOARD_WIDTH, BOARD_HIGHT
from gui import CELL_SIZE


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(background="black")
        self.resizable(width=False, height=False)

        self.geometry('{}x{}'.format(BOARD_WIDTH * CELL_SIZE, int(BOARD_HIGHT * CELL_SIZE + CELL_SIZE / 2)))
        self.title("Pacman")
        self.iconbitmap("./sprites/pacman_icon.ico")
        self.frame = game.Game(self)
        self.frame.pack()

    def change_frame(self, new_frame):
        self.frame.pack_forget()
        self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()
