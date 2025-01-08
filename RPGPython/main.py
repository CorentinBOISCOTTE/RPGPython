from Game import Game

def main():
    game = Game()
    game.start()

    while not game.close:
        game.update()

if __name__ == "__main__":
    main()