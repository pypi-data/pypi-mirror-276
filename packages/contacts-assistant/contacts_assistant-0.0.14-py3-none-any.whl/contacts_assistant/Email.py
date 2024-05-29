import re

from contacts_assistant.field import Field

class Email(Field):
    """
    A class to represent and validate an email.

    Attributes:
        value (str): The validated email.

    Methods:
        __init__(email): Initializes the Email with a validated email.
        validate_email(email): Validates the email format.
    """

    def __init__(self, email: str):
        """
        Initializes the Email instance by validating the provided email.

        Args:
            email (str): The email to be validated.

        Raises:
            ValueError: If the email format is invalid.
        """
        self.value = self.validate_email(email)

    def validate_email(self, email: str):
        """
        Validates the email format using a regular expression.

        Args:
            email (str): The email to be validated.

        Returns:
            str: The validated email.

        Raises:
            ValueError: If the email format is invalid.
        """
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

        return email
