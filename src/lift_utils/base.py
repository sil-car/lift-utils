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
from .datatypes import URL


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

    _props = {
        'attributes': {
            'required': [],
            'optional': ['lang', 'href', 'style_class'],
        },
        'elements': {
            'required': ['pcdata'],
            'optional': ['spans'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # attributes
        self.lang: Optional[Lang] = None
        self.href: Optional[URL] = None
        self.style_class: Optional[str] = None
        # elements
        self.pcdata = None
        self.spans: Optional[List[str]] = None  # Type should be 'Span'

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        for k, v in xml_tree.attrib.items():
            if k == 'lang':
                self.lang = Lang(k)
            elif k == 'href':
                self.href = URL(v)
            elif k == 'class':
                self.style_class = v

        if xml_tree.text is not None:
            self.pcdata = PCData(xml_tree.text)

        for c in xml_tree.getchildren():
            if c.tag == 'span':
                s = Span(c)
                if not self.spans:
                    self.spans = [s]
                else:
                    self.spans.append(s)

    def _build_xml_tree(self):
        # This is basically the reverse function of _update_from_xml.
        root_tag = 'span'
        attribs = (
            Span._props.get('attributes').get('required')
            + Span._props.get('attributes').get('optional')
        )
        elems = (
            Span._props.get('elements').get('required')
            + Span._props.get('elements').get('optional')
        )
        root = etree.Element(root_tag)
        for a in attribs:
            root.set(a, self.__dict__.get(a))
        for e in elems:
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

    _props = {
        'attributes': {
            'required': ['name', 'value'],
            'optional': ['id'],
        },
        'elements': {
            'required': [],
            'optional': ['annotations'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
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

        for k, v in xml_tree.attrib.items():
            if k == 'name':
                self.name = Key(v)
            elif k == 'value':
                self.value = Key(v)
            elif k == 'id':
                self.id = Key(v)

        for c in xml_tree.getchildren():
            if c.tag == 'annotation':
                a = Annotation(c)
                if not self.annotations:
                    self.annotations = [a]
                else:
                    self.annotations.append(a)

    def _build_xml_tree(self):
        # This is basically the reverse function of _update_from_xml.
        root_tag = 'trait'
        attribs = (
            Trait._props.get('attributes').get('required')
            + Trait._props.get('attributes').get('optional')
        )
        elems = (
            Trait._props.get('elements').get('required')
            + Trait._props.get('elements').get('optional')
        )
        root = etree.Element(root_tag)
        for a in attribs:
            root.set(a, self.__dict__.get(a))
        for e in elems:
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

    _props = {
        'attributes': {
            'required': ['lang'],
            'optional': [],
        },
        'elements': {
            'required': ['text'],
            'optional': ['annotations'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotations: Optional[List] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return str(self.text)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        for k, v in xml_tree.attrib.items():
            if k == 'lang':
                self.lang = Lang(v)

        for c in xml_tree.getchildren():
            if c.tag == 'text':
                self.text = Text(c.text)
            elif c.tag == 'annotation':
                a = Annotation(c)
                if not self.annotations:
                    self.annotations = [a]
                else:
                    self.annotations.append(a)

    def _update_other_from_self(self, other):
        other.lang = self.lang
        other.text = self.text
        other.annotations = self.annotations


class Text(Form):
    """Contains textual data mixed with ``span`` elements only.

    .. note:: It only inherits from ``Form`` in LIFT v0.13 (FieldWorks).
    """

    _props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': ['pcdata'],
            'optional': ['spans'],
        },
    }

    def __init__(
        self,
        text=None,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
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

        if xml_tree.text:
            self.text = PCData(xml_tree.text)

        for c in xml_tree.getchildren():
            if c.tag == 'span':
                if not self.spans:
                    s = Span(c)
                    self.spans = [s]
                else:
                    self.spans.append(s)

    def __str__(self):
        return str(self.pcdata)

    def _update_other_from_self(self, other):
        other.pcdata = self.pcdata
        other.spans = self.spans


class Multitext(Text):
    """Allows for different representations of the same information.
    It can be in a given language, or in multiple languages.
    """

    _props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': ['forms', 'text'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # elements
        self.forms = None
        self.text = None  # deprecated in v0.15

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

        if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
            txt = Text(xml_tree)
            txt._update_other_from_self(self)
            del txt

        for c in xml_tree.getchildren():
            if c.tag == 'form':
                f = Form(c)
                if not self.forms:
                    self.forms = [f]
                else:
                    self.forms.append(f)
            elif c.tag == 'text':
                if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
                    self.text = c.text

    def _update_other_from_self(self, other):
        other.forms = self.forms
        other.text = self.text


class Gloss(Form):
    """A representation of a sense's gloss.
    It's given in a particular language and script as specified by the ``lang``
    attribute.
    """

    _props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': ['traits'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
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

        for c in xml_tree.getchildren():
            if c.tag == 'trait':
                t = Trait(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)


class URLRef(LIFTUtilsBase):
    """This is a URL with a caption.
    """

    _props = {
        'attributes': {
            'required': ['href'],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': ['label'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # attributes
        self.href: URL = None
        # elements
        self.label: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        for k, v in xml_tree.attrib.items():
            if k == 'href':
                self.href = URL(v)

        for c in xml_tree.getchildren():
            if c.tag == 'label':
                self.label = Multitext(c)


class Annotation(Multitext):
    """Provides a mechanism for adding meta-information to almost any element.
    """

    _props = {
        'attributes': {
            'required': ['name', 'value'],
            'optional': ['who', 'when'],
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
            super()._update_from_xml(xml_tree)
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

        for k, v in xml_tree.attrib.items():
            if k == 'name':
                self.name = Key(v)
            elif k == 'value':
                self.value = Key(v)
            elif k == 'who':
                self.who = Key(v)
            elif k == 'when':
                self.when = DateTime(v)


class Field(Multitext):
    """A generalised element to allow an application to store information.
    It's for information in a LIFT file that isn't explicitly described in the
    LIFT standard.
    """

    _props = {
        'attributes': {
            'required': ['name'],
            'optional': ['date_created', 'date_modified'],
        },
        'elements': {
            'required': [],
            'optional': ['traits', 'annotations'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # attributes
        self.name: str = None
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
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

        for k, v in xml_tree.attrib.items():
            if k == 'name':
                self.name = v
            elif k == 'dateCreated':
                self.date_created = DateTime(v)
            elif k == 'dateModified':
                self.date_modified = DateTime(v)

        for c in xml_tree.getchildren():
            if c.tag == 'trait':
                if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
                    t = Flag(c)
                else:
                    t = Trait(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)
            elif c.tag == 'form':
                if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
                    s = Span(c)
                    if not self.forms:
                        self.forms = [s]
                    else:
                        self.forms.append(s)
            elif c.tag == 'annotation':
                a = Annotation(c)
                if not self.annotations:
                    self.annotations = [a]
                else:
                    self.annotations.append(a)


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

    _props = {
        'attributes': {
            'required': [],
            'optional': ['date_created', 'date_modified'],
        },
        'elements': {
            'required': [],
            'optional': ['fields', 'traits', 'annotations'],
        },
    }

    def __init__(
        self,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # attributes
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.fields: Optional[List[Field]] = None
        if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
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

        for k, v in xml_tree.attrib.items():
            if k == 'dateCreated':
                self.date_created = v
            elif k == 'dateModified':
                self.date_modified = v

        for c in xml_tree.getchildren():
            if c.tag == 'field':
                f = Field(c)
                if not self.fields:
                    self.fields = [f]
                else:
                    self.fields.append(f)
            elif c.tag == 'trait':
                t = Trait(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)
            elif c.tag == 'annotation':
                a = Annotation(c)
                if not self.annotations:
                    self.annotations = [a]
                else:
                    self.annotations.append(a)

    def _update_other_from_self(self, other):
        other.date_created = self.date_created
        other.date_modified = self.date_modified
        other.fields = self.fields
        other.traits = self.traits
        other.annotations = self.annotations
