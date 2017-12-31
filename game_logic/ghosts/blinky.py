from game_logic import Point
from game_logic.ghost import Ghost


class Blinky(Ghost):
    def __init__(self, x, y, board, speed):
        sprite = "./sprites/ghost_red.png"
        super().__init__(x, y, board, speed, sprite)
        self.base = Point(13, 1)

    def _update_destination(self):
        if self.board.game_state == "scatter":
            self.destination = self._account_portals(self.base)
        elif self.board.game_state == "chase":
            self.destination = self._account_portals(self.board.pacman.location)
