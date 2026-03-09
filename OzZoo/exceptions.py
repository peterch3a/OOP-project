"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
exceptions.py

Defines custom exception types used across the zoo simulation.
"""


class HabitatCapacityExceededError(Exception):
    """
    Raised when trying to add an animal to a full enclosure.

    This exception is thrown by Enclosure.add_animal and handled by
    the command layer to provide user-friendly error messages.
    """

    pass
