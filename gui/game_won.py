import tkinter as tk
import gui.game


class GameWon(tk.Frame):
    def __init__(self, parent, score):
        tk.Frame.__init__(self, parent)
        self.label1 = tk.Label(parent, text="CONGRATULATIONS", bg="black", fg="yellow", font=("MV Boli", 38, "bold"))
        self.label1.place(relx=.5, rely=.15, anchor="center")
        self.label2 = tk.Label(parent, text="FINAL SCORE: " + str(score),
                               bg="black", fg="yellow", font=("MV Boli", 13, "bold"))
        self.label2.place(relx=.5, rely=.23, anchor="center")
        self.new_game = tk.Label(parent, text="START NEW GAME", bg="black", fg="yellow", font=("MV Boli", 18, "bold"))
        self.new_game.place(relx=.5, rely=.50, anchor="center")
        self.quit = tk.Label(parent, text="QUIT", bg="black", fg="yellow", font=("MV Boli", 18, "bold"))
        self.quit.place(relx=.5, rely=.57, anchor="center")
        self.new_game.bind("<Button-1>",lambda e: parent.change_frame(gui.game.Game(parent)))
        self.new_game.bind("<Enter>", lambda e: self.new_game.configure(fg="red"))
        self.new_game.bind("<Leave>", lambda e: self.new_game.configure(fg="yellow"))
        self.quit.bind("<Button-1>", lambda e: parent.quit())
        self.quit.bind("<Enter>", lambda e: self.quit.configure(fg="red"))
        self.quit.bind("<Leave>", lambda e: self.quit.configure(fg="yellow"))

