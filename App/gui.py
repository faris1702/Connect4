import pygame, sys
from pygame.locals import *
from constant import *
import connect4


pygame.init()


#used to print text on screen
def print_text(text, color, size, x_pos, y_pos, win, highlight=None):
    font = pygame.font.SysFont(None, size)
    text = font.render(text, True, color, highlight)
    txtRct = text.get_rect()
    txtRct.center = (x_pos, y_pos)
    win.blit(text, txtRct)

def printWin(win, type):
    pygame.draw.rect(win, white, pygame.Rect(0, Y/2 - 45, X, 90))
    if type == connect4.P1:
        type = 1
    else:
        type = 2
    print_text(f"Player {type} won", green, 90, X/2, Y/2, win)
    pygame.display.update()

def printDraw(win):
    pygame.draw.rect(win, white, pygame.Rect(0, Y/2 - 45, X, 90))
    print_text("It is a draw", red, 90, X/2, Y/2, win)
    pygame.display.update()

def printLose(win):
    pygame.draw.rect(win, white, pygame.Rect(0, Y/2 - 45, X, 90))
    print_text(f"AI won", red, 90, X/2, Y/2, win)
    pygame.display.update()

def print_menu(win):
    win.fill(white)
    pygame.draw.line(win, black, (X/3,0), (X/3, Y), 1)
    pygame.draw.line(win, black, ((X/3)*2,0), ((X/3)*2, Y), 1)
    print_text("1 Player", black, 60, 105, Y/2, win)
    print_text("2 Player", black, 60, 315, Y/2, win)
    print_text("Quit", black, 60, 535, Y/2, win)
    pygame.display.update()

def print_difficulty(win):
    win.fill(white)
    pygame.draw.line(win, black, (X/3,0), (X/3, Y), 1)
    pygame.draw.line(win, black, ((X/3)*2,0), ((X/3)*2, Y), 1)
    print_text("Easy", black, 60, 105, Y/2, win)
    print_text("Medium", black, 60, 315, Y/2, win)
    print_text("Hard", black, 60, 535, Y/2, win)
    pygame.display.update()

def displayGrid(grid, win):
    win.fill(blue)
    for i in range(6):
        for j in range(7):
            if grid[i][j] == ' ':
                pygame.draw.circle(win, white, (45+(90*j), 45+(90*i)), 30)
            elif grid[i][j] == connect4.P1:
                pygame.draw.circle(win, red, (45+(90*j), 45+(90*i)), 30)
            elif grid[i][j] == connect4.P2:
                pygame.draw.circle(win, yellow, (45+(90*j), 45+(90*i)), 30)
    pygame.display.update()

