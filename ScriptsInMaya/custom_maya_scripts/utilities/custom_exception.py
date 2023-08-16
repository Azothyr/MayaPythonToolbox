"""
This module defines a custom exception class for handling specific error cases.
"""


class CustomException(Exception):
    """Used to modify how an exception is handled."""

    def __init__(self, error=None):
        self.error = error
        if self.error:
            print(self.error)
