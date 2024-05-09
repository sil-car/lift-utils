from typing import List
from typing import Optional

from .base import Extensible
from .base import Multitext
from .datatypes import Key
from .datatypes import URL


class FieldDefinition:
    _attrib_req = ['name']
    _attrib_opt = ['fd_class', 'type', 'option_range', 'writing_system']
    _elem_req = []
    _elem_opt = ['label', 'description']

    def __init__(self, xml_tree=None):
        # attributes
        self.name: Key = None
        self.fd_class: Optional[str] = None
        self.type: Optional[str] = None
        self.option_range: Optional[Key] = None
        self.writing_system: Optional[str] = None
        # elements
        self.label: Optional[Multitext] = None
        self.description: Optional[Multitext] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        pass


class RangeElement(Extensible):
    _attrib_req = ['id']
    _attrib_opt = ['parent', 'guid']
    _elem_req = []
    _elem_opt = ['description', 'label', 'abbrev']

    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.id: Key = None
        self.parent: Key = None
        self.guid: str = None
        # elements
        self.description: Optional[List[Multitext]] = None
        self.label: Optional[List[Multitext]] = None
        self.abbrev: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
        del ext


class Range(Extensible):
    _attrib_req = ['key']
    _attrib_opt = ['guid', 'href']
    _elem_req = ['range_element']
    _elem_opt = ['description', 'label', 'abbrev']

    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.id: Key = None
        self.guid: Optional[str] = None
        self.href: Optional[URL] = None
        # elements
        self.description: Optional[Multitext] = None
        self.range_element: List[RangeElement] = None
        self.label: List[Multitext] = None
        self.abbrev: List[Multitext] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
        del ext


class LiftRanges(list):
    def __init__(self, xml_tree=None):
        super().__init__()
        # elements
        self.ranges: List[Range] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        pass


class Fields(list):
    _attrib_req = []
    _attrib_opt = []
    _elem_req = []
    _elem_opt = ['field_definition']

    def __init__(self, xml_tree=None):
        super().__init__()
        # elements
        self.field_definition: Optional[List[FieldDefinition]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        pass


class Header:
    def __init__(self, xml_tree=None):
        # elements
        self.description: Optional[Multitext] = None
        self.ranges: Optional[LiftRanges[Range]] = None
        self.fields: Optional[Fields[FieldDefinition]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        pass
