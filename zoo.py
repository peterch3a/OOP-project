import random

from manager import Manager
from animal import Animal
from food import Food
from enclosure import Enclosure
from animal import Koala, Kangaroo, WedgeTailedEagle
from visitor import Visitor
from special_events import (HappyEvent, DonationEvent, BlessingEvent, VisitorEvent, DisasterEvent, FoodDepleteEvent)

class Zoo:
    LOW_FOOD_THRESHOLD = 30
    FEED_AMOUNT_PER_ANIMAL = 5

    def __init__(self):
        self.manager = Manager()
        self.enclosures = []
        self.visitors = []
        self.food = [Food("meat", 100),Food("leaves", 100)]
        self.medicine_inventory = []
        self.ticket_price = 25
        self.special_events = [HappyEvent(), DonationEvent(), BlessingEvent(), VisitorEvent(), DisasterEvent(), FoodDepleteEvent()]

    def update(self):
        for enclosure in self.enclosures:
            for animal in enclosure.animals:
                animal.deteriorate_happiness()
            enclosure.animals = [a for a in enclosure.animals if a.status != "Dead"]

        for enclosure in self.enclosures:
            enclosure.deteriorate_cleanliness()

            if enclosure.cleanliness < 30:
                print(f"Warning: Enclosure {enclosure.name} is very dirty ({enclosure.cleanliness}%).")

            for animal in enclosure.animals:
                if enclosure.cleanliness < 50:
                    animal.deteriorate_happiness(amount=8)
                else:
                    animal.deteriorate_happiness()

        for visitor in self.visitors:
            visitor.deteriorate_happiness()
            self.visitor_goto_enclosure(visitor)
            self.visitor_view_enclosure(visitor)

        self.handle_breeding()
        self.feed_animals()
        self.visitor_enter()
        self.trigger_special_event()
        self.visitors = [v for v in self.visitors if v.status != "Exited"]
        
    def add_food(self, food_type, food_quantity):
        cost = food_quantity * 1
        for food in self.food:
            if food.food_type.lower() == food_type:
                food.quantity += food_quantity
                self.manager.budget -= cost
                return food

    def show_food(self):
        print("Food in the zoo:")
        for food in self.food:
            print(f"- {food}")

    def feed_animals(self):
        food_map = {f.food_type.lower(): f for f in self.food}

        for food_type, food_obj in food_map.items():
            if 0 < food_obj.quantity < Zoo.LOW_FOOD_THRESHOLD:
                print(f"Running low on {food_type.capitalize()}! Remaining: {food_obj.quantity}")
        
        for enclosure in self.enclosures:
            for animal in enclosure.animals:
                if animal.status == "Dead":
                    continue

                diet = animal.preferred_food.lower()

                if diet not in food_map or food_map[diet].quantity <= 0:
                    print(f"No {diet} available to feed {animal.name} ({type(animal).__name__}).")
                    continue

                animal.feed(animal.happiness_gain)

                food_map[diet].quantity -= Zoo.FEED_AMOUNT_PER_ANIMAL

    def add_enclosure(self, habitat_type, cost=400):
        if self.manager.budget < cost:
            raise ValueError("Not enough budget to buy enclosure.")
        enclosure = Enclosure(habitat_type)
        self.enclosures.append(enclosure)
        self.manager.budget -= cost
        return enclosure

    def upgrade_enclosure(self, enclosure_name, cost=50):
        if self.manager.budget < cost:
            raise ValueError("Not enough budget to upgrade enclosure.")

        for enclosure in self.enclosures:
            if enclosure.name.lower() == enclosure_name.lower():
                new_cap = enclosure.upgrade()
                self.manager.budget -= cost
                return enclosure, new_cap

        raise ValueError(f"No enclosure found with name '{enclosure_name}'.")

    def show_enclosures(self):
        print("Enclosures in the zoo:")
        for enclosure in self.enclosures:
            print(f"- {enclosure}")

    def add_animal(self, species, enclosure_name):
        if not self.enclosures:
            raise ValueError("No enclosures available. Please add an enclosure first.")

        species_key = species.replace(" ", "").replace("-", "").lower()
        species_type = {"koala": Koala, "kangaroo": Kangaroo, "wedgedtailedeagle": WedgeTailedEagle}

        if species_key not in species_type:
            raise ValueError(f"Unknown species '{species}'. ""Valid species: Koala, Kangaroo, WedgeTailedEagle")

        cost = 100
        if self.manager.budget < cost:
            raise ValueError(f"Not enough budget to purchase a {species} (cost {cost}).")
        
        enclosure = None
        for e in self.enclosures:
            if e.name.lower() == enclosure_name.lower():
                enclosure = e
                break

        if enclosure is None:
            raise ValueError(f"No enclosure found with name '{enclosure_name}'.")

        self.manager.budget -= cost
        animal_class = species_type[species_key]
        animal = animal_class()
        enclosure.add_animal(animal)

        return animal, enclosure

    def show_animals(self):
        print("Animals in the zoo:")
        for enclosure in self.enclosures:
            print(enclosure)
            for animal in enclosure.animals:
                print(f"\t- {animal}")

    def handle_breeding(self):
        BREEDING_THRESHOLD = 7

        for enclosure in self.enclosures:
            species_groups = {}
            for animal in enclosure.animals:
                if animal.status == "Alive":
                    species_groups.setdefault(type(animal), []).append(animal)

            for species, group in species_groups.items():
                if len(group) < 2:
                    continue

                eligible = [
                    a for a in group
                    if a.breeding_counter >= BREEDING_THRESHOLD and not a.has_bred
                ]

                if len(eligible) >= 2:

                    if len(enclosure.animals) >= enclosure.capacity:
                        print(
                            f"Breeding blocked in enclosure {enclosure.name}: "
                            f"capacity {enclosure.capacity} reached."
                        )
                        for a in eligible:
                            a.breeding_counter = 0
                        continue

                    baby = species()
                    enclosure.add_animal(baby)

                    print(f"A new {species.__name__} has been born in enclosure {enclosure.name}!")

                    for a in eligible:
                        a.has_bred = True

    def visitor_enter(self):
        if random.random() <= 0.2:
            self.manager.budget += self.ticket_price
            visitor = Visitor()
            self.visitors.append(visitor)
            print("New visitor arrived:",visitor)

    def show_visitors(self):
        print("Visitors in the zoo:")
        for visitor in self.visitors:
            print(visitor)

    def visitor_goto_enclosure(self, visitor):
        if len(self.enclosures) == 0:
            return
        
        if random.random() <= 0.1:
            chosen_enclosure = random.choice(self.enclosures)
            visitor.enclosure = chosen_enclosure
            print(f"{visitor.name} has entered Enclosure {chosen_enclosure}")

    def visitor_view_enclosure(self, visitor):
        if visitor.status == "Exited":
            return

        enclosure = visitor.enclosure
        if enclosure is None:
            return

        if len(enclosure.animals) <= 0:
            visitor.deteriorate_happiness(5)
            visitor.enclosure = None
            print(f"{visitor.name} was dissapointed to see no animals in Enclosure: {enclosure.name}.")
            return

        avg_happiness = sum(a.happiness for a in enclosure.animals) / len(enclosure.animals)

        if avg_happiness >= 70:
            visitor.happiness = min(100, visitor.happiness + 20)
            self.manager.budget += 100
            visitor.enclosure = None
            print(f"{visitor.name} enjoyed seeing the happy animals in Enclosure {enclosure.name}. They donated $100! Your new budget is {self.manager.budget}")
        elif avg_happiness >= 40:
            visitor.happiness = min(100, visitor.happiness + 10)
            self.manager.budget += 10
            visitor.enclosure = None
            print(f"{visitor.name} had an okay time viewing Enclosure {enclosure.name}, they bought a souvenir to take home.")
        else:
            visitor.deteriorate_happiness(10)
            visitor.enclosure = None
            print(f"{visitor.name} felt sad seeing the unhappy animals in Enclosure {enclosure.name}.")
        
    def set_ticket_price(self, new_price):
        try:
            price = int(new_price)
        except ValueError:
            raise ValueError("Ticket price must be an integer.")

        if price < 0:
            raise ValueError("Ticket price cannot be negative.")

        self.ticket_price = price
        return price

    def get_enclosure(self, name):
        for enclosure in self.enclosures:
            if enclosure.name.lower() == name.lower():
                return enclosure
        return None

    def clean_enclosure(self, enclosure_name, cost=20):
        enclosure = self.get_enclosure(enclosure_name)

        if enclosure is None:
            return None, f"No enclosure found with name '{enclosure_name}'."

        if self.manager.budget < cost:
            return None, "Not enough budget to clean this enclosure."

        enclosure.clean()
        self.manager.budget -= cost
        return enclosure, None

    def show_budget(self):
        return

    def trigger_special_event(self):
        if random.random() > 0.03:
            return

        event = random.choice(self.special_events)
        print(f"\n*** SPECIAL EVENT TRIGGERED: {event.name} ***")
        event.apply(self)




