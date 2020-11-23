Project Setup
=============

We have just :doc:`installed Pyrogram <install>`. In this page we'll discuss what you need to do in order to set up a
project with the library. Let's see how it's done.

.. contents:: Contents
    :backlinks: none
    :local:

-----

API Keys
--------

The very first step requires you to obtain a valid Telegram API key (API id/hash pair):

#. Visit https://my.telegram.org/apps and log in with your Telegram Account.
#. Fill out the form to register a new Telegram application.
#. Done! The API key consists of two parts: **api_id** and **api_hash**.

.. important::

     The API key is personal and must be kept secret.

.. note::

    The API key is unique for each user, but defines a token for a Telegram *application* you are going to build. This
    means that you are able to authorize multiple users (and bots too) to access the Telegram database through the
    MTProto API by a single API key.

Configuration
-------------

Having the API key from the previous step in handy, we can now begin to configure a Pyrogram project.
There are two ways to do so, and you can choose what fits better for you:

-   First option (recommended): create a new ``config.ini`` file next to your main script, copy-paste the following and
    replace the **api_id** and **api_hash** values with your own. This is the preferred method because allows you to
    keep your credentials out of your code without having to deal with how to load them:

    .. code-block:: ini

        [pyrogram]
        api_id = 12345
        api_hash = 0123456789abcdef0123456789abcdef

-   Alternatively, you can pass your API key to Pyrogram by simply using the *api_id* and *api_hash* parameters of the
    Client class. This way you can have full control on how to store and load your credentials (e.g., you can load the
    credentials from the environment variables and directly pass the values into Pyrogram):

    .. code-block:: python

        from pyrogram import Client

        app = Client(
            "my_account",
            api_id=12345,
            api_hash="0123456789abcdef0123456789abcdef"
        )

.. note::

    To keep code snippets clean and concise, from now on it is assumed you are making use of the ``config.ini`` file,
    thus, the *api_id* and *api_hash* parameters usage won't be shown anymore.
