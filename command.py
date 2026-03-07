from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import Completer, Completion
from exceptions import HabitatCapacityExceededError

def command_category(name):
    def decorator(func):
        func.category = name
        return func
    return decorator

class ZooCompleter(Completer):
    def __init__(self, command):
        self.command = command

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        parts = text.split()

        if len(parts) == 0:
            for cmd in self._command_list():
                yield Completion(cmd, start_position=0)
            return

        if len(parts) == 1 and not text.endswith(" "):
            for cmd in self._command_list():
                if cmd.startswith(parts[0]):
                    yield Completion(cmd, start_position=-len(parts[0]))
            return

        cmd = parts[0]
        arg = parts[-1]

        for suggestion in self._arg_suggestions(cmd):
            if suggestion.lower().startswith(arg.lower()):
                yield Completion(suggestion, start_position=-len(arg))

    def _command_list(self):
        return [
            name[3:]
            for name in dir(self.command)
            if name.startswith("do_")
        ]

    def _arg_suggestions(self, cmd):
        zoo = self.command.zoo

        if cmd == "add_animal":
            species = ["Koala", "Kangaroo", "WedgeTailedEagle"]
            enclosures = [e.name for e in zoo.enclosures]
            return species + enclosures

        if cmd == "add_enclosure":
            return ["Grassland", "Forest", "Mountain"]

        if cmd == "add_food":
            return ["Meat", "Leaves"]

        if cmd in ("upgrade_enclosure", "clean_enclosure"):
            return [e.name for e in zoo.enclosures]

        return []

class Command:
    CATEGORY_ORDER = ["Status", "Shop", "System", "Manage"]

    def __init__(self, zoo):
        self._zoo = zoo
        self._zoo.command = self
        self._completer = ZooCompleter(self)
        self._session = PromptSession(completer=self._completer)
        self._intro = "Welcome to OzZoo"
        self._prompt = ">> "

    @property
    def zoo(self):
        return self._zoo

    @property
    def session(self):
        return self._session

    @property
    def intro(self):
        return self._intro

    @intro.setter
    def intro(self, value):
        self._intro = value

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, value):
        self._prompt = value

    def cmdloop(self):
        print(self._intro)
        self.show_available_commands()

        with patch_stdout():
            while True:
                try:
                    line = self._session.prompt(self._prompt)
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

                    print(f"Current budget: ${self._zoo.manager.budget}")

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
                print(f"[{category}]")
                for cmd_name, doc in categories[category]:
                    print(f"  {cmd_name:<20} {doc}")

        for category, commands in categories.items():
            if category not in self.CATEGORY_ORDER:
                print(f"\n[{category}]")
                for cmd_name, doc in commands:
                    print(f"  {cmd_name:<20} {doc}")

        print(f"\nCurrent budget: ${self._zoo.manager.budget}")

    def do_menu(self, arg):
        """Show menu"""
        self.show_available_commands()

    @command_category("Shop")
    def do_add_animal(self, arg):
        """Purchase an Animal and place it in an Enclosure, Cost: $100 - add_animal <Species> <EnclosureName>"""

        if not self._zoo.enclosures:
            print("Error: No enclosures available. Please add an enclosure first.")
            return

        parts = arg.split()

        if len(parts) != 2:
            print("Usage: add_animal <Koala|Kangaroo|WedgeTailedEagle> <EnclosureName>")
            print("Available enclosures:")
            for e in self._zoo.enclosures:
                print(f"  {e.name} ({e.habitat_type}, Capacity: {e.capacity}, Animals: {len(e._animals)})")
            return

        species, enclosure_name = parts

        try:
            animal, enclosure = self._zoo.add_animal(species, enclosure_name)
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
        self._zoo.show_animals()

    @command_category("Status")
    def do_show_budget(self, arg):
        """Show current budget amount"""
        self._zoo.show_budget()

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

        self._zoo.add_food(food_type, food_quantity)
        print(f"Purchased {food_quantity} units of {food_type}.")

    @command_category("Status")
    def do_show_food(self, arg):
        """Show current food amount"""
        self._zoo.show_food()

    @command_category("Shop")
    def do_add_enclosure(self, arg):
        """Purchase an Enclosure, Cost: $400 - add_enclosure <HabitatType>"""
        habitat = arg.strip()
        HABITATS = ["Grassland", "Forest", "Mountain"]

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
            enclosure = self._zoo.add_enclosure(matches[0])
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
            enclosure, new_cap = self._zoo.upgrade_enclosure(enclosure_name)
            print(f"Enclosure {enclosure.name} upgraded! New capacity: {new_cap}")
        except ValueError as e:
            print("Error:", e)

    @command_category("Status")
    def do_show_enclosures(self, arg):
        """Show all Enclosures"""
        self._zoo.show_enclosures()

    @command_category("Status")
    def do_show_visitors(self, arg):
        """Show all Visitors"""
        self._zoo.show_visitors()

    @command_category("Manage")
    def do_set_ticket_price(self, arg):
        """Set ticket price (Default: $25) - set_ticket_price <Amount>"""
        arg = arg.strip()

        if not arg:
            print("Usage: set_ticket_price <Amount>")
            return

        try:
            new_price = self._zoo.set_ticket_price(arg)
            print(f"Ticket price updated to ${new_price}")
        except ValueError as e:
            print("Error:", e)

    @command_category("Manage")
    def do_clean_enclosure(self, arg):
        """Clean a specific enclosure, Cost: $20 - clean_enclosure <EnclosureName>"""
        name = arg.strip()

        if not name:
            print("Usage: clean_enclosure <EnclosureName>")
            return

        enclosure, error = self._zoo.clean_enclosure(name)

        if enclosure is None:
            print("Error:", error)

    @command_category("Status")
    def do_show_cleanliness(self, arg):
        """Show cleanliness levels of all enclosures"""
        for enclosure in self._zoo.enclosures:
            print(f"Enclosure {enclosure.name}: {enclosure.cleanliness}% cleanliness")
