"""
Handler module

This module contains the Handler class, which serves as the main controller for handling user commands and managing contacts and notes.

Classes:
    Handler: A class for handling user commands and managing contacts and notes.
"""

from contacts_assistant.address import AddressType
from contacts_assistant.command_completer import CommandCompleter
from contacts_assistant.constants import (
    GREETING_BANNER,
    CONTACTS_BOOK_FILENAME,
    NOTEBOOK_FILENAME,
)
from contacts_assistant.menu import Menu
from contacts_assistant.utils import format_greeting
from contacts_assistant.contacts_book import ContactsBook
from contacts_assistant.record import Record
from contacts_assistant.notebook import Notebook
from contacts_assistant.note import Note

NOT_FOUND_MESSAGE = "Contact does not exist, you can add it"


def handle_error(func):
    """
    Decorator to handle exceptions in the wrapped function.
    Args:
        func (function): The function to wrap with error handling.
    Returns:
        function: The wrapped function with error handling.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return str(error)

    return inner


class Handler:
    """
    A class for handling user commands and managing contacts and notes.

    Attributes:
        contact_book (ContactsBook): The ContactsBook instance.
        notebook (Notebook): The Notebook instance.
        completer (CommandCompleter): The CommandCompleter instance for command auto-completion.

    Methods:
        strip_quotes(value): Strip quotes from a string value.
        greeting(): Print a greeting message.
        hello(): Print a hello message.
        add_contact(args): Add a contact to the address book or update an existing contact.
        update_phone(args): Change the phone number of an existing contact.
        delete_contact(args): Remove a contact from the address book.
        set_contact_birthday(args): Add a birthday to a contact.
        get_contact_birthday(args): Show the birthday of a contact.
        get_upcoming_birthdays(args): Show all birthdays this week.
        update_contact_email(args): Update contact email.
        add_address(args): Add or update an address of a contact.
        remove_address(args): Remove an address from a contact.
        get_contact(args, search_by): Get contact details by name, phone, or email.
        get_contact_by_name(args): Get contact details by name.
        get_contact_by_phone(args): Get contact details by phone number.
        get_contact_by_email(args): Get contact details by email.
        add_note(args): Add a note to the notebook.
        find_note(args): Find and show the details of a note.
        delete_note(args): Delete a note from the notebook.
        delete_all_notes(args): Delete all notes from the notebook.
        update_note_prompt(args): Update a note by title in the notebook via user prompt.
        search_notes(args): Search for notes containing the query in their title or content.
        filter_notes(args): Filter notes by tag.
        get_notes_in_days(args): Get notes that are due in the next specified number of days.
        print_all_notes(args): Print all notes in the notebook.
        close(): Save data to files and return a goodbye message.
        __compliance_list(): Get a dictionary of commands and their corresponding functions.
        __without_params_commands(): Get a dictionary of commands without parameters and their corresponding functions.
        execute(command, args): Execute the function corresponding to the command.
    """

    def __init__(self) -> None:
        self.contact_book = ContactsBook.load_from_file(CONTACTS_BOOK_FILENAME)
        self.notebook = Notebook.load_from_file(NOTEBOOK_FILENAME)

        if not self.contact_book:
            self.contact_book = ContactsBook()

        self.completer = CommandCompleter(
            Menu.get_commands_witn_args(), self.contact_book
        )

    def greeting(self) -> str:
        """Print greeting message"""
        res = f"{format_greeting(GREETING_BANNER)}\n"
        res += f"Welcome to the assistant bot!\n{Menu.pretty_print()}"
        return res

    def hello(self) -> str:
        """Print hello message"""
        return f"How can I help you? \n{Menu.pretty_print()}"

    @handle_error
    def add_contact(self, args):
        """
        Add a contact to the address book or update an existing contact.

        Args:
            args (Namespace): Namespace containing name and phone number.
            book (ContactsBook): The address book to add the contact to.

        Returns:
            str: Message indicating whether the contact was added or updated.
        """

        name = args.name
        phone = args.phone
        email = args.email
        birthday = args.birthday

        record = self.contact_book.find_by_name(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.contact_book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        if email:
            record.add_email(email)
        if birthday:
            record.add_birthday(birthday)

        return message

    @handle_error
    def update_phone(self, args):
        """
        Change the phone number of an existing contact.

        Args:
            args (Namespace): Namespace containing name, old phone number, and new phone number.
            book (ContactsBook): The address book containing the contact.

        Returns:
            str: Message indicating whether the phone number was changed or if the contact was not found.
        """
        name = args.name
        old_phone = args.oldphone
        new_phone = args.newphone

        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        record.edit_phone(old_phone, new_phone)
        return "Phone changed"

    @handle_error
    def delete_contact(self, args):
        """
        Removes an contact from address book.

        Args:
            args (Namespace): Namespace containing contact name.
            book (ContactsBook): The address book.

        Returns:
            str: Message indicating whether the contact was added or updated.
        """
        name = args.name
        if self.contact_book.delete(name) is None:
            return f"Contact with name {name} does not exist."
        return "Contact removed."

    @handle_error
    def set_contact_birthday(self, args):
        """
        Add a birthday to a contact.

        Args:
            args (Namespace): Namespace containing name and birthday date.
            book (ContactsBook): The address book containing the contact.

        Returns:
            str: Message indicating whether the birthday was added or if the contact was not found.
        """
        name = args.name
        birthday = args.birthday
        record = self.contact_book.find_by_name(name)
        if record:
            record.add_birthday(birthday)
            return "Birthday added."
        return NOT_FOUND_MESSAGE

    @handle_error
    def get_contact_birthday(self, args):
        """
        Show the birthday of a contact.

        Args:
            args (Namespace): Namespace containing the name of the contact.
            book (ContactsBook): The address book containing the contact.

        Returns:
            str: The birthday date or a message indicating the birthday was not added or the contact was not found.
        """

        name = args.name
        record = self.contact_book.find_by_name(name)
        if record:
            if record.birthday:
                return record.birthday
            else:
                return "Birthday not added to this contact."
        else:
            return NOT_FOUND_MESSAGE

    @handle_error
    def get_upcoming_birthdays(self, args):
        """
        Show all birthdays this week.

        Args:
            args (list):

        Returns:
            list: All upcoming birthdays.
        """
        days = args.days
        if days:
            return str(self.contact_book.get_upcoming_birthdays(int(days)))
        else:
            return str(self.contact_book.get_upcoming_birthdays())

    @handle_error
    def update_contact_email(self, args) -> str:
        """
        Update contact e-mail

        Args:
            args (Namespace): Namespace containing name, new e-mail of the contact.

        Returns:
            str: Message indicating whether the contact e-mail was updated.
        """
        name = args.name
        email = args.email
        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        else:
            record.add_email(email)
            return "Email changed"

    @handle_error
    def add_address(self, args):
        """
        add or update address of contact.

        Args:
            args (Namespace): Namespace containing contact name.
            book (ContactsBook): The address book.

        Returns:
            str: Message indicating whether the contact was added or updated.
        """
        name = args.name
        address_type = args.addresstype

        address_type = AddressType(address_type)

        street = args.street
        city = args.city
        postalcode = args.postalcode
        country = args.country
        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        if address_type in record.addresses:
            record.edit_address(address_type, street, city, postalcode, country)
            return "Address updated."
        else:
            record.add_address(address_type, street, city, postalcode, country)

        return "Address added."

    @handle_error
    def remove_address(self, args):
        """
        Removes an contact address from contact.

        Args:
            args (Namespace): Namespace containing contact name.
            book (ContactsBook): The address book.

        Returns:
            str: Message indicating whether the address deleted.
        """
        name = args.name
        address_type = args.addresstype

        address_type = AddressType(address_type)

        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        if address_type in record.addresses:
            record.remove_address(address_type)
            return "Address removed."

        return "Address not found."

    @handle_error
    def get_contact(self, args, search_by: str):
        """
        Show the phone number of a contact.

        Args:
            args (Namespace): Namespace containing the (name, phone, or email) of the contact.
            search_by (str): The type of search ('name', 'phone', 'email')

        Returns:
            str or Record: The contact's record or a message indicating the contact was not found.
        """
        if search_by == "name":
            record = self.contact_book.find_by_name(args.name)
        elif search_by == "phone":
            record = self.contact_book.find_by_phone(args.phone)
        elif search_by == "email":
            record = self.contact_book.find_by_email(args.email)
        else:
            return "Invalid search type specified"

        if record is None:
            return NOT_FOUND_MESSAGE
        return record

    @handle_error
    def get_contact_by_name(self, args):
        """
        Get contact details by name.

        Args:
            args (Namespace): Namespace containing the name of the contact.

        Returns:
            str or Record: The contact's record or a message indicating the contact was not found.
        """
        return self.get_contact(args, "name")

    @handle_error
    def get_contact_by_phone(self, args):
        """
        Get contact details by phone number.

        Args:
            args (Namespace): Namespace containing the phone number of the contact.

        Returns:
            str or Record: The contact's record or a message indicating the contact was not found.
        """
        return self.get_contact(args, "phone")

    @handle_error
    def get_contact_by_email(self, args):
        """
        Get contact details by email.

        Args:
            args (Namespace): Namespace containing the email of the contact.

        Returns:
            str or Record: The contact's record or a message indicating the contact was not found.
        """
        return self.get_contact(args, "email")

    @handle_error
    def add_note(self):
        """
        Add a note to the notebook via user prompt.

        Returns:
            str: Message indicating whether the note was added or not.
        """
        title = input("Enter title: ")
        content = input("Enter content: ")
        tags = input("Enter tags (comma-separated): ").split(",")
        due_date = input("Enter due date (DD.MM.YYYY, optional): ").strip()
        due_date = due_date if due_date else None
        note = Note(
            title=title,
            content=content,
            tags=[tag.strip() for tag in tags],
            due_date=due_date,
        )
        return self.notebook.add(note)

    @handle_error
    def find_note(self, args):
        """
        Find and Show the details of a note.
        Args:
            args (Namespace): Namespace containing the title of the note.
        Returns:
            str or Note: The note's details or a message indicating the note was not found.
        """

        title = args.title
        notes = self.notebook.search(title)
        if notes:
            return self.notebook.format_notes_with_frame(notes)
        else:
            return f"Note {title} not found."

    @handle_error
    def delete_note(self, args):
        """
        Delete a note from the notebook.
        Args:
            args (Namespace): Namespace containing the title of the note.
        Returns:
            str: Message indicating whether the note was deleted or not.
        """

        return self.notebook.remove(args.title)

    @handle_error
    def delete_all_notes(self):
        """
        Delete all notes from the notebook.
        Args:
            args (Namespace): Namespace of arguments.
            notebook (Notebook): The notebook containing the notes.
        Returns:
            str: Message indicating whether the notes were deleted or not.
        """
        return self.notebook.remove_all()

    @handle_error
    def update_note_prompt(self, args):
        """
        Update a note by title in the notebook via user prompt.
        Args:
            args (Namespace): Namespace containing the title of the note.
        Returns:
            str: Message indicating whether the note was updated or not.
        """

        title = args.title
        content = input("Enter new content: ")
        tags = input("Enter new tags (comma-separated): ").split(",")
        due_date = input("Enter new due date (DD.MM.YYYY, optional): ").strip()
        due_date = due_date if due_date else None
        new_note = Note(
            title=title,
            content=content,
            tags=[tag.strip() for tag in tags],
            due_date=due_date,
        )
        return self.notebook.update(title, new_note)

    @handle_error
    def search_notes(self, args):
        """
        Search for notes containing the query in their title or content.
        Args:
            args (Namespace): Namespace containing the search query.
        Returns:
            str: Search results or a message indicating no notes were found.
        """

        query = args.query
        results = self.notebook.search(query)
        if results:
            return self.notebook.format_notes_with_frame(results)
        else:
            return f"No notes found containing '{query}'."

    @handle_error
    def filter_notes(self, args):
        """
        Filter notes by tag.
        Args:
            args (Namespace): Namespace containing the tag to filter by.
        Returns:
            str: Filter results or a message indicating no notes were found.
        """

        tag = args.tag
        results = self.notebook.filter_by_tag(tag)
        if results:
            return self.notebook.format_notes_with_frame(results)
        else:
            return f"No notes found with tag '{tag}'."

    @handle_error
    def get_notes_in_days(self, args):
        """
        Get notes that are due in the next specified number of days.
        Args:
            args (Namespace): Namespace containing the number of days to look ahead.
        Returns:
            str: List of due notes or a message indicating no notes are due.
        """

        days = int(args.days)
        results = self.notebook.notes_due_in_days(days)
        if results:
            return self.notebook.format_notes_with_frame(results)
        else:
            return f"No notes due in the next {days} days."

    @handle_error
    def print_all_notes(self):
        """
        Print all notes in the notebook.
        Returns:
            str: String representation of all notes.
        """
        return self.notebook.print_all_notes()

    def close(self) -> str:
        """return bye message and save data to files"""
        self.notebook.save_to_file(NOTEBOOK_FILENAME)
        self.contact_book.save_to_file(CONTACTS_BOOK_FILENAME)

        return "Good bye!"

    def __compliance_list(self) -> dict:
        """Return fuction list"""
        return {
            Menu.ADD_CONTACT: self.add_contact,
            Menu.UPDATE_PHONE: self.update_phone,
            Menu.DELETE_CONTACT: self.delete_contact,
            Menu.SET_BIRTHDAY: self.set_contact_birthday,
            Menu.SHOW_BIRTHDAY: self.get_contact_birthday,
            Menu.FIND_CONTACT_BY_NAME: self.get_contact_by_name,
            Menu.FIND_CONTACT_BY_PHONE: self.get_contact_by_phone,
            Menu.FIND_CONTACT_BY_EMAIL: self.get_contact_by_email,
            Menu.UPCOMING_BIRTHDAYS: self.get_upcoming_birthdays,
            Menu.UPDATE_EMAIL: self.update_contact_email,
            Menu.ADD_ADDRESS: self.add_address,
            Menu.REMOVE_ADDRESS: self.remove_address,
            Menu.FIND_NOTE: self.find_note,
            Menu.DELETE_NOTE: self.delete_note,
            Menu.UPDATE_NOTE: self.update_note_prompt,
            Menu.SEARCH_NOTES: self.search_notes,
            Menu.FILTER_NOTES_BY_TAG: self.filter_notes,
            Menu.NOTES_DUE_IN_DAYS: self.get_notes_in_days,
        }

    def __without_params_commands(self) -> dict:
        """Return fuction list"""
        return {
            Menu.SHOW_COMMANDS: self.hello,
            Menu.SHOW_ALL_CONTACTS: self.contact_book.__str__,
            Menu.ADD_NOTE: self.add_note,
            Menu.SHOW_ALL_NOTES: self.print_all_notes,
            Menu.DELETE_ALL_NOTES: self.delete_all_notes,
            Menu.EXIT: self.close,
            Menu.CLOSE: self.close,
        }

    @handle_error
    def execute(self, command, args: list) -> str:
        """
        Execute the function corresponding the command.

        Args:
            command (Menu): Input command.
            args (Namespace): Namespace of the input params.

        Returns:
            str: Result message of the handle function execution.
        """
        if command is None:
            return ""

        if len(command.value.param_list) != 0 and args is None:
            return ""

        if command in self.__without_params_commands():
            return self.__without_params_commands().get(command)()

        return self.__compliance_list().get(command)(args)
