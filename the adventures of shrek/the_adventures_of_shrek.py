import random


class Weapon:
    def __init__(self, name, description, power):
        self.name = name
        self.description = description
        self.power = power

    def __str__(self):
        return f"{self.name} - {self.description} (Power: {self.power})"


class Shield:
    def __init__(self, name, description, power):
        self.name = name
        self.description = description
        self.power = power

    def __str__(self):
        return f"{self.name} - {self.description} (Defense: {self.power})"


class Monster:
    def __init__(self, name, description, health, attack, defense):
        self.name = name
        self.description = description
        self.health = health
        self.attack = attack
        self.defense = defense


class Location:
    def __init__(self, name, description):
        self.name = name
        self.monster = 0
        self.description = description
        self.items = []
        self.exits = {}

    def link(self, other, direction):
        self.exits[direction] = other

    def enter(self):
        pass

    def exit(self):
        pass

    def examnine(self, thing):
        print(f"There is no {thing} here.")

    def examine(self, thing):
        return self.examnine(thing)

    def describe(self):
        print(f"\n== {self.name} ==")
        print(self.description)

        if len(self.items) > 0:
            print("You see:")
            for item in self.items:
                print(f"- {item}")

        if self.monster != 0:
            print(f"A {self.monster.name} is here! {self.monster.description}")


class Player:
    def __init__(self, name, location, attack, defence, health):
        self.name = name
        self.location = location
        self.inventory = []
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defence = defence

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def move(self, direction):
        if direction in self.location.exits:
            self.location.exit()
            self.location = self.location.exits[direction]
            self.location.enter()
        else:
            print("You can't go that way.")

    def take(self, item_name):
        for item in list(self.location.items):
            if item.name.lower() == item_name.lower():

                if isinstance(item, Shield) or isinstance(item, Weapon):
                    for inventory_item in list(self.inventory):
                        if type(item) == type(inventory_item):
                            self.drop(inventory_item.name)

                if isinstance(item, Shield):
                    self.defence = item.power

                if isinstance(item, Weapon):
                    self.attack = item.power

                self.inventory.append(item)
                self.location.items.remove(item)
                print(f"You pick up the {item.name}.")
                return

        print("There is no such item here.")

    def drop(self, item_name):
        for item in list(self.inventory):
            if item.name.lower() == item_name.lower():

                if isinstance(item, Shield):
                    self.defence = 0

                if isinstance(item, Weapon):
                    self.attack = 1

                self.inventory.remove(item)
                self.location.items.append(item)
                print(f"You drop the {item.name}.")
                return

    def use(self, item_name):
        for item in list(self.inventory):
            if item.name.lower() == item_name.lower():

                if hasattr(item, "use"):
                    item.use()
                else:
                    print("You can't use that.")
                return

        print("you have no such item")

    def stat(self):
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"Defence: {self.defence}")

    def stats(self):
        return self.stat()

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("You are carrying:")
            for item in self.inventory:
                print(f"- {item}")

    def attack_monster(self, monster_name):
        if self.location.monster != 0 and self.location.monster.name.lower() == monster_name.lower():

            random_number = random.randint(
                0, max(0, self.attack + self.location.monster.defense)
            )

            if random_number > self.location.monster.defense:
                damage = random_number - self.location.monster.defense
                self.location.monster.health -= damage
                print(f"You attack the {self.location.monster.name} and dealt {damage} damage")
            else:
                print("You missed")

            random_number = random.randint(
                0, max(0, self.location.monster.attack + self.defence)
            )

            if random_number > self.defence:
                damage = random_number - self.defence
                self.health -= damage
                print(f"The {self.location.monster.name} hit you and dealt {damage} damage")
            else:
                print(f"The {self.location.monster.name} missed")

            if self.location.monster.health <= 0:
                print(f"You have defeated the {self.location.monster.name}!")
                self.location.monster = 0

            if self.health <= 0:
                print("You have been defeated")
        else:
            print("No such monster here.")


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name} - {self.description}"


class Potion(Item):
    def __init__(self, name, description, heal_amount=None):
        super().__init__(name, description)
        self.heal_amount = heal_amount

    def use(self):
        global player
        amount = self.heal_amount or player.max_health
        print("You uncork the potion and drink deeply - warmth spreads through your body as your wounds begin to close.")
        player.heal(amount)

        if self in player.inventory:
            player.inventory.remove(self)


class Forest(Location):
    def __init__(self, name, description):
        Location.__init__(self, name, description)
        self.skeleton_examined = False

    def enter(self):
        print("There is a skeleton of an old soldier here.")

    def examnine(self, thing):
        if not self.skeleton_examined:
            shield = Shield("Shield", "A battered iron shield.", 10)
            sword = Weapon("Sword", "A rusty but sharp sword.", 10)

            self.items.append(shield)
            self.items.append(sword)

            self.skeleton_examined = True
            print("You see a sword and shield.")
        else:
            print("You do not find anything.")


class Tower(Location):
    def __init__(self, name, description):
        Location.__init__(self, name, description)
        self.riddle_solved = False

    def enter(self):
        global player

        if not self.riddle_solved:
            print("Standing in front of you is a wizard.")
            print("Who dares enter my tower?")
            print("I have a riddle for you bold adventurer.")

            answer = input(
                "I am tall when I am young, and I am short when I am old. What am I? "
            ).lower().strip()

            if answer == "candle":
                print("Curse!")
                print("Here is a health potion to help with your journey")
                print("With a puff of smoke the wizard disappears")

                player.inventory.append(
                    Potion("Potion", "A vial of potion emitting warmth and light.", heal_amount=player.max_health)
                )

                self.riddle_solved = True
            else:
                print("wrong!")
                print("With a wave of his hand he blasts you out the door.")
                player.move("outside")
        else:
            print("There is nothing here.")


# WORLD SETUP

village = Location("Village", "A peaceful village surrounded by forest.")
cave_entrance = Location("Cave Entrance", "A dark cave entrance. You hear something moving inside...")
cave = Location("Cave", "A cold damp cave...")
tower_entrance = Location("Tower Entrance", "A tower soars above you. The door is slightly ajar...")
forest = Forest("Forest", "Dark trees tower around you. You hear growls nearby.")
tower = Tower("Tower", "Flickering candles cast long shadows across shelves of ancient tomes and the air hums with quiet, lingering magic.")

village.link(forest, "north")
forest.link(village, "south")
forest.link(cave_entrance, "east")
forest.link(tower_entrance, "west")
tower_entrance.link(tower, "inside")
tower_entrance.link(forest, "east")
tower.link(tower_entrance, "outside")
cave_entrance.link(cave, "inside")
cave_entrance.link(forest, "west")
cave.link(cave_entrance, "outside")

player = Player("Player", village, 1, 0, 100)

ogre = Monster(
    "Ogre",
    "The ogre looms before you - a hulking brute with greenish skin, crude armor, and a club large enough to crush stone.",
    100,
    20,
    10,
)

cave.monster = ogre


print("Welcome to the Adventure!")
player.location.describe()


while player.health > 0:
    commands = input("\n> ").strip().lower().split(" ", 1)

    if not commands:
        continue

    if commands[0] == "quit":
        print("Bye bye")
        break

    if commands[0] == "move" and len(commands) > 1:
        player.move(commands[1])

    if commands[0] == "take" and len(commands) > 1:
        player.take(commands[1])

    if commands[0] == "drop" and len(commands) > 1:
        player.drop(commands[1])

    if commands[0] == "stats":
        player.stats()

    if commands[0] == "examine" and len(commands) > 1:
        player.location.examine(commands[1])

    if commands[0] == "inventory":
        player.show_inventory()

    if commands[0] == "attack" and len(commands) > 1:
        player.attack_monster(commands[1])

    if commands[0] == "use" and len(commands) > 1:
        player.use(commands[1])