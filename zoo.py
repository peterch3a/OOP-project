"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
zoo.py

Defines the Zoo class, which coordinates all core simulation systems:
animals, enclosures, visitors, food, events, and the manager's budget.
"""

import random

from manager import Manager
from animal import Animal, Koala, Kangaroo, WedgeTailedEagle
from food import Food
from enclosure import Enclosure
from visitor import Visitor
from special_events import (
    HappyEvent,
    DonationEvent,
    BlessingEvent,
    VisitorEvent,
    DisasterEvent,
    FoodDepleteEvent,
)


class Zoo:
    """
    Represents the entire zoo simulation state.

    The Zoo coordinates:
        - Enclosures and their animals
        - Visitors and their behaviour
        - Food inventory and feeding
        - Special events
        - Budget via the Manager

    Attributes:
        _manager (Manager): Handles the zoo's budget.
        _enclosures (list[Enclosure]): All enclosures in the zoo.
        _visitors (list[Visitor]): All current visitors.
        _food (list[Food]): Food inventory.
        _ticket_price (int): Current ticket price.
        _special_events (list[SpecialEvent]): Available random events.
        _consecutive_refusals (int): Count of consecutive visitors refusing entry.
    """

    LOW_FOOD_THRESHOLD = 30
    FEED_AMOUNT_PER_ANIMAL = 5

    def __init__(self):
        """Initialise a new zoo with default budget, food, and events."""
        self._manager = Manager()
        self._enclosures: list[Enclosure] = []
        self._visitors: list[Visitor] = []
        self._food: list[Food] = [Food("meat", 100), Food("leaves", 100)]
        self._ticket_price = 25
        self._special_events = [
            HappyEvent(),
            DonationEvent(),
            BlessingEvent(),
            VisitorEvent(),
            DisasterEvent(),
            FoodDepleteEvent(),
        ]
        self._consecutive_refusals = 0

    # -------------------- Properties --------------------

    @property
    def manager(self):
        """Manager: The zoo's manager, responsible for the budget."""
        return self._manager

    @property
    def enclosures(self):
        """list[Enclosure]: All enclosures in the zoo."""
        return self._enclosures

    @property
    def visitors(self):
        """list[Visitor]: All current visitors in the zoo."""
        return self._visitors

    @visitors.setter
    def visitors(self, value):
        """Replace the current visitor list."""
        self._visitors = value

    @property
    def food(self):
        """list[Food]: The zoo's food inventory."""
        return self._food

    @property
    def ticket_price(self):
        """int: Current ticket price."""
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, value):
        """Set the ticket price."""
        self._ticket_price = value

    @property
    def special_events(self):
        """list[SpecialEvent]: All possible special events."""
        return self._special_events

    @property
    def consecutive_refusals(self):
        """int: Number of consecutive visitors who refused to enter."""
        return self._consecutive_refusals

    @consecutive_refusals.setter
    def consecutive_refusals(self, value):
        """Set consecutive refusals, ensuring it never goes below zero."""
        self._consecutive_refusals = max(0, value)

    # -------------------- Core Simulation Loop --------------------

    def update(self):
        """
        Advance the simulation by one tick.

        This method:
            - Deteriorates animal happiness and removes dead animals.
            - Deteriorates enclosure cleanliness and further affects animals.
            - Updates visitor happiness and movement.
            - Handles breeding.
            - Feeds animals.
            - Allows new visitors to enter.
            - Triggers a random special event.
            - Removes visitors who have exited.
        """
        # Animal happiness deterioration and removal of dead animals
        for enclosure in self.enclosures:
            for animal in enclosure.animals:
                animal.deteriorate_happiness()
            # Remove dead animals from each enclosure
            enclosure.animals[:] = [a for a in enclosure.animals if a.status != "Dead"]

        # Enclosure cleanliness and its impact on animals
        for enclosure in self.enclosures:
            enclosure.deteriorate_cleanliness()

            if enclosure.cleanliness < 30:
                print(
                    f"Warning: Enclosure {enclosure.name} is very dirty "
                    f"({enclosure.cleanliness}%)."
                )

            for animal in enclosure.animals:
                # Extra happiness deterioration in dirty enclosures
                if enclosure.cleanliness < 50:
                    animal.deteriorate_happiness(amount=8)
                else:
                    animal.deteriorate_happiness()

        # Visitor behaviour: happiness, movement, and viewing
        for visitor in self.visitors:
            visitor.deteriorate_happiness()
            self.visitor_goto_enclosure(visitor)
            self.visitor_view_enclosure(visitor)

        # Higher-level systems
        self.handle_breeding()
        self.feed_animals()
        self.visitor_enter()
        self.trigger_special_event()

        # Remove visitors who have exited
        self.visitors = [v for v in self.visitors if v.status != "Exited"]

    # -------------------- Food Management --------------------

    def add_food(self, food_type, food_quantity):
        """
        Purchase and add food to the zoo's inventory.

        Args:
            food_type (str): Type of food ("meat" or "leaves").
            food_quantity (int): Amount of food to add.

        Returns:
            Food | None: The updated Food object, or None if type not found.
        """
        cost = food_quantity * 1  # $1 per unit
        for food in self.food:
            if food.food_type.lower() == food_type.lower():
                food.quantity += food_quantity
                self._manager.budget -= cost
                return food
        return None

    def show_food(self):
        """Print a summary of all food in the zoo."""
        print("Food in the zoo:")
        for food in self.food:
            print(f"- {food}")

    def feed_animals(self):
        """
        Feed all animals in the zoo.

        Each animal is fed from the appropriate food type based on its
        `preferred_food`. If food is low, a warning is printed. If food
        is unavailable, the animal is skipped.
        """
        # Map food types to Food objects for quick lookup
        food_map = {f.food_type.lower(): f for f in self.food}

        # Warn if any food type is running low
        for food_type, food_obj in food_map.items():
            if 0 < food_obj.quantity < Zoo.LOW_FOOD_THRESHOLD:
                print(
                    f"Running low on {food_type.capitalize()}! "
                    f"Remaining: {food_obj.quantity}"
                )

        # Feed each animal according to its preferred food
        for enclosure in self.enclosures:
            for animal in enclosure.animals:
                if animal.status == "Dead":
                    continue

                diet = animal.preferred_food.lower()

                if diet not in food_map or food_map[diet].quantity <= 0:
                    print(
                        f"No {diet} available to feed {animal.name} "
                        f"({type(animal).__name__})."
                    )
                    continue

                # Increase happiness based on species-specific gain
                animal.feed(animal.happiness_gain)

                # Deduct a fixed amount of food per animal
                food_map[diet].quantity -= Zoo.FEED_AMOUNT_PER_ANIMAL

    # -------------------- Enclosure Management --------------------

    def add_enclosure(self, habitat_type, cost=400):
        """
        Purchase and add a new enclosure.

        Args:
            habitat_type (str): Habitat type for the enclosure.
            cost (int): Cost of the enclosure.

        Returns:
            Enclosure: The newly created enclosure.

        Raises:
            ValueError: If the budget is insufficient.
        """
        if self._manager.budget < cost:
            raise ValueError("Not enough budget to buy enclosure.")
        enclosure = Enclosure(habitat_type)
        self._enclosures.append(enclosure)
        self._manager.budget -= cost
        return enclosure

    def upgrade_enclosure(self, enclosure_name, cost=50):
        """
        Upgrade an enclosure's capacity.

        Args:
            enclosure_name (str): Name of the enclosure to upgrade.
            cost (int): Cost of the upgrade.

        Returns:
            tuple[Enclosure, int]: The upgraded enclosure and its new capacity.

        Raises:
            ValueError: If budget is insufficient or enclosure not found.
        """
        if self._manager.budget < cost:
            raise ValueError("Not enough budget to upgrade enclosure.")

        for enclosure in self._enclosures:
            if enclosure.name.lower() == enclosure_name.lower():
                new_cap = enclosure.upgrade()
                self._manager.budget -= cost
                return enclosure, new_cap

        raise ValueError(f"No enclosure found with name '{enclosure_name}'.")

    def show_enclosures(self):
        """Print a summary of all enclosures in the zoo."""
        print("Enclosures in the zoo:")
        for enclosure in self._enclosures:
            print(f"- {enclosure}")

    # -------------------- Animal Management --------------------

    def add_animal(self, species, enclosure_name):
        """
        Purchase and add an animal to a specific enclosure.

        Args:
            species (str): Species name ("Koala", "Kangaroo", "WedgeTailedEagle").
            enclosure_name (str): Name of the target enclosure.

        Returns:
            tuple[Animal, Enclosure]: The created animal and its enclosure.

        Raises:
            ValueError: If no enclosures exist, species is unknown,
                        budget is insufficient, or enclosure not found.
        """
        if not self._enclosures:
            raise ValueError("No enclosures available. Please add an enclosure first.")

        species_key = species.replace(" ", "").replace("-", "").lower()
        species_type = {
            "koala": Koala,
            "kangaroo": Kangaroo,
            "wedgetailedeagle": WedgeTailedEagle,
        }

        if species_key not in species_type:
            raise ValueError(
                f"Unknown species '{species}'. "
                "Valid species: Koala, Kangaroo, WedgeTailedEagle"
            )

        cost = 100
        if self._manager.budget < cost:
            raise ValueError(
                f"Not enough budget to purchase a {species} (cost {cost})."
            )

        # Find the target enclosure by name
        enclosure = None
        for e in self._enclosures:
            if e.name.lower() == enclosure_name.lower():
                enclosure = e
                break

        if enclosure is None:
            raise ValueError(f"No enclosure found with name '{enclosure_name}'.")

        self._manager.budget -= cost
        animal_class = species_type[species_key]
        animal: Animal = animal_class()
        enclosure.add_animal(animal)

        return animal, enclosure

    def show_animals(self):
        """Print all animals grouped by enclosure."""
        print("Animals in the zoo:")
        for enclosure in self._enclosures:
            print(enclosure)
            for animal in enclosure.animals:
                print(f"\t- {animal}")

    def handle_breeding(self):
        """
        Handle breeding logic for all animals in all enclosures.

        Animals of the same species in the same enclosure may breed if:
            - At least two animals of that species are present.
            - Their breeding counters exceed a threshold.
            - They have not already bred.
            - The enclosure has capacity.

        A new baby of the same species is added if conditions are met.
        """
        BREEDING_THRESHOLD = 7

        for enclosure in self._enclosures:
            # Group animals by species type
            species_groups: dict[type[Animal], list[Animal]] = {}
            for animal in enclosure.animals:
                if animal.status == "Alive":
                    species_groups.setdefault(type(animal), []).append(animal)

            for species, group in species_groups.items():
                if len(group) < 2:
                    continue

                # Eligible animals are happy enough and haven't bred yet
                eligible = [
                    a
                    for a in group
                    if a.breeding_counter >= BREEDING_THRESHOLD and not a.has_bred
                ]

                if len(eligible) >= 2:
                    # Capacity check before adding a baby
                    if len(enclosure.animals) >= enclosure.capacity:
                        print(
                            f"Breeding blocked in enclosure {enclosure.name}: "
                            f"capacity {enclosure.capacity} reached."
                        )
                        # Reset breeding counters to avoid repeated attempts
                        for a in eligible:
                            a.breeding_counter = 0
                        continue

                    baby = species()
                    enclosure.add_animal(baby)

                    print(
                        f"A new {species.__name__} has been born "
                        f"in enclosure {enclosure.name}!"
                    )

                    for a in eligible:
                        a.has_bred = True

    # -------------------- Visitor Management --------------------

    def visitor_enter(self):
        """
        Possibly admit a new visitor to the zoo.

        Entry chance is 40% per tick. The probability that a visitor
        accepts the ticket price decreases as the price rises above
        the base price. Consecutive refusals are tracked to warn the
        player about high prices.
        """
        if random.random() <= 0.4:
            price = self._ticket_price
            base_price = 25

            if price <= base_price:
                chance_to_enter = 1.0
            else:
                # Linear decrease in willingness as price exceeds base
                chance_to_enter = max(0, 1 - ((price - base_price) / base_price))

            if random.random() > chance_to_enter:
                self._consecutive_refusals += 1
                print(
                    f"A visitor refused to enter due to high ticket price (${price})."
                )

                if self._consecutive_refusals >= 3:
                    print(
                        "Many visitors are refusing to enter due to high ticket "
                        "prices, consider lowering the price."
                    )
                return

            # Successful entry
            self._consecutive_refusals = 0
            self._manager.budget += price
            visitor = Visitor()
            self._visitors.append(visitor)
            print("New visitor: ", visitor)

    def show_visitors(self):
        """Print all current visitors."""
        print("Visitors in the zoo:")
        for visitor in self._visitors:
            print(visitor)

    def visitor_goto_enclosure(self, visitor):
        """
        Randomly send a visitor to an enclosure.

        Args:
            visitor (Visitor): The visitor to move.
        """
        if len(self._enclosures) == 0:
            return

        # Small chance each tick that a visitor chooses an enclosure
        if random.random() <= 0.1:
            chosen_enclosure = random.choice(self._enclosures)
            visitor.enclosure = chosen_enclosure
            print(f"{visitor.name} has entered Enclosure {chosen_enclosure}")

    def visitor_view_enclosure(self, visitor):
        """
        Handle a visitor's experience viewing an enclosure.

        The visitor's happiness and the zoo's budget are affected by
        the average happiness of animals in the enclosure.

        Args:
            visitor (Visitor): The visitor currently viewing an enclosure.
        """
        if visitor.status == "Exited":
            return

        enclosure = visitor.enclosure
        if enclosure is None:
            return

        if len(enclosure.animals) <= 0:
            # No animals: visitor is disappointed
            visitor.deteriorate_happiness(5)
            visitor.enclosure = None
            print(
                f"{visitor.name} was dissapointed to see no animals in "
                f"Enclosure: {enclosure.name}."
            )
            return

        avg_happiness = sum(a.happiness for a in enclosure.animals) / len(
            enclosure.animals
        )

        if avg_happiness >= 70:
            # Very happy animals: big donation
            visitor.happiness = min(100, visitor.happiness + 20)
            self._manager.budget += 100
            visitor.enclosure = None
            print(
                f"{visitor.name} enjoyed seeing the happy animals in "
                f"Enclosure {enclosure.name}. They donated $100! "
                f"Your new budget is ${self.manager.budget}"
            )
        elif avg_happiness >= 40:
            # Moderately happy animals: small purchase
            visitor.happiness = min(100, visitor.happiness + 10)
            self._manager.budget += 10
            visitor.enclosure = None
            print(
                f"{visitor.name} had an okay time viewing Enclosure "
                f"{enclosure.name}, they bought a souvenir to take home."
            )
        else:
            # Unhappy animals: visitor feels sad
            visitor.deteriorate_happiness(10)
            visitor.enclosure = None
            print(
                f"{visitor.name} felt sad seeing the unhappy animals in "
                f"Enclosure {enclosure.name}."
            )

    # -------------------- Ticket Price & Cleaning --------------------

    def set_ticket_price(self, new_price):
        """
        Set a new ticket price.

        Args:
            new_price (str | int): New ticket price, expected to be an integer.

        Returns:
            int: The validated ticket price.

        Raises:
            ValueError: If the price is not an integer or is negative.
        """
        try:
            price = int(new_price)
        except ValueError:
            raise ValueError("Ticket price must be an integer.")

        if price < 0:
            raise ValueError("Ticket price cannot be negative.")

        self._ticket_price = price
        return price

    def get_enclosure(self, name):
        """
        Retrieve an enclosure by name.

        Args:
            name (str): Name of the enclosure.

        Returns:
            Enclosure | None: The matching enclosure, or None if not found.
        """
        for enclosure in self._enclosures:
            if enclosure.name.lower() == name.lower():
                return enclosure
        return None

    def clean_enclosure(self, enclosure_name, cost=20):
        """
        Clean a specific enclosure.

        Args:
            enclosure_name (str): Name of the enclosure to clean.
            cost (int): Cost of cleaning.

        Returns:
            tuple[Enclosure | None, str | None]:
                - The cleaned enclosure, or None if not found or insufficient budget.
                - An error message if something went wrong, otherwise None.
        """
        enclosure = self.get_enclosure(enclosure_name)

        if enclosure is None:
            return None, f"No enclosure found with name '{enclosure_name}'."

        if self._manager.budget < cost:
            return None, "Not enough budget to clean this enclosure."

        enclosure.clean()
        self._manager.budget -= cost
        return enclosure, None

    def show_budget(self):
        """
        Show the current budget.

        Currently a placeholder for CLI integration; the Command layer
        prints the budget directly after each command.
        """
        return

    # -------------------- Special Events --------------------

    def trigger_special_event(self):
        """
        Randomly trigger a special event.

        There is a small chance (3%) each tick that a random event
        from the zoo's event list will be applied.
        """
        if random.random() > 0.03:
            return

        event = random.choice(self.special_events)
        print(f"\n*** SPECIAL EVENT: {event.name} ***")
        event.apply(self)
