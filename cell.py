class Cell:
    """name, color{0, 1, 2}, queen{0, 1}, border{0, 1, 2}"""

    def __init__(self, x, y, color):
        self.name = chr(x + 97) + str(y + 1)
        self.x = x
        self.y = y
        self.color = color
        self.border = 0
        self.queen = 0
        self.ways = []
        self.can_beat = True

    def clear_cell(self):
        self.queen = 0
        self.color = 0
        self.border = 0
        self.can_beat = True
