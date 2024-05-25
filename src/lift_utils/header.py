"""Manipulate the header section."""

from copy import deepcopy
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
from .utils import obj_attributes_to_etree


class FieldDefn(Multitext):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``FieldDefinition``.
    """

    def __init__(
        self,
        tag: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
        # properties
        self.props.add_to(
            'attributes',
            Prop('tag', required=True, prop_type=Key)
        )
        self.xml_tag = 'field'
        # attributes
        self.tag = tag

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        forms = 'forms' if len(self.form_items) > 1 else 'form'
        return f"{self.tag} ({len(self.form_items)} {forms})"


class FieldDefinition(LIFTUtilsBase):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
        # properties
        attribs = [
            Prop('name', required=True, prop_type=Key),
            Prop('class_', prop_type=str),
            Prop('type', prop_type=str),
            Prop('option_range', prop_type=Key),
            Prop('writing_system', prop_type=str),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('label', prop_type=Multitext),
            Prop('description', prop_type=Multitext),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'field'
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
        elem_id: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        if config.LIFT_VERSION == '0.13':
            LIFTUtilsBase.__init__(self, xml_tree=xml_tree)
        else:
            Extensible.__init__(self, xml_tree=xml_tree)
        # properties
        attribs = [
            Prop('id', required=True, prop_type=Key),
            Prop('parent', prop_type=Key),
            Prop('guid', prop_type=str),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('description_items', prop_type=list, item_type=Multitext),
            Prop('label_items', prop_type=list, item_type=Multitext),
            Prop('abbrev_items', prop_type=list, item_type=Multitext),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'range-element'
        # attributes
        self.id = elem_id
        self.parent: Key = None
        self.guid: str = None
        # elements
        self.description_items: Optional[List[Multitext]] = None
        self.label_items: Optional[List[Multitext]] = None
        self.abbrev_items: Optional[List[Multitext]] = None

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
        range_id: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        if config.LIFT_VERSION == '0.13':
            LIFTUtilsBase.__init__(self, xml_tree=xml_tree)
        else:
            Extensible.__init__(self, xml_tree=xml_tree)
        # properties
        attribs = [
            Prop('id', required=True, prop_type=Key),
            Prop('guid', prop_type=str),
            Prop('href', prop_type=URL),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop(
                'range_elements',
                required=True,
                prop_type=list,
                item_type=RangeElement
            ),
            Prop('description', prop_type=Multitext),
            Prop('label_items', prop_type=list, item_type=Multitext),
            Prop('abbrev_items', prop_type=list, item_type=Multitext),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'range'
        # attributes
        self.id = range_id
        self.guid: Optional[str] = None
        self.href: Optional[URL] = None
        # elements
        self.description: Optional[Multitext] = None
        self.range_elements: List[RangeElement] = None
        self.label_items: List[Multitext] = None
        self.abbrev_items: List[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
            self._set_alt_objs()

    def _set_alt_objs(self):
        self.ranges_obj = deepcopy(self)
        self.lift_obj = deepcopy(self)
        if self.href:  # create two xml trees for 'range'
            self.lift_obj.props.elements = []
            self.ranges_obj.href = None
            self.ranges_obj.props.attributes = [a for a in self.ranges_obj.props.attributes[:] if a.name != 'href']  # noqa: E501

    def _to_xml_tree(self):
        self._set_alt_objs()
        self.ranges_xml_tree = obj_attributes_to_etree(self.ranges_obj, self.xml_tag)  # noqa: E501
        xml_tree = obj_attributes_to_etree(self, self.xml_tag)
        return xml_tree


class Ranges(LIFTUtilsBase):
    """The root element in a Lift Ranges file.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
        # properties
        self.props.add_to(
            'elements',
            Prop('range_items', required=True, prop_type=list, item_type=Range),  # noqa: E501
        )
        self.xml_tag = 'ranges'  # or 'lift-ranges'
        # elements
        self.range_items: List[Range] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
            self._set_alt_objs()

    def _set_alt_objs(self):
        self.ranges_obj = deepcopy(self)
        self.lift_obj = deepcopy(self)
        self.ranges_obj.xml_tag = 'lift-ranges'

    def _to_xml_tree(self):
        self._set_alt_objs()
        # For unit tests:
        self.ranges_xml_tree = obj_attributes_to_etree(self.ranges_obj, 'lift-ranges')  # noqa: E501
        xml_tree = obj_attributes_to_etree(self, 'ranges')
        return xml_tree


class FieldDefns(LIFTUtilsBase):
    """This is a simple list of ``field-defn`` elements.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``Fields``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
        # properties
        self.props.add_to(
            'elements',
            Prop('field_items', prop_type=list, item_type=FieldDefn)
        )
        self.xml_tag = 'fields'
        # elements
        self.field_items: Optional[List[FieldDefn]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


class Fields(LIFTUtilsBase):
    """This is a simple list of ``field-definition`` elements.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
        # properties
        self.props.add_to(
            'elements',
            Prop('field_definitions', prop_type=list, item_type=FieldDefinition)  # noqa: E501
        )
        # elements
        self.field_definitions: Optional[List[FieldDefinition]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


class Header(LIFTUtilsBase):
    """The header information for a LIFT file.
    It includes range information and added field definitions.

    :ivar Optional[Multitext] description: Contains a multilingual description
        of the lexicon for information purposes only.
    :ivar Optional[Ranges] ranges: Contains all the ``range`` information.
    :ivar Optional[FieldDefns] field_items: `Used by LIFT v0.13 (FieldWorks).`
        Contains definitions for all the ``field`` types used in the document.
    :ivar Optional[Fields] fields: Contains definitions for all the ``field``
        types used in the document.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
        # properties
        elems = [
            Prop('description', prop_type=Multitext),
            Prop('ranges', prop_type=Ranges),
        ]
        if config.LIFT_VERSION == '0.13':
            elems.append(Prop('fields', prop_type=FieldDefns))
        else:
            elems.append(Prop('fields', prop_type=Fields))
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'header'
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
