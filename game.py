from zoo import Zoo
from command import Command

class Game:
    def __init__(self):
        self.zoo = Zoo()
        self.command = Command(self.zoo)

    def run(self):
        exit = False
        while exit is False:
            self.command.cmdloop()
        
            # choice = input("Enter your choice: ")
            # if choice == "1":
            #     self.view_status()
            # elif choice == "2":
            #     self.add_enclosure()
            # elif choice == "3":
            #     self.add_visitor()
            # elif choice == "4":
            #     self.add_food()
            # elif choice == "5":
            #     self.add_medicine()
            # elif choice == "6":
            #     self.zoo.add_animal()
            # elif choice == "7":
            #     self.zoo.show_animals()
            # elif choice == "10":
            #     print("Exiting the game. Goodbye!")
            #     exit = True
            # else:
            #     print("Invalid choice. Please try again.")

game=Game()
game.run()

