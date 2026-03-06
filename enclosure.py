import random

class Enclosure:
    ENCLOSURE_NAMES = ['A', 'B', 'C']
    MAX_CAPACITY = 25

    def __init__(self):
        self.name = random.choice(Enclosure.ENCLOSURE_NAMES)
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def __str__(self):
        return f"Enclosure {self.name}: contains {self.animals}"