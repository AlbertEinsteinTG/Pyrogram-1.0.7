"""This example shows how to get the full dialogs list (as user)."""

from pyrogram import Client

app = Client("my_account")

with app:
    for dialog in app.iter_dialogs():
        print(dialog.chat.title or dialog.chat.first_name)
