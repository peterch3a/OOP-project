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

    def do_exit(self, arg):
        """Exit the program"""
        return True
