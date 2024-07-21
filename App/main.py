import pygame
from constant import *
import game

pygame.init()

window = pygame.display.set_mode((X,Y))
pygame.display.set_caption("Connect 4")

def main():
    while True:
        game.menu(window)


if __name__ == "__main__":
    main()