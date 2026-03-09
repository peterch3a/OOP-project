"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
enclosure.py

Defines the Enclosure class, which houses animals and tracks capacity
and cleanliness. Enclosures implement the ICleanable interface.
"""

import random
import string

from exceptions import HabitatCapacityExceededError
from interfaces import ICleanable


class Enclosure(ICleanable):
    """
    Represents an animal enclosure in the zoo.

    Attributes:
        _name (str): Unique enclosure identifier.
        _habitat_type (str): Habitat type (e.g., "Grassland", "Forest").
        _capacity (int): Maximum number of animals allowed.
        _animals (list[Animal]): Animals currently in the enclosure.
        __cleanliness (int): Cleanliness level (0–100).
    """

    BASE_CAPACITY = 10
    UPGRADE_AMOUNT = 5
    MAX_CAPACITY = 25

    def __init__(self, habitat_type):
        """
        Initialise a new enclosure with a random name and base capacity.

        Args:
            habitat_type (str): The habitat type for this enclosure.
        """
        base = random.choice(["A", "B", "C", "D", "E", "F", "G", "X", "Y", "Z"])
        suffix = "".join(random.choices(string.digits, k=1))
        self._name = f"{base}{suffix}"
        self._habitat_type = habitat_type
        self._capacity = Enclosure.BASE_CAPACITY
        self._animals = []
        self.__cleanliness = 100

    @property
    def name(self):
        """str: Unique name of the enclosure."""
        return self._name

    @property
    def habitat_type(self):
        """str: Habitat type of the enclosure."""
        return self._habitat_type

    @habitat_type.setter
    def habitat_type(self, value):
        """Set the habitat type."""
        self._habitat_type = value

    @property
    def capacity(self):
        """int: Maximum number of animals allowed."""
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        """
        Set the capacity, clamped to a non-negative value and the max capacity.

        Args:
            value (int): New capacity.

        Raises:
            ValueError: If value is negative.
        """
        if value < 0:
            raise ValueError("Capacity cannot be negative.")
        self._capacity = min(value, Enclosure.MAX_CAPACITY)

    @property
    def animals(self):
        """list[Animal]: Animals currently in the enclosure."""
        return self._animals

    @property
    def cleanliness(self):
        """int: Cleanliness level (0–100)."""
        return self.__cleanliness

    @cleanliness.setter
    def cleanliness(self, value):
        """Set cleanliness, clamped between 0 and 100."""
        self.__cleanliness = max(0, min(100, value))

    # -------------------- Behaviour --------------------

    def add_animal(self, animal):
        """
        Add an animal to the enclosure.

        Args:
            animal (Animal): The animal to add.

        Raises:
            HabitatCapacityExceededError: If the enclosure is full.
        """
        if len(self._animals) >= self._capacity:
            raise HabitatCapacityExceededError(
                f"Enclosure {self._name} is full (capacity {self._capacity})."
            )
        self._animals.append(animal)
        animal.enclosure = self

    def upgrade(self):
        """
        Upgrade the enclosure's capacity.

        Capacity increases by UPGRADE_AMOUNT up to MAX_CAPACITY.

        Returns:
            int: The new capacity.

        Raises:
            ValueError: If the enclosure is already at max capacity.
        """
        if self._capacity >= Enclosure.MAX_CAPACITY:
            raise ValueError(
                f"Enclosure {self._name} is already at max capacity "
                f"({Enclosure.MAX_CAPACITY})."
            )
        self._capacity = min(
            self._capacity + Enclosure.UPGRADE_AMOUNT, Enclosure.MAX_CAPACITY
        )
        return self._capacity

    def clean(self):
        """
        Clean the enclosure.

        Implements ICleanable. Resets cleanliness to 100 and prints a message.
        """
        self.__cleanliness = 100
        print(f"Enclosure {self._name} has been cleaned and is now spotless.")

    def deteriorate_cleanliness(self, amount=3):
        """
        Reduce cleanliness over time.

        Args:
            amount (int): Amount to reduce cleanliness by.
        """
        self.__cleanliness = max(0, self.__cleanliness - amount)

    def __str__(self):
        """Return a readable summary of the enclosure."""
        return (
            f"Enclosure {self._name} "
            f"({self._habitat_type}, Capacity: {self._capacity}, "
            f"Animals: {len(self._animals)}, Cleanliness: {self.__cleanliness}%)"
        )
