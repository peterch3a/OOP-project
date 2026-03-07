from abc import ABC, abstractmethod
import random
import string

class Animal(ABC):
    ANIMAL_NAMES = ["Lucky", "Comet", "Ollie", "Milo", "Max", "Daisy", "Luna", "Honey", "Rosie", "Bella"]
    
    def __init__(self):
        base = random.choice(self.ANIMAL_NAMES)
        suffix = ''.join(random.choices(string.digits, k=2))
        self.name = f"{base}-{suffix}"
        self.happiness = 100
        self.enclosure = None
        self.status = "Alive"
        self.required_habitat = None
        self.breeding_counter = 0
        self.has_bred = False

    def deteriorate_happiness(self, amount=5):
        if self.status == "Dead":
            return

        if self.enclosure and self.enclosure.habitat_type != self.required_habitat:
            amount += 10

        self.happiness = max(0, self.happiness - amount)

        if self.happiness <= 0 and self.status == "Alive":
            self.status = "Dead"
            print(f"{self.name} has died due to poor conditions!")

        if self.happiness > 60:
            self.breeding_counter += 1
        else:
            self.breeding_counter = 0

    def feed(self, amount):
        if self.status == "Dead":
            return

        self.happiness = min(100, self.happiness + amount)

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def diet_type(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.__class__.__name__}, Happiness: {self.happiness}, {self.status})"

class Mammal(Animal):
    def diet_type(self):
        return "Varies"

class Marsupial(Mammal):
    def make_sound(self):
        return "Chitter-chatter"

class Koala(Marsupial):
    preferred_food = "leaves"
    happiness_gain = 10
    def __init__(self):
        super().__init__()
        self.required_habitat = "Forest"

    def make_sound(self):
        return "Grunt"

class Kangaroo(Marsupial):
    preferred_food = "leaves"
    happiness_gain = 10
    def __init__(self):
        super().__init__()
        self.required_habitat = "Grassland"

    def make_sound(self):
        return "Thump"

class Bird(Animal):
    def __init__(self):
        super().__init__()
        self.can_fly = True

    def make_sound(self):
        return "Chirp"

class WedgeTailedEagle(Bird):
    preferred_food = "meat"
    happiness_gain = 10
    def __init__(self):
        super().__init__()
        self.required_habitat = "Mountain"

    def make_sound(self):
        return "Screech"

