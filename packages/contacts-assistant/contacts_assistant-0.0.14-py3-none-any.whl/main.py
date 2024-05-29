"""Main App"""

import shlex
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory

from contacts_assistant.constants import INPUT_STYLE
from contacts_assistant.handler import Handler
from contacts_assistant.menu import Menu

handler = Handler()


def handle_user_input(user_input, parser):
    """
    Process the user input.

    Args:
        user_input (str): The input string from the user.
        parser (argparse.ArgumentParser): The argument parser.

    Returns:
        tuple: The command and a list of arguments.
    """
    user_command, *args = user_input.split(maxsplit=1)
    command = Menu.get_by_name(user_command)
    if command:
        if command in (Menu.EXIT, Menu.CLOSE):
            return command, None

        args = None
        try:
            args = parser.parse_args(shlex.split(user_input))
        except (
            argparse.ArgumentError,
            argparse.ArgumentTypeError,
            ValueError,
            SystemExit,
        ) as error:
            print(error)

        return command, args
    else:
        print("Invalid command.")
        suggestions = Menu.suggest_similar_commands(user_command)
        if suggestions:
            print(
                f"Command '{user_command}' not found. Did you mean: {', '.join(suggestions)}?"
            )
        else:
            print(f"Command '{user_command}' not found.")
        return None, None


def main():
    """
    Main function to run the assistant bot.

    Continuously prompts the user for commands and executes the appropriate function.
    """
    print(handler.greeting())
    parser = Menu.create_parser()
    history = InMemoryHistory()

    while True:
        style = Style.from_dict(INPUT_STYLE)

        user_input = prompt(
            "Enter a command >>> ",
            completer=handler.completer,
            style=style,
            history=history,
        )

        command, args = handle_user_input(user_input, parser)
        if command:
            print(handler.execute(command, args))
            if command in (Menu.EXIT, Menu.CLOSE):
                break

if __name__ == "__main__":
    main()
