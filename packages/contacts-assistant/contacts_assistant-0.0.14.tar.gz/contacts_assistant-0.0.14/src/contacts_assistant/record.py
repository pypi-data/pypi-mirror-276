"""
A module containing the Record class for representing contact records.

This module provides the Record class, which represents a contact record. 
It includes attributes and methods for managing contact information.

Classes:
    Record: A class to represent a contact record.
"""

from contacts_assistant.phone import Phone
from contacts_assistant.name import Name
from contacts_assistant.birthday import Birthday
from contacts_assistant.contact_email import Email
from contacts_assistant.address import Address, AddressType


class Record:
    """
    A class to represent a contact record.

    Attributes:
        name (Name): The name of the contact.
        phones (list): A list of phone numbers associated with the contact.
        birthday (Birthday): The birthday of the contact.

    Methods:
        __init__(name): Initializes the Record with a given name.
        __str__(): Returns a string representation of the contact record.
        add_phone(number): Adds a phone number to the contact record.
        remove_phone(number): Removes a phone number from the contact record.
        edit_phone(old_number, new_number): Edits a phone number in the contact record.
        find_phone(number): Finds a phone number in the contact record.
        add_birthday(date): Adds a birthday to the contact record.
    """

    def __init__(self, name):
        """
        Initializes the Record instance with the given name.

        Args:
            name (str): The name of the contact.
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.addresses = {}

    def __str__(self):
        """
        Returns a string representation of the contact record.

        Returns:
            str: A string containing the name, phone numbers, and birthday of the contact.
        """
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

        if self.email:
            result += f", email: {self.email}"

        if self.birthday:
            result += f", birthday: {self.birthday}"

        if self.addresses:
            result += ", addresses: "
            for addr_type, address in self.addresses.items():
                result += f"{addr_type.value}: {address}, "
            result = result[:-2]  # Remove trailing comma and space
        return result

    def add_phone(self, number: str):
        """
        Adds a phone number to the contact record.

        Args:
            number (str): The phone number to be added.
        """
        self.phones.append(Phone(number))

    def remove_phone(self, number: str):
        """
        Removes a phone number from the contact record.

        Args:
            number (str): The phone number to be removed.
        """
        self.phones = list(filter(lambda phone: phone == number, self.phones))

    def edit_phone(self, old_number: str, new_number: str):
        """
        Edits a phone number in the contact record.

        Args:
            old_number (str): The current phone number to be replaced.
            new_number (str): The new phone number to replace the old one with.

        Raises:
            KeyError: If the provided number does not exist or the contact has no phone numbers.
        """
        found = False
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                found = True
                break
        if not found:
            raise KeyError(
                "Provided number does not exist or contact has no phone numbers."
            )

    def find_phone(self, number):
        """
        Finds a phone number in the contact record.

        Args:
            number (str): The phone number to find.

        Returns:
            Phone: The phone number object if found, otherwise None.
        """
        for phone in self.phones:
            if phone.value == number:
                return phone

    def add_birthday(self, date):
        """
        Adds a birthday to the contact record.

        Args:
            date (str): The birthday date string in the format specified by DATE_FORMAT: "%d.%m.%Y".
        """
        self.birthday = Birthday(date)

    def add_email(self, email: str):
        """
        Adds and validates the user's email address.

        Args:
            email (str): The email address to be validated and added.

        Raises:
            ValueError: If the email address format is invalid.
        """
        self.email = Email(email)

    def add_address(
        self,
        address_type: AddressType,
        street=None,
        city=None,
        postal_code=None,
        country=None,
    ):
        """
        Add an address to the contact record.

        Args:
            address_type (AddressType): The type of address (HOME, WORK, OTHER).
            street (str, optional): The street address.
            city (str, optional): The city.
            postal_code (str, optional): The postal code.
            country (str, optional): The country.
        """
        self.addresses[address_type] = Address(street, city, postal_code, country)

    def edit_address(
        self,
        address_type: AddressType,
        street=None,
        city=None,
        postal_code=None,
        country=None,
    ):
        """
        Edit the address of the contact record.

        Args:
            address_type (AddressType): The type of address (HOME, WORK, OTHER).
            street (str, optional): The street address.
            city (str, optional): The city.
            postal_code (str, optional): The postal code.
            country (str, optional): The country.

        Raises:
            ValueError: If no address exists to edit.
        """
        if address_type in self.addresses:
            address = self.addresses[address_type]
            if street is not None:
                address.street = street
            if city is not None:
                address.city = city
            if postal_code is not None:
                address.postal_code = postal_code
            if country is not None:
                address.country = country
        else:
            raise ValueError("No address exists to edit.")

    def remove_address(self, address_type: AddressType):
        """
        Remove the address of the specified type from the contact record.

        Args:
            address_type (AddressType): The type of address to remove (HOME, WORK, OTHER).
        """
        if address_type in self.addresses:
            del self.addresses[address_type]
