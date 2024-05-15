"""Define the basic datatypes."""

from typing import List


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


class Prop:
    def __init__(
        self,
        name: str = None,
        required: bool = False,
    ):
        self.name = name
        self.required = required


class Props:
    def __init__(
        self,
        lift_version: str = None,
        attributes: List[Prop] = None,
        elements: List[Prop] = None,
    ):
        self.lift_version = lift_version
        self.attributes = attributes
        self.elements = elements
