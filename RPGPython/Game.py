from random import randint
from Character import Character
import time

class Game:
    def __init__(self):
        self.close = False
        self.started = False
        self.character = None
        self.zone = 0

    def roll_stat(self):
        return sum(sorted([randint(1, 6) for _ in range(4)])[1:])

    def start(self):
        print("Welcome to RPGPython")
        print("Loading...")
        time.sleep(2)

        name = input("What is your name? ")
        print("You start with base stats. Rolling for your abilities...")

        stats = {stat: self.roll_stat() for stat in
                 ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']}
        modifiers = {key: (value - 10) // 2 for key, value in stats.items()}

        print("\nYour rolled stats:")
        for stat, value in stats.items():
            print(f"{stat.capitalize()}: {value} (modifier: {modifiers[stat]})")

        self.character = Character(name, stats['constitution'], stats['strength'], stats['dexterity'],
                                   stats['intelligence'], stats['wisdom'], stats['charisma'])
        print(f"\nWelcome, {name}! Your adventure begins.")
        print("Type 'start' to proceed.")

    def skill_check(self, modifier, dc):
        roll = randint(1, 20)
        total = roll + modifier
        print(f"Rolled {roll} + {modifier} = {total}")
        return total >= dc

    def check_input(self):
        user_input = input().strip().lower()
        if not self.started and user_input == "start":
            self.started = True

    def show_character_info(self):
        print("--- Character Info ---")
        print(self.character)
        print("----------------------")

    def load_current_zone(self):
        if self.zone == 0:
            self.zone0()
        if self.zone == 1:
            self.zone1()
        if self.zone == 2:
            self.zone2()
        if self.zone == 3:
            self.zone3()
        if self.zone == 4:
            self.zone4()

    def enforce_limits(self):
        if self.character.hp <= 0:
            print("Warning: Your HP has dropped to zero! Be cautious.")
        if self.character.hp > self.character.max_hp:
            self.character.hp = self.character.max_hp
            print("Your HP is at its maximum limit.")

    def grant_experience(self, amount):
        self.character.gain_experience(amount)

    def zone0(self):
        print("You find yourself in a quiet meadow. What do you do?")
        print("(a) Explore a cave\n(b) Follow a path\n(c) Rest")
        choice = input("Your choice: ").lower()

        if choice == "a":
            print("You find a shiny stone and gain some experience.")
            self.grant_experience(5)
        elif choice == "b":
            print("You discover a map etched into a tree.")
            self.grant_experience(3)
        elif choice == "c":
            print("You rest and regain 2 HP.")
            self.character.heal(2)
        else:
            print("You remain undecided.")

        self.show_character_info()
        self.zone += 1

    def zone1(self):
        print("You enter a forest. Suddenly, a wild boar charges at you.")
        if self.skill_check(self.character.dexterity, 10):
            print("You dodge successfully and gain experience.")
            self.grant_experience(5)
        else:
            print("The boar grazes you. You lose 2 HP.")
            self.character.take_damage(2)

        self.show_character_info()
        self.zone += 1

    def zone2(self):
        print("You reach an abandoned village. Do you explore the houses? (yes/no)")
        choice = input("Your choice: ").lower()

        if choice == "yes":
            print("You find a potion and restore HP.")
            self.character.heal(5)
            self.grant_experience(3)
        else:
            print("You move on cautiously.")

        self.show_character_info()
        self.zone += 1

    def zone3(self):
        print("You enter a dark labyrinth. Choose a path: (left/right/forward)")
        choice = input("Your choice: ").lower()

        if choice == "left":
            print("You encounter a trap.")
            if self.skill_check(self.character.intelligence, 12):
                print("You disarm the trap.")
                self.grant_experience(5)
            else:
                print("You take damage from the trap.")
                self.character.take_damage(4)
        elif choice == "right":
            print("You find a treasure chest.")
            self.grant_experience(5)
        else:
            print("You solve a riddle and gain experience.")
            self.grant_experience(5)

        self.show_character_info()
        self.zone += 1

    def zone4(self):
        print("You face a final boss. Prepare for battle!")
        if self.skill_check(self.character.strength, 15):
            print("You defeat the boss. Congratulations!")
            self.grant_experience(10)
        else:
            print("The boss overpowers you. You barely escape.")
            self.character.take_damage(5)

        self.show_character_info()
        self.close = True

    def update(self):
        self.check_input()
        if not self.started:
            return
        self.load_current_zone()