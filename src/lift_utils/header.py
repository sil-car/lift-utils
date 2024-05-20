"""Manipulate the header section."""

from lxml import etree
from typing import List
from typing import Optional

from . import config
from .base import Extensible
from .base import LIFTUtilsBase
from .base import Multitext
from .datatypes import Key
from .datatypes import Prop
from .datatypes import Props
from .datatypes import URL
from .utils import etree_to_obj_attributes


class FieldDefn(Multitext):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``FieldDefinition``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = [
            Prop('tag', required=True, ptype=Key),
        ]
        # attributes
        self.tag: Key = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        forms = 'forms' if len(self.forms) > 1 else 'form'
        return f"{self.tag} ({len(self.forms)} {forms})"

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        m = Multitext(xml_tree)
        m._update_other_from_self(self)
        del m

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class FieldDefinition(LIFTUtilsBase):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = [
            Prop('name', required=True, ptype=Key),
            Prop('class_', ptype=str),
            Prop('type', ptype=str),
            Prop('option_range', ptype=Key),
            Prop('writing_system', ptype=str),
        ]
        self.props.elements = [
            Prop('label', ptype=Multitext),
            Prop('description', ptype=Multitext),
        ]
        # attributes
        self.name: Key = None
        self.class_: Optional[str] = None
        self.type: Optional[str] = None
        self.option_range: Optional[Key] = None
        self.writing_system: Optional[str] = None
        # elements
        self.label: Optional[Multitext] = None
        self.description: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return self.name

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class RangeElement(Extensible):
    """The description of a particular range element found in a ``range``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = [
            Prop('id', required=True, ptype=Key),
            Prop('parent', ptype=Key),
            Prop('guid', ptype=str),
        ]
        self.props.elements = [
            Prop('descriptions', ptype=list, ltype=Multitext),
            Prop('labels', ptype=list, ltype=Multitext),
            Prop('abbrevs', ptype=list, ltype=Multitext),
        ]
        # attributes
        self.id: Key = None
        self.parent: Key = None
        self.guid: str = None
        # elements
        self.descriptions: Optional[List[Multitext]] = None
        self.labels: Optional[List[Multitext]] = None
        self.abbrevs: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class Range(Extensible):
    """A set of ``range-elements``.
    It is used to identify both the group of ``range-elements`` but also to
    some extent their type.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = [
            Prop('id', required=True, ptype=Key),
            Prop('guid', ptype=str),
            Prop('href', ptype=URL),
        ]
        self.props.elements = [
            Prop(
                'range_elements',
                required=True,
                ptype=list,
                ltype=RangeElement
            ),
            Prop('description', ptype=Multitext),
            Prop('labels', ptype=list, ltype=Multitext),
            Prop('abbrevs', ptype=list, ltype=Multitext),
        ]
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
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class LiftRanges(list, LIFTUtilsBase):
    """The root element in a Lift Ranges file.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
            self._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.elements = [
            Prop('ranges', required=True),
        ]

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        for c in xml_tree.getchildren():
            if c.tag == 'range':
                updated = False
                for _range in self[:]:
                    if _range.id == c.attrib.get('id'):
                        _range._update_from_xml(c)
                        updated = True
                        break
                if not updated:
                    self.append(Range(c))


class FieldDefns(list, LIFTUtilsBase):
    """This is a simple list of ``field-defn`` elements.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``Fields``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
            self._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        for c in xml_tree.getchildren():
            self.append(FieldDefn(c))


class Fields(list, LIFTUtilsBase):
    """This is a simple list of ``field-definition`` elements.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.elements = []
        if config.LIFT_VERSION == '0.13':
            self.props.elements.append(Prop(
                'field_definitions',
                ptype=list,
                ltype=FieldDefn
            ))
        else:
            self.props.elements.append(Prop(
                'field_definitions',
                ptype=list,
                ltype=FieldDefinition
            ))

        # elements
        if config.LIFT_VERSION == '0.13':
            self.field_definitions: Optional[List[FieldDefn]] = None
        else:
            self.field_definitions: Optional[List[FieldDefinition]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class Header(LIFTUtilsBase):
    """The header information for a LIFT file.
    It includes range information and added field definitions.

    :ivar Optional[Multitext] description: Contains a multilingual description
        of the lexicon for information purposes only.
    :ivar Optional[LiftRanges[Range]] ranges: Contains all the ``range``
        information.
    :ivar Optional[FieldDefns] fields: `Used by LIFT v0.13 (FieldWorks).`
        Contains definitions for all the ``field`` types used in the document.
    :ivar Optional[Fields] fields: Contains definitions for all the ``field``
        types used in the document.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.elements = [
            Prop('description', ptype=Multitext),
            Prop('ranges', ptype=LiftRanges, ltype=Range),
        ]
        if config.LIFT_VERSION == '0.13':
            self.props.elements.append(Prop('fields', ptype=FieldDefns))
        else:
            self.props.elements.append(Prop('fields', ptype=Fields))
        # elements
        self.description: Optional[Multitext] = None
        self.ranges: Optional[LiftRanges[Range]] = None
        if config.LIFT_VERSION == '0.13':
            self.fields: Optional[FieldDefns] = None
        else:
            self.fields: Optional[Fields] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        s = 'Header'
        if self.description:
            s = str(self.description)
        if self.ranges:
            s += f": {len(self.ranges)} ranges"
        if self.fields:
            s += f", {len(self.fields)} fields"
        return s

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)
