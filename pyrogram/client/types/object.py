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

import re
from collections import OrderedDict
from datetime import datetime
from json import dumps

import pyrogram


class Meta(type, metaclass=type("", (type,), {"__str__": lambda _: "~hi"})):
    def __str__(self):
        return "<class 'pyrogram.{}'>".format(self.__name__)


class Object(metaclass=Meta):
    def __init__(self, client: "pyrogram.BaseClient" = None):
        self._client = client

    def bind(self, client: "pyrogram.BaseClient"):
        """Bind a Client instance to this Pyrogram Object

        Parameters:
            client (:obj:`Client`):
                The Client instance to bind this object with. Useful to re-enable bound methods after serializing and
                deserializing Pyrogram objects with ``repr`` and ``eval``.
        """
        self._client = client

    @staticmethod
    def default(obj: "Object"):
        if isinstance(obj, bytes):
            return repr(obj)

        if isinstance(obj, re.Match):
            return repr(obj)

        return OrderedDict(
            [("_", "pyrogram." + obj.__class__.__name__)]
            + [
                (attr, "*" * len(getattr(obj, attr)))
                if attr == "phone_number"
                else (attr, str(datetime.fromtimestamp(getattr(obj, attr))))
                if attr.endswith("date")
                else (attr, getattr(obj, attr))
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            ]
        )

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Object.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "pyrogram.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                "{}={}".format(attr, repr(getattr(self, attr)))
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: "Object") -> bool:
        for attr in self.__dict__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)
