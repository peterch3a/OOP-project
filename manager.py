"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
manager.py

Defines the Manager class, responsible for tracking the zoo's budget.
"""


class Manager:
    """
    Represents the zoo manager's financial control.

    Attributes:
        __budget (int): Current budget amount.
    """

    def __init__(self):
        """Initialise the manager with a starting budget."""
        self.__budget = 500

    @property
    def budget(self):
        """int: Current budget amount."""
        return self.__budget

    @budget.setter
    def budget(self, value):
        """Set the current budget amount."""
        self.__budget = value
