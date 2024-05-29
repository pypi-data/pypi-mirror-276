"""
A module containing functions for formatting text with colors.

This module provides functions for formatting text with colors using the colorama library.

Functions:
    format_cmd(text: str) -> str: Formats command name with cyan color.
    format_param(text: str) -> str: Formats parameter name with yellow color.
    format_greeting(text: str) -> str: Formats greeting with green color.
    generate_input_invite() -> str: Generates input invite with green color.
"""

from colorama import Fore, Style


def format_cmd(text: str) -> str:
    """Formating command name"""
    return Fore.CYAN + text + Style.RESET_ALL


def format_param(text: str) -> str:
    """Formating parameter name"""
    return Fore.YELLOW + text + Style.RESET_ALL


def format_greeting(text: str) -> str:
    """Formating greeting"""
    return Fore.GREEN + text + Style.RESET_ALL


def generate_input_invite() -> str:
    """Generate input invite"""
    return Fore.GREEN + "\nEnter a command >>> " + Style.RESET_ALL
