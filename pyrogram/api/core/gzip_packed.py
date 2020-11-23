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

from gzip import compress, decompress
from io import BytesIO

from .primitives import Int, Bytes
from .tl_object import TLObject


class GzipPacked(TLObject):
    ID = 0x3072cfa1

    __slots__ = ["packed_data"]

    QUALNAME = "GzipPacked"

    def __init__(self, packed_data: TLObject):
        self.packed_data = packed_data

    @staticmethod
    def read(b: BytesIO, *args) -> "GzipPacked":
        # Return the Object itself instead of a GzipPacked wrapping it
        return TLObject.read(
            BytesIO(
                decompress(
                    Bytes.read(b)
                )
            )
        )

    def write(self) -> bytes:
        b = BytesIO()

        b.write(Int(self.ID, False))

        b.write(
            Bytes(
                compress(
                    self.packed_data.write()
                )
            )
        )

        return b.getvalue()
