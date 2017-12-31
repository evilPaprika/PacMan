from game_logic.point import Point

BOARD_WIDTH = 15
BOARD_HEIGHT = 15

def make_location_in_borders(location):
    return Point((location.x + 0.5) % BOARD_WIDTH - 0.5,
            (location.y + 0.5) % BOARD_HEIGHT - 0.5)