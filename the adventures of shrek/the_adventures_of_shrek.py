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