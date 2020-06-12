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

        self.message = f"Provided input is invalid{f' ({cause})' if cause else ''}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class DuplicateChannelNameError(Exception):
    """
    triggered when a channel with the same name and same owner is created
    """

    def __init__(self):
        """basic initialization of the DuplicateChannelError exception"""

        self.message = "The owner has a channel with the same name"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class AlreadyBotBanned(Exception):
    """
    triggered when a banned user is banned again
    """

    def __init__(self):
        """basic initialization of the AlreadyBotBanned exception"""

        self.message = f"This user is already botbanned"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NotBotBanned(Exception):
    """
    triggered when a unbanned user is unbanned
    """

    def __init__(self):
        """basic initialization of the NotBotBanned exception"""

        self.message = f"This user is not botbanned"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class AlreadySubscribedError(Exception):
    """
    triggered when a user tries to subscribe to someone they are already subscribed to
    """

    def __init__(self):
        """basic initialization of the AlreadySubscribed exception"""

        self.message = f"User is already subscribed to this channel"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SelfSubscribeError(Exception):
    """
    triggered when a user tries to subscribe to themselves
    """

    def __init__(self):
        """basic initialization of the SelfSubscribeError exception"""

        self.message = f"User cannot subscribe to themselves"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SubscriptionDoesntExist(Exception):
    """
    triggered when a user unsubscribes from a channel which they are not subscribed to
    """

    def __init__(self):
        """basic initialization of the SubscriptionDoesntExist exception"""

        self.message = "User attempted to unsubscribe from non-existent subscription"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class PrefixTooLongError(Exception):
    """
    triggered when an administrator tries to set a guild prefix which is longer than the character limit
    """

    def __init__(self):
        """basic initialization of the PrefixTooLongError"""

        self.message = "User attempted to set a prefix longer than the character limit"
        super().__init__(self.message)

    def __str__(self):
        return self.message
