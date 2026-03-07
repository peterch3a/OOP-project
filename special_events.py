import random
from abc import ABC, abstractmethod
from visitor import Visitor

class SpecialEvent(ABC):
    def __init__(self, name="Unnamed Event"):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def apply(self, zoo):
        pass

    def __str__(self):
        return self._name


class HappyEvent(SpecialEvent):
    def __init__(self):
        super().__init__("Happy Day")

    def apply(self, zoo):
        for enclosure in zoo.enclosures:
            for animal in enclosure.animals:
                animal.happiness = min(100, animal.happiness + 50)

        for visitor in zoo.visitors:
            visitor.happiness = min(100, visitor.happiness + 50)

        print("A beautiful sunny day! Animals and visitors gained 50 Happiness!")


class DonationEvent(SpecialEvent):
    def __init__(self):
        super().__init__("Generous Donation")

    def apply(self, zoo):
        amount = random.randint(200, 600)
        zoo.manager.budget += amount
        print(f"A local has donated a large sum to the zoo! Budget increased by ${amount}. Your new budget is ${zoo.manager.budget}")


class BlessingEvent(SpecialEvent):
    def __init__(self):
        super().__init__("Animal Blessing")

    def apply(self, zoo):
        boosted = 0
        for enclosure in zoo.enclosures:
            for animal in enclosure.animals:
                if random.random() < 0.3:
                    animal.happiness = 100
                    boosted += 1

        print(f"A magical moment! {boosted} animals gained 100 Happiness!")


class VisitorEvent(SpecialEvent):
    def __init__(self):
        super().__init__("Visitor Festival")

    def apply(self, zoo):
        new_visitors = random.randint(3, 7)

        for _ in range(new_visitors):
            v = Visitor()
            zoo.visitors.append(v)
            zoo.manager.budget += zoo.ticket_price

        print(f"A festival attracts {new_visitors} new visitors!")
        print(f"Ticket revenue earned: ${new_visitors * zoo.ticket_price}. Your new budget is ${zoo.manager.budget}")


class DisasterEvent(SpecialEvent):
    def __init__(self):
        super().__init__("Disaster Deaths")

    def apply(self, zoo):
        dead_animals = 0
        exited_visitors = 0

        for enclosure in zoo.enclosures:
            for animal in enclosure.animals:
                if random.random() < 0.4:
                    animal.status = "Dead"
                    dead_animals += 1

        for visitor in zoo.visitors:
            if random.random() < 0.7:
                visitor.status = "Exited"
                exited_visitors += 1

        print(f"A terrible disaster has occured... {dead_animals} animals died and {exited_visitors} visitors fled.")

class FoodDepleteEvent(SpecialEvent):
    def __init__(self):
        super().__init__("Food Deplete")

    def apply(self, zoo):
        for food in zoo.food:
            food.quantity = 0

        print("A pest invasion has made it's way to the animal food stocks! All food stock has been lost.")