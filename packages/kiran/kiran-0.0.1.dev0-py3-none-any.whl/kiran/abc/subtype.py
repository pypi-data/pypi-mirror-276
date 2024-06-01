from __future__ import annotations

import msgspec
import typing
from .enums import StickerType, MaskPositionPoint, MessageEntityType, PollType
from .user import User, MyUser
from .chats import Chat


class Location(msgspec.Struct):
    latitude: float
    """
    Latitude as defined by sender.
    """
    longitude: float
    """
    Longitude as defined by sender.
    """
    horizontal_accuracy: typing.Optional[float]
    """
    The radius of uncertainty for the location, measured in meters; 0-1500.
    """
    live_period: typing.Optional[int]
    """
    Period in seconds for which the location can be updated, should be between 60 and 86400.
    """
    heading: typing.Optional[int]
    """
    Direction in which user is moving, in degrees; must be between 1 and 360 if specified.
    """
    proximity_alert_radius: typing.Optional[int]
    """
    The maximum distance for proximity alerts about approaching another chat member, in meters. For sent live locations only.
    """


class MaskPosition(msgspec.Struct):
    """
    Describes the position on faces where a mask should be placed by default.
    """

    point: MaskPositionPoint
    """
    The part of the face relative to which the mask should be placed. One of `forehead`, `eyes`, `mouth`, or `chin`.
    """
    x_shift: float
    """
    Shift by X-axis measured in widths of the mask scaled to the face size, from left to right. For example, choosing -1.0 will place mask just to the left of the default mask position.
    """
    y_shift: float
    """
    Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom. For example, 1.0 will place the mask just below the default mask position.
    """
    scale: float
    """
    Mask scaling coefficient. For example, 2.0 means double size.
    """


class File(msgspec.Struct):
    """
    This object represents a file ready to be downloaded. The file can be downloaded via the link `https://api.telegram.org/file/bot<token>/<file_path>`. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling [getFile](https://core.telegram.org/bots/api#getfile).
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    file_size: typing.Optional[int]
    """
    File size in bytes.
    """
    file_path: typing.Optional[str]
    """
    File path. Use `https://api.telegram.org/file/bot<token>/<file_path>` to get the file.
    """


class PhotoSize(msgspec.Struct):
    """
    A class representing the photo size.
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    width: int
    """
    Photo width
    """
    height: int
    """
    Photo height
    """
    file_size: typing.Optional[int]
    """
    File size in bytes.
    """


class ChatPhoto(msgspec.Struct):
    """
    A class representing the chat photo.
    """

    small_file_id: str
    """
    File identifier of small `(160x160)` chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
    """
    small_file_unique_id: str
    """
    Unique file identifier of small `(160x160)` chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    big_file_id: str
    """
    File identifier of big `(640x640)` chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
    """
    big_file_unique_id: str
    """
    Unique file identifier of big `(640x640)` chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """


class BirthDate(msgspec.Struct):
    """
    Describes the birthdate of a user.
    """

    day: int
    """
    Day of birth, from 1 to 31.
    """
    month: int
    """
    Month of birth, from 1 to 12.
    """
    year: int
    """
    Year of birth, from 1 to 9999.
    """


class Sticker(msgspec.Struct):
    """
    Represents a telegram sticker.
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    type: StickerType
    """
    Type of the sticker, currently one of `regular`, `mask`, `custom_emoji`. The type of the sticker is independent from its format, which is determined by the fields is_animated and is_video.
    """
    width: int
    """
    Sticker width
    """
    height: int
    """
    Sticker height
    """
    is_animated: bool
    """
    True, if the sticker is animated
    """
    is_video: bool
    """
    True, if the sticker is a video sticker
    """
    thumbnail: typing.Optional[PhotoSize]
    """
    Sticker thumbnail in the .WEBP or .JPG format
    """
    emoji: typing.Optional[str]
    """
    Emoji associated with the sticker
    """
    set_name: typing.Optional[str]
    """
    Name of the sticker set to which the sticker belongs
    """
    premium_animation: typing.Optional[File]
    """
    For premium regular stickers, premium animation for the sticker
    """
    mask_position: typing.Optional[MaskPosition]
    """
    For mask stickers, the position where the mask should be placed
    """
    custom_emoji_id: typing.Optional[str]
    """
    For custom emoji stickers, unique identifier of the custom emoji
    """
    needs_repainting: typing.Optional[bool]
    """
    True, if the sticker must be repainted to a text color
    """
    file_size: typing.Optional[int]
    """
    File size in bytes
    """


class BusinessIntro(msgspec.Struct):
    """
    Contains information about the start page settings of a Telegram Business account.
    """

    title: typing.Optional[str]
    """
    Title text of the business intro
    """
    message: typing.Optional[str]
    """
    Message text of the business intro
    """
    sticker: typing.Optional[Sticker]
    """
    Sticker of the business intro
    """


class BusinessLocation(msgspec.Struct):
    """
    Contains information about the location of a Telegram Business account.
    """

    address: str
    """
    Address of the business.
    """
    location: typing.Optional[Location]
    """
    Location of the business.
    """


class BusinessOpeningHoursInterval(msgspec.Struct):
    """
    Describes an interval of time during which a business is open.
    """

    opening_minute: int
    """
    The minute's sequence number in a week, starting on Monday, marking the start of the time interval during which the business is open; 0 - 7 * 24 * 60
    """
    closing_minute: int
    """
    The minute's sequence number in a week, starting on Monday, marking the end of the time interval during which the business is open; 0 - 8 * 24 * 60
    """


class BusinessOpeningHours(msgspec.Struct):
    """
    Contains information about the opening hours of a Telegram Business account.
    """

    time_zone_name: typing.List[str]
    """
    Unique name of the time zone for which the opening hours are defined
    """
    opening_hours: typing.Optional[typing.List[BusinessOpeningHoursInterval]]


class ReactionTypeEmoji(msgspec.Struct):
    """
    The reaction is based on an emoji.
    """

    type: str
    """
    The type of the emoji. Always "emoji"
    """
    emoji: str
    """
    Reaction emoji. Currently, it can be one of "👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂", "🤷", "🤷‍♀", "😡"
    """


class ReactionTypeCustomEmoji(msgspec.Struct):
    """
    The reaction is based on a custom emoji.
    """

    type: str
    """
    The type of the emoji. Always "custom_emoji"
    """
    custom_emoji_id: str
    """
    Custom emoji identifier
    """


class LinkPreviewOptions(msgspec.Struct):
    """
    Describes the options used for link preview generation.

    ---
    Reference: [telegram.LinkPreviewOptions](https://core.telegram.org/bots/api#linkpreviewoptions)
    """

    is_disabled: typing.Optional[bool]
    """
    True, if the link preview is disabled
    """
    url: typing.Optional[str]
    """
    URL to use for the link preview. If empty, then the first URL found in the message text will be used.
    """
    prefer_small_media: typing.Optional[bool]
    """
    True, if the media in the link preview is supposed to be shrunk; ignored if the URL isn't explicitly specified or media size change isn't supported for the preview.
    """
    prefer_large_media: typing.Optional[bool]
    """
    True, if the media in the link preview is supposed to be enlarged; ignored if the URL isn't explicitly specified or media size change isn't supported for the preview.
    """
    show_above_text: typing.Optional[bool]
    """
    True, if the link preview must be shown above the message text; otherwise, the link preview will be shown below the message text.
    """


class MessageEntity(msgspec.Struct):
    """
    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
    """

    type: MessageEntityType
    """
    The entity type
    """
    offset: int
    """
    Offset in [UTF-16 code units](https://core.telegram.org/api/entities#entity-length) to the start of the entity
    """
    length: int
    """
    Length of the entity in [UTF-16 code units](https://core.telegram.org/api/entities#entity-length)
    """
    url: typing.Optional[str]
    """
    Optional. For `text_link` only, URL that will be opened after user taps on the text
    """
    user: typing.Optional[typing.Union[User, MyUser]]
    """
    For “text_mention” only, the mentioned user
    """
    language: typing.Optional[str]
    """
    For “pre” only, the programming language of the entity
    """
    custom_emoji_id: typing.Optional[str]
    """
    For `custom_emoji` only, unique identifier of the custom emoji.
    """


class TextQuote(msgspec.Struct):
    text: str
    """
    Text of the quoted part of a message that is replied to by the given message.
    """
    entities: typing.Optional[typing.List[MessageEntity]]
    """ Special entities that appear in the quote. Currently, only bold, italic, underline, strikethrough, spoiler, and custom_emoji entities are kept in quotes. """
    position: int
    """
    Approximate quote position in the original message in UTF-16 code units as specified by the sender
    """
    is_manual: bool
    """
    True, if the quote was chosen manually by the message sender. Otherwise, the quote was added automatically by the server.
    """


class Story(msgspec.Struct):
    """
    Represents a telegram story
    """

    chat: Chat
    """
    Chat that posted the story
    """
    id: int
    """
    Unique identifier of the story
    """


class Animation(msgspec.Struct):
    """
    This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound).
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    width: int
    """
    Video width as defined by sender
    """
    height: int
    """
    Video height as defined by sender
    """
    duration: int
    """
    Duration of the video in seconds as defined by sender
    """
    thumbnail: typing.Optional[PhotoSize]
    """
    Animation thumbnail as defined by sender.
    """
    file_name: typing.Optional[str]
    """
    Original animation filename as defined by sender
    """
    mime_type: typing.Optional[str]
    """
    MIME type of the file as defined by sender
    """
    file_size: typing.Optional[int]
    """
    File size in bytes.
    """


class Audio(msgspec.Struct):
    """
    This object represents an audio file to be treated as music by the Telegram clients.
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    duration: int
    """
    Duration of the audio in seconds as defined by sender
    """
    performer: typing.Optional[str]
    """
    Performer of the audio as defined by sender or by audio tags
    """
    title: typing.Optional[str]
    """
    Title of the audio as defined by sender or by audio tags
    """
    file_name: typing.Optional[str]
    """
    Original filename as defined by sender
    """
    mime_type: typing.Optional[str]
    """
    MIME type of the file as defined by sender
    """
    file_size: typing.Optional[int]
    """
    File size in bytes
    """
    thumbnail: typing.Optional[PhotoSize]
    """
    Thumbnail of the album cover to which the music file belongs
    """


class Document(msgspec.Struct):
    """
    A general file (as opposed to photos, voice messages and audio files).
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    thumbnail: typing.Optional[PhotoSize]
    """
    Document thumbnail as defined by sender
    """
    file_name: typing.Optional[str]
    """
    Original filename as defined by sender
    """
    mime_type: typing.Optional[str]
    """
    MIME type of the file as defined by sender
    """
    file_size: typing.Optional[int]
    """
    File size in bytes
    """


class Video(msgspec.Struct):
    """
    This object represents a video file.
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    width: int
    """
    Video width as defined by sender
    """
    height: int
    """
    Video height as defined by sender
    """
    duration: int
    """
    Duration of the video in seconds as defined by sender
    """
    thumbnail: typing.Optional[PhotoSize]
    """
    Video thumbnail
    """
    file_name: typing.Optional[str]
    """
    Original filename as defined by sender
    """
    mime_type: typing.Optional[str]
    """
    MIME type of the file as defined by sender
    """
    file_size: typing.Optional[int]
    """
    File size in bytes
    """


class VideoNote(msgspec.Struct):
    """
    This object represents a [video message](https://telegram.org/blog/video-messages-and-telescope) (available in Telegram apps as of [v.4.0](https://telegram.org/blog/video-messages-and-telescope)).
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    length: int
    """
    Video width and height (diameter of the video message) as defined by sender
    """
    duration: int
    """
    Duration of the video in seconds as defined by sender
    """
    thumbnail: typing.Optional[PhotoSize]
    """
    Video thumbnail
    """
    file_size: typing.Optional[int]
    """
    File size in bytes
    """


class Voice(msgspec.Struct):
    """
    This object represents a voice note.
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file
    """
    file_unique_id: str
    """
    Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    """
    duration: int
    """
    Duration of the audio in seconds as defined by sender
    """
    mime_type: typing.Optional[str]
    """
    MIME type of the file as defined by sender
    """
    file_size: typing.Optional[int]
    """
    File size in bytes
    """


class Contact(msgspec.Struct):
    """
    This object represents a phone contact.
    """

    phone_number: str
    """
    Contact's phone number
    """
    first_name: str
    """
    Contact's first name
    """
    last_name: typing.Optional[str]
    """
    Contact's last name
    """
    user_id: typing.Optional[int]
    """
    Contact's user identifier in Telegram
    """
    vcard: typing.Optional[str]
    """
    Additional data about the contact in the form of a [vCard](https://en.wikipedia.org/wiki/VCard)
    """


class Dice(msgspec.Struct):
    emoji: str
    """
    Emoji on which the dice throw animation is based
    """
    value: int
    """
    Value of the dice, 1-6 for `🎲`, `🎯` and `🎳` base emoji, 1-5 for `🏀` and `⚽` base emoji, 1-64 for `🎰` base emoji
    """


class Game(msgspec.Struct):
    """
    This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers.
    """

    title: str
    """
    Title of the game
    """
    description: str
    """
    Description of the game
    """
    photo: typing.List[PhotoSize]
    """
    Photo that will be displayed in the game message in chats.
    """
    text: typing.Optional[str]
    """
    Brief description of the game or high scores included in the game message. Can be automatically generated by Web API.
    """
    text_entities: typing.Optional[typing.List[MessageEntity]]
    """
    Special entities that appear in text, such as usernames, URLs, bot commands, etc.
    """
    animation: typing.Optional[Animation]
    """
    Animation that will be displayed in the game message in chats. Upload via BotFather
    """


class PollOptions(msgspec.Struct):
    """
    Information about one answer option in a poll.
    """

    text: str
    """
    Option text, 1-100 characters
    """
    text_entities: typing.Optional[typing.List[MessageEntity]]
    """
    Special entities that appear in the option text. Currently, only custom emoji entities are allowed in poll option texts.
    """
    voter_count: int
    """
    Number of users that voted for this option
    """


class Poll(msgspec.Struct):
    """
    This object contains information about a poll.
    """

    id: str
    """
    Unique poll identifier
    """
    question: str
    """
    Poll question, 1-300 characters
    """
    question_entities: typing.Optional[typing.List[MessageEntity]]
    """
    Special entities that appear in the question. Currently, only custom emoji entities are allowed in poll questions
    """
    options: typing.List[PollOptions]
    """
    List of poll options
    """
    total_voter_count: int
    """
    Total number of users that voted in the poll
    """
    is_closed: bool
    """
    True, if the poll is closed
    """
    is_anonymous: bool
    """
    True, if the poll is anonymous
    """
    type: typing.Optional[PollType]
    """
    Poll type, currently can be `regular` or `quiz`
    """
    allows_multiple_answers: bool
    """
    True, if the poll allows multiple answers
    """
    correct_option_id: typing.Optional[int]
    """
    0-based identifier of the correct answer option. Available only for polls in the quiz mode, which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot.
    """
    explanation: typing.Optional[str]
    """
    Optional. The text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters
    """
    explanation_entities: typing.Optional[typing.List[MessageEntity]]
    """
    Optional. Special entities that appear in the poll explanation, which can be specified instead of *explanation*.
    """
    open_period: typing.Optional[int]
    """
    Optional. Amount of time in seconds the poll will be active after creation
    """
    close_date: typing.Optional[int]
    """
    Optional. Point in time (Unix timestamp) when the poll will be automatically closed
    """


class Venue:
    """
    This object represents a venue.
    """

    location: Location
    """
    Venue location
    """
    title: str
    """
    Name of the venue
    """
    address: str
    """
    Address of the venue
    """
    foursquare_id: typing.Optional[str]
    """
    Optional. Foursquare identifier of the venue
    """
    foursquare_type: typing.Optional[str]
    """
    Optional. Foursquare type of the venue. (For example, “arts_entertainment/default”, “arts_entertainment/aquarium” or “food/ice cream”.) 
    """
    google_place_id: typing.Optional[str]
    """
    Optional. Google Places identifier of the venue
    """
    google_place_type: typing.Optional[str]
    """
    Optional. Google Places type of the venue. (See [supported types](https://developers.google.com/places/web-service/supported_types).)
    """


class MessageAutoDeleteTimerChanged(msgspec.Struct):
    """
    This object represents a service message about a change in auto-delete timer settings.
    """

    message_auto_delete_time: int
    """
    New auto-delete time for messages in the chat
    """


class InaccessibleMessage(msgspec.Struct):
    """
    This object describes a message that was deleted or is otherwise inaccessible to the bot.
    """

    chat: Chat
    """
    Chat the message was belonged to.
    """
    message_id: int
    """
    Unique message identifier
    """
    date: int
    """
    Always 0. The field can be used to differentiate regular and inaccessible messages.
    """
