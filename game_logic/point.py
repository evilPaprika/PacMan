class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance(self, other):
        x = abs(self.x - other.x)
        y = abs(self.y - other.y)
        return y if y > x else x
        # return (self.x - other.x)**2 + (self.y - other.y)**2

    def __hash__(self) -> int:
        a = round(self.x)
        b = round(self.y)
        return int((a + b) * (a + b + 1) / 2 + a)

    def __eq__(self, other):
        return abs(self.x - other.x) < 0.00001 and abs(self.y - other.y) < 0.00001

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __str__(self):
        return "{}, {}".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __round__(self):
        return Point(round(self.x), round(self.y))
    
    def normalise(self):
        n_x = self.x / abs(self.x) if self.x != 0 else 0
        n_y = self.y / abs(self.y) if self.y != 0 else 0
        return Point(n_x, n_y)

    def heading_same_way(self, other):
        # напр (0.5, 0) и (1, 0)
        return self.normalise() == other.normalise()
