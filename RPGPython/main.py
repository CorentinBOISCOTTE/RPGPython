import pygame
from Game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RPG Adventure")

    game = Game(screen)
    game.start_adventure()

    pygame.quit()

if __name__ == "__main__":
    main()
