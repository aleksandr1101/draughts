import pygame
import sys
from cell import Cell
import random
import utils
import moving
from board import Board


# initializing game
pygame.init()

# create the screen
screenX = 600
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))
bg = utils.get_picture("board.jpg", (screenX, screenY))

# title and icon
pygame.display.set_caption("Checkers")
icon = utils.get_picture("checkers.png")
pygame.display.set_icon(icon)

# initial settings
board = Board()
board.start_new_game()
# board.cells[(4, 3)].color = 2
# board.cells[(2, 5)].color = 0
# board.cells[(5, 2)].queen = 1
running = True

# game loop
while running:
    for event in pygame.event.get():
        # quit the game
        if event.type == pygame.QUIT:
            running = False

        # load, save or start new game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                board.start_new_game()
            elif event.key == pygame.K_s:
                utils.save_state()
            elif event.key == pygame.K_o:
                utils.open_state()

        # moving the draughts
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = int(y / 75)
            col = int(x / 75)
            if ((row + col) % 2 == 0) or (board.cells[(row, col)] is board.chosen):
                # Canceling the selection
                board.chosen = None
                board.clear_borders()
            else:
                # pressed cell
                cell = board.cells[(row, col)]
                if cell.border == 2:
                    # if we choose the move
                    moving.do_move(board, board.chosen, cell)
                elif cell.border == 0:
                    # if we re-choose the cell
                    board.clear_borders()
                    if cell.color != board.turn:
                        # wrong color
                        board.chosen = None
                        continue
                    else:
                        # find possible moves
                        cell.border = 1
                        board.chosen = cell
                        steps = moving.find_steps(board, cell)
                        utils.mark_cells(steps)

    # setting up bg
    screen.blit(bg, (0, 0))

    # drawing cells
    for key in board.cells:
        x, y = key
        t = board.cells[key]
        utils.draw_cell(screen, t)

    # update screen
    pygame.display.update()
