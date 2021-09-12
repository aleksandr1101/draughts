import utils
import moving


def check_draughts_fight(c1, c2, c3, turn, active):
    """Checking if we can beat by draught"""
    if ((c1.queen == 0) and (c1.color == turn) and ((active is None) or (c1 == active)) and
            (c2.color != 0) and (c2.color != turn) and (c3.color == 0) and c2.can_beat):
        return True
    return False


def check_queen_fight_for_one_way(board, d, start, finish, step, res=0):
    """Checking if we can beat by queen by increasing way or decreasing way of diagonal"""
    cells = board.cells
    turn = board.turn
    cnt1 = 0
    cnt2 = -1
    ans = []
    for j in range(start, finish, step):
        c2 = cells[d[j]]
        if c2.color == turn:
            break
        elif c2.color == 0:
            if cnt2 == -1:
                cnt1 += 1
            else:
                ans.append(c2)
                cnt2 += 1
        else:
            if cnt2 == -1 and c2.can_beat == 1:
                cnt2 = 0
            else:
                break
    if res == 0:
        return cnt1 >= 0 and cnt2 > 0
    else:
        return ans


def check_queen_fight(board, d, i):
    """Checking if we can beat by queen"""
    cells = board.cells
    c1 = cells[d[i]]
    active = board.active
    if c1.color != board.turn or c1.queen != 1 or ((active is not None) and (c1 != active)):
        return False
    # checking for the increasing and decreasing j
    return (check_queen_fight_for_one_way(board, d, i + 1, len(d), 1) or
            check_queen_fight_for_one_way(board, d, i - 1, -1, -1))


def check_fight(board):
    """Checking if fight is obligatory"""
    cells = board.cells
    turn = board.turn
    active = board.active
    for d in board.diagonals:
        for i in range(0, len(d) - 2):
            c1 = cells[d[i + 0]]
            c2 = cells[d[i + 1]]
            c3 = cells[d[i + 2]]
            if check_draughts_fight(c1, c2, c3, turn, active) or check_draughts_fight(c3, c2, c1, turn, active):
                return True
        for i in range(0, len(d)):
            if check_queen_fight(board, d, i):
                return True
    return False


def find_killed(board, c1, c2):
    """find killed draught between c1 and c2"""
    d = None
    cells = board.cells
    for i in board.diagonals:
        if ((c1.x, c1.y) in i) and ((c2.x, c2.y) in i):
            d = i
            break
    tmp = None
    cnt = 0
    for i in d:
        cell = cells[i]
        if cell == c1 or cell == c2:
            cnt += 1
        if cnt == 2:
            break
        if cell.color != 0:
            tmp = cell
    return tmp


def do_move(board, c1, c2):
    board.clear_borders()
    c2.color = c1.color
    c2.queen = c1.queen
    if (c2.x == 0) and (c2.color == 1) or (c2.x == 7) and (c2.color == 2):
        c2.queen = 1
    c1.color = 0
    c1.queen = 0
    if board.must_beat:
        tmp = find_killed(board, c1, c2)
        tmp.can_beat = False
        board.active = c2
        board.chosen = c2
        if check_fight(board):
            c2.border = 1
            steps = moving.find_steps(board, c2)
            utils.mark_cells(steps)
        else:
            board.pass_move()
    else:
        board.pass_move()


def get_clear_cells(board, d, start, finish, step):
    """get clear cells on the diag d from start to finish"""
    ans = []
    for i in range(start, finish, step):
        cell = board.cells[d[i]]
        if cell.color == 0:
            ans.append(cell)
        else:
            break
    return ans


def find_step_for_queen(board, cell):
    ans = []
    for d in cell.ways:
        i = d.index((cell.x, cell.y))
        if board.must_beat == 0:
            ans.extend(get_clear_cells(board, d, i + 1, len(d), 1))
            ans.extend(get_clear_cells(board, d, i - 1, -1, -1))
        else:
            ans.extend(check_queen_fight_for_one_way(board, d, i + 1, len(d), 1, 1))
            ans.extend(check_queen_fight_for_one_way(board, d, i - 1, -1, -1, 1))
    return ans


def find_step_for_draught(board, cell):
    x = cell.x
    y = cell.y
    ans = []
    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            x1 = x + i
            y1 = y + j
            if not (x1, y1) in board.cells:
                continue
            c2 = board.cells[(x1, y1)]
            if board.must_beat == 1:
                x2 = x1 + i
                y2 = y1 + j
                if not (x2, y2) in board.cells:
                    continue
                c3 = board.cells[(x2, y2)]
                if check_draughts_fight(cell, c2, c3, board.turn, board.active):
                    ans.append(c3)
            else:
                if (board.turn == 1) and (i == 1) or (board.turn == 2) and (i == -1):
                    continue
                if c2.color == 0:
                    ans.append(c2)
    return ans


def find_steps(board, cell, flag=False):
    if not flag:
        if (board.active is not None) and (cell != board.active):
            return
        board.must_beat = check_fight(board)
    f = find_step_for_draught
    if cell.queen == 1:
        f = find_step_for_queen
    return f(board, cell)
