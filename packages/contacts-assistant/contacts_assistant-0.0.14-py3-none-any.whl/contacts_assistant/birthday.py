"""
A module containing the Birthday class for representing and validating birthdays.

Classes:
    Birthday: A class to represent and validate a birthday.
"""

from datetime import datetime

from contacts_assistant.field import Field
from contacts_assistant.constants import DATE_FORMAT


class Birthday(Field):
    """
    A class to represent and validate a birthday.

    Inherits from Field to provide a consistent interface for different types of fields.

    Attributes:
        value (datetime): The validated birthday date.

    Methods:
        __init__(value: str): Initializes the Birthday with a validated date string.
        __str__(): Returns a string representation of the birthday.
    """

    def __init__(self, value: str):
        """
        Initializes the Birthday instance by validating the provided date string.

        Args:
            value (str): The date string to be validated in the format specified by DATE_FORMAT.

        Raises:
            ValueError: If the date string is not in the correct format.
        """
        try:
            self.value = datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        """
        Returns a string representation of the birthday.

        Returns:
            str: The birthday as a string in the format specified by DATE_FORMAT.
        """
        return f"{self.value.strftime(DATE_FORMAT)}"
