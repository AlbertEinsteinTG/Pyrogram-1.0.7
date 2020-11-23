#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import html
from typing import List

import pyrogram
from pyrogram.api import types
from .chat_photo import ChatPhoto
from .restriction import Restriction
from ..object import Object
from ..update import Update


class User(Object, Update):
    """A Telegram user or bot.

    Parameters:
        id (``int``):
            Unique identifier for this user or bot.

        is_self(``bool``, *optional*):
            True, if this user is you yourself.

        is_contact(``bool``, *optional*):
            True, if this user is in your contacts.

        is_mutual_contact(``bool``, *optional*):
            True, if you both have each other's contact.

        is_deleted(``bool``, *optional*):
            True, if this user is deleted.

        is_bot (``bool``, *optional*):
            True, if this user is a bot.

        is_verified (``bool``, *optional*):
            True, if this user has been verified by Telegram.

        is_restricted (``bool``, *optional*):
            True, if this user has been restricted. Bots only.
            See *restriction_reason* for details.

        is_scam (``bool``, *optional*):
            True, if this user has been flagged for scam.

        is_support (``bool``, *optional*):
            True, if this user is part of the Telegram support team.

        first_name (``str``, *optional*):
            User's or bot's first name.

        last_name (``str``, *optional*):
            User's or bot's last name.

        status (``str``, *optional*):
            User's Last Seen & Online status.
            Can be one of the following:
            "*online*", user is online right now.
            "*offline*", user is currently offline.
            "*recently*", user with hidden last seen time who was online between 1 second and 2-3 days ago.
            "*within_week*", user with hidden last seen time who was online between 2-3 and seven days ago.
            "*within_month*", user with hidden last seen time who was online between 6-7 days and a month ago.
            "*long_time_ago*", blocked user or user with hidden last seen time who was online more than a month ago.
            *None*, for bots.

        last_online_date (``int``, *optional*):
            Last online date of a user. Only available in case status is "*offline*".

        next_offline_date (``int``, *optional*):
            Date when a user will automatically go offline. Only available in case status is "*online*".

        username (``str``, *optional*):
            User's or bot's username.

        language_code (``str``, *optional*):
            IETF language tag of the user's language.

        dc_id (``int``, *optional*):
            User's or bot's assigned DC (data center). Available only in case the user has set a public profile photo.
            Note that this information is approximate; it is based on where Telegram stores a user profile pictures and
            does not by any means tell you the user location (i.e. a user might travel far away, but will still connect
            to its assigned DC). More info at `FAQs </faq#what-are-the-ip-addresses-of-telegram-data-centers>`_.

        phone_number (``str``, *optional*):
            User's phone number.

        photo (:obj:`ChatPhoto <pyrogram.ChatPhoto>`, *optional*):
            User's or bot's current profile photo. Suitable for downloads only.

        restrictions (List of :obj:`Restriction`, *optional*):
            The list of reasons why this bot might be unavailable to some users.
            This field is available only in case *is_restricted* is True.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        id: int,
        is_self: bool = None,
        is_contact: bool = None,
        is_mutual_contact: bool = None,
        is_deleted: bool = None,
        is_bot: bool = None,
        is_verified: bool = None,
        is_restricted: bool = None,
        is_scam: bool = None,
        is_support: bool = None,
        first_name: str = None,
        last_name: str = None,
        status: str = None,
        last_online_date: int = None,
        next_offline_date: int = None,
        username: str = None,
        language_code: str = None,
        dc_id: int = None,
        phone_number: str = None,
        photo: ChatPhoto = None,
        restrictions: List[Restriction] = None
    ):
        super().__init__(client)

        self.id = id
        self.is_self = is_self
        self.is_contact = is_contact
        self.is_mutual_contact = is_mutual_contact
        self.is_deleted = is_deleted
        self.is_bot = is_bot
        self.is_verified = is_verified
        self.is_restricted = is_restricted
        self.is_scam = is_scam
        self.is_support = is_support
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.last_online_date = last_online_date
        self.next_offline_date = next_offline_date
        self.username = username
        self.language_code = language_code
        self.dc_id = dc_id
        self.phone_number = phone_number
        self.photo = photo
        self.restrictions = restrictions

    def __format__(self, format_spec):
        if format_spec == "mention":
            return '<a href="tg://user?id={0}">{1}</a>'.format(self.id, html.escape(self.first_name))

        return html.escape(str(self))

    @staticmethod
    def _parse(client, user: types.User) -> "User" or None:
        if user is None:
            return None

        return User(
            id=user.id,
            is_self=user.is_self,
            is_contact=user.contact,
            is_mutual_contact=user.mutual_contact,
            is_deleted=user.deleted,
            is_bot=user.bot,
            is_verified=user.verified,
            is_restricted=user.restricted,
            is_scam=user.scam,
            is_support=user.support,
            first_name=user.first_name,
            last_name=user.last_name,
            **User._parse_status(user.status, user.bot),
            username=user.username,
            language_code=user.lang_code,
            dc_id=getattr(user.photo, "dc_id", None),
            phone_number=user.phone,
            photo=ChatPhoto._parse(client, user.photo, user.id, user.access_hash),
            restrictions=pyrogram.List([Restriction._parse(r) for r in user.restriction_reason]) or None,
            client=client
        )

    @staticmethod
    def _parse_status(user_status: types.UpdateUserStatus, is_bot: bool = False):
        if isinstance(user_status, types.UserStatusOnline):
            status, date = "online", user_status.expires
        elif isinstance(user_status, types.UserStatusOffline):
            status, date = "offline", user_status.was_online
        elif isinstance(user_status, types.UserStatusRecently):
            status, date = "recently", None
        elif isinstance(user_status, types.UserStatusLastWeek):
            status, date = "within_week", None
        elif isinstance(user_status, types.UserStatusLastMonth):
            status, date = "within_month", None
        else:
            status, date = "long_time_ago", None

        last_online_date = None
        next_offline_date = None

        if is_bot:
            status = None

        if status == "online":
            next_offline_date = date

        if status == "offline":
            last_online_date = date

        return {
            "status": status,
            "last_online_date": last_online_date,
            "next_offline_date": next_offline_date
        }

    @staticmethod
    def _parse_user_status(client, user_status: types.UpdateUserStatus):
        return User(
            id=user_status.user_id,
            **User._parse_status(user_status.status),
            client=client
        )

    async def archive(self):
        """Bound method *archive* of :obj:`User`.

        Use as a shortcut for:

        .. code-block:: python

            client.archive_chats(123456789)

        Example:
            .. code-block:: python

                user.archive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.archive_chats(self.id)

    async def unarchive(self):
        """Bound method *unarchive* of :obj:`User`.

        Use as a shortcut for:

        .. code-block:: python

            client.unarchive_chats(123456789)

        Example:
            .. code-block:: python

                user.unarchive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.unarchive_chats(self.id)

    def block(self):
        """Bound method *block* of :obj:`User`.

        Use as a shortcut for:

        .. code-block:: python

            client.block_user(123456789)

        Example:
            .. code-block:: python

                user.block()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.block_user(self.id)

    def unblock(self):
        """Bound method *unblock* of :obj:`User`.

        Use as a shortcut for:

        .. code-block:: python

            client.unblock_user(123456789)

        Example:
            .. code-block:: python

                user.unblock()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.unblock_user(self.id)

    def get_common_chats(self):
        """Bound method *get_common_chats* of :obj:`User`.

        Use as a shortcut for:

        .. code-block:: python

            client.get_common_chats(123456789)

        Example:
            .. code-block:: python

                user.get_common_chats()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.get_common_chats(self.id)
