"""
A module containing the Name class for representing and validating names.

The Name class is responsible for representing names.

Classes:
    Name: A class to represent and validate a name.
"""

from contacts_assistant.field import Field


class Name(Field):
    """
    A class to represent and validate a name.

    Inherits from Field to provide a consistent interface for different types of fields.

    Attributes:
        value (str): The validated name.

    Methods:
        __init__(name): Initializes the Name with a given name string.
    """

    def __init__(self, name):
        """
        Initializes the Name instance with the given name string.

        Args:
            name (str): The name string to be assigned to the field.
        """
        self.value = name
