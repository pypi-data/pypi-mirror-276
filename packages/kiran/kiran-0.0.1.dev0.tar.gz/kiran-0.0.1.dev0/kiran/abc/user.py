from __future__ import annotations

import typing
from .base import BaseUser


class User(BaseUser):
    """
    An instance representing a user or a telegram bot with minimilistic details.
    """

    last_name: typing.Optional[str]
    """
    User's or bot's last name
    """
    username: typing.Optional[str]
    """
    User's or bot's username
    """
    language_code: typing.Optional[str]
    """
    IETF language tag of the user's language
    """
    is_premium: bool
    """
    True, if this user is a Telegram Premium user
    """


class MyUser(User):
    """
    A Telegram user or bot that represents your state instance.
    """

    can_join_groups: bool
    """
    True, if the bot can be invited to groups
    """
    can_join_groups: bool
    """
    True, if privacy mode is disabled for the bot
    """
    can_read_all_group_messages: bool
    """
    True, if the bot can read all messages in channels
    """
    supports_inline_queries: bool
    """
    True, if the bot supports inline queries
    """
    can_connect_to_business: bool
    """
    True, if the bot can be connected to a Telegram Business account to receive its messages.
    """
