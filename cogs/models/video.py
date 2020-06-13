"""
video.py
video model for cleaner code
"""


class Video:

    def __init__(self, **kwargs):
        """
        basic initialization of the video class
        """

        self.video_id = kwargs.get('video_id', None)
        self.channel_id = kwargs.get('channel_id', None)
        self.user_id = kwargs.get('user_id', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.status = kwargs.get('status', None)
        self.new_subscribers = kwargs.get('new_subscribers', None)
        self.new_money = kwargs.get('new_money', None)
        self.views = kwargs.get('views', None)
        self.likes = kwargs.get('likes', None)
        self.dislikes = kwargs.get('dislikes', None)
        self.subscriber_cap = kwargs.get('subscriber_cap', None)
        self.iteration = kwargs.get('iteration', None)
        self.last_updated = kwargs.get('last_updated', None)
        self.uploaded_at = kwargs.get('uploaded_at', None)

    def __str__(self):

        return self.name

    def __repr__(self):

        return self.name

    def __int__(self):

        return self.video_id
