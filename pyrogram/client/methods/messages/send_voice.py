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

import os
from typing import Union

import pyrogram
from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient, utils
from pyrogram.errors import FilePartMissing


class SendVoice(BaseClient):
    async def send_voice(
        self,
        chat_id: Union[int, str],
        voice: str,
        file_ref=None,
        caption: str = "",
        parse_mode: Union[str, None] = object,
        duration: int = 0,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
        reply_markup: Union[
            "pyrogram.InlineKeyboardMarkup",
            "pyrogram.ReplyKeyboardMarkup",
            "pyrogram.ReplyKeyboardRemove",
            "pyrogram.ForceReply"
        ] = None,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> Union["pyrogram.Message", None]:
        """Send audio files.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            voice (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio from the Internet, or
                pass a file path as string to upload a new audio that exists on your local machine.

            file_ref (``str``, *optional*):
                A valid file reference obtained by a recently fetched media message.
                To be used in combination with a file id in case a file reference is needed.

            caption (``str``, *optional*):
                Voice message caption, 0-1024 characters.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            duration (``int``, *optional*):
                Duration of the voice message in seconds.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            schedule_date (``int``, *optional*):
                Date when the message will be automatically sent. Unix time.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            :obj:`Message` | ``None``: On success, the sent voice message is returned, otherwise, in case the upload
            is deliberately stopped with :meth:`~Client.stop_transmission`, None is returned.

        Example:
            .. code-block:: python

                # Send voice note by uploading from local file
                app.send_voice("me", "voice.ogg")

                # Add caption to the voice note
                app.send_voice("me", "voice.ogg", caption="voice note")

                # Set voice note duration
                app.send_voice("me", "voice.ogg", duration=20)
        """
        file = None

        try:
            if os.path.exists(voice):
                file = await self.save_file(voice, progress=progress, progress_args=progress_args)
                media = types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(voice) or "audio/mpeg",
                    file=file,
                    attributes=[
                        types.DocumentAttributeAudio(
                            voice=True,
                            duration=duration
                        )
                    ]
                )
            elif voice.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=voice
                )
            else:
                media = utils.get_input_media_from_file_id(voice, file_ref, 3)

            while True:
                try:
                    r = await self.send(
                        functions.messages.SendMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=media,
                            silent=disable_notification or None,
                            reply_to_msg_id=reply_to_message_id,
                            random_id=self.rnd_id(),
                            schedule_date=schedule_date,
                            reply_markup=reply_markup.write() if reply_markup else None,
                            **await self.parser.parse(caption, parse_mode)
                        )
                    )
                except FilePartMissing as e:
                    await self.save_file(voice, file_id=file.id, file_part=e.x)
                else:
                    for i in r.updates:
                        if isinstance(
                            i,
                            (types.UpdateNewMessage, types.UpdateNewChannelMessage, types.UpdateNewScheduledMessage)
                        ):
                            return await pyrogram.Message._parse(
                                self, i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(i, types.UpdateNewScheduledMessage)
                            )
        except BaseClient.StopTransmission:
            return None
