from random import randint

class Character:
    def __init__(self, name, constitution, strength, dexterity, intelligence, wisdom, charisma):
        self.name = name
        self.constitution = constitution
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

        self.max_hp = 10 + self.calculate_modifier(constitution)
        self.hp = self.max_hp
        self.experience = 0
        self.level = 1

    @staticmethod
    def calculate_modifier(score):
        return (score - 10) // 2

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.die()

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        hp_increase = max(1, randint(1, 10) + Character.calculate_modifier(self.constitution))
        self.max_hp += hp_increase
        self.hp = self.max_hp
        print(f"{self.name} leveled up to Level {self.level}! Max HP is now {self.max_hp}.")

    def die(self):
        print(f"{self.name} has died... Game Over!")
        exit()

    def __str__(self):
        return (f"{self.name}, {self.hp}/{self.max_hp} HP, Level {self.level}\n"
                f"Strength: {self.strength}, Dexterity: {self.dexterity}, "
                f"Constitution: {self.constitution}, Intelligence: {self.intelligence}, "
                f"Wisdom: {self.wisdom}, Charisma: {self.charisma}")
