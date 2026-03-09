"""
 Name: Peter Chea
 ID: s3742440
 Unit: NIT2112 Object Oriented Programming
 Task: Assessment 3/4 - Project
"""

"""
interfaces.py

Defines abstract interfaces used across the zoo simulation.
"""

from abc import ABC, abstractmethod


class ICleanable(ABC):
    """
    Interface for cleanable structures.

    Any class implementing this interface must provide a `clean` method
    that performs cleaning actions on the structure.
    """

    @abstractmethod
    def clean(self):
        """
        Perform cleaning actions on the structure.

        Implementations should reset cleanliness-related state and may
        print feedback or log actions.
        """
        pass
