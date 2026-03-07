from abc import ABC, abstractmethod

class ICleanable(ABC):

    @abstractmethod
    def clean(self):
        """Perform cleaning actions on the structure."""
        pass
