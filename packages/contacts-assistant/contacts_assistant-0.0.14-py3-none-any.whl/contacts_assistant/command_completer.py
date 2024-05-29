"""
A module containing the CommandCompleter class for providing command-line command and parameter completions.

Classes:
    CommandCompleter: A custom completer for command-line commands and parameters.
"""

from prompt_toolkit.completion import Completer, Completion


class CommandCompleter(Completer):
    """
    A custom completer for command-line commands and parameters.

    This completer provides suggestions for commands and parameters based on
    the available command arguments.

    Attributes:
        command_args (dict): A dictionary containing command names as keys and
            lists of corresponding parameters as values.
        book: A book object, representing the book data for suggestions.

    Methods:
        __init__(command_args, book): Initializes the CommandCompleter instance.
        get_completions(document, complete_event): Generates completions based
            on the current command input.
    """

    def __init__(self, command_args, book):
        """
        Initialize the CommandCompleter instance.

        Args:
            command_args (dict): A dictionary containing command names as keys and
                lists of corresponding parameters as values.
            book: A book object, representing the book data for suggestions.
        """
        super().__init__()
        self.command_args = command_args
        self.book = book

    def get_completions(self, document, complete_event):
        """
        Generate completions based on the current command input.

        Args:
            document: The current input text.
            complete_event: The completion event.

        Yields:
            Completion: A completion object representing a suggested completion.
        """
        text_before_cursor = document.text_before_cursor
        tokens = text_before_cursor.split()
        if len(tokens) == 0:
            return

        # If the user is typing the command
        if len(tokens) == 1:
            word_before_cursor = tokens[0]
            for command in self.command_args:
                if command.startswith(word_before_cursor):
                    yield Completion(command, start_position=-len(word_before_cursor))
        else:
            # User has entered a command and is now typing parameters
            command = tokens[0]
            if command in self.command_args:
                param_prefix = tokens[-1]
                for param in self.command_args[command]:
                    if param.startswith(param_prefix) and param not in tokens:
                        yield Completion(param, start_position=-len(param_prefix))
