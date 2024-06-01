from __future__ import annotations

import msgspec
import typing

from .user import User, MyUser
from .chats import Chat
from .base import BaseMessageOrigin
from .subtype import (
    LinkPreviewOptions,
    TextQuote,
    Story,
    MessageEntity,
    Animation,
    Audio,
    Document,
    PhotoSize,
    Sticker,
    Video,
    VideoNote,
    Voice,
    Contact,
    Dice,
    Game,
    Poll,
    Venue,
    Location,
    MessageAutoDeleteTimerChanged,
    InaccessibleMessage
)


class MessageOriginUser(BaseMessageOrigin):
    """
    The message was originally sent by a known user.
    """

    sender_user: typing.Union[User, MyUser]
    """
    User that sent the message originally.
    """


class MessageOriginHiddenUser(BaseMessageOrigin):
    """
    The message was originally sent by a hidden user.
    """

    sender_user_name: str
    """
    Name of the user that sent the message originally.
    """


class MessageOriginChat(BaseMessageOrigin):
    """
    The message was originally sent on behalf of a chat to a group chat.
    """

    sender_chat: Chat
    """
    Chat that sent the message originally.
    """
    author_signature: typing.Optional[str]
    """
    For messages originally sent by an anonymous chat administrator, original message author signature.
    """


class MessageOriginChannel(BaseMessageOrigin):
    """
    The message was originally sent on behalf of a channel to a group chat.
    """

    chat: Chat
    """
    Channel that sent the message originally.
    """
    message_id: int
    """
    Unique message identifier inside the chat
    """
    author_signature: typing.Optional[str]
    """
    Signature of the original post author.
    """


class ExternalReplyInfo:
    """
    This object contains information about a message that is being replied to, which may come from another chat or forum topic.
    """

    origin: typing.Union[
        MessageOriginUser,
        MessageOriginHiddenUser,
        MessageOriginChat,
        MessageOriginChannel,
    ]
    """
    Origin of the message replied to by the given message.
    """
    chat: typing.Optional[Chat]
    """
    Chat the original message belongs to. Available only if the chat is a supergroup or a channel.
    """
    message_id: typing.Optional[int]
    """
    Unique message identifier inside the original chat. Available only if the original chat is a supergroup or a channel.
    """
    link_preview_options: typing.Optional[LinkPreviewOptions]


class Message(msgspec.Struct):
    """
    A telegram message.
    """

    message_id: int
    """
    Unique message identifier inside this chat
    """
    message_thread_id: typing.Optional[int]
    """
    Unique identifier of a message thread to which the message belongs; for supergroups only
    """
    sender_chat: typing.Optional[Chat]
    """
    Sender of the message, sent on behalf of a chat. For example, the channel itself for channel posts, the supergroup itself for messages from anonymous group administrators, the linked channel for messages automatically forwarded to the discussion group. For backward compatibility, the field from contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat.
    """
    sender_boost_count: typing.Optional[int]
    """
    If the sender of the message boosted the chat, the number of boosts added by the user.
    """
    sender_business_bot: typing.Optional[typing.Union[User, MyUser]]
    """
    The bot that actually sent the message on behalf of the business account. Available only for outgoing messages sent on behalf of the connected business account.
    """
    business_connection_id: int
    """
    Unique identifier of the business connection from which the message was received. If non-empty, the message belongs to a chat of the corresponding business account that is independent from any potential bot chat which might share the same identifier.
    """
    chat: Chat
    """
    Conversation the message belongs to.
    """
    forward_origin: typing.Optional[
        typing.Union[
            MessageOriginUser,
            MessageOriginHiddenUser,
            MessageOriginChat,
            MessageOriginChannel,
        ]
    ]
    """
    Information about the original message for forwarded messages.
    """
    is_topic_message: typing.Optional[bool]
    """
    True, if the message is sent to a forum topic.
    """
    is_automatic_forward: typing.Optional[bool]
    """
    True, if the message is a channel post that was automatically forwarded to the connected discussion group.
    """
    reply_to_message: typing.Optional[Message]
    """
    For replies in the same chat and message thread, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply.
    """
    external_reply: typing.Optional[ExternalReplyInfo]
    """
    Information about the message that is being replied to, which may come from another chat or forum topic.
    """
    quote: typing.Optional[TextQuote]
    """
    For replies that quote part of the original message, the quoted part of the message.
    """
    reply_to_story: typing.Optional[Story]
    """
    For replies to a story, the original story.
    """
    via_bot: typing.Optional[typing.Union[User, MyUser]]
    """
    Bot through which the message was sent.
    """
    edit_date: typing.Optional[int]
    """
    Date the message was last edited in Unix time.
    """
    has_protected_content: typing.Optional[bool]
    """
    True, if the message can't be forwarded.
    """
    is_from_offline: typing.Optional[bool]
    """
    True, if the message was sent by an implicit action, for example, as an away or a greeting business message, or as a scheduled message.
    """
    media_group_id: typing.Optional[str]
    """
    The unique identifier of a media message group this message belongs to.
    """
    author_signature: typing.Optional[str]
    """
    Signature of the post author for messages in channels, or the custom title of an anonymous group administrator.
    """
    text: typing.Optional[str]
    """
    For text messages, the actual UTF-8 text of the message.
    """
    entities: typing.Optional[typing.List[MessageEntity]]
    """
    For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.
    """
    link_preview_options: typing.Optional[LinkPreviewOptions]
    """
    Options used for link preview generation for the message, if it is a text message and link preview options were changed.
    """
    effect_id: typing.Optional[str]
    """
    Unique identifier of the message effect added to the message, if any.
    """
    animation: typing.Optional[Animation]
    """
    Original animation filename as defined by sender
    """
    audio: typing.Optional[Audio]
    """
    Original audio filename as defined by sender
    """
    document: typing.Optional[Document]
    """
    Message is a general file, information about the file.
    """
    photo: typing.Optional[typing.List[PhotoSize]]
    """
    Message is a photo, available sizes of the photo.
    """
    sticker: typing.Optional[Sticker]
    """
    Message is a sticker, information about the sticker.
    """
    story: typing.Optional[Story]
    """
    Message is a forwarded story.
    """
    video: typing.Optional[Video]
    """
    Message is a video, information about the video.
    """
    video_note: typing.Optional[VideoNote]
    """
    Message is a [video note](https://telegram.org/blog/video-messages-and-telescope), information about the video message
    """
    voice: typing.Optional[Voice]
    """
    Message is a voice message, information about the file
    """
    caption: typing.Optional[str]
    """
    Caption for the animation, audio, document, photo, video or voice
    """
    caption_entities: typing.Optional[typing.List[MessageEntity]]
    """
    For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption
    """
    show_caption_above_media: typing.Optional[bool]
    """
    True, if the caption must be shown above the message media
    """
    has_media_spoiler: typing.Optional[bool]
    """
    True, if the message media is covered by a spoiler animation
    """
    contact: typing.Optional[Contact]
    """
    Message is a shared contact, information about the contact
    """
    dice: typing.Optional[Dice]
    """
    Message is a dice with random value
    """
    game: typing.Optional[Game]
    """
    Message is a game, information about the game. [More about games »](https://core.telegram.org/bots/api#games)
    """
    poll: typing.Optional[Poll]
    """
    Message is a native poll, information about the poll
    """
    venue: typing.Optional[Venue]
    """
    Message is a venue, information about the venue. For backward compatibility, when this field is set, the location field will also be set.
    """
    location: typing.Optional[Location]
    """
    Message is a shared location, information about the location
    """
    new_chat_members: typing.Optional[typing.List[typing.Union[User, MyUser]]]
    """
    New members that were added to the group or supergroup and information about them (the bot itself may be one of these members)
    """
    left_chat_member: typing.Optional[typing.Union[User, MyUser]]
    """
    A member was removed from the group, information about them (this member may be the bot itself)
    """
    new_chat_title: typing.Optional[str]
    """
    A chat title was changed to this value
    """
    new_chat_photo: typing.Optional[typing.List[PhotoSize]]
    """
    A chat photo was change to this value
    """
    deleted_chat_photo: typing.Optional[bool]
    """
    Service message: the chat photo was deleted
    """
    group_chat_created: typing.Optional[bool]
    """
    Service message: the group has been created
    """
    supergroup_chat_created: typing.Optional[bool]
    """
    Service message: the supergroup has been created. This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created. It can only be found in `reply_to_message` if someone replies to a very first message in a directly created supergroup.
    """
    channel_chat_created: typing.Optional[bool]
    """
    Service message: the channel has been created. This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created. It can only be found in `reply_to_message` if someone replies to a very first message in a channel.
    """
    message_auto_delete_timer_changed: typing.Optional[MessageAutoDeleteTimerChanged]
    """
    Service message: auto-delete timer settings changed in the chat.
    """
    migrate_from_chat_id: typing.Optional[int]
    """
    The supergroup has been migrated from a group with the specified identifier. 
    """
    pinned_message: typing.Optional[typing.Union[Message, InaccessibleMessage]]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    from_user: typing.Optional[typing.Union[User, MyUser]] = msgspec.field(
        name="from", default=None
    )
    """
    Sender of the message; empty for messages sent to channels. For backward compatibility, the field contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat.
    """
