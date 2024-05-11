"""Define the basic datatypes."""


class PCData(str):
    def __new__(cls, content=None):
        if content is not None:
            return super().__new__(cls, content)


class DateTime(str):
    # format (str): YYYY-MM-DDTHH:MM:SSZZZZZZ
    # ZZZZZZ: +/-, H, H, :, M, M (offset from GMT)
    def __new__(cls, content=None):
        if content is not None:
            return super().__new__(cls, content)


class Key(str):
    def __new__(cls, content=None):
        if content is not None:
            return super().__new__(cls, content)


class Lang(str):
    # format (str): ISO[-SCRIPT[-x-PRIVATE]]
    def __new__(cls, content=None):
        if content is not None:
            return super().__new__(cls, content)


class RefId(str):
    # format (HEX GUID): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    def __new__(cls, content=None):
        if content is not None:
            return super().__new__(cls, content)


class URL(str):
    def __new__(cls, content=None):
        if content is not None:
            return super().__new__(cls, content)
