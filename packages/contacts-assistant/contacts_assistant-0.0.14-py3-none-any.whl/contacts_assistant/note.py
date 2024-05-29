"""
A module containing the Note class for managing notes.

This module provides the Note class, which represents a note with a title, content, tags, and optional due date.

Classes:
    Note: A class to represent a note.
"""

import json
from datetime import datetime
from textwrap import fill
from contacts_assistant.constants import DATE_FORMAT, MAX_SIMBOLS_IN_ROW


class Note:
    """
    A class to represent a note.

    Attributes:
        title (str): The title of the note.
        content (str): The content of the note.
        tags (list): List of tags associated with the note.
        due_date (datetime): Due date of the note.
        created_at (datetime): Date when the note was created.

    Methods:
        __init__(title, content, tags=None, due_date=None): Initializes a Note instance.
        _validate_date(date_str): Validates the date format.
        to_dict(): Converts the Note instance to a dictionary.
        from_dict(data): Creates a Note instance from a dictionary.
        from_json(json_obj): Creates a Note instance from a JSON object.
        __str__(): Gets the string representation of the Note instance.
    """

    def __init__(self, title, content, tags=None, due_date=None):
        """
        Initialize a Note instance.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
            tags (list, optional): List of tags associated with the note.
            due_date (str, optional): Due date of the note in DD.MM.YYYY format.

        Raises:
            ValueError: If due_date is not in the correct format.
        """
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.due_date = self._validate_date(due_date) if due_date else None
        self.created_at = datetime.now()

    def _validate_date(self, date_str):
        """
        Validate the date format.

        Args:
            date_str (str): Date string in DD.MM.YYYY format.

        Returns:
            datetime: Parsed datetime object.

        Raises:
            ValueError: If date_str is not in the correct format.
        """
        try:
            return datetime.strptime(date_str, DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Please use DD.MM.YYYY")

    def to_dict(self):
        """
        Convert the Note instance to a dictionary.

        Returns:
            dict: Dictionary representation of the Note instance.
        """
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "due_date": self.due_date.strftime(DATE_FORMAT) if self.due_date else None,
            "created_at": self.created_at.strftime(DATE_FORMAT),
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Note instance from a dictionary.

        Args:
            data (dict): Dictionary containing note data.

        Returns:
            Note: A Note instance created from the dictionary data.
        """
        note = Note(
            title=data["title"],
            content=data["content"],
            tags=data.get("tags", []),
            due_date=data.get("due_date"),
        )
        note.created_at = datetime.strptime(
            data.get("created_at", datetime.now().strftime(DATE_FORMAT)), DATE_FORMAT
        )
        return note

    @staticmethod
    def from_json(json_obj):
        """
        Create a Note instance from a JSON object.

        Args:
            json_obj (str): JSON string representing the note data.

        Returns:
            Note: A Note instance created from the JSON data.
        """
        data = json.loads(json_obj)
        return Note.from_dict(data)

    def __str__(self):
        """
        Get the string representation of the Note instance.

        Returns:
            str: String representation of the Note instance.
        """
        due_date_str = (
            self.due_date.strftime(DATE_FORMAT) if self.due_date else "Not specified"
        )
        title = fill(self.title, MAX_SIMBOLS_IN_ROW)
        content = fill(self.content, MAX_SIMBOLS_IN_ROW) + " \n" * 2
        tag = f"Tags:       {', '.join(self.tags)}\n"
        due_date = f"Due Date:   {due_date_str}\n"
        created_at = f"Created At: {self.created_at.strftime(DATE_FORMAT)}"
        return (
            title
            + "\n"
            + "═" * MAX_SIMBOLS_IN_ROW
            + "\n"
            + content
            + tag
            + due_date
            + created_at
        )
