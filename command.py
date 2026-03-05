import cmd

class Command(cmd.Cmd):
    intro = 'Welcome to this simple command prompt'
    prompt = ">> "

    def __init__(self, zoo):
        super().__init__()
        self.zoo = zoo

    def preloop(self):
        self.show_available_commands()

    def postcmd(self, stop, line):
        self.show_available_commands()
        return stop

    def show_available_commands(self):
        print("\nAvailable commands:")
        for name in self.get_names():
            if name.startswith("do_"):
                cmd_name = name[3:]
                method = getattr(self, name)
                doc = method.__doc__ or ""
                print(f"  {cmd_name:<15} {doc}")
        print()

    def do_add_animal(self, arg):
        """Add an Animal"""
        added_animal = self.zoo.add_animal()
        print("Added Animal:", added_animal)

    def do_show_animals(self, arg):
        """Show all animals"""
        self.zoo.show_animals()

    def do_show_budget(self, arg):
        """Show current budget amount"""
        self.zoo.show_budget()

    def do_add_food(self, arg):
        """Purchase food"""
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

    def do_show_food(self, arg):
        """Show current food amount"""
        self.zoo.show_food()


    # def do_exit(self, arg):
    #     """Exit the program"""
    #     return True
