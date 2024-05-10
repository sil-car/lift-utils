from typing import List
from typing import Optional

from .base import Extensible
from .base import Multitext
from .datatypes import Key
from .datatypes import URL


class FieldDefinition:
    props = {
        'attributes': {
            'required': ['name'],
            'optional': ['fd_class', 'type', 'option_range', 'writing_system'],
        },
        'elements': {
            'required': [],
            'optional': ['label', 'description'],
        },
    }

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
        from lxml import etree
        print(etree.tostring(xml_tree, pretty_print=True).decode())
        for k, v in xml_tree.attrib.items():
            if k == 'name':
                self.name = Key(v)
            elif k == 'class':
                self.fd_class = v
            elif k == 'type':
                self.type = v
            elif k == 'option-range':
                self.option_range = Key(v)
            elif k == 'writing-system':
                self.writing_system = v

        for c in xml_tree.getchildren():
            if c.tag == 'label':
                self.label = Multitext(c)
            elif c.tag == 'description':
                self.description = Multitext(c)


class RangeElement(Extensible):
    props = {
        'attributes': {
            'required': ['id'],
            'optional': ['parent', 'guid'],
        },
        'elements': {
            'required': [],
            'optional': ['description', 'label', 'abbrev'],
        },
    }

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
    props = {
        'attributes': {
            'required': ['key'],
            'optional': ['guid', 'href'],
        },
        'elements': {
            'required': ['range_element'],
            'optional': ['description', 'label', 'abbrev'],
        },
    }

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
    props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': [],
        },
    }

    def __init__(self, xml_tree=None):
        super().__init__()
        # elements
        self.ranges: List[Range] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        pass


class Fields(list):
    props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': ['field_definitions'],
        },
    }

    def __init__(self, xml_tree=None):
        super().__init__()
        # elements
        self.field_definitions: Optional[List[FieldDefinition]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for c in xml_tree.getchildren():
            f = FieldDefinition(c)
            if not self.field_definitions:
                self.field_definitions = [f]
            else:
                self.field_definitions.append(f)


class Header:
    props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': [],
        },
    }

    def __init__(self, xml_tree=None):
        # elements
        self.description: Optional[Multitext] = None
        self.ranges: Optional[LiftRanges[Range]] = None
        self.fields: Optional[Fields[FieldDefinition]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for c in xml_tree.getchildren():
            if c.tag == 'description':
                self.description = Multitext(c)
            elif c.tag == 'ranges':
                self.ranges = LiftRanges(c)
            elif c.tag == 'fields':
                self.fields = Fields(c)
