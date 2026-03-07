import random
import string

class Visitor:
    VISITOR_NAMES = [
        "Bob", "James", "Geoff", "Nathan", "John",
        "Sarah", "Jane", "Alice", "Mary", "Eve"
    ]

    def __init__(self):
        base = random.choice(self.VISITOR_NAMES)
        suffix = ''.join(random.choices(string.digits, k=2))
        self._name = f"{base}-{suffix}"
        self.__happiness = 100
        self._status = "Present"
        self._enclosure = None

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
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def enclosure(self):
        return self._enclosure

    @enclosure.setter
    def enclosure(self, value):
        self._enclosure = value

    def deteriorate_happiness(self, amount=10):
        if self._status == "Exited":
            return

        self.happiness = self.__happiness - amount

        if self.__happiness <= 0 and self._status == "Present":
            self._status = "Exited"
            print(f"{self._name} has left the Zoo.")

    def __str__(self):
        return (f"{self._name} (Happiness: {self.__happiness})")
    
    