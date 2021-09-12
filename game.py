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
        if event.type == pygame.MOUSEBUTTONDOWN and board.turn == 1:
            utils.go_move(event, board)

    if board.turn == 2:
        k = list(board.cells.keys())
        random.shuffle(k)
        for key in k:
            cell = board.cells[key]
            if cell.color != 2:
                continue
            steps = moving.find_steps(board, cell)
            if (steps is not None) and (len(steps) > 0):
                s = steps[random.randint(0, len(steps) - 1)]
                board.chosen = cell
                cell.border = 1
                moving.do_move(board, cell, s)
                break

    # setting up bg
    screen.blit(bg, (0, 0))

    # drawing cells
    for key in board.cells:
        x, y = key
        t = board.cells[key]
        utils.draw_cell(screen, t)

    # update screen
    pygame.display.update()
