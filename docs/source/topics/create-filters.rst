Creating Filters
================

Pyrogram already provides lots of built-in :class:`~pyrogram.Filters` to work with, but in case you can't find
a specific one for your needs or want to build a custom filter by yourself (to be used in a different kind of handler,
for example) you can use :meth:`~pyrogram.Filters.create`.

.. note::

    At the moment, the built-in filters are intended to be used with the :class:`~pyrogram.MessageHandler` only.

.. contents:: Contents
    :backlinks: none
    :local:

-----

Custom Filters
--------------

An example to demonstrate how custom filters work is to show how to create and use one for the
:class:`~pyrogram.CallbackQueryHandler`. Note that callback queries updates are only received by bots as result of a
user pressing an inline button attached to the bot's message; create and :doc:`authorize your bot <../start/auth>`,
then send a message with an inline keyboard to yourself. This allows you to test your filter by pressing the inline
button:

.. code-block:: python

    from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

    app.send_message(
        "username",  # Change this to your username or id
        "Pyrogram custom filter test",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Press me", "pyrogram")]]
        )
    )

Basic Filters
-------------

For this basic filter we will be using only the first parameter of :meth:`~pyrogram.Filters.create`.

The code below creates a simple filter for hardcoded, static callback data. This filter will only allow callback queries
containing "pyrogram" as data, that is, the function *func* you pass returns True in case the callback query data
equals to ``"pyrogram"``.

.. code-block:: python

    static_data_filter = Filters.create(lambda _, query: query.data == "pyrogram")

The ``lambda`` operator in python is used to create small anonymous functions and is perfect for this example, the same
could be achieved with a normal function, but we don't really need it as it makes sense only inside the filter scope:

.. code-block:: python

    def func(_, query):
        return query.data == "pyrogram"

    static_data_filter = Filters.create(func)

The filter usage remains the same:

.. code-block:: python

    @app.on_callback_query(static_data_filter)
    def pyrogram_data(_, query):
        query.answer("it works!")

Filters with Arguments
----------------------

A much cooler filter would be one that accepts "pyrogram" or any other data as argument at usage time.
A dynamic filter like this will make use of named arguments for the :meth:`~pyrogram.Filters.create` method.

This is how a dynamic custom filter looks like:

.. code-block:: python

    def dynamic_data_filter(data):
        return Filters.create(
            lambda flt, query: flt.data == query.data,
            data=data  # "data" kwarg is accessed with "flt.data" above
        )

And its usage:

.. code-block:: python

    @app.on_callback_query(dynamic_data_filter("pyrogram"))
    def pyrogram_data(_, query):
        query.answer("it works!")
