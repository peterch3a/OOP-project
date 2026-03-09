"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
animal.py

Defines the abstract Animal base class and concrete animal species used in the zoo
simulation. Animals track happiness, enclosure assignment, breeding readiness,
and species‑specific behaviour such as sounds and preferred food.
"""

from abc import ABC, abstractmethod
import random
import string


class Animal(ABC):
    """
    Abstract base class representing a generic animal in the zoo.

    Attributes:
        _name (str): Unique name generated for the animal.
        __happiness (int): Current happiness level (0–100).
        _enclosure (Enclosure | None): The enclosure the animal resides in.
        _status (str): "Alive" or "Dead".
        _required_habitat (str | None): Habitat type required for optimal health.
        _breeding_counter (int): Counter used to determine breeding readiness.
        _has_bred (bool): Whether the animal has already bred this cycle.
    """

    ANIMAL_NAMES = [
        "Lucky", "Comet", "Ollie", "Milo", "Max",
        "Daisy", "Luna", "Honey", "Rosie", "Bella"
    ]

    def __init__(self):
        """Initialise a new animal with randomised name and full happiness."""
        base = random.choice(self.ANIMAL_NAMES)
        suffix = ''.join(random.choices(string.digits, k=2))
        self._name = f"{base}-{suffix}"

        self.__happiness = 100
        self._enclosure = None
        self._status = "Alive"
        self._required_habitat = None
        self._breeding_counter = 0
        self._has_bred = False

    # -------------------- Properties --------------------

    @property
    def name(self):
        """str: Unique name of the animal."""
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
    def enclosure(self):
        """Enclosure | None: The enclosure the animal resides in."""
        return self._enclosure

    @enclosure.setter
    def enclosure(self, enclosure):
        """Assign the animal to an enclosure."""
        self._enclosure = enclosure

    @property
    def status(self):
        """str: "Alive" or "Dead"."""
        return self._status

    @status.setter
    def status(self, value):
        """Set the animal's status."""
        self._status = value

    @property
    def required_habitat(self):
        """str | None: Habitat type required for optimal health."""
        return self._required_habitat

    @required_habitat.setter
    def required_habitat(self, value):
        """Set the required habitat type."""
        self._required_habitat = value

    @property
    def breeding_counter(self):
        """int: Counter used to determine breeding readiness."""
        return self._breeding_counter

    @breeding_counter.setter
    def breeding_counter(self, value):
        """Set breeding counter, ensuring it never goes below zero."""
        self._breeding_counter = max(0, value)

    @property
    def has_bred(self):
        """bool: Whether the animal has already bred this cycle."""
        return self._has_bred

    @has_bred.setter
    def has_bred(self, value):
        """Set breeding flag."""
        self._has_bred = bool(value)

    # -------------------- Behaviour --------------------

    def deteriorate_happiness(self, amount=5):
        """
        Reduce happiness due to time, environment, or poor conditions.

        Happiness decreases by the given amount. If the animal is in an
        unsuitable habitat, an additional penalty is applied.

        If happiness reaches 0, the animal dies.

        Args:
            amount (int): Base amount of happiness to reduce.
        """
        if self._status == "Dead":
            return

        # Habitat mismatch penalty
        if self._enclosure and self._enclosure.habitat_type != self._required_habitat:
            amount += 10

        self.happiness = self.__happiness - amount

        # Death condition
        if self.__happiness <= 0 and self._status == "Alive":
            self._status = "Dead"
            print(f"{self._name} has died due to poor conditions!")

        # Breeding readiness logic
        if self.__happiness > 60:
            self._breeding_counter += 1
        else:
            self._breeding_counter = 0

    def feed(self, amount):
        """
        Increase happiness when fed.

        Args:
            amount (int): Amount of happiness to restore.
        """
        if self._status == "Dead":
            return
        self.happiness = self.__happiness + amount

    @abstractmethod
    def make_sound(self):
        """Return the sound this animal makes."""
        pass

    @abstractmethod
    def diet_type(self):
        """Return the general diet category for this animal."""
        pass

    def __str__(self):
        """Return a readable summary of the animal."""
        return f"{self._name} ({self.__class__.__name__}, Happiness: {self.__happiness}, {self._status})"


# -------------------- Species Classes --------------------

class Mammal(Animal):
    """Base class for mammals."""
    def diet_type(self):
        return "Varies"


class Marsupial(Mammal):
    """Base class for marsupials."""
    def make_sound(self):
        return "Chitter-chatter"


class Koala(Marsupial):
    """Koala species with forest habitat and leaf diet."""
    preferred_food = "leaves"
    happiness_gain = 10

    def __init__(self):
        super().__init__()
        self.required_habitat = "Forest"

    def make_sound(self):
        return "Grunt"


class Kangaroo(Marsupial):
    """Kangaroo species with grassland habitat and leaf diet."""
    preferred_food = "leaves"
    happiness_gain = 10

    def __init__(self):
        super().__init__()
        self.required_habitat = "Grassland"

    def make_sound(self):
        return "Thump"


class Bird(Animal):
    """Base class for birds, capable of flight."""
    def __init__(self):
        super().__init__()
        self._can_fly = True

    def diet_type(self):
        return "Varies"

    @property
    def can_fly(self):
        """bool: Whether the bird can fly."""
        return self._can_fly

    def make_sound(self):
        return "Chirp"


class WedgeTailedEagle(Bird):
    """Wedge‑tailed eagle species with mountain habitat and meat diet."""
    preferred_food = "meat"
    happiness_gain = 10

    def __init__(self):
        super().__init__()
        self.required_habitat = "Mountain"

    def make_sound(self):
        return "Screech"
