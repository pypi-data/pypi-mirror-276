"""
A module containing the Field class, a base class to represent a generic field.

Classes:
    Field: A base class to represent a generic field.
"""


class Field:
    """
    A base class to represent a generic field.

    This class is intended to be inherited by specific field types like Name, Email, Phone, and Birthday.

    Attributes:
        value (str): The value of the field.

    Methods:
        __init__(value): Initializes the Field with a value.
        __str__(): Returns a string representation of the field.
    """

    def __init__(self, value):
        """
        Initializes the Field instance with the given value.

        Args:
            value (str): The value to be assigned to the field.
        """
        self.value = value

    def __str__(self):
        """
        Returns a string representation of the field.

        Returns:
            str: The string representation of the field's value.
        """
        return str(self.value)
