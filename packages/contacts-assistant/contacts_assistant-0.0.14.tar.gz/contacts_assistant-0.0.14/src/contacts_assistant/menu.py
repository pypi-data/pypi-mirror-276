"""
This module defines the Menu class and related structures for managing commands in a assistant bot application.

Classes:
    Menu: An enumeration representing various commands and their parameters in the contacts assistant application.

Constants:
    Command: A namedtuple representing a command, its minimum required parameters, parameter list, and hint.
    Parametr: A namedtuple representing a parameter, including its name, whether it's required, hint, and choices (if applicable).
"""

import difflib
import argparse
from enum import Enum
from collections import namedtuple

from contacts_assistant.constants import MENU_BORDER
from contacts_assistant.utils import format_cmd, format_param

Command = namedtuple("Command", ["min_required_params", "param_list", "hint"])
Parametr = namedtuple(
    "Parametr",
    ["name", "required", "hint", "choices"],
    defaults=(None, False, None, None),
)


class Menu(Enum):
    """
    Enum representing various commands and their parameters in the contacts assistant application.

    Attributes:
        SHOW_COMMANDS: Show the list of available commands.
        ADD_CONTACT: Add a new contact or update an existing contact.
        UPDATE_PHONE: Update the phone number of a contact.
        DELETE_CONTACT: Delete a contact.
        SET_BIRTHDAY: Set the birthday of a contact.
        SHOW_BIRTHDAY: Show the birthday of a contact.
        FIND_CONTACT_BY_NAME: Find a contact by name.
        FIND_CONTACT_BY_PHONE: Find a contact by phone number.
        FIND_CONTACT_BY_EMAIL: Find a contact by email address.
        SHOW_ALL_CONTACTS: Show all contacts.
        UPCOMING_BIRTHDAYS: Show upcoming birthdays within the specified number of days.
        UPDATE_EMAIL: Update the email address of a contact.
        ADD_ADDRESS: Add or update the address of a contact.
        REMOVE_ADDRESS: Remove the address of a contact.
        ADD_NOTE: Add a new note.
        FIND_NOTE: Find a note by title.
        DELETE_NOTE: Delete a note.
        DELETE_ALL_NOTES: Delete all notes.
        UPDATE_NOTE: Update a note by title.
        SEARCH_NOTES: Search for notes containing the query in their title or content.
        FILTER_NOTES_BY_TAG: Filter notes by tag.
        NOTES_DUE_IN_DAYS: Show notes that are due within the next specified number of days.
        SHOW_ALL_NOTES: Show all notes.
        EXIT: Exit the application.
        CLOSE: Close the application.
    """

    SHOW_COMMANDS = Command(0, [], "Show the list of available commands")

    ADD_CONTACT = Command(
        2,
        [
            Parametr("name", True, "Name of the contact"),
            Parametr("phone", True, "Phone number of the contact (format: XXXXXXXXXX)"),
            Parametr("email", False, "Email address of the contact"),
            Parametr("birthday", False, "Birthday of the contact"),
        ],
        "Add a new contact or update an existing contact",
    )

    UPDATE_PHONE = Command(
        3,
        [
            Parametr("name", True, "Name of the contact"),
            Parametr("oldphone", True, "Old phone number"),
            Parametr("newphone", True, "New phone number (format: XXXXXXXXXX)"),
        ],
        "Update the phone number of a contact",
    )

    DELETE_CONTACT = Command(
        1, [Parametr("name", True, "Name of the contact")], "Delete a contact"
    )

    SET_BIRTHDAY = Command(
        2,
        [
            Parametr("name", True, "Name of the contact"),
            Parametr("birthday", True, "Birthday of the contact"),
        ],
        "Set the birthday of a contact",
    )

    SHOW_BIRTHDAY = Command(
        1,
        [Parametr("name", True, "Name of the contact")],
        "Show the birthday of a contact",
    )

    FIND_CONTACT_BY_NAME = Command(
        1, [Parametr("name", True, "Name of the contact")], "Find a contact by name"
    )

    FIND_CONTACT_BY_PHONE = Command(
        1,
        [Parametr("phone", True, "Phone number of the contact")],
        "Find a contact by phone number",
    )

    FIND_CONTACT_BY_EMAIL = Command(
        1,
        [Parametr("email", True, "Email address of the contact")],
        "Find a contact by email address",
    )

    SHOW_ALL_CONTACTS = Command(0, [], "Show all contacts")

    UPCOMING_BIRTHDAYS = Command(
        0,
        [
            Parametr(
                "days", False, "Number of days to look ahead for upcoming birthdays"
            )
        ],
        "Show upcoming birthdays within the specified number of days",
    )

    UPDATE_EMAIL = Command(
        2,
        [
            Parametr("name", True, "Name of the contact"),
            Parametr("email", True, "New email address of the contact"),
        ],
        "Update the email address of a contact",
    )

    ADD_ADDRESS = Command(
        2,
        [
            Parametr("name", True, "Name of the contact"),
            Parametr(
                "addresstype",
                False,
                "Type of address (Home, Work, Other)",
                ["Home", "Work", "Other"],
            ),
            Parametr("street", False, "Street address"),
            Parametr("city", False, "City"),
            Parametr("postalcode", False, "Postal code"),
            Parametr("country", False, "Country"),
        ],
        "Add or update the address of a contact",
    )

    REMOVE_ADDRESS = Command(
        2,
        [
            Parametr("name", True, "Name of the contact"),
            Parametr(
                "addresstype",
                False,
                "Type of address (Home, Work, Other)",
                ["Home", "Work", "Other"],
            ),
        ],
        "Remove the address of a contact",
    )

    ADD_NOTE = Command(0, [], "Add a new note")

    FIND_NOTE = Command(
        1, [Parametr("title", True, "Title of the note")], "Find a note by title"
    )

    DELETE_NOTE = Command(
        1, [Parametr("title", True, "Title of the note")], "Delete a note"
    )

    DELETE_ALL_NOTES = Command(0, [], "Delete all notes")

    UPDATE_NOTE = Command(
        1, [Parametr("title", True, "Title of the note")], "Update a note by title"
    )

    SEARCH_NOTES = Command(
        1,
        [Parametr("query", True, "Search query")],
        "Search for notes containing the query in their title or content",
    )

    FILTER_NOTES_BY_TAG = Command(
        1, [Parametr("tag", True, "Tag to filter notes by")], "Filter notes by tag"
    )

    NOTES_DUE_IN_DAYS = Command(
        1,
        [Parametr("days", True, "Number of days to look ahead for due notes")],
        "Show notes that are due within the next specified number of days",
    )

    SHOW_ALL_NOTES = Command(0, [], "Show all notes")

    EXIT = Command(0, [], "Exit the application")

    CLOSE = Command(0, [], "Close the application")

    @classmethod
    def pretty_print(cls):
        """Print all menu items"""
        res = ""
        res += MENU_BORDER
        for k, v in {x.name.lower(): x.value for x in cls}.items():
            res += f"[x] {format_cmd(k)} "
            res += f"{format_param(' '.join([f'[{x.name}]' for x in v.param_list]))} "
            res += f"{v.hint}\n"
        res += MENU_BORDER
        return res

    @classmethod
    def get_commands_list(cls) -> list:
        """Return all keys"""
        return [x.name.lower() for x in cls]

    @classmethod
    def get_by_name(cls, name: str) -> list:
        """Return all keys"""

        return {x.name.lower().strip(): x for x in cls}.get(name.lower().strip())

    @classmethod
    def check_params(cls, command, args: list) -> str:
        """Return all keys"""
        row = cls(command)
        min = row.value[0]
        max = len(row.value[1])
        if not min <= len(args) <= max:
            raise ValueError(
                f"This command requires {min} to {max} parameters {row.value[1]}"
            )

    @classmethod
    def get_commands_witn_args(cls) -> dict:
        """Return all commands with params"""
        commands = {}
        for command in cls:
            commands[command.name.lower()] = [
                "--" + x.name for x in command.value.param_list
            ]

        return commands

    @staticmethod
    def suggest_similar_commands(input_command):
        """
        Suggests similar commands based on user input command.
        """
        available_commands = Menu.get_commands_list()
        similar_commands = difflib.get_close_matches(input_command, available_commands)
        return similar_commands

    @classmethod
    def create_parser(cls):
        """
        Create an ArgumentParser instance for parsing command-line arguments.

        This method dynamically generates argument parsers for each command defined in the Menu class,
        with appropriate help messages based on command hints and parameter details.

        Returns:
            argparse.ArgumentParser: An ArgumentParser instance configured with subparsers for each command.
        """
        parser = argparse.ArgumentParser(
            description="Assistant bot", exit_on_error=False
        )

        subparsers = parser.add_subparsers(dest="commands")

        for command in cls:
            commandparser = subparsers.add_parser(
                command.name.lower(), help=command.value.hint, exit_on_error=False
            )
            for param in command.value.param_list:
                commandparser.add_argument(
                    "--" + param.name,
                    dest=param.name,
                    required=param.required,
                    help=param.hint,
                    choices=param.choices,
                )

        return parser
