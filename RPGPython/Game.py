from random import *
from ASCII_art import *
from Character import Character
import time

class Game:
    def __init__(self):
        self.character = None
        self.close = False
        self.inventory = []
        self.spoke_to_merchant = False
        self.spoke_to_blacksmith = False
        self.spoke_to_elder = False

    @staticmethod
    def display_loading(delay=True):
        if delay:
            time.sleep(2)

    @staticmethod
    def roll_stat():
        """4d6, take the 3 highest"""
        return sum(sorted([randint(1, 6) for _ in range(4)])[1:])

    @staticmethod
    def skill_check(ability_score, difficulty, ability):
        """d20"""
        modifier = Character.calculate_modifier(ability_score)
        roll = randint(1, 20)
        total = roll + modifier
        print(f"{ability} check...")
        time.sleep(1)
        print(f"Rolled a {roll} + {modifier} (modifier) = {total} (DC: {difficulty})")
        time.sleep(1)
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
        elif item == "magic scroll":
            print("You use the magic scroll to enhance your next action!")
            self.character.strength = min(20, self.character.strength + 2)
            self.inventory.remove(item)
        else:
            print(f"{item} cannot be used right now.")

    def character_status(self):
        print("\n--- Character Status ---")
        print(self.character)
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print("------------------------")

    def check_game_over(self):
        if self.character.hp <= 0:
            print(f"{self.character.name} has succumbed to their injuries. Game Over!")
            exit()

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
        events = [
            "A friendly merchant approaches and offers supplies. Something seems off about him, you decline his offer.",
            "You hear a rustling in the bushes. Something is watching you.",
            "The night is calm, and you rest peacefully."
        ]
        print(events[randint(0, len(events) - 1)])
        print("What will you do?")
        print("(a) Enter the forest cautiously\n(b) Set up camp for the night")

        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            print("You step into the forest and hear strange noises. A wild animal appears!")
            self.wait_input()
        elif choice == "b":
            print("You set up camp and rest. You recover your strength.")
            time.sleep(2)
            print("Do you wish to continue the adventure? (if you say no you will quit being an adventurer) [y/n]")
            user_input = self.get_valid_choice(["y", "n"])
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

        choice = self.get_valid_choice(["a", "b", "c"])
        if choice == "a":
            if self.skill_check(self.character.strength, 12, "Strength"):
                print("You strike the boar with your weapon and it runs away. You gain 5 experience points.")
                self.character.gain_experience(5)
            else:
                print("You miss! The boar charges and hits you for 3 HP.")
                self.character.take_damage(3)
        elif choice == "b":
            if self.skill_check(self.character.charisma, 10, "Charisma"):
                print("You shout and wave your arms. The boar flees. You gain 3 experience points.")
                self.character.gain_experience(3)
            else:
                print("Your attempt fails. The boar charges and grazes you for 2 HP.")
                self.character.take_damage(2)
        elif choice == "c":
            if self.skill_check(self.character.dexterity, 10, "Dexterity"):
                print("You climb the tree quickly and avoid the boar. It eventually leaves.")
            else:
                print("You struggle to climb and the boar hits you for 3 HP before running off.")
                self.character.take_damage(3)

        self.check_game_over()
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
        print("What do you wish to do now?")
        print("(a) Continue\n(b) Find a nearby village")

        user_input = self.get_valid_choice(["a", "b"])
        if user_input == "a":
            self.zone3()
        elif user_input == "b":
            self.visit_village()

        self.zone3()

    def merchant_interaction(self):
        if self.spoke_to_merchant:
            print("Use that scroll wisely.")
            return

        print("\nYou approach a merchant, who greets you with a toothy grin.")
        print('"Adventurer! I see you are on a dangerous quest. I have rare items for sale!"')
        print('"However, if you prove your worth, I might part with a magic scroll for free."')
        print("(a) Try to persuade the merchant for the magic scroll\n(b) Ask to see their wares\n(c) Leave")

        choice = self.get_valid_choice(["a", "b", "c"])
        if choice == "a":
            if self.skill_check(self.character.charisma, 13, "Charisma"):
                print("The merchant is impressed by your words and hands over the magic scroll.")
                self.collect_item("magic scroll")
                self.spoke_to_merchant = True
            else:
                print('"You’ll need to try harder than that," the merchant says, shaking his head.')
        elif choice == "b":
            print("The merchant shows you a variety of items, but you don't have gold to purchase anything.")
            print('"Come back when you’re richer, adventurer!" he says with a wink.')
        elif choice == "c":
            print("You thank the merchant and leave.")
        time.sleep(1)

    def blacksmith_interaction(self):
        if self.spoke_to_blacksmith:
            print("Come on! Go get that wolf!")
            return

        print("\nYou approach the village blacksmith, who is hammering away at a glowing piece of metal.")
        print('"Hail, adventurer," the blacksmith says gruffly. "You look like you could use a better weapon."')
        print('"I can forge you a stronger blade if you help me with a task first."')
        print("(a) Offer to help the blacksmith\n(b) Ask about the task\n(c) Decline and leave")

        choice = self.get_valid_choice(["a", "b", "c"])
        if choice == "a":
            print('"There’s a dangerous wolf in the forest. Bring me its fang, and I’ll forge you something special."')
            print("You agree to the task and prepare yourself for the challenge.")
            self.collect_item("quest: wolf fang")
            self.spoke_to_blacksmith = True
        elif choice == "b":
            print('"There’s a dangerous wolf in the forest. Bring me its fang, and I’ll forge you something special."')
            print("The blacksmith looks you over. 'Think you can handle it?'")
            follow_up = self.get_valid_choice(["yes", "no"])
            if follow_up == "yes":
                print("You accept the blacksmith’s task and prepare for the challenge.")
                self.collect_item("quest: wolf fang")
                self.spoke_to_blacksmith = True
            else:
                print("You decide not to take the task and leave.")
        elif choice == "c":
            print("You thank the blacksmith and leave.")
        time.sleep(1)

    def elder_interaction(self):
        if self.spoke_to_elder:
            print("You must be wise young one. That was a difficult riddle.")
            return

        print("\nYou approach the village elder, who is sitting under a large tree.")
        print('"Greetings, adventurer," the elder says with a kind smile. "You seek wisdom, do you not?"')
        print('"Answer me this riddle, and I shall grant you my blessing."')
        print("The elder clears his throat and begins:")
        print('"I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?"')
        print("(a) Answer the riddle\n(b) Politely decline and leave")

        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            if self.skill_check(self.character.wisdom, 12, "Wisdom"):
                print("'An echo', you say.")
                print("The elder nods approvingly. 'You are wise indeed. Take this blessing.'")
                self.character.gain_experience(5)
                print("You gained 5 experience points!")
                self.spoke_to_elder = True
            else:
                print("The elder shakes his head. 'That is not the correct answer.'")
        elif choice == "b":
            print("You thank the elder and leave.")
        time.sleep(1)

    def visit_village(self):
        print("You find a small village where the locals welcome you with a meal. You heal 1 HP.")
        self.character.heal(1)
        print("\nThe village seems bustling with activity. As you explore, you encounter several villagers.")
        print("Who would you like to talk to?")
        print("(a) The merchant\n(b) The blacksmith\n(c) The elder\n(d) Leave the village")

        choice = self.get_valid_choice(["a", "b", "c", "d"])
        if choice == "a":
            self.merchant_interaction()
        elif choice == "b":
            self.blacksmith_interaction()
        elif choice == "c":
            self.elder_interaction()
        elif choice == "d":
            print("You decide to leave the village and continue your adventure.")
            return

        # Ask the player if they wish to continue exploring the village or leave
        print("\nDo you wish to talk to someone else in the village or leave?")
        print("(a) Talk to someone else\n(b) Leave the village")
        next_action = self.get_valid_choice(["a", "b"])
        if next_action == "a":
            self.visit_village()  # Recursively call the function to allow further interaction
        else:
            print("You decide to leave the village and continue your adventure.")

    def zone3(self):
        self.wolf_fight()
        self.check_game_over()
        self.character_status()
        time.sleep(2)
        self.end_game()

    def wolf_fight(self):
        draw_wolf()
        print("\nYou reach the heart of the forest and encounter a powerful wolf!")
        print("(a) Fight the wolf\n(b) Try to tame it\n(c) Sneak past it\n(d) Use an item")

        choice = self.get_valid_choice(["a", "b", "c", "d"])
        if choice == "a":
            if self.skill_check(self.character.strength, 15, "Strength"):
                print("You defeat the wolf in a fierce battle! You gain 10 experience points.")
                self.character.gain_experience(10)
            else:
                print("The wolf is too strong! You lose 5 HP but manage to drive it away.")
                self.character.take_damage(5)
        elif choice == "b":
            if self.skill_check(self.character.charisma, 15, "Charisma"):
                print("You calm the wolf and gain its trust. It leaves peacefully.")
                self.character.gain_experience(8)
            else:
                print("The wolf growls and attacks! You lose 4 HP.")
                self.character.take_damage(4)
        elif choice == "c":
            if self.skill_check(self.character.dexterity, 12, "Dexterity"):
                print("You sneak past the wolf without being noticed.")
            else:
                print("The wolf spots you and attacks! You lose 5 HP.")
                self.character.take_damage(5)
        elif choice == "d":
            self.character_status()
            item = input("Which item do you want to use? ").lower()
            self.use_item(item)
            self.wait_input()
            self.wolf_fight()

    def end_game(self):
        print("\nYou emerge from the forest, battered but alive. The adventure ends here.")
        print(f"Level {self.character.level} {self.character.name} finished the adventure with {self.character.hp} HP.")
        print("Thank you for playing RPGPython!")
