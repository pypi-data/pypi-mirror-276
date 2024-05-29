"""
This module provides helper functions for date manipulation,
including formatting workdays and calculating the next birthday.
"""

from datetime import date as dt_date
from datetime import timedelta

from contacts_assistant.constants import DATE_FORMAT


class DateHelper:
    """
    A helper class for date-related operations.
    """

    @staticmethod
    def get_formated_workday(date: dt_date):
        """
        Returns the formatted workday for the given date.
        If the date falls on a weekend, it returns the next Monday.

        Args:
            date (date): The date to be checked.

        Returns:
            str: The formatted workday in standard format.
        """
        if date.weekday() >= 5:
            return (date + timedelta(7 - date.weekday())).strftime(DATE_FORMAT)
        return date.strftime(DATE_FORMAT)

    @staticmethod
    def _is_leap(year):
        "year -> true if leap year, else false."
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def get_next_birthday(birthday: dt_date, fromdate: dt_date):
        """
        Calculates the next birthday from a given date.

        Args:
            birthday (date): The date of birth.
            fromdate (date): The date from which to calculate the next birthday.

        Returns:
            date: The next birthday date.
        """
        if (
            DateHelper._is_leap(birthday.year)
            and not DateHelper._is_leap(fromdate.year)
            and (birthday.day == 29)
            and (birthday.month == 2)
        ):
            birthday_this_year = dt_date(fromdate.year, 3, 1)
        else:
            birthday_this_year = dt_date(fromdate.year, birthday.month, birthday.day)
        if birthday_this_year < fromdate:
            return DateHelper.get_next_birthday(
                birthday, dt_date(fromdate.year + 1, 1, 1)
            )
        return birthday_this_year
