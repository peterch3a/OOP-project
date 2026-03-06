import cmd

def command_category(name):
    def decorator(func):
        func.category = name
        return func
    return decorator

class Command(cmd.Cmd):
    CATEGORY_ORDER = ["Status","Shop","System"]

    intro = 'Welcome to OzZoo'
    prompt = ">> "

    def __init__(self, zoo):
        super().__init__()
        self.zoo = zoo

    def preloop(self):
        self.show_available_commands()

    def postcmd(self, stop, line):
        return stop

    def show_available_commands(self):
        categories = {}

        # Collect commands into categories
        for name in self.get_names():
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

        print()

    def do_menu(self, arg):
        """Show menu"""
        self.show_available_commands()

    @command_category("Shop")
    def do_add_animal(self, arg):
        """Purchase an Animal *Requires an Enclosure*"""
        try:
            added_animal = self.zoo.add_animal()
            print("Added Animal:", added_animal)
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

        if food_type.lower() not in ("meat", "fruit"):
            print("Error: Food type must be 'Meat' or 'Fruit'")
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
            print(f"Remaining budget: {self.zoo.manager.budget}")
        except ValueError as e:
            print("Error:", e)

    @command_category("Status")
    def do_show_enclosures(self, arg):
        """Show all Enclosures"""
        self.zoo.show_enclosures()

    # def do_exit(self, arg):
    #     """Exit the program"""
    #     return True
