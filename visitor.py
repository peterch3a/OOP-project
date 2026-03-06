import random

class Visitor:
    VISITOR_NAMES = ["Bob", "Alice", "Geoff"]
    
    def __init__(self):
        self.name = random.choice(Visitor.VISITOR_NAMES)
        self.happiness = 100
        self.status = "Present"

    def deteriorate_happiness(self, amount=10):
        if self.status == "Exited":
            return

        self.happiness = max(0, self.happiness - amount)

        if self.happiness <= 0 and self.status == "Present":
            self.status = "Exited"
            print(f"{self.name} has left the Zoo!")
    
    def __str__(self):
        return f"{self.name} ({self.__class__.__name__}, Happiness: {self.happiness}, {self.status})"
