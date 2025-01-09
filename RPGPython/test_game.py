from Character import Character

def test_character_level_up():
    character = Character("TestHero", 6, 10, 8, 15, 3, 14)
    character.gain_experience(10)
    assert character.level == 2

def test_character_healing():
    character = Character("TestHero", 6, 10, 8, 15, 3, 14)
    character.hp = 5
    character.heal(3)
    assert character.hp == 8
    character.heal(10)
    assert character.hp == character.max_hp
