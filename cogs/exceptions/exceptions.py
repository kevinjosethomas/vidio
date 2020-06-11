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


class InvalidChannel(Exception):

    def __init__(self, cause: str = "channel_id or user_id"):
        """basic initialization of the InvalidChannel exception"""

        self.message = f"Invalid {cause} was provided"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NotEnoughMoney(Exception):

    def __init__(self):
        """basic initialization of the NotEnoughMoney exception"""

        self.message = "Provided user doesn't have enough money"
        super().__init__(self.message)

    def __str__(self):
        return self.message
