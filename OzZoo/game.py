"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
game.py

Entry point for the zoo simulation. Creates the Zoo and Command
instances, starts the background simulation thread, and runs the
interactive command loop.
"""

import threading
import time

from zoo import Zoo
from command import Command


class Game:
    """
    Coordinates the zoo simulation and the command interface.

    Attributes:
        zoo (Zoo): The zoo instance.
        command (Command): The command interface for user interaction.
    """

    def __init__(self):
        """Initialise the game with a new Zoo and Command interface."""
        self.zoo = Zoo()
        self.command = Command(self.zoo)

    def start_simulation_thread(self):
        """
        Start the background simulation thread.

        The thread:
            - Waits 1 second before starting.
            - Calls zoo.update() every 3 seconds.
            - Runs as a daemon so it stops when the main program exits.
        """

        def loop():
            time.sleep(1)
            while True:
                self.zoo.update()
                time.sleep(3)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

    def run(self):
        """
        Run the game.

        Starts the simulation thread and enters the command loop.
        """
        self.start_simulation_thread()
        self.command.cmdloop()


# Run the game when this module is executed directly
game = Game()
game.run()
