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
        prop_type=None,
        item_type=None,
    ):
        self.name = name
        self.required = required
        self.prop_type = prop_type
        self.item_type = item_type


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

    def add_to(self, prop_group_name, prop_obj):
        prop_group = self.__dict__.get(prop_group_name)
        if prop_obj.name not in [p.name for p in prop_group]:
            prop_group.append(prop_obj)
