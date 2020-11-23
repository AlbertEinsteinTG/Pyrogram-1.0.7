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

import pyrogram

from pyrogram.api import types
from ..object import Object


class ChatMember(Object):
    """Contains information about one member of a chat.

    Parameters:
        user (:obj:`User`):
            Information about the user.

        status (``str``):
            The member's status in the chat.
            Can be "creator", "administrator", "member", "restricted", "left" or "kicked".

        title (``str``, *optional*):
            A custom title that will be shown to all members instead of "Owner" or "Admin".
            Creator (owner) and administrators only. Can be None in case there's no custom title set.

        until_date (``int``, *optional*):
            Restricted and kicked only.
            Date when restrictions will be lifted for this user; unix time.

        joined_date (``int``, *optional*):
            Date when the user joined, unix time.
            Not available for creator.

        invited_by (:obj:`User`, *optional*):
            Administrators and self member only. Information about the user who invited this member.
            In case the user joined by himself this will be the same as "user".

        promoted_by (:obj:`User`, *optional*):
            Administrators only. Information about the user who promoted this member as administrator.

        restricted_by (:obj:`User`, *optional*):
            Restricted and kicked only. Information about the user who restricted or kicked this member.

        is_member (``bool``, *optional*):
            Restricted only. True, if the user is a member of the chat at the moment of the request.

        can_be_edited (``bool``, *optional*):
            Administrators only.
            True, if you are allowed to edit administrator privileges of the user.

        can_post_messages (``bool``, *optional*):
            Administrators only. Channels only.
            True, if the administrator can post messages in the channel.

        can_edit_messages (``bool``, *optional*):
            Administrators only. Channels only.
            True, if the administrator can edit messages of other users and can pin messages.

        can_delete_messages (``bool``, *optional*):
            Administrators only.
            True, if the administrator can delete messages of other users.

        can_restrict_members (``bool``, *optional*):
            Administrators only.
            True, if the administrator can restrict, ban or unban chat members.

        can_promote_members (``bool``, *optional*):
            Administrators only.
            True, if the administrator can add new administrators with a subset of his own privileges or demote
            administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed
            by the user).

        can_change_info (``bool``, *optional*):
            Administrators and restricted only.
            True, if the user is allowed to change the chat title, photo and other settings.

        can_invite_users (``bool``, *optional*):
            Administrators and restricted only.
            True, if the user is allowed to invite new users to the chat.

        can_pin_messages (``bool``, *optional*):
            Administrators and restricted only. Groups and supergroups only.
            True, if the user is allowed to pin messages.

        can_send_messages (``bool``, *optional*):
            Restricted only.
            True, if the user is allowed to send text messages, contacts, locations and venues.

        can_send_media_messages (``bool``, *optional*):
            Restricted only.
            True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes.

        can_send_stickers (``bool``, *optional*):
            True, if the user is allowed to send stickers, implies can_send_media_messages.

        can_send_animations (``bool``, *optional*):
            True, if the user is allowed to send animations (GIFs), implies can_send_media_messages.

        can_send_games (``bool``, *optional*):
            True, if the user is allowed to send games, implies can_send_media_messages.

        can_use_inline_bots (``bool``, *optional*):
            True, if the user is allowed to use inline bots, implies can_send_media_messages.

        can_add_web_page_previews (``bool``, *optional*):
            Restricted only.
            True, if the user is allowed to add web page previews to their messages.

        can_send_polls (``bool``, *optional*):
            Restricted only.
            True, if the user is allowed to send polls.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        user: "pyrogram.User",
        status: str,
        title: str = None,
        until_date: int = None,
        joined_date: int = None,
        invited_by: "pyrogram.User" = None,
        promoted_by: "pyrogram.User" = None,
        restricted_by: "pyrogram.User" = None,
        is_member: bool = None,

        # Admin permissions
        can_be_edited: bool = None,
        can_post_messages: bool = None,  # Channels only
        can_edit_messages: bool = None,  # Channels only
        can_delete_messages: bool = None,
        can_restrict_members: bool = None,
        can_promote_members: bool = None,
        can_change_info: bool = None,
        can_invite_users: bool = None,
        can_pin_messages: bool = None,  # Groups and supergroups only

        # Restricted user permissions
        can_send_messages: bool = None,  # Text, contacts, locations and venues
        can_send_media_messages: bool = None,  # Audios, documents, photos, videos, video notes and voice notes
        can_send_stickers: bool = None,
        can_send_animations: bool = None,
        can_send_games: bool = None,
        can_use_inline_bots: bool = None,
        can_add_web_page_previews: bool = None,
        can_send_polls: bool = None
    ):
        super().__init__(client)

        self.user = user
        self.status = status
        self.title = title
        self.until_date = until_date
        self.joined_date = joined_date
        self.invited_by = invited_by
        self.promoted_by = promoted_by
        self.restricted_by = restricted_by
        self.is_member = is_member

        self.can_be_edited = can_be_edited
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_restrict_members = can_restrict_members
        self.can_promote_members = can_promote_members
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages

        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_stickers = can_send_stickers
        self.can_send_animations = can_send_animations
        self.can_send_games = can_send_games
        self.can_use_inline_bots = can_use_inline_bots
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_send_polls = can_send_polls

    @staticmethod
    def _parse(client, member, users) -> "ChatMember":
        user = pyrogram.User._parse(client, users[member.user_id])

        invited_by = (
            pyrogram.User._parse(client, users[member.inviter_id])
            if getattr(member, "inviter_id", None) else None
        )

        if isinstance(member, (types.ChannelParticipant, types.ChannelParticipantSelf, types.ChatParticipant)):
            return ChatMember(
                user=user,
                status="member",
                joined_date=member.date,
                invited_by=invited_by,
                client=client
            )

        if isinstance(member, (types.ChannelParticipantCreator, types.ChatParticipantCreator)):
            return ChatMember(
                user=user,
                status="creator",
                title=getattr(member, "rank", None),
                client=client
            )

        if isinstance(member, types.ChatParticipantAdmin):
            return ChatMember(
                user=user,
                status="administrator",
                joined_date=member.date,
                invited_by=invited_by,
                client=client
            )

        if isinstance(member, types.ChannelParticipantAdmin):
            permissions = member.admin_rights

            return ChatMember(
                user=user,
                status="administrator",
                title=member.rank,
                joined_date=member.date,
                invited_by=invited_by,
                promoted_by=pyrogram.User._parse(client, users[member.promoted_by]),
                can_be_edited=member.can_edit,
                can_change_info=permissions.change_info,
                can_post_messages=permissions.post_messages,
                can_edit_messages=permissions.edit_messages,
                can_delete_messages=permissions.delete_messages,
                can_restrict_members=permissions.ban_users,
                can_invite_users=permissions.invite_users,
                can_pin_messages=permissions.pin_messages,
                can_promote_members=permissions.add_admins,
                client=client
            )

        if isinstance(member, types.ChannelParticipantBanned):
            denied_permissions = member.banned_rights

            return ChatMember(
                user=user,
                status="kicked" if member.banned_rights.view_messages else "restricted",
                until_date=denied_permissions.until_date,
                joined_date=member.date,
                is_member=not member.left,
                restricted_by=pyrogram.User._parse(client, users[member.kicked_by]),
                can_send_messages=not denied_permissions.send_messages,
                can_send_media_messages=not denied_permissions.send_media,
                can_send_stickers=not denied_permissions.send_stickers,
                can_send_animations=not denied_permissions.send_gifs,
                can_send_games=not denied_permissions.send_games,
                can_use_inline_bots=not denied_permissions.send_inline,
                can_add_web_page_previews=not denied_permissions.embed_links,
                can_send_polls=not denied_permissions.send_polls,
                can_change_info=not denied_permissions.change_info,
                can_invite_users=not denied_permissions.invite_users,
                can_pin_messages=not denied_permissions.pin_messages,
                client=client
            )
