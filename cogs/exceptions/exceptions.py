"""
file containing all custom errors needed for the bot
"""


class UnknownError(Exception):

    def __init__(self, reason: str = "Unkown reason!"):
        """basic initialization of UnknownError exception"""

        self.message = reason
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidUser(Exception):

    def __init__(self):
        """basic initialization of the InvalidUser exception"""

        self.message = "Invalid user_id was provided"
        super().__init__(self.message)

    def __str__(self):
        return self.message

