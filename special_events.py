"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
special_events.py

Defines special events that can occur randomly in the zoo simulation.
Events can affect animals, visitors, budget, and food.
"""

import random
from abc import ABC, abstractmethod

from visitor import Visitor


class SpecialEvent(ABC):
    """
    Abstract base class for special events.

    Attributes:
        _name (str): Human-readable name of the event.
    """

    def __init__(self, name="Unnamed Event"):
        """
        Initialise a special event.

        Args:
            name (str): Name of the event.
        """
        self._name = name

    @property
    def name(self):
        """str: Name of the event."""
        return self._name

    @abstractmethod
    def apply(self, zoo):
        """
        Apply the event's effects to the zoo.

        Args:
            zoo (Zoo): The zoo instance to modify.
        """
        pass

    def __str__(self):
        """Return the event's name."""
        return self._name


class HappyEvent(SpecialEvent):
    """
    Event that boosts happiness for all animals and visitors.

    Name: "Happy Day"
    """

    def __init__(self):
        super().__init__("Happy Day")

    def apply(self, zoo):
        """
        Apply the happy day effect.

        All animals and visitors gain 50 happiness, capped at 100.
        """
        for enclosure in zoo.enclosures:
            for animal in enclosure.animals:
                animal.happiness = min(100, animal.happiness + 50)

        for visitor in zoo.visitors:
            visitor.happiness = min(100, visitor.happiness + 50)

        print("A beautiful sunny day! Animals and visitors gained 50 Happiness!")


class DonationEvent(SpecialEvent):
    """
    Event that grants a random donation to the zoo.

    Name: "Generous Donation"
    """

    def __init__(self):
        super().__init__("Generous Donation")

    def apply(self, zoo):
        """
        Apply the donation event.

        Adds a random amount between $200 and $600 to the budget.
        """
        amount = random.randint(200, 600)
        zoo.manager.budget += amount
        print(
            f"A local has donated a large sum to the zoo! "
            f"Budget increased by ${amount}. Your new budget is ${zoo.manager.budget}"
        )


class BlessingEvent(SpecialEvent):
    """
    Event that randomly boosts some animals to full happiness.

    Name: "Animal Blessing"
    """

    def __init__(self):
        super().__init__("Animal Blessing")

    def apply(self, zoo):
        """
        Apply the blessing event.

        Each animal has its happiness set to 100.
        """
        boosted = 0
        for enclosure in zoo.enclosures:
            for animal in enclosure.animals:
                    animal.happiness = 100
                    boosted += 1

        print(f"A magical moment! {boosted} animals gained 100 Happiness!")


class VisitorEvent(SpecialEvent):
    """
    Event that attracts a burst of new visitors.

    Name: "Visitor Festival"
    """

    def __init__(self):
        super().__init__("Visitor Festival")

    def apply(self, zoo):
        """
        Apply the visitor festival event.

        Adds 3–7 new visitors and collects ticket revenue for each.
        """
        new_visitors = random.randint(3, 7)

        for _ in range(new_visitors):
            v = Visitor()
            zoo.visitors.append(v)
            zoo.manager.budget += zoo.ticket_price

        print(f"A festival attracts {new_visitors} new visitors!")
        print(
            f"Ticket revenue earned: ${new_visitors * zoo.ticket_price}. "
            f"Your new budget is ${zoo.manager.budget}"
        )


class DisasterEvent(SpecialEvent):
    """
    Event that causes random animal deaths and visitor exits.

    Name: "Disaster Deaths"
    """

    def __init__(self):
        super().__init__("Disaster Deaths")

    def apply(self, zoo):
        """
        Apply the disaster event.

        Each animal has a 40% chance to die.
        Each visitor has a 70% chance to exit the zoo.
        """
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

        print(
            f"A terrible disaster has occured... {dead_animals} animals died "
            f"and {exited_visitors} visitors fled."
        )


class FoodDepleteEvent(SpecialEvent):
    """
    Event that wipes out all food stock.

    Name: "Food Deplete"
    """

    def __init__(self):
        super().__init__("Food Deplete")

    def apply(self, zoo):
        """
        Apply the food depletion event.

        Sets the quantity of all food types to zero.
        """
        for food in zoo.food:
            food.quantity = 0

        print(
            "A pest invasion has made it's way to the animal food stocks! "
            "All food stock has been lost."
        )
