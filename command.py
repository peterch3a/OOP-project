from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from exceptions import HabitatCapacityExceededError

def command_category(name):
    def decorator(func):
        func.category = name
        return func
    return decorator

class Command:
    CATEGORY_ORDER = ["Status","Shop","System","Manage"]
    intro = 'Welcome to OzZoo'
    prompt = ">> "

    def __init__(self, zoo):
        self.zoo = zoo
        self.zoo.command = self
        self.session = PromptSession()

    def cmdloop(self):
        print(self.intro)
        self.show_available_commands()

        with patch_stdout():
            while True:
                try:
                    line = self.session.prompt(self.prompt)
                    line = line.strip()

                    if not line:
                        continue

                    parts = line.split(maxsplit=1)
                    cmd = parts[0]
                    arg = parts[1] if len(parts) > 1 else ""

                    method_name = f"do_{cmd}"
                    if hasattr(self, method_name):
                        method = getattr(self, method_name)
                        method(arg)
                    else:
                        print(f"Unknown command: {cmd}")

                    print(f"Current budget: ${self.zoo.manager.budget}")

                except KeyboardInterrupt:
                    print("Interrupted. Press Ctrl+D to exit.")
                    continue
                except EOFError:
                    print("\nExiting...")
                    break

    def show_available_commands(self):
        categories = {}

        for name in dir(self):
            if name.startswith("do_"):
                method = getattr(self, name)
                category = getattr(method, "category", "System")
                cmd_name = name[3:]
                doc = method.__doc__ or ""

                categories.setdefault(category, []).append((cmd_name, doc))

        print("\nAvailable commands:")

        for category in self.CATEGORY_ORDER:
            if category in categories:
                print(f"\n[{category}]")
                for cmd_name, doc in categories[category]:
                    print(f"  {cmd_name:<15} {doc}")

        for category, commands in categories.items():
            if category not in self.CATEGORY_ORDER:
                print(f"\n[{category}]")
                for cmd_name, doc in commands:
                    print(f"  {cmd_name:<15} {doc}")
        
        print(f"Current budget: ${self.zoo.manager.budget}")

    def do_menu(self, arg):
        """Show menu"""
        self.show_available_commands()

    @command_category("Shop")
    def do_add_animal(self, arg):
        """Purchase an Animal and place it in an Enclosure, Cost: $100 - add_animal <Species> <EnclosureName>"""

        if not self.zoo.enclosures:
            print("Error: No enclosures available. Please add an enclosure first.")
            return

        parts = arg.split()

        if len(parts) != 2:
            print("Usage: add_animal <Koala|Kangaroo|WedgeTailedEagle> <EnclosureName>")
            print("Available enclosures:")
            for e in self.zoo.enclosures:
                print(f"  {e.name} ({e.habitat_type}, capacity {e.capacity})")
            return

        species, enclosure_name = parts

        try:
            animal, enclosure = self.zoo.add_animal(species, enclosure_name)
            print(f"Added {species}: {animal}")
            print(f"Placed in enclosure {enclosure.name} ({enclosure.habitat_type})")
            print(f"{animal.name} lets out a {animal.make_sound()}")
        except HabitatCapacityExceededError as e:
            print("Capacity Error:", e)
        except ValueError as e:
            print("Error:", e)

    @command_category("Status")
    def do_show_animals(self, arg):
        """Show all Animals"""
        self.zoo.show_animals()

    @command_category("Status")
    def do_show_budget(self, arg):
        """Show current budget amount"""
        self.zoo.show_budget()

    @command_category("Shop")
    def do_add_food(self, arg):
        """Purchase food, Cost: $1 per food - add_food <FoodType> <Quantity>"""
        parts = arg.split()

        if len(parts) != 2:
            print("Usage: add_food <FoodType> <Quantity>")
            return
        
        food_type = parts[0]
        food_quantity = parts[1]

        if food_type.lower() not in ("meat", "leaves"):
            print("Error: Food type must be 'Meat' or 'Leaves'")
            return

        try:
            food_quantity = int(food_quantity)
        except ValueError:
            print("Error: Quantity must be an integer")
            return

        self.zoo.add_food(food_type, food_quantity)
        print(f"Purchased {food_quantity} units of {food_type}.")


    @command_category("Status")
    def do_show_food(self, arg):
        """Show current food amount"""
        self.zoo.show_food()

    @command_category("Shop")
    def do_add_enclosure(self, arg):
        """Purchase an Enclosure, Cost: $400 - add_enclosure <HabitatType>"""
        habitat = arg.strip()
        HABITATS = ["Grassland", "Forest","Mountain"]

        if not habitat:
            print("Usage: add_enclosure <HabitatType>")
            print("Available habitats:", ", ".join(HABITATS))
            return

        matches = [h for h in HABITATS if h.lower() == habitat.lower()]
        if not matches:
            print(f"Invalid habitat '{habitat}'.")
            print("Available habitats:", ", ".join(HABITATS))
            return

        try:
            enclosure = self.zoo.add_enclosure(matches[0])
            print(f"Added Enclosure: {enclosure}")
        except Exception as e:
            print(f"Error: {e}")

    @command_category("Shop")
    def do_upgrade_enclosure(self, arg):
        """Upgrade an enclosure's capacity by 5 (max 25), Cost: $50 - upgrade_enclosure <EnclosureName>"""
        enclosure_name = arg.strip()

        if not enclosure_name:
            print("Usage: upgrade_enclosure <EnclosureName>")
            return

        try:
            enclosure, new_cap = self.zoo.upgrade_enclosure(enclosure_name)
            print(f"Enclosure {enclosure.name} upgraded! New capacity: {new_cap}")
        except ValueError as e:
            print("Error:", e)

    @command_category("Status")
    def do_show_enclosures(self, arg):
        """Show all Enclosures"""
        self.zoo.show_enclosures()

    @command_category("Status")
    def do_show_visitors(self, arg):
        """Show all Visitors"""
        self.zoo.show_visitors()

    @command_category("Manage")
    def do_set_ticket_price(self, arg):
        """Set ticket price (Default: $25) - set_ticket_price <Amount>"""
        arg = arg.strip()

        if not arg:
            print("Usage: set_ticket_price <Amount>")
            return

        try:
            new_price = self.zoo.set_ticket_price(arg)
            print(f"Ticket price updated to ${new_price}")
        except ValueError as e:
            print("Error:", e)

    @command_category("Manage")
    def do_clean_enclosure(self, arg):
        """Clean a specific enclosure, Cost: $20 — clean_enclosure <EnclosureName>"""
        name = arg.strip()

        if not name:
            print("Usage: clean_enclosure <EnclosureName>")
            return

        enclosure, error = self.zoo.clean_enclosure(name)

        if enclosure is None:
            print("Error:", error)

    @command_category("Status")
    def do_show_cleanliness(self, arg):
        """Show cleanliness levels of all enclosures"""
        for enclosure in self.zoo.enclosures:
            print(f"{enclosure.name}: {enclosure.cleanliness}% cleanliness")



    # @command_category("System")
    # def do_trigger_event(self, arg):
    #     """Trigger a special event manually - trigger_event <EventName>"""

    #     arg = arg.strip()

    #     if not arg:
    #         print("Available special events:")
    #         for event in self.zoo.special_events:
    #             print(" -", event.name)
    #         return

    #     matches = [e for e in self.zoo.special_events if e.name.lower() == arg.lower()]

    #     if not matches:
    #         print(f"No event named '{arg}'.")
    #         return

    #     event = matches[0]
    #     print(f"\n*** MANUAL EVENT TRIGGERED: {event.name} ***")
    #     event.apply(self.zoo)


    # def do_exit(self, arg):
    #     """Exit the program"""
    #     return True