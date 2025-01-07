from random import randint
from Character import Character
import time

class Game:
    def __init__(self):
        self.close = False
        self.character = None

    def start(self):
        print("Welcome to RPGPython")
        print("Loading...")
        time.sleep(5)
        name = ""
        print("What is your name?")
        name = input()
        print("You start with 10HP")
        print("Welcome " + name + "!")
        strength = randint(-5, 5)
        dexterity = randint(-5, 5)
        constitution = randint(-5, 5)
        intelligence = randint(-5, 5)
        wisdom = randint(-5, 5)
        charisma = randint(-5, 5)
        print("You have a strength bonus of " + str(strength) + ".")
        print("You have a dexterity bonus of " + str(dexterity) + ".")
        print("You have a constitution bonus of " + str(constitution) + ".")
        print("You have an intelligence bonus of " + str(intelligence) + ".")
        print("You have a wisdom bonus of " + str(wisdom) + ".")
        print("You have a charisma bonus of " + str(charisma) + ".")
        self.character = Character(name, 10, strength, dexterity, constitution, intelligence, wisdom, charisma)
        print("Advice : you can type <<close>> to leave the game")
        print("Avice : type <<info>> to get your player's information")

    def check_input(self):
        user_input = str(input())
        if user_input == "close":
            print("Closing...")
            time.sleep(3)
            self.close = True
        if user_input == "info":
            print(self.character)

    def update(self):
        self.check_input()

