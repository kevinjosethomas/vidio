class Channel:
    """Stores instance of a vidio channel"""

    def __init__(**kwargs):
        """Initializes Channel object"""

        self.channel_id = kwargs.get("channel_id")
        self.banner = kwargs.get("banner")
        self.name = kwargs.get("name")
        self.vanity = kwargs.get("vanity")
        self.description = kwargs.get("description")
        self.awards = kwargs.get("awards", [])
        self.subscribers = kwargs.get("subscribers", 0)
        self.balance = kwargs.get("balance", 0)
        self.views = kwargs.get("views", 0)
        self.genre = kwargs.get("genre")
        self.created_at = kwargs.get("created_at")
