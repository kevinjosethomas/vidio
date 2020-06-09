"""
user.py
user model for cleaner code
"""


class User:

    def __init__(self, **kwargs):
        """
        basic initialization of the user class
        """

        self.user_id = kwargs.get('user_id', None)
        self.money = kwargs.get('money', None)
        self.commands = kwargs.get('commands', None)

    def __str__(self):

        return str(self.user_id)

    def __repr__(self):

        return str(self.user_id)

    def __int__(self):

        return self.user_id
