import tkinter as tk
from PIL import ImageTk
import game_logic.board as board
from game_logic import BOARD_HIGHT
from game_logic import BOARD_WIDTH
from gui import CELL_SIZE
from gui.drawing_object import DrawingObject
from gui.game_lost import GameLost
from gui.game_won import GameWon


class Game(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.board = board.Board()
        self.canvas = tk.Canvas(self, width=BOARD_WIDTH * CELL_SIZE, height=(BOARD_HIGHT * CELL_SIZE) + CELL_SIZE / 2,
                                background="black")
        self.initialise_canvas()
        self.canvas.pack()
        self.frame_update_loop()

    def frame_update_loop(self):
        self.canvas.itemconfig(self.score_canvas, text="score: " + str(self.board.pacman.score))
        self.canvas.itemconfig(self.lives_canvas, text="lives left: " + "●" * self.board.pacman.lives)
        for m_obj in self.moving_drawing_objects:
            m_obj.update_sprite()
            self.update_moving_object_position(m_obj)
        for s_obj in self.static_drawing_objects[:]:
            if s_obj.board_object.is_dead:
                self.canvas.delete(s_obj.canvas_ID)
                self.static_drawing_objects.remove(s_obj)
        if self.board.game_won:
            self.parent.change_frame(GameLost(self.parent, self.board.pacman.score))
        if self.board.game_lost:
            self.parent.change_frame(GameWon(self.parent, self.board.pacman.score))

        self.after(8, self.frame_update_loop)

    def update_moving_object_position(self, m_obj):
        self.canvas.coords(m_obj.canvas_ID, m_obj.board_object.location.x * CELL_SIZE,
                           m_obj.board_object.location.y * CELL_SIZE)

    def initialise_canvas(self):
        self.images = []
        bg = ImageTk.PhotoImage(file="./sprites/map40_3.png")
        self.images.append(bg)
        self.canvas.create_image(0, 0, image=bg, anchor="nw")
        self.canvas.focus_set()
        self.score_canvas = self.canvas.create_text(100, BOARD_HIGHT * CELL_SIZE,
                                                    text="score: " + str(self.board.pacman.score), fill="yellow",
                                                    font=("MV Boli", 17, "bold"), anchor='w')
        self.lives_canvas = self.canvas.create_text(340, BOARD_HIGHT * CELL_SIZE,
                                                    text="lives left: " + str(self.board.pacman.lives), fill="yellow",
                                                    font=("MV Boli", 17, "bold"), anchor='w')
        self.static_drawing_objects = []
        self.moving_drawing_objects = []
        for obj in self.board.food:
            img = ImageTk.PhotoImage(file=obj.get_sprite())
            self.static_drawing_objects.append(DrawingObject(obj, self.canvas.create_image(obj.location.x * CELL_SIZE,
                                                                                           obj.location.y * CELL_SIZE,
                                                                                           image=img, anchor="nw"), img,
                                                             self.canvas))
        for obj in self.board.moving_gameObjects:
            img = ImageTk.PhotoImage(file=obj.get_sprite())
            self.moving_drawing_objects.append(DrawingObject(obj, self.canvas.create_image(obj.location.x * CELL_SIZE,
                                                                                           obj.location.y * CELL_SIZE,
                                                                                           image=img, anchor="nw"), img,
                                                             self.canvas))
        self.canvas.bind('<Up>', lambda e: self.board.pacman.set_direction_up())
        self.canvas.bind('<Down>', lambda e: self.board.pacman.set_direction_down())
        self.canvas.bind('<Left>', lambda e: self.board.pacman.set_direction_left())
        self.canvas.bind('<Right>', lambda e: self.board.pacman.set_direction_right())
