class Manager:
    def __init__(self):
        self.__budget = 500

    @property
    def budget(self):
        return self.__budget
    
    @budget.setter
    def budget(self, value):
        self.__budget = value