from __future__ import annotations

import fastenum


class ChatType(fastenum.Enum):
    """
    Enum representing a chat type.
    """

    PRIVATE = "private"
    """Represents a private chat."""
    GROUP = "group"
    """Represents a group chat."""
    SUPER_GROUP = "supergroup"
    """Represents a supergroup chat."""
    CHANNEL = "channel"
    """Represents a channel chat."""


class StickerType(fastenum.Enum):
    """
    Enum representing a sticker type.
    """

    REGULAR = "regular"
    """Represents a standard sticker."""
    MASK = "mask"
    """Represents a mask sticker."""
    CUSTOM_EMOJI = "custom_emoji"
    """Represents a custom emoji sticker."""


class MaskPositionPoint(fastenum.Enum):
    """
    Enum representing a mask position point.
    """

    FOREHEAD = "forehead"
    """Represents a mask position point on the forehead."""
    EYES = "eyes"
    """Represents a mask position point on the eyes."""
    MOUTH = "mouth"
    """Represents a mask position point on the mouth."""
    CHIN = "chin"
    """Represents a mask position point on the chin."""


class MessageOriginType(fastenum.Enum):
    """
    Enum representing a message origin type.
    """

    USER = "user"
    """Represents a message origin type of a user."""
    HIDDEN_USER = "hidden_user"
    """Represents a message origin type of a hidden user."""
    CHAT = "chat"
    """Represents a message origin type of a chat."""
    CHANNEL = "channel"
    """Represents a message origin type of a channel."""


class MessageEntityType(fastenum.Enum):
    """
    Type of the message entity.
    """

    MENTION = "mention"
    """A mention: `@username`."""
    HASHTAG = "hashtag"
    """A hashtag: `#hashtag`."""
    CASHTAG = "cashtag"
    """A cashtag: `$USD`."""
    BOT_COMMAND = "bot_command"
    """A bot command: `/start@jobs_bot`."""
    URL = "url"
    """A URL: `https://telegram.org`."""
    EMAIL = "email"
    """An email address: `do-not-reply@telegram.org`."""
    PHONE_NUMBER = "phone_number"
    """A phone number: `+1-212-555-0123`."""
    BOLD = "bold"
    """Bold Text"""
    ITALIC = "italic"
    """Italic Text"""
    UNDERLINE = "underline"
    """Underline Text"""
    STRIKETHROUGH = "strikethrough"
    """Strikethrough Text"""
    SPOILER = "spoiler"
    """Spoiler Text"""
    BLOCK_QUOTE = "blockquote"
    """Blockquote Text"""
    EXPANDABLE_BLOCK_QUOTE = "expandable_blockquote"
    """Expandable Blockquote Text"""
    CODE = "code"
    """Code Text"""
    PRE = "pre"
    """Pre Text"""
    TEXT_LINK = "text_link"
    """Text Link"""
    TEXT_MENTION = "text_mention"
    """Text Mention"""
    CUSTOM_EMOJI = "custom_emoji"
    """Custom Emoji"""


class PollType(fastenum.Enum):
    """
    Enum representing a poll type.
    """

    QUIZ = "quiz"
    """Represents a quiz poll."""
    POLL = "poll"
    """Represents a regular poll."""
