from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


def command_category(name):
    def decorator(func):
        func.category = name
        return func
    return decorator

class Command:
    CATEGORY_ORDER = ["Status","Shop","System"]
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

                    print(f"Current budget: {self.zoo.manager.budget}")

                except KeyboardInterrupt:
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

    def do_menu(self, arg):
        """Show menu"""
        self.show_available_commands()

    @command_category("Shop")
    def do_add_animal(self, arg):
        """Purchase an Animal and place it in an Enclosure: add_animal <Species> <EnclosureName>"""

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
        """Purchase food <FoodType> <Quantity>"""
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

    @command_category("Status")
    def do_show_food(self, arg):
        """Show current food amount"""
        self.zoo.show_food()

    @command_category("Shop")
    def do_add_enclosure(self, arg):
        """Purchase an Enclosure <HabitatType>"""
        habitat = arg.strip()
        HABITATS = ["Grassland", "Eucalyptus Forest","Mountain Range"]

        if not habitat:
            print("Usage: add_enclosure <HabitatType>")
            print("Available habitats:", ", ".join(HABITATS))
            return

        matches = [h for h in HABITATS if h.lower() == habitat.lower()]
        if not matches:
            print(f"Invalid habitat '{habitat}'.")
            print("Available habitats:", ", ".join(HABITATS))
            return

        habitat = matches[0]
        enclosure = self.zoo.add_enclosure(habitat)
        print(f"Added Enclosure: {enclosure}")

    @command_category("Shop")
    def do_upgrade_enclosure(self, arg):
        """Upgrade an enclosure's capacity by 5 (max 25): upgrade_enclosure <EnclosureName>"""
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

    # def do_exit(self, arg):
    #     """Exit the program"""
    #     return True