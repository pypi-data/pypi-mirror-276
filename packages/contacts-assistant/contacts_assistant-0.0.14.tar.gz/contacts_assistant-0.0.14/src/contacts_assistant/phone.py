"""
A module containing the Phone class for representing and validating phone numbers.

This module provides the Phone class, which inherits from Field to provide a consistent interface for different types of fields. 
The Phone class is responsible for validating and representing phone numbers.

Classes:
    Phone: A class to represent and validate a phone number.
"""

from contacts_assistant.field import Field


class Phone(Field):
    """
    A class to represent and validate a phone number.

    Inherits from Field to provide a consistent interface for different types of fields.

    Attributes:
        value (str): The validated phone number.

    Methods:
        __init__(number): Initializes the Phone with a given phone number.
        validate_number(number): Validates the phone number format.
    """

    def __init__(self, number):
        """
        Initializes the Phone instance with the given phone number.

        Args:
            number (str): The phone number to be validated and assigned to the field.

        Raises:
            ValueError: If the phone number format is invalid.
        """
        self.value = self.validate_number(number)

    def validate_number(self, number):
        """
        Validates the format of the phone number.

        The phone number must have exactly 10 digits and contain only numeric characters.

        Args:
            number (str): The phone number to be validated.

        Returns:
            str: The validated phone number.

        Raises:
            ValueError: If the phone number format is invalid.
        """
        if len(number) != 10:
            raise ValueError("Telephone number should have 10 numbers")

        if not number.isdigit():
            raise ValueError("Telephone number should have only numbers")

        return number
