

class UnknownError(Exception):
    """Triggered when no other exception handles the error"""

    def __init__(self, reason: str = "Unknown Error!"):
        self.message = reason
        super().__init__(self.message)


class GuildError(Exception):
    """Triggered when the exception relates to guilds"""

    def __init__(self, reason: str = "Unknown Guild Error!"):
        self.message = reason
        super().__init__(self.message)
