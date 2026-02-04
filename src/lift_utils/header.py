"""Manipulate the header section."""

from typing import List, Optional

from lxml import etree

from . import config
from .base import Extensible, LIFTUtilsBase, Multitext
from .datatypes import URL, Key


class FieldDefn(Multitext):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``FieldDefinition``.
    """

    XML_TAG = "field"

    def __init__(
        self, tag: Key = None, xml_tree: Optional[etree._Element] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("tag",))
        self._attributes_optional = set()
        self._elements_required = set()
        self._elements_optional = set(("form", "pcdata", "span", "trait"))
        config.TAG_CLASSES.update(
            {
                "tag": Key,
            }
        )

        # attributes
        self.tag = tag

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

    def __str__(self):
        forms = "forms" if len(self.form_items) > 1 else "form"
        return f"{self.tag} ({len(self.form_items)} {forms})"


class FieldDefinition(LIFTUtilsBase):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.
    """

    XML_TAG = "field"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        self._attributes_required = set(("name",))
        self._attributes_optional = set(
            ("class", "option-range", "type", "writing-system")
        )
        self._elements_required = set()
        self._elements_optional = set(("label", "description"))
        config.TAG_CLASSES.update(
            {
                "name": Key,
                "class": str,
                "option-range": Key,
                "type": str,
                "writing-system": str,
                "label": Multitext,
                "description": Multitext,
            }
        )

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
            self._from_xml_tree(xml_tree)

    def __str__(self):
        return self.name


class FieldDefns(LIFTUtilsBase):
    """This is a simple list of ``field-defn`` elements.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``Fields``.
    """

    XML_TAG = "fields"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        self._attributes_required = set()
        self._attributes_optional = set()
        self._elements_required = set()
        self._elements_optional = set(("field",))
        config.TAG_CLASSES.update(
            {
                "field": FieldDefn,
            }
        )

        # elements
        self.field_items: Optional[List[FieldDefn]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class Fields(LIFTUtilsBase):
    """This is a simple list of ``field-definition`` elements."""

    # FIXME: Should this class have an XML tag?
    XML_TAG = None

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        self._attributes_required = set()
        self._attributes_optional = set()
        self._elements_required = set()
        self._elements_optional = set(("field",))
        config.TAG_CLASSES.update(
            {
                "field": FieldDefinition,
            }
        )

        # elements
        self.field_items: Optional[List[FieldDefinition]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class RangeElement13(LIFTUtilsBase):
    """The description of a particular range element found in a ``range``."""

    XML_TAG = "range-element"

    def __init__(
        self, elem_id: Key = None, xml_tree: Optional[etree._Element] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("id",))
        self._attributes_optional = set(("guid", "parent"))
        self._elements_required = set()
        self._elements_optional = set(
            (
                "abbrev",
                "description",
                "label",
            )
        )
        config.TAG_CLASSES.update(
            {
                "id": Key,
                "guid": str,
                "parent": Key,
                "abbrev": Multitext,
                "description": Multitext,
                "label": Multitext,
            }
        )

        # attributes
        self.id = elem_id
        self.parent: Key = None
        self.guid: str = None
        # elements
        self.description_items: Optional[List[Multitext]] = None
        self.label_items: Optional[List[Multitext]] = None
        self.abbrev_items: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class RangeElement(Extensible):
    """The description of a particular range element found in a ``range``.

    .. note:: Does not inherit from Extensible in LIFT v0.13 (FieldWorks).
    """

    XML_TAG = "range-element"

    def __init__(
        self, elem_id: Key = None, xml_tree: Optional[etree._Element] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("id",))
        self._attributes_optional = set(
            ("dateCreated", "dateModified", "guid", "parent")
        )
        self._elements_required = set()
        self._elements_optional = set(
            (
                "annotation",
                "abbrev",
                "description",
                "field",
                "label",
                "trait",
            )
        )
        config.TAG_CLASSES.update(
            {
                "id": Key,
                "guid": str,
                "parent": Key,
                "abbrev": Multitext,
                "description": Multitext,
                "label": Multitext,
            }
        )

        # attributes
        self.id = elem_id
        self.parent: Key = None
        self.guid: str = None
        # elements
        self.description_items: Optional[List[Multitext]] = None
        self.label_items: Optional[List[Multitext]] = None
        self.abbrev_items: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class Range13(LIFTUtilsBase):
    """A set of ``range-elements``.
    It is used to identify both the group of ``range-elements`` but also to
    some extent their type.
    """

    XML_TAG = "range"

    def __init__(
        self, range_id: Key = None, xml_tree: Optional[etree._Element] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("id",))
        self._attributes_optional = set(("guid", "href"))
        self._elements_required = set(("range-element",))
        self._elements_optional = set(
            (
                "abbrev",
                "description",
                "label",
            )
        )
        config.TAG_CLASSES.update(
            {
                "id": Key,
                "guid": str,
                "href": URL,
                "range-element": RangeElement13,
                "abbrev": Multitext,
                "description": Multitext,
                "label": Multitext,
            }
        )

        # attributes
        self.id = range_id
        self.guid: Optional[str] = None
        self.href: Optional[URL] = None
        # elements
        self.range_element_items: List[RangeElement13] = None
        self.abbrev_items: Optional[List[Multitext]] = None
        self.description: Optional[Multitext] = None
        self.label_items: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class Range(Extensible):
    """A set of ``range-elements``.
    It is used to identify both the group of ``range-elements`` but also to
    some extent their type.
    """

    XML_TAG = "range"

    def __init__(
        self, range_id: Key = None, xml_tree: Optional[etree._Element] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("id",))
        self._attributes_optional = set(("dateCreated", "dateModified", "guid", "href"))
        self._elements_required = set(("range-element",))
        self._elements_optional = set(
            ("abbrev", "annotation", "description", "field", "label", "trait")
        )
        config.TAG_CLASSES.update(
            {
                "id": Key,
                "guid": str,
                "href": URL,
                "range-element": RangeElement,
                "abbrev": Multitext,
                "description": Multitext,
                "label": Multitext,
            }
        )

        # attributes
        self.id = range_id
        self.guid: Optional[str] = None
        self.href: Optional[URL] = None
        # elements
        self.range_element_items: List[RangeElement] = None
        self.abbrev_items: Optional[List[Multitext]] = None
        self.description: Optional[Multitext] = None
        self.label_items: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class Ranges(LIFTUtilsBase):
    """The root element in a Lift Ranges file."""

    XML_TAG = "ranges"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        self._attributes_required = set()
        self._attributes_optional = set()
        self._elements_required = set(("range",))
        self._elements_optional = set()
        config.TAG_CLASSES.update(
            {
                "range": Range,
            }
        )

        # elements
        if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
            config.TAG_CLASSES["range"] = Range13
            self.range_items: List[Range13] = None
        else:
            self.range_items: List[Range] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


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

    XML_TAG = "header"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        self._attributes_required = set()
        self._attributes_optional = set()
        self._elements_required = set(("description", "fields", "ranges"))
        self._elements_optional = set()
        config.TAG_CLASSES.update(
            {
                "description": Multitext,
                "fields": Fields,
                "ranges": Ranges,
            }
        )

        # elements
        self.description: Optional[Multitext] = None
        self.ranges: Optional[Ranges] = None
        if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
            config.TAG_CLASSES["fields"] = FieldDefns
            self.fields: Optional[FieldDefns] = None
        else:
            self.fields: Optional[Fields] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

    def __str__(self):
        s = "Header"
        if self.description:
            s = str(self.description)
        if self.ranges and self.ranges.range_items:
            s += f": {len(self.range_items)} ranges"
        if self.fields:
            s += f", {len(self.fields)} fields"
        return s
