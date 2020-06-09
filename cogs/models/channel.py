"""
channel.py
channel model for cleaner code
"""


class Channel:

    def __init__(self, **kwargs):
        """
        basic initialization of the channel class
        """

        self.channel_id = kwargs.get('channel_id', None)
        self.user_id = kwargs.get('user_id', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.subscribers = kwargs.get('subscribers', None)
        self.total_views = kwargs.get('total_views', None)
        self.category = kwargs.get('category', None)
        self.created_at = kwargs.get('created_at', None)

    def __str__(self):

        return self.name

    def __repr__(self):

        return self.name

    def __int__(self):

        return self.channel_id
