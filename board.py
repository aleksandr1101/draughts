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
        d.append([(7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)])
        d.append([(7, 6), (6, 5), (5, 4), (4, 3), (3, 2), (2, 1), (1, 0)])
        d.append([(6, 7), (5, 6), (4, 5), (3, 4), (2, 3), (1, 2), (0, 1)])
        d.append([(7, 2), (6, 3), (5, 4), (4, 5), (3, 6), (2, 7)])
        d.append([(5, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 5)])
        d.append([(7, 4), (6, 3), (5, 2), (4, 1), (3, 0)])
        d.append([(4, 7), (3, 6), (2, 5), (1, 4), (0, 3)])
        d.append([(3, 0), (2, 1), (1, 2), (0, 3)])
        d.append([(7, 4), (6, 5), (5, 6), (4, 7)])
        d.append([(7, 2), (6, 1), (5, 0)])
        d.append([(2, 7), (1, 6), (0, 5)])
        d.append([(7, 6), (6, 7)])
        d.append([(1, 0), (0, 1)])
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
