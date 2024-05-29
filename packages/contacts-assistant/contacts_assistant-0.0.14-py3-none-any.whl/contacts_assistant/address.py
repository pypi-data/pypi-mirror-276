"""
Module containing classes to represent addresses and related enums.
"""

from enum import Enum
from contacts_assistant.field import Field


class AddressType(Enum):
    """
    Enumeration class for address types.
    """

    HOME = "Home"
    WORK = "Work"
    OTHER = "Other"


class City(Field):
    """
    Class to represent the city field of an address.
    """


class Country(Field):
    """
    Class to represent the country field of an address.
    """


class Street(Field):
    """
    Class to represent the street field of an address.
    """


class PostalCode(Field):
    """
    Class to represent the postal code field of an address.
    """


class Address:
    """
    Class to represent an address.
    """

    def __init__(
        self,
        street=None,
        city=None,
        postal_code=None,
        country=None,
    ) -> None:
        """
        Initialize the address fields.
        :param street: Street address. Default is None.
        :param city: City name. Default is None.
        :param postal_code: Postal code. Default is None.
        :param country: Country name. Default is None.

        """
        self.street = None
        self.city = None
        self.postal_code = None
        self.country = None

        if street:
            self.street = Street(street)
        if city:
            self.city = City(city)
        if postal_code:
            self.postal_code = PostalCode(postal_code)
        if country:
            self.country = Country(country)

    def __str__(self) -> str:
        """
        Return a string representation of the address.

        :return: A string representation of the address.
        """
        address_parts = []
        if self.street:
            address_parts.append(self.street.value)
        if self.city:
            address_parts.append(self.city.value)
        if self.postal_code:
            address_parts.append(self.postal_code.value)
        if self.country:
            address_parts.append(self.country.value)
        return ", ".join(address_parts)
