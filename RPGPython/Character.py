class Character:
    def __init__(self, name, hp, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.experience = 0
        self.level = 0

    def __str__(self):
        return str(self.name) + ", " + str(self.hp) + "HP" + ", strength bonus : " + str(
            self.strength) + ", dexterity : " + str(self.dexterity) + ", constitution bonus : " + str(
            self.constitution) + ", intelligence bonus : " + str(self.intelligence) + ", wisdom bonus : " + str(self.wisdom) + ", charisma bonus : " + str(self.charisma)