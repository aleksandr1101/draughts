from cell import Cell
import utils
import moving


class Board:
    def __init__(self):
        self.turn = 1
        self.chosen = None
        self.must_beat = False
        self.active = None
        # diagonals
        self.diagonals = list()
        d = self.diagonals
        for i in range(7):
            if i % 2 == 0:
                lst1 = list()
                lst2 = list()
                for j in range(8 - i):
                    lst1.append((7 - j, j + i))
                    lst2.append((7 - j - i, j))
                d.append(lst1)
                if i != 0:
                    d.append(lst2)
            else:
                lst1 = list()
                lst2 = list()
                for j in range(8 - i):
                    lst1.append((7 - j, 7 - j - i))
                    lst2.append((7 - j - i, 7 - j))
                d.append(lst1)
                d.append(lst2)

        # init cells
        self.cells = dict()
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.cells[(i, j)] = Cell(i, j, 0)
        for d in self.diagonals:
            for i in d:
                self.cells[i].ways.append(d)

    def start_new_game(self):
        self.turn = 1
        self.must_beat = False
        self.chosen = None
        cells = self.cells
        # clean cells
        for key in cells:
            utils.clear_cell(cells[key])

        # setting black pieces
        for i in range(0, 3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    cells[(i, j)].color = 2

        # setting white pieces
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    cells[(i, j)].color = 1

    def clear_borders(self):
        for key in self.cells:
            self.cells[key].border = 0

    def pass_move(self):
        self.turn = (1 if self.turn == 2 else 2)
        self.active = None
        self.chosen = None
        self.must_beat = False
        for key in self.cells:
            cell = self.cells[key]
            if cell.can_beat is False:
                cell.clear_cell()
        if not self.have_steps():
            self.start_new_game()

    def have_steps(self):
        self.must_beat = moving.check_fight(self)
        if self.must_beat:
            return True
        for key in self.cells:
            cell = self.cells[key]
            if cell.color == self.turn:
                t = moving.find_steps(self, cell, True)
                if len(t) > 0:
                    return True
        return False
