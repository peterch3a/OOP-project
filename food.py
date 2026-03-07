class Food:
    def __init__(self, food_type, quantity):
        self._food_type = food_type
        self._quantity = quantity

    @property
    def food_type(self):
        return self._food_type

    @food_type.setter
    def food_type(self, value):
        self._food_type = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    def __str__(self):
        return f"{self._quantity} ({self._food_type})"