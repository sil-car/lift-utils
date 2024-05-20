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


class LIFTUtilsBase:
    """This is a base class for all LIFT-related objects in this package.

    :ivar etree xml_tree: The object's current data.
    """
    def __init__(self, xml_tree: etree = None):
        self.xml_tree = None
        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def to_xml(self):
        """Convert the object's data to XML."""
        return etree.tostring(
            self.xml_tree,
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()

    def print(self, format='xml'):
        """Print the object's data to stdout; as XML by default."""
        try:
            if format == 'xml':
                print(self.to_xml(), flush=True)
            else:
                return
        except BrokenPipeError:
            sys.stdout = None

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree


class Span(LIFTUtilsBase):
    """A Unicode string marked with language and formatting information.
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
            Prop('lang', ptype=Lang),
            Prop('href', ptype=URL),
            Prop('class_', ptype=str),
        ]
        self.props.elements = [
            Prop('pcdata', required=True, ptype=PCData),
            Prop('spans', ptype=list, ltype=Span),
        ]
        # attributes
        self.lang: Optional[Lang] = None
        self.href: Optional[URL] = None
        self.class_: Optional[str] = None
        # elements
        self.pcdata: PCData = None
        self.spans: Optional[List[Span]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)

    def _build_xml_tree(self):
        # This is basically the reverse function of _update_from_xml.
        root_tag = 'span'
        root = etree.Element(root_tag)
        for attrib in self.props.attributes:
            a = attrib.name
            root.set(a, self.__dict__.get(a))
        for elem in self.props.elements:
            e = elem.name
            if isinstance(self.__dict__.get(e), list):
                for i in self.__dict__.get(e):
                    etree.SubElement(root, e[:-1])
            elif hasattr(self.__dict__.get(e), 'xml_tree'):
                e._build_xml_tree()
            elif e == 'pcdata':
                root.text = self.__dict__.get(e)
            elif self.__dict__.get(e):
                etree.SubElement(root, e)
        return root


class Trait(LIFTUtilsBase):
    """An important mechanism for giving type information to an object.
    It can also be used for adding binary constraints.
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
            Prop('value', required=True, ptype=Key),
            Prop('id', ptype=Key),
        ]
        self.props.elements = [
            Prop('annotations', ptype=list, ltype=Annotation),
        ]
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

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)

    def _build_xml_tree(self):
        # This is basically the reverse function of _update_from_xml.
        root_tag = 'trait'
        root = etree.Element(root_tag)
        for attrib in self.props.attributes:
            a = attrib.name
            root.set(a, self.__dict__.get(a))
        for elem in self.props.elements:
            e = elem.name
            if isinstance(self.__dict__.get(e), list):
                # list element
                for i in self.__dict__.get(e):
                    if hasattr(self.__dict__.get(e), 'xml_tree'):
                        root.append(e._build_xml_tree())
                    else:
                        etree.SubElement(root, e[:-1])
            elif hasattr(self.__dict__.get(e), 'xml_tree'):
                # element with own xml_tree to be generated
                root.append(e._build_xml_tree())
            elif e == 'pcdata':
                # text data
                root.text = self.__dict__.get(e)
                # new empty element
            elif self.__dict__.get(e):
                etree.SubElement(root, e)
        return root


class Flag(Trait):
    """An important mechanism for giving type information to an object.
    It can also be use for adding binary constraints.

    .. note:: Used by LIFT v0.13 (FieldWorks). Mentioned in specification but
        not defined; assumed to be equivalent to ``Trait``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
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
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = [
            Prop('lang', required=True, ptype=Lang),
        ]
        self.props.elements = [
            Prop('text', required=True, ptype=Text),
            Prop('annotations', ptype=list, ltype=Annotation),
        ]
        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return str(self.text)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)

    def _update_other_from_self(self, other):
        other.lang = self.lang
        other.text = self.text
        other.annotations = self.annotations


class Text(Form):
    """Contains textual data mixed with ``span`` elements only.

    .. note:: It only inherits from ``Form`` in LIFT v0.13 (FieldWorks).
    """

    def __init__(
        self,
        text=None,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.elements = [
            Prop('pcdata', required=True, ptype=PCData),
            Prop('spans', ptype=list, ltype=Span),
        ]
        # elements
        self.pcdata: str = None
        if text is not None:
            self.pcdata = PCData(text)
        self.spans: Optional[List[Span]] = None
        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        f = Form(xml_tree)
        f._update_other_from_self(self)
        del f

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)

    def __str__(self):
        return str(self.pcdata)

    def _update_other_from_self(self, other):
        other.pcdata = self.pcdata
        other.spans = self.spans


class Multitext(Text):
    """Allows for different representations of the same information.
    It can be in a given language, or in multiple languages.
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
            Prop('forms', ptype=list, ltype=Form),
            Prop('text', ptype=str),
        ]
        # elements
        self.forms: Optional[List[Form]] = None
        self.text: Optional[str] = None  # deprecated in v0.15

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

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        if config.LIFT_VERSION == '0.13':
            txt = Text(xml_tree)
            txt._update_other_from_self(self)
            del txt

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)

    def _update_other_from_self(self, other):
        other.forms = self.forms
        other.text = self.text


class Gloss(Form):
    """A representation of a sense's gloss.
    It's given in a particular language and script as specified by the ``lang``
    attribute.
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
            Prop('traits', ptype=list, ltype=Trait),
        ]
        # elements
        self.traits: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.text} ({self.lang})"

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        form = Form(xml_tree)
        form._update_other_from_self(self)
        del form

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class URLRef(LIFTUtilsBase):
    """This is a URL with a caption.
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
            Prop('href', required=True, ptype=URL),
        ]
        self.props.elements = [
            Prop('label', ptype=Multitext),
        ]
        # attributes
        self.href: URL = None
        # elements
        self.label: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class Annotation(Multitext):
    """Provides a mechanism for adding meta-information to almost any element.
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
            Prop('value', required=True, ptype=Key),
            Prop('who', ptype=Key),
            Prop('when', ptype=DateTime),
        ]
        # attributes
        self.name: Key = None
        self.value: Key = None
        self.who: Optional[Key] = None
        self.when: Optional[DateTime] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        mul = Multitext(xml_tree)
        mul._update_other_from_self(self)
        del mul

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


class Field(Multitext):
    """A generalised element to allow an application to store information.
    It's for information in a LIFT file that isn't explicitly described in the
    LIFT standard.
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
            Prop('date_created', ptype=DateTime),
            Prop('date_modified', ptype=DateTime),
        ]
        if config.LIFT_VERSION == '0.13':
            self.props.attributes.append(Prop(
                'type',
                required=True,
                ptype=Key
            ))
        else:
            self.props.attributes.append(Prop(
                'name',
                required=True,
                ptype=Key
            ))
        self.props.elements = [
            Prop('annotations', ptype=list, ltype=Annotation),
        ]
        if config.LIFT_VERSION == '0.13':
            self.props.elements.append(Prop('traits', ptype=list, ltype=Flag))
            self.props.elements.append(Prop('forms', ptype=list, ltype=Span))
        else:
            self.props.elements.append(Prop('traits', ptype=list, ltype=Trait))
        # attributes
        if config.LIFT_VERSION == '0.13':
            self.type: Key = None
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

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        mul = Multitext(xml_tree)
        mul._update_other_from_self(self)
        del mul

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)


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
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = [
            Prop('date_created', ptype=DateTime),
            Prop('date_modified', ptype=DateTime),
        ]
        self.props.elements = [
            Prop('fields', ptype=list, ltype=Field),
            Prop('traits', ptype=list, ltype=Trait),
            Prop('annotations', ptype=list, ltype=Annotation),
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

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)

    def _update_other_from_self(self, other):
        other.date_created = self.date_created
        other.date_modified = self.date_modified
        other.fields = self.fields
        other.traits = self.traits
        other.annotations = self.annotations
