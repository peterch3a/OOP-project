from abc import ABC, abstractmethod
import random

class Animal(ABC):
    POSSIBLE_NAMES = ["Bob", "Alice", "Geoff"]
    
    def __init__(self):
        self.name = random.choice(Animal.POSSIBLE_NAMES)
        self.age = random.randint(1, 20)
        self.happiness = 100
        self.enclosure = None
        self.status = "Alive"

    def deteriorate_happiness(self, amount=10):
        if (self.happiness <= 0 and self.status == "Alive"):
            self.status = "Dead"
            print(self.name," has died!")
        self.happiness = max(0, self.happiness - amount)

    def feed(self, amount):
        if (self.happiness > 50 or self.status == "Dead"):
            return
        
        
        self.happiness = max(0, self.happiness + amount)


    # @abstractmethod
    # def make_sound(self):
    #     pass

    # @abstractmethod
    # def diet_type(self):
    #     pass

    def __str__(self):
        return f"{self.name} ({self.__class__.__name__}, {self.happiness}, {self.status})"

# class Mammal(Animal):
#     def __init__(self, name, age, fur_type, health_status="Healthy"):
#         super().__init__(name, age, health_status)
#         self.fur_type = fur_type

#     def diet_type(self):
#         return "Varies (herbivore, carnivore, omnivore)"

# class Marsupial(Mammal):
#     def __init__(self, name, age, fur_type, pouch_size, health_status="Healthy"):
#         super().__init__(name, age, fur_type, health_status)
#         self.pouch_size = pouch_size

#     def make_sound(self):
#         return "Chitter-chatter"

#     def carry_in_pouch(self, item):
#         return f"{self.name} carries {item} in its pouch."

# class Kangaroo(Marsupial):
#     def make_sound(self):
#         return "Thump-thump"

# class Bird(Animal):
#     def __init__(self, name, age, wing_span, can_fly=True, health_status="Healthy"):
#         super().__init__(name, age, health_status)
#         self.wing_span = wing_span
#         self.can_fly = can_fly

#     def make_sound(self):
#         return "Generic bird chirp"

#     def diet_type(self):
#         return "Omnivore (varies by species)"

# class FlightlessBird(Bird):
#     def __init__(self, name, age, wing_span, health_status="Healthy"):
#         super().__init__(name, age, wing_span, can_fly=False, health_status=health_status)

#     def make_sound(self):
#         return "Low grunt or honk"

# class Penguin(FlightlessBird):
#     def make_sound(self):
#         return "Squawk"