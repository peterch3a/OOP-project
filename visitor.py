import random
import string

class Visitor:
    VISITOR_NAMES = ["Bob", "James", "Geoff", "Nathan", "John", "Sarah", "Jane", "Alice", "Mary", "Eve"]
    
    def __init__(self):
        base = random.choice(self.VISITOR_NAMES)
        suffix = ''.join(random.choices(string.digits, k=2))
        self.name = f"{base}-{suffix}"
        self.happiness = 100
        self.status = "Present"
        self.enclosure = None

    def deteriorate_happiness(self, amount=10):
        if self.status == "Exited":
            return

        self.happiness = max(0, self.happiness - amount)

        if self.happiness <= 0 and self.status == "Present":
            self.status = "Exited"
            print(f"{self.name} has left the Zoo.")
    
    def __str__(self):
        return f"{self.name} ({self.__class__.__name__}, Happiness: {self.happiness}, Enclosure: {self.enclosure})"
