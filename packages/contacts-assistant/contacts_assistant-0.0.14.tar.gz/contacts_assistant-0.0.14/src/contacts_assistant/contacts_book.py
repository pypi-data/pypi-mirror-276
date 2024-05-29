"""
This module provides classes and functions for managing contacts.

Classes:
    ContactsBook: A class for managing a collection of contacts.
"""

from datetime import date
from collections import UserDict
import pickle

from contacts_assistant.date_helpers import DateHelper


class ContactsBook(UserDict):
    """
    A class to represent an address book that stores and manages records.

    Inherits from UserDict to utilize a dictionary as the underlying data structure.

    Methods:
        __str__(): Returns a string representation of the address book.
        add_record(record): Adds a new record to the address book.
        find(name): Finds and returns a record by name.
        delete(name): Deletes a record by name.
        get_upcoming_birthdays(): Returns a list of upcoming birthdays within the next 7 days.
    """

    def __str__(self):
        """
        Returns a string representation of the address book.

        Returns:
            str: A string with each record in the address book on a new line.
        """
        return self.__format_book()

    def __format_book(self):
        """
        Format a list of Record objects into a neatly aligned table.

        Returns:
            str: A formatted string representing the contact list.
        """
        contact_list = self.data.values()
        # Calculate the maximum width of each column
        name_width = max(
            (len(str(contact.name)) for contact in contact_list),
            default=10,
        )
        phone_width = max(
            list(
                len(str(phone)) for contact in contact_list for phone in contact.phones
            ),
            default=10,
        )
        email_width = max(
            list(len(str(contact.email)) for contact in contact_list if contact.email),
            default=15,
        )
        birthday_width = max(
            list(
                len(str(contact.birthday))
                for contact in contact_list
                if contact.birthday
            ),
            default=10,
        )
        address_width = max(
            list(
                len(str(address))
                for contact in contact_list
                for address in contact.addresses.values()
            ),
            default=20,
        )

        # Header
        header = f"{'Name':<{name_width}}  {'Phones':<{phone_width}}  {'Email':<{email_width}}  {'Birthday':<{birthday_width}}  {'Addresses':<{address_width}}"
        header_separator = "-" * (
            name_width + phone_width + email_width + birthday_width + address_width + 10
        )

        # Rows
        rows = []
        for contact in contact_list:
            name = str(contact.name)
            email = str(contact.email) if contact.email else ""
            birthday = str(contact.birthday) if contact.birthday else ""

            for index in range(0, max([len(contact.phones), len(contact.addresses)])):
                phone = ""
                address = ""
                if len(contact.phones) > index:
                    phone = str(contact.phones[index])

                if len(contact.addresses) > index:
                    address = f"{(list(contact.addresses.keys())[index]).value }: {contact.addresses[(list(contact.addresses.keys())[index])]}"

                rows.append(
                    f"{name:<{name_width}}  {phone:<{phone_width}}  {email:<{email_width}}  {birthday:<{birthday_width}}  {address:<{address_width}}"
                )
                email = ""
                name = ""
                birthday = ""

        return header + "\n" + header_separator + "\n" + "\n".join(rows)

    def add_record(self, record):
        """
        Adds a new record to the address book.

        Args:
            record: The record to be added.

        Raises:
            KeyError: If a record with the same name already exists in the address book.
        """
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find_by_name(self, name: str):
        """
        Finds and returns a record by name.

        Args:
            name (str): The name of the record to find.

        Returns:
            The record if found, otherwise None.
        """
        if name in self.data:
            return self.data[name]
        else:
            return None

    def find_by_phone(self, phone: str):
        """
        Finds and returns a record by phone number.

        Args:
            phone (str): The phone number of the record to find.

        Returns:
            The record if found, otherwise None.
        """
        for record in self.data.values():
            if record.find_phone(phone):
                return record
        return None

    def find_by_email(self, email: str):
        """
        Finds and returns a record by email address.

        Args:
            email (str): The email address of the record to find.

        Returns:
            The record if found, otherwise None.
        """
        for record in self.data.values():
            if record.email.value == email:
                return record
        return None

    def delete(self, name):
        """
        Deletes a record by name.
        Args:
            name: The name of the record to delete.

        Returns:
            The record which was deleted, if record not found returns None.
        """
        if name in self.data:
            removedcontact = self.data[name]
            del self.data[name]
            return removedcontact
        else:
            return None

    def get_upcoming_birthdays(self, days=7):
        """
        Get a list of upcoming birthdays within the specified number of days.
        If a birthday falls on a weekend, the congratulation date is moved to the next Monday.
        Args:
            days (int): The number of days to look ahead for upcoming birthdays. Defaults to 7.

        Returns:
            list: A list of dictionaries with names and congratulation dates for upcoming birthdays.
        """
        today = date.today()
        upcoming_birthdays = []
        for contact in list(
            filter(lambda x: x.birthday is not None, self.data.values())
        ):
            next_contact_birthday = DateHelper.get_next_birthday(
                contact.birthday.value, today
            )

            diffdays = (next_contact_birthday - today).days
            if diffdays in range(0, days):
                upcoming_birthdays.append(
                    f"Contact name: {contact.name.value}, congratulation date: {DateHelper.get_formated_workday(next_contact_birthday)}"
                )

        return upcoming_birthdays

    def save_to_file(self, filepath):
        """
        Saves the address book data to a file using pickle.

        Args:
            book (ContactsBook): The address book object to be saved.
            filepath (str): The name of the file where the data will be saved. Defaults to FILENAME.

        Raises:
            Exception: If there is an error during the file operation.
        """
        try:
            with open(filepath, "wb") as file:
                pickle.dump(self, file)
        except Exception as e:
            raise Exception(f"Error saving data: {e}")

    @staticmethod
    def load_from_file(filepath):
        """
        Loads the address book data from a file using pickle.

        Args:
            filepath (str): The name of the file from which the data will be loaded. Defaults to FILENAME.

        Returns:
            ContactsBook: The loaded address book object. If the file does not exist, returns a new ContactsBook instance.

        Raises:
            Exception: If there is an error during the file operation other than FileNotFoundError.
        """
        try:
            with open(filepath, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return ContactsBook()
        except Exception as e:
            raise Exception(f"Error loading data: {e}")
