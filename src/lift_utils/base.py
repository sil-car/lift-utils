"""Manipulate base linguistic elements."""

import sys
from lxml import etree
from typing import List
from typing import Optional

from . import config
from .datatypes import PCData
from .datatypes import DateTime
from .datatypes import Key
from .datatypes import Lang
from .datatypes import Prop
from .datatypes import Props
from .datatypes import URL
from .utils import etree_to_obj_attributes
from .utils import obj_attributes_to_etree


class LIFTUtilsBase:
    """This is a base class for all LIFT-related objects in this package.

    :ivar etree xml_tree: The object's current data.
    """
    def __init__(self, xml_tree: etree = None):
        self.xml_tree = xml_tree
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = []
        self.props.elements = []

    def to_xml(self):
        """Convert the object's data to XML."""
        if self.xml_tree:
            return etree.tostring(
                self.xml_tree,
                encoding='UTF-8',
                pretty_print=True,
                xml_declaration=True
            ).decode().rstrip()

    def print(self, format='xml'):
        """Print the object's data to stdout; as XML by default."""
        if self.xml_tree:
            try:
                if format == 'xml':
                    print(self.to_xml(), flush=True)
                else:
                    return
            except BrokenPipeError:
                sys.stdout = None

    def _update_from_xml(self, xml_tree):
        # Set initial xml_tree.
        self.xml_tree = xml_tree
        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class Span(LIFTUtilsBase):
    """A Unicode string marked with language and formatting information.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('lang', prop_type=Lang),
            Prop('href', prop_type=URL),
            Prop('class_', prop_type=str),
        ])
        self.props.elements.extend([
            Prop('pcdata', required=True, prop_type=PCData),
            Prop('tail', prop_type=PCData),
            Prop('spans', prop_type=list, item_type=Span),
        ])
        # attributes
        self.lang: Optional[Lang] = None
        self.href: Optional[URL] = None
        self.class_: Optional[str] = None
        # elements
        self.pcdata: PCData = None
        self.tail: Optional[PCData] = None
        self.spans: Optional[List[Span]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'span')
        return xml_tree


class Trait(LIFTUtilsBase):
    """An important mechanism for giving type information to an object.
    It can also be used for adding binary constraints.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('name', required=True, prop_type=Key),
            Prop('value', required=True, prop_type=Key),
            Prop('id', prop_type=Key),
        ])
        self.props.elements.extend([
            Prop('annotations', prop_type=list, item_type=Annotation),
        ])
        # attributes
        self.name: Key = None
        self.value: Key = None
        self.id: Optional[Key] = None
        # elements
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.name}: {self.value}"

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'trait')
        return xml_tree


class Flag(Trait):
    """An important mechanism for giving type information to an object.
    It can also be use for adding binary constraints.

    .. note:: Used by LIFT v0.13 (FieldWorks). Mentioned in specification but
        not defined; assumed to be equivalent to ``Trait``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)


class Form(LIFTUtilsBase):
    """A representation of a string in a particular language and script.
    This is specified by the ``lang`` attribute.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('lang', required=True, prop_type=Lang)
        ])
        self.props.elements.extend([
            Prop('text', required=True, prop_type=Text),
            Prop('annotations', prop_type=list, item_type=Annotation),
        ])
        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return str(self.text)

    def _update_other_from_self(self, other):
        other.lang = self.lang
        other.text = self.text
        other.annotations = self.annotations

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'form')
        return xml_tree


class Text(LIFTUtilsBase):
    """Contains textual data mixed with ``span`` elements only.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.elements.extend([
            Prop('pcdata', required=True, prop_type=PCData),
            Prop('spans', prop_type=list, item_type=Span),
        ])
        # elements
        self.pcdata: PCData = None
        self.spans: Optional[List[Span]] = None
        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{str(self.pcdata)}{''.join(str(s) for s in self.spans)}"

    def _update_other_from_self(self, other):
        other.pcdata = self.pcdata
        other.spans = self.spans

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'text')
        return xml_tree


class URLRef(LIFTUtilsBase):
    """This is a URL with a caption.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('href', required=True, prop_type=URL),
        ])
        self.props.elements.extend([
            Prop('label', prop_type=Multitext),
        ])
        # attributes
        self.href: URL = None
        # elements
        self.label: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'urlref')
        return xml_tree


class Multitext(Text):
    """Allows for different representations of the same information.
    It can be in a given language, or in multiple languages.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.elements.extend([
            Prop('forms', prop_type=list, item_type=Form),
            Prop('traits', prop_type=list, item_type=Trait),
        ])
        # elements
        self.forms: Optional[List[Form]] = None
        self.traits: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        s = 'multitext'
        if self.forms:
            self.forms.sort()
            s = f"{self.forms[0].text} ({self.forms[0].lang})"
            ct = len(self.forms)
            if ct > 1:
                s = f"{s} ({ct} forms)"
        return s

    def _update_other_from_self(self, other):
        other.forms = self.forms
        other.text = self.text

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'multitext')
        return xml_tree


class Gloss(Form):
    """A representation of a sense's gloss.
    It's given in a particular language and script as specified by the ``lang``
    attribute.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.elements.extend([
            Prop('traits', prop_type=list, item_type=Trait),
        ])
        # elements
        self.traits: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.text} ({self.lang})"

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'gloss')
        return xml_tree


class Annotation(Multitext):
    """Provides a mechanism for adding meta-information to almost any element.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('name', required=True, prop_type=Key),
            Prop('value', required=True, prop_type=Key),
            Prop('who', prop_type=Key),
            Prop('when', prop_type=DateTime),
        ])
        # attributes
        self.name: Key = None
        self.value: Key = None
        self.who: Optional[Key] = None
        self.when: Optional[DateTime] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'annotation')
        return xml_tree


class Field(Multitext):
    """A generalised element to allow an application to store information.
    It's for information in a LIFT file that isn't explicitly described in the
    LIFT standard.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.attributes.extend([
            Prop('date_created', prop_type=DateTime),
            Prop('date_modified', prop_type=DateTime),
        ])
        if config.LIFT_VERSION == '0.13':
            self.props.attributes.extend([
                Prop('prop_type', required=True, prop_type=Key),
            ])
        else:
            self.props.attributes.extend([
                Prop('name', required=True, prop_type=Key),
            ])
        self.props.elements.extend([
            Prop('annotations', prop_type=list, item_type=Annotation),
        ])
        if config.LIFT_VERSION == '0.13':
            self.props.elements.extend([
                Prop('traits', prop_type=list, item_type=Flag),
                Prop('forms', prop_type=list, item_type=Span),
            ])
        else:
            self.props.elements.extend([
                Prop('traits', prop_type=list, item_type=Trait),
            ])
        # attributes
        if config.LIFT_VERSION == '0.13':
            self.prop_type: Key = None
        else:
            self.name: Key = None
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        if config.LIFT_VERSION == '0.13':
            self.traits: Optional[List[Flag]] = None
            self.forms: Optional[List[Span]] = None
        else:
            self.traits: Optional[List[Trait]] = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, 'field')
        return xml_tree


class Extensible(LIFTUtilsBase):
    """Used to provide certain extra information in a controlled way.

    :ivar Optional[DateTime] date_created: Contains a date/timestamp saying
        when the element was added to the dictionary.
    :ivar Optional[DateTime] date_modified: Contains a date/timestamp saying
        when the element was last changed.
    :ivar Optional[List[Field]] fields: Holds extra textual information.
    :ivar Optional[List[Trait]] traits: Adds type or constraint information.
    :ivar Optional[List[Annotation]] annotation: Adds meta-information
        describing the element.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = [
            Prop('date_created', prop_type=DateTime),
            Prop('date_modified', prop_type=DateTime),
        ]
        self.props.elements = [
            Prop('fields', prop_type=list, item_type=Field),
            Prop('traits', prop_type=list, item_type=Trait),
            Prop('annotations', prop_type=list, item_type=Annotation),
        ]
        # attributes
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.fields: Optional[List[Field]] = None
        if config.LIFT_VERSION == '0.13':
            # TODO: Find definition of "Flag" in v0.13.
            # self.traits: Optional[List[Flag]] = None
            self.traits: Optional[List[Trait]] = None
        else:
            self.traits: Optional[List[Trait]] = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_other_from_self(self, other):
        other.date_created = self.date_created
        other.date_modified = self.date_modified
        other.fields = self.fields
        other.traits = self.traits
        other.annotations = self.annotations

    def _add_attribs_to_xml_tree(self, xml_tree):
        for attrib in self.props.attributes:
            a = attrib.name
            x = config.XML_NAMES.get(a, a)
            xml_tree.set(x, self.__dict__.get(a))
        return xml_tree
