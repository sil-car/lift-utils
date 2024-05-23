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
        self.xml_tag = None
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = []
        self.props.elements = []

    # def to_xml(self):
    #     """Convert the object's data to XML."""
    #     if self.xml_tree:
    #         return etree.tostring(
    #             self.xml_tree,
    #             encoding='UTF-8',
    #             pretty_print=True,
    #             xml_declaration=True
    #         ).decode().rstrip()

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

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, self.xml_tag)
        return xml_tree


class Span(LIFTUtilsBase):
    """A Unicode string marked with language and formatting information.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        attribs = [
            Prop('lang', prop_type=Lang),
            Prop('href', prop_type=URL),
            Prop('class_', prop_type=str),            
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('pcdata', required=True, prop_type=PCData),
            Prop('tail', prop_type=PCData),
            Prop('spans', prop_type=list, item_type=Span),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'span'
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
        attribs = [
            Prop('name', required=True, prop_type=Key),
            Prop('value', required=True, prop_type=Key),
            Prop('id', prop_type=Key),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        self.props.add_to(
            'elements',
            Prop('annotations', prop_type=list, item_type=Annotation)
        )
        self.xml_tag = 'trait'
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
        super().__init__(xml_tree)


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
        self.props.add_to(
            'attributes',
            Prop('lang', required=True, prop_type=Lang)
        )
        elems = [
            Prop('text', required=True, prop_type=Text),
            Prop('annotations', prop_type=list, item_type=Annotation),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'form'
        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return str(self.text)


class Text(LIFTUtilsBase):
    """Contains textual data mixed with ``span`` elements only.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        elems = [
            Prop('pcdata', required=True, prop_type=PCData),
            Prop('spans', prop_type=list, item_type=Span),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'text'
        # elements
        self.pcdata: PCData = None
        self.spans: Optional[List[Span]] = None
        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{str(self.pcdata)}{''.join(str(s) for s in self.spans)}"


class URLRef(LIFTUtilsBase):
    """This is a URL with a caption.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        self.props.add_to(
            'attributes',
            Prop('href', required=True, prop_type=URL)
        )
        self.props.add_to(
            'elements',
            Prop('label', prop_type=Multitext)
        )
        self.xml_tag = 'urlref'
        # attributes
        self.href: URL = None
        # elements
        self.label: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


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
        elems = [
            Prop('forms', prop_type=list, item_type=Form),
            Prop('traits', prop_type=list, item_type=Trait),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        # Multitext is only used as a super class for other classes, so it
        # doesn't have it's own XML tag.
        self.xml_tag = None
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
        self.props.add_to(
            'elements',
            Prop('traits', prop_type=list, item_type=Trait)
        )
        self.xml_tag = 'gloss'
        # elements
        self.traits: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.text} ({self.lang})"


class Annotation(Multitext):
    """Provides a mechanism for adding meta-information to almost any element.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree)
        # properties
        attribs = [
            Prop('name', required=True, prop_type=Key),
            Prop('value', required=True, prop_type=Key),
            Prop('who', prop_type=Key),
            Prop('when', prop_type=DateTime),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        self.xml_tag = 'annotation'
        # attributes
        self.name: Key = None
        self.value: Key = None
        self.who: Optional[Key] = None
        self.when: Optional[DateTime] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


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
        attribs = [
            Prop('date_created', prop_type=DateTime),
            Prop('date_modified', prop_type=DateTime),
        ]
        if config.LIFT_VERSION == '0.13':
            attribs.append(Prop('prop_type', required=True, prop_type=Key))
        else:
            attribs.append(Prop('name', required=True, prop_type=Key))
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('annotations', prop_type=list, item_type=Annotation),
            Prop('traits', prop_type=list, item_type=Trait),
        ]
        if config.LIFT_VERSION == '0.13':
            elems.append(Prop('forms', prop_type=list, item_type=Span))
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'field'
        # attributes
        if config.LIFT_VERSION == '0.13':
            self.prop_type: Key = None
        else:
            self.name: Key = None
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        if config.LIFT_VERSION == '0.13':
            # self.traits: Optional[List[Flag]] = None
            self.traits: Optional[List[Trait]] = None
            self.forms: Optional[List[Span]] = None
        else:
            self.traits: Optional[List[Trait]] = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


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
        attribs = [
            Prop('date_created', prop_type=DateTime),
            Prop('date_modified', prop_type=DateTime),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('fields', prop_type=list, item_type=Field),
            Prop('traits', prop_type=list, item_type=Trait),
            Prop('annotations', prop_type=list, item_type=Annotation),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        # Extensible is only used as a super class for other classes, so it
        # doesn't need its own XML tag.
        self.xml_tag = None
        # attributes
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.fields: Optional[List[Field]] = None
        if config.LIFT_VERSION == '0.13':
            # TODO: Find definition of "Flag" in v0.13?
            # self.traits: Optional[List[Flag]] = None
            self.traits: Optional[List[Trait]] = None
        else:
            self.traits: Optional[List[Trait]] = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _add_attribs_to_xml_tree(self, xml_tree):
        for attrib in self.props.attributes:
            a = attrib.name
            x = config.XML_NAMES.get(a, a)
            xml_tree.set(x, self.__dict__.get(a))
        return xml_tree
