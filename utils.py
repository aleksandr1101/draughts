import pygame
from os import path


def clear_cell(cell):
    cell.can_beat = 1
    cell.color = 0
    cell.border = 0
    cell.queen = 0


def clear_borders(cells):
    for key in cells:
        cells[key].border = 0


def start_new_game(cells):
    # clean cells
    for key in cells:
        clear_cell(cells[key])

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


def open_state():
    # todo: write this part
    return None


def save_state():
    # todo: write this part
    return None


# load picture ./src/name with rect
def get_picture(name, rect=None):
    if rect is not None:
        p = pygame.transform.scale(pygame.image.load(path.join("img", name)), rect)
    else:
        p = pygame.image.load(path.join("img", name))
    return p


def draw_cell(screen, cell):
    x = cell.x
    y = cell.y

    if cell.border == 1:
        pygame.draw.rect(screen, (102, 0, 255), (y * 75, x * 75, 75, 75), 2)
    elif cell.border == 2:
        pygame.draw.rect(screen, (254, 254, 34), (y * 75, x * 75, 75, 75), 2)

    if cell.color != 0:
        s = ("draught" if cell.queen == 0 else "queen") + "_" + ("black" if cell.color == 2 else "white") + ".png"
        pic = get_picture(s, (75, 75))
        screen.blit(pic, (y * 75, x * 75))


def toast(screen, s):
    """print the text on the screen"""
    text = pygame.font.Font(None, 30).render(str(s), 1, (0, 0, 0))
    screen.blit(text, (300, 300))


def mark_cells(cells):
    """make the border above the possible moves"""
    for i in cells:
        i.border = 2
