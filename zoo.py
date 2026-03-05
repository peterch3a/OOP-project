from abc import ABC, abstractmethod
import random

class Zoo:
    def __init__(self):
        self.enclosures = []
        self.visitors = []
        self.food_inventory = []
        self.medicine_inventory = []
        self.animals = []

    def add_enclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def add_visitor(self, visitor):
        self.visitors.append(visitor)

    def add_food(self, food):
        self.food_inventory.append(food)

    def add_medicine(self, medicine):
        self.medicine_inventory.append(medicine)

    def __str__(self):
        return f"Zoo: {self.name} with {len(self.enclosures)} enclosures"
    
    def show_animals(self):
        print("Animals in the zoo:")
        for animal in self.animals:
            print(f"- {animal}")

    def add_animal(self):
        animal = Animal()
        self.animals.append(animal)
        return animal

class Animal(ABC):
    possible_names = ["Bob", "Alice", "Geoff"]
    possible_health = ["Healthy", "Injured", "Sick", "Recovering"]

    def __init__(self):
        self.name = random.choice(Animal.possible_names)
        self.age = random.randint(1, 20)
        self.health_status = random.choice(Animal.possible_health)
        self.enclosure = None

    # @abstractmethod
    # def make_sound(self):
    #     pass

    # @abstractmethod
    # def diet_type(self):
    #     pass

    def __str__(self):
        return f"{self.name} ({self.__class__.__name__}, {self.health_status})"

# class Mammal(Animal):
#     def __init__(self, name, age, fur_type, health_status="Healthy"):
#         super().__init__(name, age, health_status)
#         self.fur_type = fur_type

#     def diet_type(self):
#         return "Varies (herbivore, carnivore, omnivore)"

# class Marsupial(Mammal):
#     def __init__(self, name, age, fur_type, pouch_size, health_status="Healthy"):
#         super().__init__(name, age, fur_type, health_status)
#         self.pouch_size = pouch_size

#     def make_sound(self):
#         return "Chitter-chatter"

#     def carry_in_pouch(self, item):
#         return f"{self.name} carries {item} in its pouch."

# class Kangaroo(Marsupial):
#     def make_sound(self):
#         return "Thump-thump"

# class Bird(Animal):
#     def __init__(self, name, age, wing_span, can_fly=True, health_status="Healthy"):
#         super().__init__(name, age, health_status)
#         self.wing_span = wing_span
#         self.can_fly = can_fly

#     def make_sound(self):
#         return "Generic bird chirp"

#     def diet_type(self):
#         return "Omnivore (varies by species)"

# class FlightlessBird(Bird):
#     def __init__(self, name, age, wing_span, health_status="Healthy"):
#         super().__init__(name, age, wing_span, can_fly=False, health_status=health_status)

#     def make_sound(self):
#         return "Low grunt or honk"

# class Penguin(FlightlessBird):
#     def make_sound(self):
#         return "Squawk"

class Food:
    def __init__(self, name, food_type, quantity):
        self.name = name
        self.food_type = food_type
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} ({self.food_type})"

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

