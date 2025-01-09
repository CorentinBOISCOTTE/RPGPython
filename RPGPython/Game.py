from random import *

from ASCII_art import *
from Character import Character
import time

class Game:
    def __init__(self):
        self.character = None
        self.close = False
        self.inventory = []

    @staticmethod
    def display_loading(delay=True):
        if delay:
            time.sleep(2)

    @staticmethod
    def roll_stat():
        """4d6, take the 3 highest"""
        return sum(sorted([randint(1, 6) for _ in range(4)])[1:])

    @staticmethod
    def skill_check(ability_score, difficulty):
        """d20"""
        modifier = Character.calculate_modifier(ability_score)
        roll = randint(1, 20)
        total = roll + modifier
        print(f"Rolled a {roll} + {modifier} (modifier) = {total} (DC: {difficulty})")
        return total >= difficulty

    @staticmethod
    def get_valid_choice(options):
        choice = input("Your choice: ").lower()
        while choice not in options:
            print(f"Invalid choice! Please choose from {', '.join(options)}.")
            choice = input("Your choice: ").lower()
        return choice

    @staticmethod
    def wait_input():
        user_input = str(input("Do you wish to continue? [y/n]").lower())
        if user_input == "y":
            return
        elif user_input == "n":
            print("Thank you for playing.")
            exit()

    def collect_item(self, item):
        self.inventory.append(item)
        print(f"You have collected a {item}.")

    def use_item(self, item):
        if item not in self.inventory:
            print(f"You don't have a {item} in your inventory.")
            return
        if item == "healing potion":
            self.character.heal(5)
            draw_healing()
            print("You used a healing potion and restored 5 HP!")
            self.inventory.remove(item)
        else:
            print(f"{item} cannot be used right now.")

    def character_status(self):
        print("\n--- Character Status ---")
        print(self.character)
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print("------------------------")


    def start_adventure(self):
        print("Welcome to RPGPython - A Text-Based Adventure")
        print("Loading...")
        self.display_loading()

        name = input("What is your name, adventurer? ")
        print("\nRolling stats for your abilities...\n")

        stats = {stat: self.roll_stat() for stat in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']}
        modifiers = {key: (value - 10) // 2 for key, value in stats.items()}

        print("Your stats:")
        for stat, value in stats.items():
            print(f"{stat.capitalize()}: {value} (modifier: {modifiers[stat]})")

        self.character = Character(name, stats['constitution'], stats['strength'], stats['dexterity'],
                                   stats['intelligence'], stats['wisdom'], stats['charisma'])
        print(f"\nWelcome, {name}! Let your adventure begin.")
        time.sleep(2)
        self.zone0()

    def zone0(self):
        draw_forest()
        print("\nYou find yourself at the edge of a dense forest. The sun is setting.")
        print("What will you do?")
        print("(a) Enter the forest cautiously\n(b) Set up camp for the night")

        choice = self.get_valid_choice(["a", "b"]).lower()
        if choice == "a":
            print("You step into the forest and hear strange noises. A wild animal appears!")
            self.wait_input()
        elif choice == "b":
            print("You set up camp and rest. You recover your strength.")
            time.sleep(2)
            user_input = input("Do you wish to continue the adventure? (if you say no you will quit being an adventurer) [y/n]").lower()
            if user_input == "y":
                print("You decide to continue the adventure and wander into the forest.")
                time.sleep(2)
            else:
                print("You quit being an adventurer, you prefer sleeping by the campfire.")
                exit()

        self.zone1()

    def zone1(self):
        draw_boar()
        print("\nYou encounter a wild boar! It looks aggressive.")
        print("(a) Attack the boar\n(b) Try to scare it away\n(c) Climb a tree to escape")

        choice = self.get_valid_choice(["a", "b", "c"]).lower()
        if choice == "a":
            if self.skill_check(self.character.strength, 12):
                print("You strike the boar with your weapon and it runs away. You gain 5 experience points.")
                self.character.gain_experience(5)
            else:
                print("You miss! The boar charges and hits you for 3 HP.")
                self.character.take_damage(3)
        elif choice == "b":
            if self.skill_check(self.character.charisma, 10):
                print("You shout and wave your arms. The boar flees. You gain 3 experience points.")
                self.character.gain_experience(3)
            else:
                print("Your attempt fails. The boar charges and grazes you for 2 HP.")
                self.character.take_damage(2)
        elif choice == "c":
            if self.skill_check(self.character.dexterity, 10):
                print("You climb the tree quickly and avoid the boar. It eventually leaves.")
            else:
                print("You struggle to climb and the boar hits you for 3 HP before running off.")
                self.character.take_damage(3)

        if self.character.hp == 0:
            return

        self.character_status()
        self.wait_input()
        self.zone2()

    def zone2(self):
        draw_cabin()
        print("\nYou find an abandoned cabin in the woods.")
        print("(a) Search the cabin\n(b) Ignore it and move on")

        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            draw_potion()
            print("You search the cabin and find a healing potion!")
            self.collect_item("healing potion")
            self.character.gain_experience(3)
        elif choice == "b":
            print("You decide not to risk entering the cabin.")
        self.character_status()
        print("What do you wish to do now ?")
        print("(a) Continue\n(b) Find a nearby village")

        user_input = self.get_valid_choice(["a", "b"]).lower()
        if user_input == "a":
            self.zone3()
        elif user_input == "b":
            print("You find a small village where the locals welcome you with a meal. You heal 1 HP")
            self.character.heal(1)
            time.sleep(1)
            user_input = input("Do you wish to continue the adventure? (if you say no you will quit being an adventurer, and you will stay with the villagers) [y/n]").lower()
            if user_input == "y":
                print("You decide to continue the adventure and go even deeper into the forest.")
                time.sleep(2)
            else:
                print("You quit being an adventurer, you will stay with the villagers and found a family.")
                exit()
        self.zone3()

    def zone3(self):
        self.wolf_fight()

        if self.character.hp == 0:
            return

        self.character_status()
        time.sleep(2)
        self.end_game()

    def wolf_fight(self):
        draw_wolf()
        print("\nYou reach the heart of the forest and encounter a powerful wolf!")
        print("(a) Fight the wolf\n(b) Try to tame it\n(c) Sneak past it\n(d) Use an item")

        choice = self.get_valid_choice(["a", "b", "c", "d"]).lower()
        if choice == "a":
            if self.skill_check(self.character.strength, 15):
                print("You defeat the wolf in a fierce battle! You gain 10 experience points.")
                self.character.gain_experience(10)
            else:
                print("The wolf is too strong! You lose 5 HP but manage to drive it away.")
                self.character.take_damage(5)
        elif choice == "b":
            if self.skill_check(self.character.charisma, 15):
                print("You calm the wolf and gain its trust. It leaves peacefully.")
                self.character.gain_experience(8)
            else:
                print("The wolf growls and attacks! You lose 4 HP.")
                self.character.take_damage(4)
        elif choice == "c":
            if self.skill_check(self.character.dexterity, 12):
                print("You sneak past the wolf without being noticed.")
            else:
                print("The wolf spots you and attacks! You lose 5 HP.")
                self.character.take_damage(5)
        elif choice == "d":
            item = input("Which item do you want to use? ").lower()
            self.use_item(item)
            self.wait_input()
            self.wolf_fight()

    def end_game(self):
        print("\nYou emerge from the forest, battered but alive. The adventure ends here.")
        print(f"Level {self.character.level} {self.character.name} finished the adventure with {self.character.hp} HP.")
        print("Thank you for playing RPGPython!")