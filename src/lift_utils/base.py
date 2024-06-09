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
from .errors import RequiredValueException
from .utils import etree_to_obj_attributes
from .utils import etree_to_xmlstring
from .utils import obj_attributes_to_etree


class LIFTUtilsBase:
    """This is a base class for all LIFT-related objects in this package.

    :ivar etree._Element xml_tree: The object's current data.
    """
    def __init__(self, xml_tree: etree._Element = None):
        self.xml_tag = None
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = []
        self.props.elements = []

    def print(self, _format='xml'):
        """Print the object's data to stdout; as XML by default."""
        try:
            if _format == 'xml':
                print(self._to_xml(), flush=True)
            else:
                return
        except BrokenPipeError:
            sys.stdout = None

    def _add_list_item(self, _name, _class, **kwargs):
        new_obj = _class(**kwargs)
        if self.__dict__.get(_name) is None:
            self.__dict__[_name] = [new_obj]
        else:
            self.__dict__[_name].append(new_obj)
        return len(self.__dict__.get(_name)) - 1

    def _update_from_xml(self, xml_tree):
        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(self, self.xml_tag)
        return xml_tree

    def _to_xml(self, xml_tree=None):
        if xml_tree is None:
            xml_tree = self._to_xml_tree()
        return etree_to_xmlstring(xml_tree)


class Span(LIFTUtilsBase):
    """A Unicode string marked with language and formatting information.
    """

    def __init__(
        self,
        text: str = None,
        tail: str = None,
        lang: str = None,
        href: str = None,
        span_class: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
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
            Prop('span_items', prop_type=list, item_type=Span),
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
        self.span_items: Optional[List[Span]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif text is not None:
            self.pcdata = PCData(text)
            if tail is not None:
                self.tail = PCData(tail)
            if lang is not None:
                self.lang = Lang(lang)
            if href is not None:
                self.href = URL(href)
            if span_class is not None:
                self.class_ = span_class
        else:
            raise RequiredValueException(('text',))


class Trait(LIFTUtilsBase):
    """An important mechanism for giving type information to an object.
    It can also be used for adding binary constraints.
    """

    def __init__(
        self,
        name: str = None,
        value: str = None,
        trait_id: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
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
            Prop('annotation_items', prop_type=list, item_type=Annotation)
        )
        self.xml_tag = 'trait'
        # attributes
        self.name: Key = None
        self.value: Key = None
        self.id: Optional[Key] = None
        # elements
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif name is not None and value is not None:
            self.name = Key(name)
            self.value = Key(value)
            if trait_id is not None:
                self.id = Key(trait_id)
        else:
            raise RequiredValueException(('name', 'value'))

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
        super().__init__()


class Text(LIFTUtilsBase):
    """Contains textual data mixed with ``span`` elements only.
    """

    def __init__(
        self,
        text: str = None,
        xml_tree: Optional[etree._Element] = None,
        subinit=False
    ):
        super().__init__()
        # properties
        elems = [
            Prop('pcdata', required=True, prop_type=PCData),
            Prop('span_items', prop_type=list, item_type=Span),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'text'
        # elements
        self.pcdata = None
        self.span_items: Optional[List[Span]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._update_from_xml(xml_tree)
        elif text is not None:
            self.pcdata = PCData(text)
        else:
            raise RequiredValueException(('text',))

    def __str__(self):
        if self.span_items:
            s = f"{str(self.pcdata)}{''.join(str(s) for s in self.span_items)}"
        else:
            s = str(self.pcdata)
        return s


class Form(LIFTUtilsBase):
    """A representation of a string in a particular language and script.
    This is specified by the ``lang`` attribute.
    """

    def __init__(
        self,
        lang: Lang = None,
        text: Text = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        self.props.add_to(
            'attributes',
            Prop('lang', required=True, prop_type=Lang)
        )
        elems = [
            Prop('text', required=True, prop_type=Text),
            Prop('annotation_items', prop_type=list, item_type=Annotation),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'form'
        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._update_from_xml(xml_tree)
        elif lang is not None and text is not None:
            self.lang = Lang(lang)
            self.text = Text(text=text)
        else:
            raise RequiredValueException(('lang', 'text'))

    def __str__(self):
        return str(self.text)


class URLRef(LIFTUtilsBase):
    """This is a URL with a caption.
    """

    def __init__(
        self,
        href: str = None,
        label: dict = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
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
        self.href = None
        # elements
        self.label: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif href is not None:
            self.href = URL(href)
            if label is not None:
                self.set_label(label)
        else:
            raise RequiredValueException(('href',))

    def set_label(self, label_dict):
        if not isinstance(label_dict, dict):
            raise RequiredValueException(('dict of {{lang: text}} pairs',))
        self.label = Multitext(label_dict)

    def __str__(self):
        return str(self.href)


class Multitext(Text):
    """Allows for different representations of the same information.
    It can be in a given language, or in multiple languages.
    """

    def __init__(
        self,
        form_dict: dict = None,
        # trait_dict: dict = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=False)
        # properties
        elems = [
            Prop('form_items', prop_type=list, item_type=Form),
            Prop('trait_items', prop_type=list, item_type=Trait),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        # Multitext is only used as a super class for other classes, so it
        # doesn't have it's own XML tag.
        self.xml_tag = None
        # elements
        self.form_items: Optional[List[Form]] = None
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._update_from_xml(xml_tree)
        elif form_dict is not None:
            self.set_form_items(form_dict)

    def __str__(self):
        s = 'multitext'
        if self.form_items:
            # self.form_items.sort()
            s = f"{self.form_items[0].text} ({self.form_items[0].lang})"
            ct = len(self.form_items)
            if ct > 1:
                s = f"{s} ({ct} forms)"
        return s

    def set_form_items(self, form_dict):
        self.form_items = []
        for lg, tx in form_dict.items():
            self.form_items.append(Form(lang=lg, text=tx))


class Gloss(Form):
    """A representation of a sense's gloss.
    It's given in a particular language and script as specified by the ``lang``
    attribute.
    """

    def __init__(
        self,
        lang: str = None,
        text: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=False)
        # properties
        self.props.add_to(
            'elements',
            Prop('trait_items', prop_type=list, item_type=Trait)
        )
        self.xml_tag = 'gloss'
        # elements
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif lang is not None and text is not None:
            self.lang = Lang(lang)
            self.text = Text(text=text)
        else:
            raise RequiredValueException(('lang', 'text'))

    def __str__(self):
        return f"{self.text} ({self.lang})"

    def set_trait_items(self, trait_dict):
        self.trait_items = []
        for name, data in trait_dict.items():
            value = data.get('value')
            trait_id = data.get('trait_id')
            self.trait_items.append(
                Trait(name=name, value=value, trait_id=trait_id)
            )


class Annotation(Multitext):
    """Provides a mechanism for adding meta-information to almost any element.
    """

    def __init__(
        self,
        name: str = None,
        value: str = None,
        who: str = None,
        when: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
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
        elif name is not None and value is not None:
            self.name = Key(name)
            self.value = Key(value)
            if who is not None:
                self.who = Key(who)
            if when is not None:
                self.when = DateTime(when)
        else:
            raise RequiredValueException(('name', 'value'))


class Field(Multitext):
    """A generalised element to allow an application to store information.
    It's for information in a LIFT file that isn't explicitly described in the
    LIFT standard.
    """

    def __init__(
        self,
        field_type: str = None,
        name: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        attribs = [
            Prop('date_created', prop_type=DateTime),
            Prop('date_modified', prop_type=DateTime),
        ]
        if config.LIFT_VERSION == '0.13':
            attribs.append(Prop('type', required=True, prop_type=Key))
        else:
            attribs.append(Prop('name', required=True, prop_type=Key))
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('annotation_items', prop_type=list, item_type=Annotation),
            Prop('trait_items', prop_type=list, item_type=Trait),
        ]
        if config.LIFT_VERSION == '0.13':
            elems.append(Prop('form_items', prop_type=list, item_type=Span))
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'field'
        # attributes
        if config.LIFT_VERSION == '0.13':
            self.type: Key = None
        else:
            self.name: Key = None
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        if config.LIFT_VERSION == '0.13':
            # self.trait_items: Optional[List[Flag]] = None
            self.trait_items: Optional[List[Trait]] = None
            self.form_items: Optional[List[Span]] = None
        else:
            self.trait_items: Optional[List[Trait]] = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif config.LIFT_VERSION == '0.13' and field_type is not None:
            self.type = Key(field_type)
        elif config.LIFT_VERSION == '0.15' and name is not None:
            self.name = Key(name)
        else:
            if config.LIFT_VERSION == '0.13':
                value = 'field_type'
            else:
                value = 'name'
            raise RequiredValueException((value,))


class Extensible(LIFTUtilsBase):
    """Used to provide certain extra information in a controlled way.

    :ivar Optional[DateTime] date_created: Contains a date/timestamp saying
        when the element was added to the dictionary.
    :ivar Optional[DateTime] date_modified: Contains a date/timestamp saying
        when the element was last changed.
    :ivar Optional[List[Field]] field_items: Holds extra textual information.
    :ivar Optional[List[Trait]] trait_items: Adds type or constraint
        information.
    :ivar Optional[List[Annotation]] annotation: Adds meta-information
        describing the element.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        attribs = [
            Prop('date_created', prop_type=DateTime),
            Prop('date_modified', prop_type=DateTime),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('field_items', prop_type=list, item_type=Field),
            Prop('trait_items', prop_type=list, item_type=Trait),
            Prop('annotation_items', prop_type=list, item_type=Annotation),
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
        self.field_items: Optional[List[Field]] = None
        if config.LIFT_VERSION == '0.13':
            # TODO: Find definition of "Flag" in v0.13?
            # self.trait_items: Optional[List[Flag]] = None
            self.trait_items: Optional[List[Trait]] = None
        else:
            self.trait_items: Optional[List[Trait]] = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def add_annotation(self, name=None, value=None, who=None, when=None):
        return self._add_list_item(
            'annotation_items',
            Annotation,
            name=name,
            value=value,
            who=who,
            when=when,
        )

    def add_field(self, name=None):
        if config.LIFT_VERSION == '0.13':
            kwargs = {'field_type': name}
        else:
            kwargs = {'name': name}
        return self._add_list_item('field_items', Field, **kwargs)

    def add_trait(self, name=None, value=None, trait_id=None):
        return self._add_list_item(
            'trait_items',
            Trait,
            name=name,
            value=value,
            trait_id=trait_id,
        )

    def _add_attribs_to_xml_tree(self, xml_tree):
        for attrib in self.props.attributes:
            a = attrib.name
            x = config.XML_NAMES.get(a, a)
            xml_tree.set(x, self.__dict__.get(a))
        return xml_tree

    def set_date_created(self):
        self.date_created = DateTime()

    def set_date_modified(self):
        self.date_modified = DateTime()
