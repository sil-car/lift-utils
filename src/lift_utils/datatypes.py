"""Define the basic datatypes."""

import uuid

from .utils import get_current_timestamp


class PCData(str):
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)


class DateTime(str):
    # format (str): YYYY-MM-DDTHH:MM:SSZZZZZZ
    # ZZZZZZ: +/-, H, H, :, M, M (offset from GMT)
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)
        else:
            return get_current_timestamp()


class Key(str):
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)


class Lang(str):
    # format (str): ISO[-SCRIPT[-x-PRIVATE]]
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)


class RefId(str):
    # format (HEX GUID): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)
        else:  # generate new UUID
            return super().__new__(cls, str(uuid.uuid4()))


class URL(str):
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)
