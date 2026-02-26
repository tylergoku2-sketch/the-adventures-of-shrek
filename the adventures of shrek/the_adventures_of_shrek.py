import random

def __init__(self, name, description, power):
        self.name = name
        self.description = description
        self.power = power

def __str__(self):
        return f"{self.name}: {self.description} (Power: {self.power})"

class Sheild:
    def __init__(self, name, description, defense):
        self.name = name
        self.description = description
        self.defense = defense
    def __str__(self):
        return f"{self.name}: {self.description}. Power: {self.power}"

    class Monster:
        def __init__(self, name, description, health, attack, defense):
            self.name = name
            self.health = health
            self.attack = attack
            self.defense = defense
            self.description = description

class Location:
    def __init__(self, name, description):
        self.name = name
        self.monster = 0
        self.description = description
        self.items = []
        self.exits = []

def link(self, other, direction):
        self.exits[direction] = other

def enter(self):
    pass

def examine(self, thing):
    print(f"There is no {thing} here")

def describe(self):
    print(f"\n== {self.name} here")
    print(self.description)
    if len(self.items) > 0:
        print("\nYou see:")
        for item in self.items:
            print(f" - {item}")
            if self.monster != 0:
                print(f"\nA {self.monster.name} is here! {self.description}")
      