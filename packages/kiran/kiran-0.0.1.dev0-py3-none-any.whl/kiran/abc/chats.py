from __future__ import annotations

import typing
from .base import BaseChat
from .subtype import (
    ChatPhoto,
    BirthDate,
    BusinessIntro,
    BusinessLocation,
    BusinessOpeningHours,
    ReactionTypeCustomEmoji,
    ReactionTypeEmoji,
)
from .message import Message


class Chat(BaseChat):
    """
    A instance representing a chat.
    """

    title: typing.Optional[str]
    """
    Title, for supergroups, channels and group chats
    """
    username: typing.Optional[str]
    """
    Username, for private chats supergroups and channels if available
    """
    first_name: typing.Optional[str]
    """
    First name of the other party in a private chat
    """
    last_name: typing.Optional[str]
    """
    Last name of the other party in a private chat
    """
    is_forum: bool
    """
    True, if the supergroup is a forum has
    """


class ChatInfo(Chat):
    """
    A instance representing a grouped information of a chat.
    """

    accent_color_id: typing.Optional[int]
    """
    Identifier of the accent color for the chat name and backgrounds of the chat photo, reply header, and link preview.
    """
    max_reaction_count: typing.Optional[int]
    """
    Maximum number of messages of the specified type in the chat
    """
    photo: typing.Optional[ChatPhoto]
    """
    Chat photo, if any.
    """
    active_usernames: typing.Optional[typing.List[str]]
    """
    If non-empty, the list of [all active chat usernames;](https://telegram.org/blog/topics-in-groups-collectible-usernames#collectible-usernames) for private chats, supergroups and channels
    """
    birthdate: typing.Optional[BirthDate]
    """
    For private chats, the date of birth of the user.
    """
    business_intro: typing.Optional[BusinessIntro]
    """
    For private chats with business accounts, the intro of the business
    """
    business_location: typing.Optional[BusinessLocation]
    """
    For private chats with business accounts, the location of the business
    """
    business_opening_hours: typing.Optional[BusinessOpeningHours]
    """
    For private chats with business accounts, the opening hours of the business
    """
    personal_chat: typing.Optional[Chat]
    """
    For private chats, the personal channel of the user
    """
    available_reactions: typing.Optional[
        typing.List[typing.Union[ReactionTypeCustomEmoji, ReactionTypeEmoji]]
    ]
    """
    List of available reactions allowed in the chat. If omitted, then all [emoji reactions](https://core.telegram.org/bots/api#reactiontypeemoji) are allowed.
    """
    background_custom_emoji_id: typing.Optional[str]
    """
    Custom emoji identifier of the emoji chosen by the chat for the reply header and link preview background
    """
    profile_accent_color_id: typing.Optional[int]
    """
    Identifier of the accent color for the chat's profile background. See [profile accent colors](https://core.telegram.org/bots/api#profile-accent-colors) for more details.
    """
    profile_background_custom_emoji_id: typing.Optional[str]
    """
    Custom emoji identifier of the emoji chosen by the chat for its profile background.
    """
    emoji_status_custom_emoji_id: typing.Optional[str]
    """
    Custom emoji identifier of the emoji status of the chat or the other party in a private chat.
    """
    emoji_status_expiration_date: typing.Optional[int]
    """
    Expiration date of the emoji status of the chat or the other party in a private chat, in Unix time, if any.
    """
    bio: typing.Optional[str]
    """
    Bio of the other party in a private chat.
    """
    has_private_forwards: typing.Optional[bool]
    """
    True, if privacy settings of the other party in the private chat allows to use `tg://user?id=<user_id>` links only in chats with the user.
    """
    has_restricted_voice_and_video_messages: typing.Optional[bool]
    """
    True, if the privacy settings of the other party restrict sending voice and video note messages in the private chat.
    """
    join_to_send_messages: typing.Optional[bool]
    """
    True, if users need to join the supergroup before they can send messages.
    """
    join_by_request: typing.Optional[bool]
    """
    True, if all users directly joining the supergroup without using an invite link need to be approved by supergroup administrators.
    """
    description: typing.Optional[str]
    """
    Description, for groups, supergroups and channel chats.
    """
    invite_link: typing.Optional[str]
    """
    Primary invite link, for groups, supergroups and channel chats
    """
    pinned_message: typing.Optional[Message]
