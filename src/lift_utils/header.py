from typing import Optional

from datatypes import Key
from base import Multitext


# Header elements

class FieldDefinitions:
    # attributes
    name: Key = ''
    fd_class: Optional[str] = None
    fd_type: Optional[str] = None
    option_range: Optional[Key] = None
    writing_system: Optional[str] = None
    # elements
    label: Optional[Multitext] = None
    description: Optional[Multitext] = None


class Range:
    pass


class Ranges(list):
    pass


class Fields(list):
    pass


class Header:
    # elements
    description: Optional[Multitext] = None
    ranges: Optional[Ranges] = None
    fields: Optional[Fields] = None
