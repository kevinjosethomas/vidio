
class UnknownError(Exception):
    """Triggered when no other exception handles the error"""

    def __init__(self, reason: str = "Unknown error!"):
        self.message = reason
        super().__init__(self.message)
