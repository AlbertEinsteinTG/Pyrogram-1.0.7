<p align="center">
    <a href="https://github.com/pyrogram/pyrogram">
        <img src="https://i.imgur.com/BOgY9ai.png" alt="Pyrogram">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://docs.pyrogram.org">
        Documentation
    </a>
    •
    <a href="https://github.com/pyrogram/pyrogram/releases">
        Releases
    </a>
    •
    <a href="https://t.me/Pyrogram">
        Community
    </a>
</p>

## Pyrogram

``` python
from pyrogram import Client, Filters

app = Client("my_account")


@app.on_message(Filters.private)
def hello(client, message):
    message.reply_text("Hello {}".format(message.from_user.first_name))


app.run()
```

**Pyrogram** is an elegant, easy-to-use [Telegram](https://telegram.org/) client library and framework written from the
ground up in Python and C. It enables you to easily create custom apps for both user and bot identities (bot API alternative) via the [MTProto API](https://core.telegram.org/api#telegram-api).

> [Pyrogram in fully-asynchronous mode is also available »](https://github.com/pyrogram/pyrogram/issues/181)
>
> [Working PoC of Telegram voice calls using Pyrogram »](https://github.com/bakatrouble/pytgvoip)

### Features

- **Easy**: You can install Pyrogram with pip and start building your applications right away.
- **Elegant**: Low-level details are abstracted and re-presented in a much nicer and easier way.
- **Fast**: Crypto parts are boosted up by [TgCrypto](https://github.com/pyrogram/tgcrypto), a high-performance library
  written in pure C.
- **Documented**: Pyrogram API methods, types and public interfaces are well documented.
- **Type-hinted**: Exposed Pyrogram types and method parameters are all type-hinted.
- **Updated**, to make use of the latest Telegram API version and features.
- **Bot API-like**: Similar to the Bot API in its simplicity, but much more powerful and detailed.
- **Pluggable**: The Smart Plugin system allows to write components with minimal boilerplate code.
- **Comprehensive**: Execute any advanced action an official client is able to do, and even more.

### Requirements

- Python 3.5.3 or higher.
- A [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys).

### Installing

``` bash
pip3 install pyrogram
```

### Resources

- The Docs contain lots of resources to help you getting started with Pyrogram: https://docs.pyrogram.org.
- Reading [Examples in this repository](https://github.com/pyrogram/pyrogram/tree/master/examples) is also a good way
  for learning how Pyrogram works.
- Seeking extra help? Don't be shy, come join and ask our [Community](https://t.me/PyrogramChat)!
- For other requests you can send an [Email](mailto:dan@pyrogram.org) or a [Message](https://t.me/haskell).

### Contributing

Pyrogram is brand new, and **you are welcome to try it and help make it even better** by either submitting pull
requests or reporting issues/bugs as well as suggesting best practices, ideas, enhancements on both code
and documentation. Any help is appreciated!

### Copyright & License

- Copyright (C) 2017-2020 Dan <<https://github.com/delivrance>>
- Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)
