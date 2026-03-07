import random
from exceptions import HabitatCapacityExceededError
from interfaces import ICleanable

class Enclosure(ICleanable):
    BASE_CAPACITY = 10
    UPGRADE_AMOUNT = 5
    MAX_CAPACITY = 25

    def __init__(self, habitat_type):
        self.name = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
        self.habitat_type = habitat_type
        self.capacity = Enclosure.BASE_CAPACITY
        self.animals = []
        self.cleanliness = 100

    def add_animal(self, animal):
        if len(self.animals) >= self.capacity:
            raise HabitatCapacityExceededError( f"Enclosure {self.name} is full (capacity {self.capacity}).")
        self.animals.append(animal)
        animal.enclosure = self

    def upgrade(self):
        if self.capacity >= Enclosure.MAX_CAPACITY:
            raise ValueError( f"Enclosure {self.name} is already at max capacity ({Enclosure.MAX_CAPACITY}).")
        self.capacity = min(self.capacity + Enclosure.UPGRADE_AMOUNT,Enclosure.MAX_CAPACITY)
        return self.capacity

    def clean(self):
        """Implementation of the ICleanable interface."""
        self.cleanliness = 100
        print(f"Enclosure {self.name} has been cleaned and is now spotless.")

    def deteriorate_cleanliness(self, amount=3):
        self.cleanliness = max(0, self.cleanliness - amount)

    def __str__(self):
        return f"Enclosure {self.name} ({self.habitat_type}, capacity {self.capacity}, animals {len(self.animals)}, cleanliness {self.cleanliness}%)"

