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
from .datatypes import URL


class FieldDefn(Multitext):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``FieldDefinition``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('tag', required=True, prop_type=Key),
        ])
        # attributes
        self.tag: Key = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        forms = 'forms' if len(self.forms) > 1 else 'form'
        return f"{self.tag} ({len(self.forms)} {forms})"


class FieldDefinition(LIFTUtilsBase):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('name', required=True, prop_type=Key),
            Prop('class_', prop_type=str),
            Prop('type', prop_type=str),
            Prop('option_range', prop_type=Key),
            Prop('writing_system', prop_type=str),
        ])
        self.props.elements.extend([
            Prop('label', prop_type=Multitext),
            Prop('description', prop_type=Multitext),
        ])
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


class RangeElement(Extensible, LIFTUtilsBase):
    """The description of a particular range element found in a ``range``.

    .. note:: Does not inherit from Extensible in LIFT v0.13 (FieldWorks).
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        if config.LIFT_VERSION == '0.13':
            LIFTUtilsBase.__init__(self, xml_tree)
        else:
            Extensible.__init__(self, xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('id', required=True, prop_type=Key),
            Prop('parent', prop_type=Key),
            Prop('guid', prop_type=str),
        ])
        self.props.elements.extend([
            Prop('descriptions', prop_type=list, item_type=Multitext),
            Prop('labels', prop_type=list, item_type=Multitext),
            Prop('abbrevs', prop_type=list, item_type=Multitext),
        ])
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


class Range(Extensible, LIFTUtilsBase):
    """A set of ``range-elements``.
    It is used to identify both the group of ``range-elements`` but also to
    some extent their type.

    .. note:: Does not inherit from Extensible in LIFT v0.13 (FieldWorks).
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        if config.LIFT_VERSION == '0.13':
            LIFTUtilsBase.__init__(self, xml_tree)
        else:
            Extensible.__init__(self, xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('id', required=True, prop_type=Key),
            Prop('guid', prop_type=str),
            Prop('href', prop_type=URL),
        ])
        self.props.elements.extend([
            Prop(
                'range_elements',
                required=True,
                prop_type=list,
                item_type=RangeElement
            ),
            Prop('description', prop_type=Multitext),
            Prop('labels', prop_type=list, item_type=Multitext),
            Prop('abbrevs', prop_type=list, item_type=Multitext),
        ])
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


class Ranges(LIFTUtilsBase):
    """The root element in a Lift Ranges file.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.elements.extend([
            Prop('ranges', required=True, prop_type=list, item_type=Range),
        ])
        # elements
        self.ranges: List[Range] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


class FieldDefns(LIFTUtilsBase):
    """This is a simple list of ``field-defn`` elements.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``Fields``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.elements.extend([
            Prop('fields', prop_type=list, item_type=FieldDefn)
        ])
        # elements
        self.fields: Optional[List[FieldDefn]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


class Fields(LIFTUtilsBase):
    """This is a simple list of ``field-definition`` elements.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.elements.extend([
            Prop(
                'field_definitions',
                prop_type=list,
                item_type=FieldDefinition
            ),
        ])
        # elements
        self.field_definitions: Optional[List[FieldDefinition]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


class Header(LIFTUtilsBase):
    """The header information for a LIFT file.
    It includes range information and added field definitions.

    :ivar Optional[Multitext] description: Contains a multilingual description
        of the lexicon for information purposes only.
    :ivar Optional[Ranges[Range]] ranges: Contains all the ``range``
        information.
    :ivar Optional[FieldDefns] fields: `Used by LIFT v0.13 (FieldWorks).`
        Contains definitions for all the ``field`` types used in the document.
    :ivar Optional[Fields] fields: Contains definitions for all the ``field``
        types used in the document.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.elements.extend([
            Prop('description', prop_type=Multitext),
            Prop('ranges', prop_type=Ranges),
        ])
        if config.LIFT_VERSION == '0.13':
            self.props.elements.append(Prop(
                'fields',
                prop_type=FieldDefns
            ))
        else:
            self.props.elements.append(Prop(
                'fields',
                prop_type=Fields
            ))
        # elements
        self.description: Optional[Multitext] = None
        self.ranges: Optional[Ranges] = None
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
