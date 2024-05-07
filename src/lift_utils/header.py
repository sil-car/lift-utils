from typing import Optional

from .datatypes import Key
from .base import Multitext


class FieldDefinitions:
    def __init__(self):
        # attributes
        self.name: Key = ''
        self.fd_class: Optional[str] = None
        self.type: Optional[str] = None
        self.option_range: Optional[Key] = None
        self.writing_system: Optional[str] = None
        # elements
        self.label: Optional[Multitext] = None
        self.description: Optional[Multitext] = None


class Range:
    pass


class Ranges(list):
    pass


class Fields(list):
    pass


class Header:
    def __init__(self):
        # elements
        self.description: Optional[Multitext] = None
        self.ranges: Optional[Ranges] = None
        self.fields: Optional[Fields] = None
