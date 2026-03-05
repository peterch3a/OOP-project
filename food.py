
class Food:
    def __init__(self, food_type, quantity):
        self.food_type = food_type
        self.quantity = quantity

    def __str__(self):
        return f"{self.quantity} ({self.food_type})"
    