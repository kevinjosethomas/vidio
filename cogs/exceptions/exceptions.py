"""
file containing all custom errors needed for the bot
"""


class UnknownError(Exception):

    def __init__(self, reason: str = "Unkown reason!"):
        """basic initializatin of UnknownError exception"""

        self.message = reason
        super().__init__(self.message)

    def __str__(self):

        return self.message




