"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
visitor.py

Defines the Visitor class, representing guests in the zoo. Visitors
have happiness, a status, and may be assigned to an enclosure.
"""

import random
import string


class Visitor:
    """
    Represents a visitor in the zoo.

    Attributes:
        _name (str): Unique visitor name.
        __happiness (int): Current happiness level (0–100).
        _status (str): "Present" or "Exited".
        _enclosure (Enclosure | None): The enclosure the visitor is currently in.
    """

    VISITOR_NAMES = [
        "Bob",
        "James",
        "Geoff",
        "Nathan",
        "John",
        "Sarah",
        "Jane",
        "Alice",
        "Mary",
        "Eve",
    ]

    def __init__(self):
        """Initialise a new visitor with a random name and full happiness."""
        base = random.choice(self.VISITOR_NAMES)
        suffix = "".join(random.choices(string.digits, k=2))
        self._name = f"{base}-{suffix}"
        self.__happiness = 100
        self._status = "Present"
        self._enclosure = None

    @property
    def name(self):
        """str: Unique name of the visitor."""
        return self._name

    @property
    def happiness(self):
        """int: Current happiness level (0–100)."""
        return self.__happiness

    @happiness.setter
    def happiness(self, value):
        """Set happiness, clamped between 0 and 100."""
        self.__happiness = max(0, min(100, value))

    @property
    def status(self):
        """str: Visitor status, e.g., 'Present' or 'Exited'."""
        return self._status

    @status.setter
    def status(self, value):
        """Set the visitor's status."""
        self._status = value

    @property
    def enclosure(self):
        """Enclosure | None: The enclosure the visitor is currently in."""
        return self._enclosure

    @enclosure.setter
    def enclosure(self, value):
        """Assign the visitor to an enclosure."""
        self._enclosure = value

    # -------------------- Behaviour --------------------

    def deteriorate_happiness(self, amount=10):
        """
        Reduce visitor happiness over time or due to poor experiences.

        If happiness reaches 0, the visitor exits the zoo.

        Args:
            amount (int): Amount of happiness to reduce.
        """
        if self._status == "Exited":
            return

        self.happiness = self.__happiness - amount

        if self.__happiness <= 0 and self._status == "Present":
            self._status = "Exited"
            print(f"{self._name} has left the Zoo.")

    def __str__(self):
        """Return a readable summary of the visitor."""
        return f"{self._name} (Happiness: {self.__happiness})"
