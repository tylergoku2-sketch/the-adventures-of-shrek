import random


# ------------------ ITEMS ------------------

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"


class Weapon(Item):
    def __init__(self, name, description, power):
        super().__init__(name, description)
        self.power = power

    def __str__(self):
        return f"{self.name}: {self.description} (Power: {self.power})"


class Shield(Item):
    def __init__(self, name, description, power):
        super().__init__(name, description)
        self.power = power

    def __str__(self):
        return f"{self.name}: {self.description} (Defense: {self.power})"


class Potion(Item):
    def use(self, player):
        print("You drink the potion. Warmth spreads through your body.")
        player.heal(player.max_health)
        player.inventory.remove(self)


# ------------------ MONSTER ------------------

class Monster:
    def __init__(self, name, description, health, attack, defense):
        self.name = name
        self.description = description
        self.health = health
        self.attack = attack
        self.defense = defense


# ------------------ LOCATIONS ------------------

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.exits = {}
        self.monster = None

    def link(self, other, direction):
        self.exits[direction] = other

    def enter(self):
        pass

    def exit(self):
        pass

    def examine(self, thing):
        print(f"There is no {thing} here.")

    def describe(self):
        print(f"\n== {self.name} ==")
        print(self.description)

        if self.items:
            print("\nYou see:")
            for item in self.items:
                print(f" - {item}")

        if self.monster:
            print(f"\nA {self.monster.name} is here!")
            print(self.monster.description)

        # Special message if ogre is dead
        if self.name == "cookie_factory" and self.monster is None:
            print("\nThe corpse of the ogre lies motionless on the ground.")


class Forest(Location):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.skeleton_examined = False

    def enter(self):
        print("There is a skeleton of an old soldier here.")

    def examine(self, thing):
        if thing.lower() == "skeleton":
            if not self.skeleton_examined:
                self.items.append(Shield("Shield", "An old iron shield", 10))
                self.items.append(Weapon("Sword", "A rusted but sharp blade", 15))
                self.skeleton_examined = True
                print("You find a sword and shield!")
            else:
                print("You find nothing else.")


class Tower(Location):
    global player

    def __init__(self, name, description):
        super().__init__(name, description)
        self.riddle_solved = False

    def enter(self):
        if not self.riddle_solved:
            print("\nA harry potter blocks your path.")
            answer = input("I am tall when young and short when old. What am I? ").lower().strip()

            if answer == "candle":
                print("Correct!  here is a health potion for your travels then  harry potter swishes his wand and vanishes in smoke.")
                player.inventory.append(Potion("Potion", "A glowing healing potion"))
                self.riddle_solved = True
            else:
                print("Wrong! harry potter blasts you outside.")
                player.move("outside")
        else:
            print("The tower is quiet.")


# ------------------ PLAYER ------------------

class Player:
    def __init__(self, name, location, attack, defense, health):
        self.name = name
        self.location = location
        self.attack = attack
        self.defense = defense
        self.health = health
        self.max_health = health
        self.inventory = []

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def move(self, direction):
        if direction in self.location.exits:
            self.location = self.location.exits[direction]
            self.location.describe()
            self.location.enter()
        else:
            print("You can't go that way.")

    def take(self, item_name):
        for item in self.location.items:
            if item.name.lower() == item_name.lower():

                for inv_item in self.inventory[:]:
                    if type(inv_item) == type(item):
                        self.drop(inv_item.name)

                if isinstance(item, Weapon):
                    self.attack = item.power
                elif isinstance(item, Shield):
                    self.defense = item.power

                self.inventory.append(item)
                self.location.items.remove(item)
                print(f"You pick up the {item.name}.")
                return

        print("There is no such item here.")

    def drop(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():

                if isinstance(item, Weapon):
                    self.attack = 1
                elif isinstance(item, Shield):
                    self.defense = 0

                self.inventory.remove(item)
                self.location.items.append(item)
                print(f"You drop the {item.name}.")
                return

        print("You don't have that item.")

    def use(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if hasattr(item, "use"):
                    item.use(self)
                    return
        print("You can't use that.")

    def stats(self):
        print("\n--- Player Stats ---")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
            return

        print("\nInventory:")
        for item in self.inventory:
            print(f" - {item}")

    def attack_monster(self, monster_name):
        monster = self.location.monster

        if not monster or monster.name.lower() != monster_name.lower():
            print("No such monster here.")
            return

        # Player attack
        roll = random.randint(0, self.attack + monster.defense)
        damage = max(0, roll - monster.defense)

        if damage > 0:
            monster.health -= damage
            print(f"You hit the {monster.name} for {damage} damage!")
        else:
            print("You missed!")

        if monster.health <= 0:
            print(f"\nYou have slain the {monster.name}!")
            print("The cookie factory grows silent. The threat is gone forever.")
            self.location.monster = None
            return

        # Monster counterattack
        roll = random.randint(0, monster.attack + self.defense)
        damage = max(0, roll - self.defense)

        if damage > 0:
            self.health -= damage
            print(f"The {monster.name} hits you for {damage} damage!")
        else:
            print(f"The {monster.name} missed!")

        if self.health <= 0:
            print("You have been defeated!")


# ------------------ COMMAND LIST ------------------

def show_commands():
    print("\n--- Available Commands ---")
    print("move <direction>")
    print("examine <thing>")
    print("take <item>")
    print("drop <item>")
    print("attack <monster>")
    print("use <item>")
    print("inventory")
    print("stats")
    print("help")
    print("quit")


# ------------------ WORLD SETUP ------------------

village = Location("Village", "A peaceful village.")
forest = Forest("Forest", "Dark trees surround you.")
cookie_factory_entrance = Location("the cookie factory Entrance", "A factory full of cookies.")
cookie_factory = Location("cookie factory", "the cookie factory.")
tower_entrance = Location("Tower Entrance", "A tall tower stands here.")
tower = Tower("Tower", "A room filled with ancient tomes.")

village.link(forest, "north")
forest.link(village, "south")
forest.link(cookie_factory_entrance, "east")
forest.link(tower_entrance, "west")
cookie_factory_entrance.link(cookie_factory, "inside")
cookie_factory_entrance.link(forest, "west")
cookie_factory.link(cookie_factory, "outside")
tower_entrance.link(tower, "inside")
tower_entrance.link(forest, "east")
tower.link(tower_entrance, "outside")

player = Player("Player", village, 1, 0, 100)

cookiemonster = Monster(
    "cookie monster",
    " the blue monster  with blue fluffy skin and a massive cookie.",
    50, 15, 5
)

cookie_factory.monster = cookiemonster


# ------------------ GAME START ------------------

print("Welcome to the Adventure!")
show_commands()
player.location.describe()


# ------------------ GAME LOOP ------------------

while player.health > 0:
    command = input("\n> ").strip().lower().split(" ", 1)

    if not command:
        continue

    action = command[0]
    argument = command[1] if len(command) > 1 else ""

    if action == "quit":
        print("Goodbye!")
        break
    elif action == "help":
        show_commands()
    elif action == "move":
        player.move(argument)
    elif action == "take":
        player.take(argument)
    elif action == "drop":
        player.drop(argument)
    elif action == "stats":
        player.stats()
    elif action == "examine":
        player.location.examine(argument)
    elif action == "inventory":
        player.show_inventory()
    elif action == "attack":
        player.attack_monster(argument)
    elif action == "use":
        player.use(argument)
    else:
        print("Unknown command.")