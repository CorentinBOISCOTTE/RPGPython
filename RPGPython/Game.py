from asyncio import wait_for
from random import randint
from Character import Character
import time
import os

class Game:
    def __init__(self):
        self.close = False
        self.character = None

    def start(self):
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

    def update(self):
        user_input = str(input())
        if user_input == "close":
            print("Closing...")
            time.sleep(5)
            self.close = True
