"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
food.py

Defines the Food class, representing a type of food and its quantity
in the zoo's inventory.
"""


class Food:
    """
    Represents a food type and its available quantity.

    Attributes:
        _food_type (str): Type of food (e.g., "meat", "leaves").
        _quantity (int): Amount of food units available.
    """

    def __init__(self, food_type, quantity):
        """
        Initialise a new Food entry.

        Args:
            food_type (str): Type of food.
            quantity (int): Initial quantity.
        """
        self._food_type = food_type
        self._quantity = quantity

    @property
    def food_type(self):
        """str: The type of food."""
        return self._food_type

    @food_type.setter
    def food_type(self, value):
        """Set the food type."""
        self._food_type = value

    @property
    def quantity(self):
        """int: The current quantity of this food."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """Set the quantity of this food."""
        self._quantity = value

    def __str__(self):
        """Return a readable summary of the food."""
        return f"{self._quantity} ({self._food_type})"
