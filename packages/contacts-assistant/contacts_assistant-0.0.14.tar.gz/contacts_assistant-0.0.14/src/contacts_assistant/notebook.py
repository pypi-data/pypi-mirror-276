"""
A module containing the Notebook class for managing notes.

This module provides the Notebook class, which represents a collection of notes. 
It includes methods for adding, searching, removing, updating, and filtering notes.

Classes:
    Notebook: A class to represent a collection of notes.
"""

import json
from datetime import datetime, timedelta

from contacts_assistant.note import Note


class Notebook:
    """
    A class to represent a collection of notes.

    Attributes:
        notes (list): A list of Note objects representing the notes in the notebook.

    Methods:
        __init__(): Initializes a Notebook instance.
        add(note, suppress_message=False): Adds a note to the notebook.
        search(query): Searches for notes containing the query in their title or content.
        remove(title): Removes notes with the specified title.
        remove_all(): Removes all notes from the notebook.
        update(title, new_note): Updates a note with new note data.
        filter_by_tag(tag): Filters notes by tag.
        notes_due_in_days(days): Gets notes due in the next specified number of days.
        to_dict(): Converts the Notebook instance to a dictionary.
        from_dict(data): Creates a Notebook instance from a dictionary.
        save_to_file(filepath): Saves the Notebook instance to a file.
        load_from_file(filepath): Loads a Notebook instance from a file.
        print_all_notes(): Gets a string representation of all notes in the notebook.
        format_notes_with_frame(notes): Formats a list of notes with a decorative frame.
        _format_note_with_frame(note): Formats a note with a decorative frame (internal method).
        __str__(): Gets the string representation of the Notebook instance.
    """

    def __init__(self):
        """
        Initialize a Notebook instance.
        """
        self.notes = []

    def add(self, note, suppress_message=False):
        """
        Add a note to the notebook.

        Args:
            note (Note): The note to add.
            suppress_message (bool, optional): Suppress the "Note added" message if True.
        """
        self.notes.append(note)
        if not suppress_message:
            return "Note added."

    def search(self, query):
        """
        Search for notes containing the query in their title or content.

        Args:
            query (str): The search query.

        Returns:
            list: List of notes matching the search query.
        """
        query = query.lower()
        result = []
        for note in self.notes:
            if query in note.title.lower() or query in note.content.lower():
                result.append(note)
        return result

    def remove(self, title):
        """
        Remove notes with the specified title.

        Args:
            title (str): The title of the notes to remove.

        Returns:
            str: Message indicating whether the note was removed or not.
        """
        notes = self.search(title)
        if not notes:
            return "Note not found."

        print(f"Found {len(notes)} note(s) with title '{title}':")
        for note in notes:
            print(self._format_note_with_frame(note))

        while True:
            confirmation = (
                input("Press Enter to delete the note or X to cancel: ").strip().lower()
            )
            if confirmation == "x":
                return "Note deletion canceled."
            elif confirmation == "":
                self.notes = [note for note in self.notes if note not in notes]
                return f"{len(notes)} note(s) deleted."

    def remove_all(self):
        """
        Remove all notes from the notebook.

        Returns:
            str: Message indicating whether the notes were removed or not.
        """
        if not self.notes:
            return "No notes available to delete."

        print(f"Found {len(self.notes)} note(s):")
        for note in self.notes:
            print(self._format_note_with_frame(note))

        while True:
            confirmation = (
                input("Press Enter to delete all notes or X to cancel: ")
                .strip()
                .lower()
            )
            if confirmation == "x":
                return "Note deletion canceled."
            elif confirmation == "":
                self.notes = []
                return "All notes deleted."

    def update(self, title, new_note):
        """
        Update a note with a new note data.

        Args:
            title (str): The title of the note to update.
            new_note (Note): The new note data.

        Returns:
            str: Message indicating whether the note was updated or not.
        """
        notes = self.search(title)
        if not notes:
            return "Note not found."

        current_note = notes[0]
        print(f"Current note:\n{self._format_note_with_frame(current_note)}")
        print(f"New note:\n{self._format_note_with_frame(new_note)}")

        while True:
            confirmation = (
                input("Press Enter to save the changes or X to cancel: ")
                .strip()
                .lower()
            )
            if confirmation == "x":
                return "Note update canceled."
            elif confirmation == "":
                current_note.title = new_note.title
                current_note.content = new_note.content
                current_note.tags = new_note.tags
                current_note.due_date = new_note.due_date
                return "Note updated."

    def filter_by_tag(self, tag):
        """
        Filter notes by tag.

        Args:
            tag (str): The tag to filter by.

        Returns:
            list: List of notes with the specified tag.
        """
        result = []
        for note in self.notes:
            if tag in note.tags:
                result.append(note)
        return result

    def notes_due_in_days(self, days):
        """
        Get notes that are due in the next specified number of days.

        Args:
            days (int): The number of days to look ahead for due notes.

        Returns:
            list: List of notes that are due in the next specified number of days.
        """
        result = []
        target_date = datetime.now() + timedelta(days=days)
        for note in self.notes:
            if note.due_date and note.due_date <= target_date:
                result.append(note)
        return result

    def to_dict(self):
        """
        Convert the Notebook instance to a dictionary.

        Returns:
            dict: Dictionary representation of the Notebook instance.
        """
        result = {"notes": []}
        for note in self.notes:
            result["notes"].append(note.to_dict())
        return result

    @staticmethod
    def from_dict(data):
        """
        Create a Notebook instance from a dictionary.

        Args:
            data (dict): Dictionary containing notebook data.

        Returns:
            Notebook: A Notebook instance created from the dictionary data.
        """
        notebook = Notebook()
        for note_data in data.get("notes", []):
            notebook.notes.append(Note.from_dict(note_data))
        return notebook

    def save_to_file(self, filepath):
        """
        Save the Notebook instance to a file.

        Args:
            filepath (str): The path to the file where the notebook data will be saved.
        """
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_from_file(filepath):
        """
        Load a Notebook instance from a file.

        Args:
            filepath (str): The path to the file from which the notebook data will be loaded.

        Returns:
            Notebook: A Notebook instance loaded from the file.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    data = {"notes": data}
                return Notebook.from_dict(data)
        except FileNotFoundError:
            return Notebook()

    def print_all_notes(self):
        """
        Get a string representation of all notes in the notebook.

        Returns:
            str: String representation of all notes in the notebook.
        """
        if not self.notes:
            return "No notes available."
        result = "\n"
        for note in self.notes:
            result += self._format_note_with_frame(note) + "\n\n"
        return result.strip()

    def format_notes_with_frame(self, notes):
        """
        Format a list of notes with a decorative frame.

        Args:
            notes (list): List of notes to format.

        Returns:
            str: Formatted string with all notes within frames.
        """
        if not notes:
            return "No notes found."
        result = "\n"
        for note in notes:
            result += self._format_note_with_frame(note) + "\n\n"
        return result.strip()

    def _format_note_with_frame(self, note):
        """
        Format a note with a decorative frame.

        Args:
            note (Note): The note to format.

        Returns:
            str: String representation of the note with a decorative frame.
        """
        lines = str(note).split("\n")
        width = max(len(line) for line in lines)
        frame = ["╔" + "═" * (width + 2) + "╗"]
        frame += ["║ " + line.ljust(width) + " ║" for line in lines]
        frame += ["╚" + "═" * (width + 2) + "╝"]
        return "\n".join(frame)

    def __str__(self):
        """
        Get the string representation of the Notebook instance.

        Returns:
            str: String representation of the Notebook instance.
        """
        return self.print_all_notes()
