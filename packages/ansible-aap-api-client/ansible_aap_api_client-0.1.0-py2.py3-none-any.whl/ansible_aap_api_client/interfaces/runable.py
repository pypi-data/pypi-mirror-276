"""
Runable interface
"""

from abc import ABC, abstractmethod


class Runable(ABC):  # pylint: disable=too-few-public-methods
    """Interface for a runable object"""

    @abstractmethod
    def run(self) -> None:
        """Abstract method to run an object

        :rtype: None
        :returns: Nothing
        """
