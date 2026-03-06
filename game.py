import threading
import time
from zoo import Zoo
from command import Command

class Game:
    def __init__(self):
        self.zoo = Zoo()
        self.command = Command(self.zoo)

    def start_simulation_thread(self):
        def loop():
            time.sleep(1)
            while True:
                self.zoo.update()
                time.sleep(2)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

    def run(self):
        self.start_simulation_thread()
        self.command.cmdloop()

game=Game()
game.run()



