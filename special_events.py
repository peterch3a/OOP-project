import random
from abc import ABC, abstractmethod
from visitor import Visitor

class SpecialEvent(ABC):
    name = "Unnamed Event"

    @abstractmethod
    def apply(self, zoo):
        pass

    def __str__(self):
        return self.name

class HappyDayEvent(SpecialEvent):
    name = "Happy Day"

    def apply(self, zoo):
        for enclosure in zoo.enclosures:
            for animal in enclosure.animals:
                animal.happiness = min(100, animal.happiness + 20)

        for visitor in zoo.visitors:
            visitor.happiness = min(100, visitor.happiness + 20)

        print("A beautiful sunny day! Animals and visitors feel happier.")

class GenerousDonationEvent(SpecialEvent):
    name = "Generous Donation"

    def apply(self, zoo):
        amount = random.randint(200, 600)
        zoo.manager.budget += amount
        print(f"A wealthy donor supports the zoo! Budget increased by ${amount}.")

class AnimalBlessingEvent(SpecialEvent):
    name = "Animal Blessing"

    def apply(self, zoo):
        boosted = 0
        for enclosure in zoo.enclosures:
            for animal in enclosure.animals:
                if random.random() < 0.3:
                    animal.happiness = 100
                    boosted += 1

        print(f"A magical moment! {boosted} animals feel exceptionally joyful.")

class VisitorFestivalEvent(SpecialEvent):
    name = "Visitor Festival"

    def apply(self, zoo):
        new_visitors = random.randint(3, 7)
        for _ in range(new_visitors):
            v = Visitor()
            zoo.visitors.append(v)
            zoo.manager.budget += zoo.ticket_price

        print(f"A festival attracts {new_visitors} new visitors!")
        print(f"Ticket revenue earned: ${new_visitors * zoo.ticket_price}")

class DisasterDeathsEvent(SpecialEvent):
    name = "Disaster Deaths"

    def apply(self, zoo):
        dead_animals = 0
        exited_visitors = 0

        for enclosure in zoo.enclosures:
            for animal in enclosure.animals:
                if random.random() < 0.15:
                    animal.status = "Dead"
                    dead_animals += 1

        for visitor in zoo.visitors:
            if random.random() < 0.20:
                visitor.status = "Exited"
                exited_visitors += 1

        print(f"A sudden disaster! {dead_animals} animals died and {exited_visitors} visitors fled.")


class FoodShortageEvent(SpecialEvent):
    name = "Food Shortage"

    def apply(self, zoo):
        for food in zoo.food:
            food.quantity = 0

        print("A supply chain failure! All food stocks have been lost.")
