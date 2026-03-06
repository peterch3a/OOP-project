import random

from manager import Manager
from animal import Animal
from food import Food
from enclosure import Enclosure
from animal import Koala, Kangaroo, WedgeTailedEagle

class Zoo:
    LOW_FOOD_THRESHOLD = 30
    FEED_AMOUNT_PER_ANIMAL = 5
    ANIMAL_COSTS = {"Koala": 150,"Kangaroo": 150, "WedgeTailedEagle": 100}

    def __init__(self):
        self.manager = Manager()
        self.enclosures = []
        self.visitors = []
        self.food = [Food("meat", 100),Food("leaves", 100)]
        self.medicine_inventory = []
        
    def update(self):
        for enclosure in self.enclosures:
            for animal in enclosure.animals:
                animal.deteriorate_happiness()

        self.handle_breeding()
        self.feed_animals()

    def add_food(self, food_type, food_quantity):
        for food in self.food:
            if food.food_type.lower() == food_type:
                food.quantity += food_quantity
                return food

    def show_food(self):
        print("Food in the zoo:")
        for food in self.food:
            print(f"- {food}")

    def feed_animals(self):
        food_map = {f.food_type.lower(): f for f in self.food}

        for food_type, food_obj in food_map.items():
            if 0 < food_obj.quantity < Zoo.LOW_FOOD_THRESHOLD:
                self.command.print_warning(
                    f"Running low on {food_type.capitalize()}! Remaining: {food_obj.quantity}"
                )
        
        for enclosure in self.enclosures:
            for animal in enclosure.animals:
                if animal.status == "Dead":
                    continue

                diet = animal.preferred_food.lower()

                if diet not in food_map or food_map[diet].quantity <= 0:
                    self.command.print_warning(
                        f"No {diet} available to feed {animal.name} ({type(animal).__name__})."
                    )
                    continue

                animal.feed(animal.happiness_gain)

                food_map[diet].quantity -= Zoo.FEED_AMOUNT_PER_ANIMAL

            # if food_map[diet].quantity < 0:
            #     food_map[diet].quantity = 0

    def add_enclosure(self, habitat_type):
        enclosure = Enclosure(habitat_type)
        self.enclosures.append(enclosure)
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

        species_type = {"Koala": Koala, "Kangaroo": Kangaroo, "WedgeTailedEagle": WedgeTailedEagle}

        if species not in species_type:
            raise ValueError(f"Unknown species '{species}'.")

        cost = Zoo.ANIMAL_COSTS[species]
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

        animal = species_type[species]()
        

        enclosure = random.choice(self.enclosures)
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
                        # a.breeding_counter = 0

    def show_budget(self):
        print("Budget: ",self.manager.budget)

    # def add_visitor(self, visitor):
    #     self.visitors.append(visitor)

    # def add_medicine(self, medicine):
    #     self.medicine_inventory.append(medicine)

    # def __str__(self):
    #     return f"Zoo: {self.name} with {len(self.enclosures)} enclosures"

# class Medicine:
#     def __init__(self, name, dosage):
#         self.name = name
#         self.dosage = dosage

#     def __str__(self):
#         return f"{self.name}, dosage: {self.dosage}"

# class Habitat:
#     def __init__(self, habitat_type, temperature, humidity):
#         self.habitat_type = habitat_type
#         self.temperature = temperature
#         self.humidity = humidity

#     def __str__(self):
#         return f"{self.habitat_type} (Temp: {self.temperature}, Humidity: {self.humidity})"



