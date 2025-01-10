import pygame
from random import randint
from Character import Character


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.character = None
        self.inventory = []
        self.spoke_to_merchant = False
        self.spoke_to_blacksmith = False
        self.spoke_to_elder = False
        self.font = pygame.font.Font(None, 24)
        self.current_text = ""  # Text displayed on the screen
        self.waiting_for_input = False
        self.clock = pygame.time.Clock()

    def start_adventure(self):
        self.character_creation()
        self.zone0()

    def character_creation(self):
        self.display_message("Welcome, adventurer! What is your name?")
        name = self.get_player_input()
        self.display_message(f"Hello, {name}! Rolling your stats...")
        pygame.time.wait(2000)

        stats = {stat: self.roll_stat() for stat in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']}
        self.character = Character(name, stats['constitution'], stats['strength'], stats['dexterity'], stats['intelligence'], stats['wisdom'], stats['charisma'])
        self.display_message(f"Your stats:\n" + "\n".join([f"{k.capitalize()}: {v}" for k, v in stats.items()]))
        pygame.time.wait(3000)

    def roll_stat(self):
        rolls = [randint(1, 6) for _ in range(4)]
        total = sum(sorted(rolls)[1:])  # Drop the lowest roll
        self.display_message(f"Rolls: {rolls}, total (top 3): {total}")
        pygame.time.wait(1000)
        return total

    def zone0(self):
        self.display_message("You are at the edge of a dense forest. The sun is setting.\n(a) Enter the forest cautiously\n(b) Set up camp")
        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            self.display_message("You step into the forest and hear strange noises. A wild animal appears!")
            pygame.time.wait(2000)
            self.zone1()
        elif choice == "b":
            self.display_message("You set up camp and rest. You recover some HP.")
            self.character.heal(5)
            pygame.time.wait(2000)
            self.zone1()

    def zone1(self):
        self.display_message("You encounter a wild boar! It looks aggressive.\n(a) Attack the boar\n(b) Try to scare it away\n(c) Climb a tree to escape")
        choice = self.get_valid_choice(["a", "b", "c"])
        if choice == "a":
            if self.skill_check(self.character.strength, 12, "Strength"):
                self.display_message("You strike the boar and it runs away. You gain 5 XP.")
                self.character.gain_experience(5)
            else:
                self.display_message("You miss! The boar hits you for 3 HP.")
                self.character.take_damage(3)
        elif choice == "b":
            if self.skill_check(self.character.charisma, 10, "Charisma"):
                self.display_message("You shout and scare the boar away. You gain 3 XP.")
                self.character.gain_experience(3)
            else:
                self.display_message("Your attempt fails. The boar grazes you for 2 HP.")
                self.character.take_damage(2)
        elif choice == "c":
            if self.skill_check(self.character.dexterity, 10, "Dexterity"):
                self.display_message("You climb the tree and avoid the boar.")
            else:
                self.display_message("You struggle to climb and the boar hits you for 3 HP.")
                self.character.take_damage(3)
        pygame.time.wait(2000)
        self.zone2()

    def zone2(self):
        self.display_message("You find an abandoned cabin in the woods.\n(a) Search the cabin\n(b) Ignore it and move on")
        choice = self.get_valid_choice(["a", "b"])
        if choice == "a":
            self.display_message("You search the cabin and find a healing potion!")
            self.collect_item("healing potion")
        elif choice == "b":
            self.display_message("You decide not to risk entering the cabin.")
        pygame.time.wait(2000)
        self.zone3()

    def zone3(self):
        self.display_message("You reach a small village bustling with activity.\n(a) Visit the merchant\n(b) Visit the blacksmith\n(c) Visit the elder\n(d) Leave the village")
        choice = self.get_valid_choice(["a", "b", "c", "d"])
        if choice == "a":
            self.merchant_interaction()
        elif choice == "b":
            self.blacksmith_interaction()
        elif choice == "c":
            self.elder_interaction()
        elif choice == "d":
            self.display_message("You leave the village and continue your journey.")
        pygame.time.wait(2000)
        self.zone4()

    def zone4(self):
        self.display_message("You venture deeper into the forest. An eerie silence falls...\nThe adventure continues...")
        pygame.time.wait(2000)

    def skill_check(self, ability_score, difficulty, ability_name):
        roll = randint(1, 20)
        modifier = (ability_score - 10) // 2
        total = roll + modifier
        self.display_message(f"{ability_name} Check:\nRolled: {roll}\nModifier: {modifier}\nTotal: {total}\nDifficulty: {difficulty}")
        pygame.time.wait(2000)
        return total >= difficulty

    def collect_item(self, item):
        self.inventory.append(item)
        self.display_message(f"You have collected a {item}.")
        pygame.time.wait(1000)

    def use_item(self, item):
        if item not in self.inventory:
            self.display_message(f"You don't have a {item} in your inventory.")
            return
        if item == "healing potion":
            self.character.heal(5)
            self.display_message("You used a healing potion and restored 5 HP!")
            self.inventory.remove(item)
        else:
            self.display_message(f"The {item} cannot be used right now.")

    def merchant_interaction(self):
        if self.spoke_to_merchant:
            self.display_message("The merchant waves you goodbye.")
        else:
            self.display_message("The merchant offers you a magic scroll in exchange for a favor.")
            self.collect_item("magic scroll")
            self.spoke_to_merchant = True

    def blacksmith_interaction(self):
        if self.spoke_to_blacksmith:
            self.display_message("The blacksmith greets you warmly.")
        else:
            self.display_message("The blacksmith asks for help with a task.")
            self.collect_item("quest: wolf fang")
            self.spoke_to_blacksmith = True

    def elder_interaction(self):
        if self.spoke_to_elder:
            self.display_message("The elder thanks you for solving their riddle.")
        else:
            self.display_message("The elder presents a riddle. Answer wisely!")
            if self.skill_check(self.character.wisdom, 12, "Wisdom"):
                self.display_message("You solve the riddle and gain the elder's blessing!")
                self.character.gain_experience(5)
                self.spoke_to_elder = True
            else:
                self.display_message("You fail to solve the riddle.")

    def display_message(self, text):
        self.current_text = text
        self.render()

    def render(self):
        self.screen.fill((0, 0, 0))
        lines = self.current_text.split("\n")
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20 + i * 30))
            pygame.display.flip()

    def get_player_input(self):
        name = ""
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
            self.display_message(f"Enter your name: {name}")
            self.render()
            try:
                pygame.display.flip()
            except Exception as e:
                print(f"Display flip error: {e}")
                pygame.quit()
                exit()
            self.clock.tick(60)
        return name

    @staticmethod
    def get_valid_choice(options):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key).lower()
                    if key in options:
                        return key
