Bound Methods
=============

Some Pyrogram types define what are called bound methods. Bound methods are functions attached to a class which are
accessed via an instance of that class. They make it even easier to call specific methods by automatically inferring
some of the required arguments.

.. code-block:: python
    :emphasize-lines: 8

    from pyrogram import Client

    app = Client("my_account")


    @app.on_message()
    def hello(client, message)
        message.reply("hi")


    app.run()

.. contents:: Contents
    :backlinks: none
    :local:

-----

.. currentmodule:: pyrogram

Message
-------

.. hlist::
    :columns: 3

    {message_hlist}

.. toctree::
    :hidden:

    {message_toctree}

Chat
----

.. hlist::
    :columns: 4

    {chat_hlist}

.. toctree::
    :hidden:

    {chat_toctree}

User
----

.. hlist::
    :columns: 2

    {user_hlist}

.. toctree::
    :hidden:

    {user_toctree}

CallbackQuery
-------------

.. hlist::
    :columns: 3

    {callback_query_hlist}

.. toctree::
    :hidden:

    {callback_query_toctree}

InlineQuery
-----------

.. hlist::
    :columns: 2

    {inline_query_hlist}

.. toctree::
    :hidden:

    {inline_query_toctree}
