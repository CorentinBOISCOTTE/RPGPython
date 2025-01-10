import pygame
from random import randint
from Character import Character

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.character = None
        self.close = False
        self.inventory = []
        self.spoke_to_merchant = False
        self.spoke_to_blacksmith = False
        self.spoke_to_elder = False
        self.font = pygame.font.Font(None, 24)
        self.text_lines = []
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.button_rect = pygame.Rect(30, 900, 150, 50)
        self.button_surface = pygame.Surface((150, 50))
        self.text = self.font.render("Continue", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(self.button_surface.get_width() / 2, self.button_surface.get_height() / 2))
        self.forest_image = pygame.image.load("images/forest.png").convert()
        self.boar_image = pygame.image.load("images/boar.png").convert()
        self.shrek_toilet_image = pygame.image.load("images/shrek_toilet.jpg").convert()
        self.healing_potion_image = pygame.image.load("images/healing_potion.jpg").convert()
        self.healing_image = pygame.image.load("images/healing.jpg").convert()
        self.village_image = pygame.image.load("images/village.jpg").convert()
        self.wolf_image = pygame.image.load("images/wolf.png").convert()
        self.current_image = None

    def wait_for_continue(self):
        while True:
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        return

    def character_status(self):
        stats = [
            ("Strength", self.character.strength),
            ("Dexterity", self.character.dexterity),
            ("Constitution", self.character.constitution),
            ("Intelligence", self.character.intelligence),
            ("Wisdom", self.character.wisdom),
            ("Charisma", self.character.charisma),
        ]

        self.add_message("--- Character Status ---")
        self.add_message(f"Name: {self.character.name}")
        self.add_message(f"Level: {self.character.level}")
        self.add_message(f"HP: {self.character.hp}/{self.character.max_hp}")

        for stat_name, stat_value in stats:
            modifier = self.calculate_modifier(stat_value)
            self.add_message(f"{stat_name}: {stat_value} (modifier = {modifier})")

        inventory_display = ', '.join(self.inventory) if self.inventory else 'Empty'
        self.add_message(f"Inventory: {inventory_display}")
        self.add_message("------------------------")

        self.render()
        self.wait_for_continue()

    def start_adventure(self):
        self.add_message("Welcome to RPGPython - A Text-Based Adventure")
        self.display_loading()
        name = self.get_player_input("What is your name, adventurer?")
        self.add_message("\\nRolling stats for your abilities...")
        pygame.time.wait(2000)

        stats = {stat: self.roll_stat() for stat in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']}
        self.character = Character(name, stats['constitution'], stats['strength'], stats['dexterity'], stats['intelligence'], stats['wisdom'], stats['charisma'], self)
        #self.add_message("Your stats:\\n" + "\\n".join([f"{stat.capitalize()}: {value} (modifier = {self.calculate_modifier(value)})" for stat, value in stats.items()]))
        #self.wait_for_continue()
        self.character_status()
        self.zone0()

    def display_loading(self):
        self.add_message("Loading...")
        pygame.time.wait(2000)

    def check_game_over(self):
        self.add_message(f"{self.character.name} has succumbed to their injuries. Game Over!")
        self.wait_for_continue()
        pygame.quit()
        exit()

    @staticmethod
    def roll_stat():
        rolls = [randint(1, 6) for _ in range(4)]
        return sum(sorted(rolls)[1:])

    @staticmethod
    def calculate_modifier(ability_score):
        return (ability_score - 10) // 2

    def zone0(self):
        self.current_image = self.forest_image
        events = [
            "A friendly merchant approaches and offers supplies. Something seems off about him, you decline his offer.",
            "You hear a rustling in the bushes. Something is watching you.",
            "The night is calm, and you rest peacefully."
        ]
        self.add_message(events[randint(0, len(events) - 1)])
        self.add_message("You find yourself at the edge of a dense forest. The sun is setting.\\n(a) Enter the forest cautiously\\n(b) Set up camp for the night")
        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            self.add_message("You step into the forest and hear strange noises. A wild animal appears!")
            self.wait_for_continue()
            self.zone1()
        elif choice == "b":
            self.add_message("You set up camp and rest. You recover your strength.")
            self.character.heal(5)
            self.wait_for_continue()
            self.zone1()

    def zone1(self):
        self.current_image = self.boar_image
        self.text_lines = []
        self.add_message("You encounter a wild boar! It looks aggressive.\\n(a) Attack the boar\\n(b) Try to scare it away\\n(c) Climb a tree to escape")
        choice = self.get_valid_choice(["a", "b", "c"])
        if choice == "a":
            if self.skill_check(self.character.strength, 12, "Strength"):
                self.add_message("You strike the boar with your weapon and it runs away. You gain 5 XP.")
                self.character.gain_experience(5)
            else:
                self.add_message("You miss! The boar charges and hits you for 3 HP.")
                self.character.take_damage(3)
        elif choice == "b":
            if self.skill_check(self.character.charisma, 10, "Charisma"):
                self.add_message("You shout and wave your arms. The boar flees. You gain 3 XP.")
                self.character.gain_experience(3)
            else:
                self.add_message("Your attempt fails. The boar charges and grazes you for 2 HP.")
                self.character.take_damage(2)
        elif choice == "c":
            if self.skill_check(self.character.dexterity, 10, "Dexterity"):
                self.add_message("You climb the tree quickly and avoid the boar. It eventually leaves.")
            else:
                self.add_message("You struggle to climb and the boar hits you for 3 HP before running off.")
                self.character.take_damage(3)
        self.character_status()
        self.zone2()

    def zone2(self):
        self.current_image = self.shrek_toilet_image
        self.text_lines = []
        self.add_message("You find an abandoned cabin in the woods.\\n(a) Search the cabin\\n(b) Ignore it and move on")
        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            self.text_lines = []
            self.current_image = self.healing_potion_image
            self.add_message("You search the cabin and find a healing potion!")
            self.collect_item("healing potion")
            self.character.gain_experience(3)
            self.character_status()
        elif choice == "b":
            self.add_message("You decide not to risk entering the cabin.")
            self.wait_for_continue()
        self.text_lines = []
        self.add_message("You see a village in the distance. Do you want to go there?\\n(a) Continue your adventure\\n(b) Go to the village")
        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            self.add_message("You wander deeper into the forest.")
            self.wait_for_continue()
            self.zone3()
        elif choice == "b":
            self.add_message("You walk towards the village.")
            self.wait_for_continue()
            self.current_image = self.village_image
            self.text_lines = []
            self.add_message("It is a small village where the locals welcome you with a meal. You heal 2 HP.")
            self.character.heal(2)
            self.character_status()
            self.visit_village()

    def visit_village(self):
        self.text_lines = []
        self.add_message("The village seems bustling with activity. Who would you like to talk to?\\n(a) The merchant\\n(b) The blacksmith\\n(c) The elder\\n(d) Leave the village")
        choice = self.get_valid_choice(["a", "b", "c", "d"])
        if choice == "a":
            self.merchant_interaction()
        elif choice == "b":
            self.blacksmith_interaction()
        elif choice == "c":
            self.elder_interaction()
        elif choice == "d":
            self.add_message("You decide to leave the village and continue your adventure.")
            self.zone3()
        self.visit_village()  # Recursively allow further interaction

    def merchant_interaction(self):
        self.text_lines = []
        if self.spoke_to_merchant:
            self.add_message("Use that scroll wisely.")
            return
        self.add_message("You approach a merchant, who greets you with a toothy grin.")
        self.add_message("'Adventurer! I see you are on a dangerous quest. I have rare items for sale!'")
        self.add_message("'However, if you prove your worth, I might part with a magic scroll for free.'")
        self.add_message("(a) Try to persuade the merchant for the magic scroll\\n(b) Ask to see their wares\\n(c) Leave")
        choice = self.get_valid_choice(["a", "b", "c"])
        if choice == "a":
            if self.skill_check(self.character.charisma, 13, "Charisma"):
                self.add_message("The merchant is impressed by your words and hands over the magic scroll.")
                self.collect_item("magic scroll")
                self.character_status()
                self.spoke_to_merchant = True
            else:
                self.add_message("'You’ll need to try harder than that,' the merchant says, shaking his head.")
        elif choice == "b":
            self.add_message("The merchant shows you a variety of items, but you don't have gold to purchase anything.")
            self.add_message("'Come back when you’re richer, adventurer!' he says with a wink.")
        elif choice == "c":
            self.add_message("You thank the merchant and leave.")

    def blacksmith_interaction(self):
        self.text_lines = []
        if self.spoke_to_blacksmith:
            self.add_message("Come on! Go get that wolf!")
            return
        self.add_message("You approach the village blacksmith, who is hammering away at a glowing piece of metal.")
        self.add_message("'Hail, adventurer,' the blacksmith says gruffly. 'You look like you could use a better weapon.'")
        self.add_message("'I can forge you a stronger blade if you help me with a task first.'")
        self.add_message("(a) Offer to help the blacksmith\\n(b) Ask about the task\\n(c) Decline and leave")
        choice = self.get_valid_choice(["a", "b", "c"])
        if choice == "a":
            self.add_message("'There’s a dangerous wolf in the forest. Bring me its fang, and I’ll forge you something special.'")
            self.add_message("You agree to the task and prepare yourself for the challenge.")
            self.collect_item("quest: wolf fang")
            self.spoke_to_blacksmith = True
        elif choice == "b":
            self.add_message("'There’s a dangerous wolf in the forest. Bring me its fang, and I’ll forge you something special.'")
            self.add_message("The blacksmith looks you over. 'Think you can handle it?'")
            follow_up = self.get_valid_choice(["y", "n"])
            if follow_up == "y":
                self.add_message("You accept the blacksmith’s task and prepare for the challenge.")
                self.collect_item("quest: wolf fang")
                self.spoke_to_blacksmith = True
            else:
                self.add_message("You decide not to take the task and leave.")
        elif choice == "c":
            self.add_message("You thank the blacksmith and leave.")

    def elder_interaction(self):
        self.text_lines = []
        if self.spoke_to_elder:
            self.add_message("You must be wise, young one. That was a difficult riddle.")
            return
        self.add_message("You approach the village elder, who is sitting under a large tree.")
        self.add_message("'Greetings, adventurer,' the elder says with a kind smile. 'You seek wisdom, do you not?'")
        self.add_message("'Answer me this riddle, and I shall grant you my blessing.'")
        self.add_message("The elder clears his throat and begins:")
        self.add_message("'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?'")
        self.add_message("(a) Answer the riddle\\n(b) Politely decline and leave")
        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            if self.skill_check(self.character.wisdom, 12, "Wisdom"):
                self.add_message("'An echo,' you say.")
                self.add_message("The elder nods approvingly. 'You are wise indeed. Take this blessing.'")
                self.character.gain_experience(5)
                self.character_status()
                self.spoke_to_elder = True
            else:
                self.add_message("The elder shakes his head. 'That is not the correct answer.'")
        elif choice == "b":
            self.add_message("You thank the elder and leave.")

    def zone3(self):
        self.wolf_fight()
        self.end_game()

    def wolf_fight(self):
        self.text_lines = []
        self.current_image = self.wolf_image
        self.add_message("You encounter a powerful wolf!\\n(a) Fight the wolf\\n(b) Try to tame it\\n(c) Sneak past it\\n(d) Use an item")
        choice = self.get_valid_choice(["a", "b", "c", "d"])
        if choice == "a":
            if self.skill_check(self.character.strength, 15, "Strength"):
                self.add_message("You defeat the wolf in a fierce battle! You gain 10 experience points.")
                self.character.gain_experience(10)
            else:
                self.add_message("The wolf is too strong! You lose 5 HP but manage to drive it away.")
                self.character.take_damage(5)
        elif choice == "b":
            if self.skill_check(self.character.charisma, 15, "Charisma"):
                self.add_message("You calm the wolf and gain its trust. It leaves peacefully.")
                self.character.gain_experience(8)
            else:
                self.add_message("The wolf growls and attacks! You lose 4 HP.")
                self.character.take_damage(4)
        elif choice == "c":
            if self.skill_check(self.character.dexterity, 12, "Dexterity"):
                self.add_message("You sneak past the wolf without being noticed.")
            else:
                self.add_message("The wolf spots you and attacks! You lose 5 HP.")
                self.character.take_damage(5)
        elif choice == "d":
            self.add_message(f"Your inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
            self.wait_for_continue()
            item = self.get_player_input("Which item do you want to use?").lower()
            self.use_item(item)
            self.wolf_fight()

    def end_game(self):
        self.add_message(f"You emerge from the forest, battered but alive.\\nLevel {self.character.level} {self.character.name} finished the adventure with {self.character.hp} HP.\\nThank you for playing RPGPython!")
        self.character_status()
        pygame.quit()
        exit()

    def skill_check(self, ability_score, difficulty, ability_name):
        roll = randint(1, 20)
        modifier = self.calculate_modifier(ability_score)
        total = roll + modifier
        self.add_message(f"{ability_name} check...\\n")
        pygame.time.wait(2000)
        self.add_message(f"Roll: {roll} + (modifier): {modifier} = Total: {total} (DC: {difficulty})")
        self.wait_for_continue()
        return total >= difficulty

    def collect_item(self, item):
        self.inventory.append(item)
        self.add_message(f"You have collected a {item}.")

    def use_item(self, item):
        if item not in self.inventory:
            self.add_message(f"You don't have a {item} in your inventory.")
            return
        if item == "healing potion":
            self.current_image = self.healing_image
            self.character.heal(5)
            self.add_message("You used a healing potion and restored 5 HP!")
            self.inventory.remove(item)
            self.character_status()
        elif item == "magic scroll":
            self.character.strength = min(20, self.character.strength + 2)
            self.add_message("You use the magic scroll to enhance your next action!")
            self.inventory.remove(item)
            self.character_status()
        else:
            self.add_message(f"The {item} cannot be used right now.")

    def add_message(self, text):
        self.text_lines.extend(text.split("\\n"))
        self.render()

    def render(self):
        self.screen.fill((255, 255, 255))
        for i, line in enumerate(self.text_lines[-20:]):  # Display only the last 20 lines
            text_surface = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (20, 20 + i * 30))
        self.button_surface.blit(self.text, self.text_rect)
        self.screen.blit(self.button_surface, (self.button_rect.x, self.button_rect.y))
        if self.current_image:
            self.screen.blit(self.current_image, (1000, 100))
        pygame.display.flip()

    def get_player_input(self, prompt="Enter your input:"):
        name = ""
        self.add_message(prompt + f" {name}")
        pygame.display.flip()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            self.text_lines = []
            self.add_message(prompt + f" {name}")

            pygame.display.flip()

            pygame.time.wait(10)

        return name

    def get_valid_choice(self, options):
        self.add_message("Choose one: " + ", ".join(options))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key).lower()
                    if key in options:
                        return key