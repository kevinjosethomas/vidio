"""
file containing all custom errors needed for the bot
"""


class UnknownError(Exception):
    """
    triggered when no other exception covers the error
    """

    def __init__(self, reason: str = "Unkown reason!"):
        """basic initialization of UnknownError exception"""

        self.message = reason
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidUser(Exception):
    """
    triggered when a user is not in the database
    """

    def __init__(self):
        """basic initialization of the InvalidUser exception"""

        self.message = "Invalid user_id was provided"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidChannel(Exception):
    """
    triggered when a channel is not in the database
    """

    def __init__(self, cause: str = "channel_id or user_id"):
        """basic initialization of the InvalidChannel exception"""

        self.message = f"Invalid {cause} was provided"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NotEnoughMoneyError(Exception):
    """
    triggered when a user initiates an action which they don't have enough money for
    """

    def __init__(self):
        """basic initialization of the NotEnoughMoneyError exception"""

        self.message = "Provided user doesn't have enough money"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ChannelLimitError(Exception):
    """
    triggered when a user already has 3 channels under their name
    """

    def __init__(self):
        """basic initialization of the ChannelLimitError exception"""

        self.message = "Provided user already has 3 channels"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidInputError(Exception):
    """
    triggered when provided input is too long or has invalid characters
    """

    def __init__(self, cause=""):
        """basic initalization of the InvalidInputError exception"""

        self.message = f"Provided input is invalid{' ({cause})' if cause else ''}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
