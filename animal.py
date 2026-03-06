from abc import ABC, abstractmethod
import random

class Animal(ABC):
    ANIMAL_NAMES = ["Bob", "Alice", "Geoff"]
    
    def __init__(self):
        self.name = random.choice(Animal.ANIMAL_NAMES)
        self.age = random.randint(1, 20)
        self.happiness = 100
        self.enclosure = None
        self.status = "Alive"
        self.required_habitat = None

    def deteriorate_happiness(self, amount=10):
        if self.status == "Dead":
            return

        if self.enclosure and self.enclosure.habitat_type != self.required_habitat:
            amount += 10

        self.happiness = max(0, self.happiness - amount)

        if self.happiness <= 0 and self.status == "Alive":
            self.status = "Dead"
            print(f"{self.name} has died due to poor conditions!")

    #     if (self.happiness <= 0 and self.status == "Alive"):
    #         self.status = "Dead"
    #         print(self.name," has died!")
    #     self.happiness = max(0, self.happiness - amount)

    def feed(self, amount):
        if (self.happiness > 50 or self.status == "Dead"):
            return
        
        self.happiness = max(0, self.happiness + amount)


    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def diet_type(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.__class__.__name__}, {self.happiness}, {self.status})"

class Mammal(Animal):
    def diet_type(self):
        return "Varies"

class Marsupial(Mammal):
    def make_sound(self):
        return "Chitter-chatter"

class Koala(Marsupial):
    def __init__(self):
        super().__init__()
        self.required_habitat = "Eucalyptus Forest"

    def make_sound(self):
        return "Grunt"

class Kangaroo(Marsupial):
    def __init__(self):
        super().__init__()
        self.required_habitat = "Grassland"

    def make_sound(self):
        return "Thump-thump"

class Bird(Animal):
    def __init__(self):
        super().__init__()
        self.can_fly = True

    def make_sound(self):
        return "Chirp"

    def diet_type(self):
        return "Omnivore"

class WedgeTailedEagle(Bird):
    def __init__(self):
        super().__init__()
        self.required_habitat = "Mountain Range"

    def make_sound(self):
        return "Screech"

