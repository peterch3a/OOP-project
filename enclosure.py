import random
from exceptions import HabitatCapacityExceededError
from interfaces import ICleanable


class Enclosure(ICleanable):
    BASE_CAPACITY = 10
    UPGRADE_AMOUNT = 5
    MAX_CAPACITY = 25

    def __init__(self, habitat_type):
        self._name = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
        self._habitat_type = habitat_type
        self._capacity = Enclosure.BASE_CAPACITY
        self._animals = []
        self.__cleanliness = 100

    # -------- properties --------

    @property
    def name(self):
        return self._name

    @property
    def habitat_type(self):
        return self._habitat_type

    @habitat_type.setter
    def habitat_type(self, value):
        self._habitat_type = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if value < 0:
            raise ValueError("Capacity cannot be negative.")
        self._capacity = min(value, Enclosure.MAX_CAPACITY)

    @property
    def animals(self):
        return self._animals

    @property
    def cleanliness(self):
        return self.__cleanliness

    @cleanliness.setter
    def cleanliness(self, value):
        self.__cleanliness = max(0, min(100, value))

    # -------- behaviour --------

    def add_animal(self, animal):
        if len(self._animals) >= self._capacity:
            raise HabitatCapacityExceededError(
                f"Enclosure {self._name} is full (capacity {self._capacity})."
            )
        self._animals.append(animal)
        animal.enclosure = self

    def upgrade(self):
        if self._capacity >= Enclosure.MAX_CAPACITY:
            raise ValueError(
                f"Enclosure {self._name} is already at max capacity ({Enclosure.MAX_CAPACITY})."
            )
        self._capacity = min(self._capacity + Enclosure.UPGRADE_AMOUNT,
                             Enclosure.MAX_CAPACITY)
        return self._capacity

    def clean(self):
        self.__cleanliness = 100
        print(f"Enclosure {self._name} has been cleaned and is now spotless.")

    def deteriorate_cleanliness(self, amount=3):
        self.__cleanliness = max(0, self.__cleanliness - amount)

    def __str__(self):
        return (
            f"Enclosure {self._name} "
            f"({self._habitat_type}, capacity {self._capacity}, "
            f"animals {len(self._animals)}, cleanliness {self.__cleanliness}%)"
        )