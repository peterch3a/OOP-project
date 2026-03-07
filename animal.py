from abc import ABC, abstractmethod
import random
import string

class Animal(ABC):
    ANIMAL_NAMES = [
        "Lucky", "Comet", "Ollie", "Milo", "Max",
        "Daisy", "Luna", "Honey", "Rosie", "Bella"
    ]

    def __init__(self):
        base = random.choice(self.ANIMAL_NAMES)
        suffix = ''.join(random.choices(string.digits, k=2))
        self._name = f"{base}-{suffix}"
        self.__happiness = 100
        self._enclosure = None
        self._status = "Alive"
        self._required_habitat = None
        self._breeding_counter = 0
        self._has_bred = False

    @property
    def name(self):
        return self._name

    @property
    def happiness(self):
        return self.__happiness

    @happiness.setter
    def happiness(self, value):
        self.__happiness = max(0, min(100, value))

    @property
    def enclosure(self):
        return self._enclosure

    @enclosure.setter
    def enclosure(self, enclosure):
        self._enclosure = enclosure

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def required_habitat(self):
        return self._required_habitat

    @required_habitat.setter
    def required_habitat(self, value):
        self._required_habitat = value

    @property
    def breeding_counter(self):
        return self._breeding_counter

    @breeding_counter.setter
    def breeding_counter(self, value):
        self._breeding_counter = max(0, value)

    @property
    def has_bred(self):
        return self._has_bred

    @has_bred.setter
    def has_bred(self, value):
        self._has_bred = bool(value)

    def deteriorate_happiness(self, amount=5):
        if self._status == "Dead":
            return

        if self._enclosure and self._enclosure.habitat_type != self._required_habitat:
            amount += 10

        self.happiness = self.__happiness - amount

        if self.__happiness <= 0 and self._status == "Alive":
            self._status = "Dead"
            print(f"{self._name} has died due to poor conditions!")

        if self.__happiness > 60:
            self._breeding_counter += 1
        else:
            self._breeding_counter = 0

    def feed(self, amount):
        if self._status == "Dead":
            return
        self.happiness = self.__happiness + amount

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def diet_type(self):
        pass

    def __str__(self):
        return f"{self._name} ({self.__class__.__name__}, Happiness: {self.__happiness}, {self._status})"

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
        self._can_fly = True

    def diet_type(self):
        return "Varies"

    @property
    def can_fly(self):
        return self._can_fly

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