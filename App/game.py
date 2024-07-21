import pygame, sys
from pygame.locals import *
import connect4
import gui
from constant import *

def convert(x_pos):
    #convert x coordinates from mouse click to col index
    x = x_pos // 90
    return x

def menu(win):
    gui.print_menu(win)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x < X/3:  #1 player chosen
                    select_diff(win)
                elif x < (X/3)*2:  #2 player chosen
                    init_game(win, 2)
                else:
                    pygame.quit()
                    sys.exit()


def select_diff(win):
    gui.print_difficulty(win)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x < X/3:
                    diff = 1
                elif x < (X/3)*2:
                    diff = 3
                else:
                    diff = 6
                init_game(win, 1, diff)

def init_game(win, game_type, diff = 0):
    grid = connect4.createGrid()
    f_grid, p_grid = connect4.get_bitmap(grid, connect4.P1)

    gui.displayGrid(grid, win)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

    while True:
        player = connect4.getTurn(grid)

        #if player vs AI
        if game_type == 1 and player == connect4.P2:
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            pygame.time.delay(500)
            best_move = connect4.bestMove(f_grid, p_grid, diff)
            connect4.selectSlot(grid, player, best_move)
            f_grid, p_grid = connect4.bit_select_move(f_grid, p_grid, best_move)
            gui.displayGrid(grid, win)
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = convert(x)
                print("col selected:", col)
                if connect4.checkFullSlot(grid, col) == False:
                    connect4.selectSlot(grid, player, col)
                    f_grid, p_grid = connect4.bit_select_move(f_grid, p_grid, col)
                    gui.displayGrid(grid, win)
                connect4.displayGrid(grid)

            #check end game result
            result1 = connect4.checkWin(f_grid^p_grid)
            result2 = connect4.checkTie(grid)

            if result1:  # if win
                if player == connect4.P1 or game_type == 2:
                    gui.printWin(win, player)
                else:
                    gui.printLose(win)
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pygame.time.delay(1000)
                menu(win)

            elif result2:
                gui.printDraw(win)
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pygame.time.delay(1000)
                menu(win)

            pygame.display.update()

                
