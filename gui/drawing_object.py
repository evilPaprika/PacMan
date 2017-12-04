from PIL import ImageTk


class DrawingObject:
    def __init__(self, board_object, canvas_id, image, canvas):
        self.board_object = board_object
        self.canvas_ID = canvas_id
        self.image = image
        self.canvas = canvas

    def update_sprite(self):
        self.image = ImageTk.PhotoImage(file=self.board_object.get_sprite())
        self.canvas.itemconfig(self.canvas_ID, image=self.image)
