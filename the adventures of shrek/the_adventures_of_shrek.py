import random

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        def __str__(self):
            return f"{self.name}: {self.description}."

        def use(self):
            pass
    
class Weapon:
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

class Player:
    def __init__(self, NAME, LOCATION, ATTACK , DEFENSE, HEALTH):
        self.inventory = []       
        self.name = NAME
        self.location = LOCATION
        self.attack = ATTACK
        self.defense = DEFENSE
        self.health = HEALTH

        def heal(self, amount):
            self.HEALTH = min(self.HEALTH + amount, self.max_HEALTH)

        def move(self, direction):
                if direction in self.location.exits:
                    self.location.exit()
                    self.location = self.location.exits[direction]
                    self.location.describe()
                    self.location.enter()
                else:
                      print("you cant go that way")
    
    def take(self, item_name):
        for item in self.location.items:
            if item.name.lower() == item_name.lower():
              if type(item) == Sheild or type(item) == Weapon:
                for inventory_item in self.inventory:
                    if type(item) == type(inventory_item):
                        self.drop(inventory_item.name)

            if type(item) == Sheild:
                self.defense = item.power
    
            if type(item) == Weapon:
                self.attack = item.power

            self.inventory.append(item)
            self.location.items.remove(item)
            print(f"you pick up the {item.name}.")
            return
    print(f"There is no such item here.")

    def drop(self, item_name):
            for item in self.inventory:
                if item.name.lower() == item_name.lower():
                    if type(item) == Sheild:
                        self.defense = 0
                    if type(item) == Weapon:
                        self.attack = 1
                    self.inventory.remove(item)
                    self.location.items.append(item)
                    print(f"you drop up the {item.name}.")
                    return

    def use(self, item_name):
            for item in self.inventory:
                if item.name.lower() == item_name.lower():
                   item.use()
                   return

            print(f"you have no such item")

    def stats(self):
        print(f"HEALTH: {self.health}")
        print(f"ATTACK: {self.attack}")
        print(f"DEFENSE: {self.defense}")

    def show_inventory(self):
        if len(self.inventory) == 0:
            print("your inventory is empty.")
        else:
            print("you are carrying:")
            for item in self.inventory:
                print(f" - {item}")

    def attack_monster(self, monster_name):
        if self.location.monster != 0 and self.location.monster.name.lower() == monster_name.lower():
            random_number = random.randint(0, self.attack + self.location.monster.defense)

            if random_number > self.location.monster.defense:
                damage = random_number - self.location.monster.defense
                self.location.monster.health -= damage

                print(f"you hit the {self.location.monster.name} and dealt {damage} damage")
            else:
                print(f"you missed")

            random_number = random.randint(0, self.location.monster.attack + self.defense)

            if random_number > self.defense:
                damage = random_number - self.defense
                self.health -= damage
                
                print(f"the {self.location.monster.name} hit you and dealt {damage} damage")
            else:
                print(f"the {self.location.monster.name} missed")

                if self.location.monster.health <= 0:
                    print(f"you defeated the {self.location.monster.name}")
                    self.location.monster = 0
                    if self.health <= 0:
                        print("you have been defeated")
                    else:
                        print("no such monster here")

class Potion(Item):
    def use(self):
        global Player
        print("you uncork the potion and drint deeply - warmth spreads through your body as your wounds begin to close.")
        Player.heal(Player.max_health)
        Player.inventory.remove(self)

class Forest(location):
    def __init__(self, name,discription):
        Location.__init__(self, name, discription)
        self.skeleton_examined = False

    def enter(self):
        print("there is a skeleton of an old soldier here.")
         
 
    def examine(self, thing):
        if thing.lower() == "skeleton":
            if self.sekleton_examined == False:
                shield = Sheild("Shield", "Shield", 100)
                sword = Weapon("Sword", "Sword", 100) 

                self.items.append(shield)
                self.items.append(sword)

                self.skeleton_examined = True
                print("you see a sword and shield.")
            else:
              print("you do not find anything")