import random
from manager import Manager
from animal import Animal
from food import Food

class Zoo:
    LOW_FOOD_THRESHOLD = 30
    FEED_AMOUNT_PER_ANIMAL = 5

    def __init__(self):
        self.manager = Manager()
        self.enclosures = []
        self.visitors = []
        self.food = [Food("meat", 100),Food("fruit", 100)]
        self.medicine_inventory = []
        self.animals = []

    def update(self):
        for animal in self.animals:
            animal.deteriorate_happiness()

        self.feed_animals()

    def add_food(self, food_type, food_quantity):
        food = Food(food_type, food_quantity)
        self.food.append(food)
        return food

    def show_food(self):
        print("Food in the zoo:")
        for food in self.food:
            print(f"- {food}")

    def feed_animals(self):
        total_food = sum(f.quantity for f in self.food)

        if total_food < Zoo.LOW_FOOD_THRESHOLD:
            print(f"WARNING: Food is running low! Total remaining: {total_food}")

        if total_food <= 0:
            print("No food available! Animals cannot be fed.")
            return

        for animal in self.animals:
            if total_food <= 0:
                print("Food ran out while feeding animals.")
                break

            animal.feed(Zoo.FEED_AMOUNT_PER_ANIMAL)

            self.consume_food(Zoo.FEED_AMOUNT_PER_ANIMAL)
            total_food -= Zoo.FEED_AMOUNT_PER_ANIMAL

    def consume_food(self, amount_needed):
        remaining = amount_needed

        for food in self.food:
            if food.quantity >= remaining:
                food.quantity -= remaining
                return
            else:
                remaining -= food.quantity
                food.quantity = 0

        self.food = [f for f in self.food if f.quantity > 0]

    # def add_enclosure(self, enclosure):
    #     self.enclosures.append(enclosure)

    # def add_visitor(self, visitor):
    #     self.visitors.append(visitor)

    # def add_medicine(self, medicine):
    #     self.medicine_inventory.append(medicine)

    # def __str__(self):
    #     return f"Zoo: {self.name} with {len(self.enclosures)} enclosures"

    def add_animal(self):
        animal = Animal()
        self.animals.append(animal)
        return animal

    def show_animals(self):
        print("Animals in the zoo:")
        for animal in self.animals:
            print(f"- {animal}")

    def show_budget(self):
        print("Budget: ",self.manager.budget)



class Medicine:
    def __init__(self, name, dosage):
        self.name = name
        self.dosage = dosage

    def __str__(self):
        return f"{self.name}, dosage: {self.dosage}"

class Habitat:
    def __init__(self, habitat_type, temperature, humidity):
        self.habitat_type = habitat_type
        self.temperature = temperature
        self.humidity = humidity

    def __str__(self):
        return f"{self.habitat_type} (Temp: {self.temperature}, Humidity: {self.humidity})"

class Enclosure:
    def __init__(self, name, habitat):
        self.name = name
        self.habitat = habitat
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def __str__(self):
        return f"Enclosure: {self.name}, Habitat: {self.habitat}"

savannah = Habitat("Savannah", temperature=30, humidity=40)
kangaroo_enclosure = Enclosure("Outback Zone", savannah)

# k1 = Kangaroo("Joey", age=3, fur_type="Short brown", pouch_size="Medium")
# kangaroo_enclosure.add_animal(k1)

penguin_habitat = Habitat("Arctic", temperature=0, humidity=70)
penguin_enclosure = Enclosure("Penguin Cove", penguin_habitat)

# p1 = Penguin("Pingu", age=2, wing_span=50)
# penguin_enclosure.add_animal(p1)

