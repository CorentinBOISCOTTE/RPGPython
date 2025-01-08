import pytest
from Character import Character

def test_character_level_up():
    character = Character("TestHero")
    character.gain_experience(10)
    assert character.level == 2
    assert character.max_hp == 15
    assert character.hp == 15
    assert character.strength == 6

def test_character_healing():
    character = Character("TestHero")
    character.hp = 5
    character.heal(3)
    assert character.hp == 8
    character.heal(10)
    assert character.hp == character.max_hp
