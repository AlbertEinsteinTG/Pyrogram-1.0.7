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

import asyncio
import logging
import os
from typing import Union, List

import pyrogram
from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient, utils
from pyrogram.errors import FloodWait

log = logging.getLogger(__name__)


class SendMediaGroup(BaseClient):
    # TODO: Add progress parameter
    async def send_media_group(
        self,
        chat_id: Union[int, str],
        media: List[Union["pyrogram.InputMediaPhoto", "pyrogram.InputMediaVideo"]],
        disable_notification: bool = None,
        reply_to_message_id: int = None
    ) -> List["pyrogram.Message"]:
        """Send a group of photos or videos as an album.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            media (List of :obj:`InputMediaPhoto` and :obj:`InputMediaVideo`):
                A list describing photos and videos to be sent, must include 2–10 items.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

        Returns:
            List of :obj:`Message`: On success, a list of the sent messages is returned.

        Example:
            .. code-block:: python

                from pyrogram import InputMediaPhoto, InputMediaVideo

                app.send_media_group(
                    "me",
                    [
                        InputMediaPhoto("photo1.jpg"),
                        InputMediaPhoto("photo2.jpg", caption="photo caption"),
                        InputMediaVideo("video.mp4", caption="a video")
                    ]
                )
        """
        multi_media = []

        for i in media:
            if isinstance(i, pyrogram.InputMediaPhoto):
                if os.path.exists(i.media):
                    while True:
                        try:
                            media = await self.send(
                                functions.messages.UploadMedia(
                                    peer=await self.resolve_peer(chat_id),
                                    media=types.InputMediaUploadedPhoto(
                                        file=await self.save_file(i.media)
                                    )
                                )
                            )
                        except FloodWait as e:
                            log.warning("Sleeping for {}s".format(e.x))
                            await asyncio.sleep(e.x)
                        else:
                            break

                    media = types.InputMediaPhoto(
                        id=types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash,
                            file_reference=media.photo.file_reference
                        )
                    )
                elif i.media.startswith("http"):
                    media = await self.send(
                        functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=types.InputMediaPhotoExternal(
                                url=i.media
                            )
                        )
                    )

                    media = types.InputMediaPhoto(
                        id=types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash,
                            file_reference=media.photo.file_reference
                        )
                    )
                else:
                    media = utils.get_input_media_from_file_id(i.media, i.file_ref, 2)
            elif isinstance(i, pyrogram.InputMediaVideo):
                if os.path.exists(i.media):
                    while True:
                        try:
                            media = await self.send(
                                functions.messages.UploadMedia(
                                    peer=await self.resolve_peer(chat_id),
                                    media=types.InputMediaUploadedDocument(
                                        file=await self.save_file(i.media),
                                        thumb=None if i.thumb is None else self.save_file(i.thumb),
                                        mime_type=self.guess_mime_type(i.media) or "video/mp4",
                                        attributes=[
                                            types.DocumentAttributeVideo(
                                                supports_streaming=i.supports_streaming or None,
                                                duration=i.duration,
                                                w=i.width,
                                                h=i.height
                                            ),
                                            types.DocumentAttributeFilename(file_name=os.path.basename(i.media))
                                        ]
                                    )
                                )
                            )
                        except FloodWait as e:
                            log.warning("Sleeping for {}s".format(e.x))
                            await asyncio.sleep(e.x)
                        else:
                            break

                    media = types.InputMediaDocument(
                        id=types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference
                        )
                    )
                elif i.media.startswith("http"):
                    media = await self.send(
                        functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=types.InputMediaDocumentExternal(
                                url=i.media
                            )
                        )
                    )

                    media = types.InputMediaDocument(
                        id=types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference
                        )
                    )
                else:
                    media = utils.get_input_media_from_file_id(i.media, i.file_ref, 4)

            multi_media.append(
                types.InputSingleMedia(
                    media=media,
                    random_id=self.rnd_id(),
                    **await self.parser.parse(i.caption, i.parse_mode)
                )
            )

        while True:
            try:
                r = await self.send(
                    functions.messages.SendMultiMedia(
                        peer=await self.resolve_peer(chat_id),
                        multi_media=multi_media,
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id
                    )
                )
            except FloodWait as e:
                log.warning("Sleeping for {}s".format(e.x))
                await asyncio.sleep(e.x)
            else:
                break

        return await utils.parse_messages(
            self,
            types.messages.Messages(
                messages=[m.message for m in filter(
                    lambda u: isinstance(u, (types.UpdateNewMessage, types.UpdateNewChannelMessage)),
                    r.updates
                )],
                users=r.users,
                chats=r.chats
            )
        )
