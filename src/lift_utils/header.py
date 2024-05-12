"""Manipulate the header section."""

from lxml import etree
from typing import List
from typing import Optional

from . import config
from .base import Extensible
from .base import LIFTUtilsBase
from .base import Multitext
from .datatypes import Key
from .datatypes import URL


class FieldDefn(Multitext):
    """A field definition gives information about a particular field type that
    may be used by an application to add information not part of the LIFT
    standard.

    .. note:: Used by LIFT v0.13 (FieldWorks).
    """

    _props = {
        'attributes': {
            'required': ['tag'],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': [],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super().update_from_xml(xml_tree)
        # attributes
        self.tag: Key = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        forms = 'forms' if len(self.forms) > 1 else 'form'
        return f"{self.tag} ({len(self.forms)} {forms})"

    def update_from_xml(self, xml_tree):
        m = Multitext(xml_tree)
        m._update_other_from_self(self)
        del m

        for k, v in xml_tree.attrib.items():
            if k == 'tag':
                self.tag = Key(v)


class FieldDefinition(LIFTUtilsBase):
    """A field definition gives information about a particular field type that
    may be used by an application to add information not part of the LIFT
    standard.
    """

    _props = {
        'attributes': {
            'required': ['name'],
            'optional': ['fd_class', 'type', 'option_range', 'writing_system'],
        },
        'elements': {
            'required': [],
            'optional': ['label', 'description'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super().update_from_xml(xml_tree)
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

    def __str__(self):
        return self.name

    def update_from_xml(self, xml_tree):
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
    """A ``range-element`` is the description of a particular range element
    found in a particular ``range``.
    """

    _props = {
        'attributes': {
            'required': ['id'],
            'optional': ['parent', 'guid'],
        },
        'elements': {
            'required': [],
            'optional': ['description', 'label', 'abbrev'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super().update_from_xml(xml_tree)
        # attributes
        self.id: Key = None
        self.parent: Key = None
        self.guid: str = None
        # elements
        self.descriptions: Optional[List[Multitext]] = None
        self.labels: Optional[List[Multitext]] = None
        self.abbrevs: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        for k, v in xml_tree.attrib.items():
            if k == 'id':
                self.id = Key(v)
            elif k == 'parent':
                self.parent = Key(v)
            elif k == 'guid':
                self.guid = v

        for c in xml_tree.getchildren():
            if c.tag == 'description':
                m = Multitext(c)
                if not self.descriptions:
                    self.descriptions = [m]
                else:
                    self.descriptions.append(m)
            elif c.tag == 'label':
                m = Multitext(c)
                if not self.labels:
                    self.labels = [m]
                else:
                    self.labels.append(m)
            elif c.tag == 'abbrev':
                m = Multitext(c)
                if not self.abbrevs:
                    self.abbrevs = [m]
                else:
                    self.abbrevs.append(m)


class Range(Extensible):
    """A ``range`` is a set of ``range-elements`` and is used to identify both
    the group of ``range-elements`` but also to some extent their type.
    """

    _props = {
        'attributes': {
            'required': ['key'],
            'optional': ['guid', 'href'],
        },
        'elements': {
            'required': ['range_element'],
            'optional': ['description', 'label', 'abbrev'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super().update_from_xml(xml_tree)
        # attributes
        self.id: Key = None
        self.guid: Optional[str] = None
        self.href: Optional[URL] = None
        # elements
        self.description: Optional[Multitext] = None
        self.range_elements: List[RangeElement] = None
        self.labels: List[Multitext] = None
        self.abbrevs: List[Multitext] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        for k, v in xml_tree.attrib.items():
            if k == 'id':
                self.id = Key(v)
            elif k == 'guid':
                self.guid = v
            elif k == 'href':
                self.href = URL(v)

        for c in xml_tree.getchildren():
            if c.tag == 'description':
                self.description = Multitext(c)
            elif c.tag == 'range-element':
                r = RangeElement(c)
                if not self.range_elements:
                    self.range_elements = [r]
                else:
                    self.range_elements.append(r)
            elif c.tag == 'label':
                m = Multitext(c)
                if not self.labels:
                    self.labels = [m]
                else:
                    self.labels.append(m)
            elif c.tag == 'abbrev':
                m = Multitext(c)
                if not self.abbrevs:
                    self.abbrevs = [c]
                else:
                    self.abbrevs.append(c)


class LiftRanges(list, LIFTUtilsBase):
    """The root element in a Lift Ranges file.
    """

    _props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': ['ranges'],
            'optional': [],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super().update_from_xml(xml_tree)
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for c in xml_tree.getchildren():
            if c.tag == 'range':
                updated = False
                for _range in self[:]:
                    if _range.id == c.attrib.get('id'):
                        _range.update_from_xml(c)
                        updated = True
                        break
                if not updated:
                    self.append(Range(c))


class FieldDefns(list, LIFTUtilsBase):
    """This is a simple list of ``field-defn``.

    .. note:: Used by LIFT v0.13 (FieldWorks).
    """

    _props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': [],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super().update_from_xml(xml_tree)
        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for c in xml_tree.getchildren():
            self.append(FieldDefn(c))


class Fields(list, LIFTUtilsBase):
    """This is a simple list of ``field-definition`` elements.
    """

    _props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': ['field_definitions'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super().update_from_xml(xml_tree)
        # elements
        if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
            self.field_definitions: Optional[List[FieldDefn]] = None
        else:
            self.field_definitions: Optional[List[FieldDefinition]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for c in xml_tree.getchildren():
            if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
                f = FieldDefn(c)
            else:
                f = FieldDefinition(c)
            if not self.field_definitions:
                self.field_definitions = [f]
            else:
                self.field_definitions.append(f)


class Header(LIFTUtilsBase):
    """This holds the header information for a LIFT file including range
    information and added field definitions.

    :ivar Optional[Multitext] description: Contains a multilingual description
        of the lexicon for information purposes only.
    :ivar Optional[LiftRanges[Range]] ranges: Contains all the ``range``
        information.
    :ivar Optional[FieldDefns] fields: `Used by LIFT v0.13 (FieldWorks).`
        Contains definitions for all the ``field`` types used in the document.
    :ivar Optional[Fields] fields: Contains definitions for all the ``field``
        types used in the document.
    """

    _props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': [],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super().update_from_xml(xml_tree)
        # elements
        self.description: Optional[Multitext] = None
        self.ranges: Optional[LiftRanges[Range]] = None
        if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
            self.fields: Optional[FieldDefns] = None
        else:
            self.fields: Optional[Fields] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for c in xml_tree.getchildren():
            if c.tag == 'description':
                self.description = Multitext(c)
            elif c.tag in ['ranges', 'lift-ranges']:
                self.ranges = LiftRanges(c)
            elif c.tag == 'fields':
                if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
                    self.fields = FieldDefns(c)
                else:
                    self.fields = Fields(c)
