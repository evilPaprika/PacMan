from game_logic import Point
from game_logic.ghost import Ghost


class Clyde(Ghost):
    def __init__(self, x, y, board, speed):
        sprite = "./sprites/ghost_yellow.png"
        super().__init__(x, y, board, sprite, speed)
        self.base = Point(1, 13)

    def _update_destination(self):
        if self.board.game_state == "scatter":
            self.destination = self._account_portals(self.base)
        elif self.board.game_state == "chase":
            if self.location.distance(self.board.pacman.location) > 8:
                self.destination = self._account_portals(self.board.pacman.location)
            else:
                self.destination = self._account_portals(self.base)
