"""Manipulate base linguistic elements."""

import sys
from typing import List, Optional

from lxml import etree

from . import config
from .datatypes import URL, DateTime, Key, Lang, PCData
from .errors import RequiredValueError
from .utils import etree_to_xmlstring


class LIFTUtilsBase:
    """This is a base class for all LIFT nodes.

    :ivar etree._Element xml_tree: The node's current data.
    """

    XML_TAG = None
    XML_PY_NAMES = {
        # keys are LIFT XML tags; values are Python object properties
        "abbrev": "abbrev_items",
        "annotation": "annotation_items",
        "class": "class_",
        "dateCreated": "date_created",
        "dateDeleted": "date_deleted",
        "dateModified": "date_modified",
        "description": "description_items",
        "entry": "entry_items",
        "etymology": "etymology_items",
        "example": "example_items",
        "field": "field_items",
        "form": "form_items",
        "gloss": "gloss_items",
        "grammatical-info": "grammatical_info",
        "illustration": "illustration_items",
        "label": "label_items",
        "lexical-unit": "lexical_unit",
        "media": "media_items",
        "note": "note_items",
        "option-range": "option_range",
        "pronunciation": "pronunciation_items",
        "range-element": "range_element_items",
        "range": "range_items",
        "relation": "relation_items",
        "reversal": "reversal_items",
        "sense": "sense_items",
        "span": "span_items",
        "subsense": "subsense_items",
        "trait": "trait_items",
        "translation": "translation_items",
        "usage": "usage_items",
        "variant": "variant_items",
        "writing-system": "writing_system",
    }

    def __init__(self, parent_item=None, xml_tree: etree._Element = None):
        # Initialize property values.
        self._attributes_required = set()
        self._attributes_optional = set()
        self._elements_required = set()
        self._elements_optional = set()
        # Store a cumulative dict of key="tag name," value="Python class". This
        # can't be defined declaratively because classes must be defined first,
        # but this also needs to be referred to before all classes are defined.
        self.tag_classes = {"tail": PCData}
        # Link to parent node for tree traversal.
        self.parent_item = parent_item

    def print(self, _format="xml"):
        """Print the node's data to stdout; as XML by default."""
        try:
            if _format == "xml":
                print(self._to_xml(), flush=True)
            else:
                raise NotImplementedError
        except BrokenPipeError:
            sys.stdout = None

    def prop_name_from_xml_name(self, xml_name):
        """Return the object property name from the given XML attribute or
        element name."""

        name = None
        exc = {
            "description": (
                "FieldDefinition",
                "Header",
                "Range",
                "Range13",
            ),
            "form": ("Etymology",),
            "label": (
                "FieldDefinition",
                "URLRef",
            ),
        }
        for x_name, classes in exc.items():
            if self.__class__.__name__ in classes and xml_name == x_name:
                # Exceptional situations where "description" is the python attrib
                # rather than "description_items", so the XML_PY_NAMES conversion
                # dict should not be used.
                name = xml_name
        if name is None:
            name = self.XML_PY_NAMES.get(xml_name, xml_name)
        if config.LIFT_VERSION == "0.13":
            if self.__class__.__name__ == "Field" and name == "name":
                name = "type"
        else:
            if self.__class__.__name__ == "Field" and name == "type":
                name = "name"
        return name

    def show(self):
        """Print an overview of the object in the terminal window."""
        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                print(f"{k}: {v}")

    def _add_list_item(self, _name, _class, **kwargs):
        new_obj = _class(parent_item=self, **kwargs)
        if getattr(self, _name) is None:
            setattr(self, _name, [new_obj])
        else:
            getattr(self, _name).append(new_obj)
        return new_obj

    def _from_xml_tree(self, xml_tree):
        # Convert XML attributes to python properties.
        attribs = [a for a in self._attributes_required]
        attribs.extend([a for a in self._attributes_optional])
        for xml_name in attribs:
            py_name = self.prop_name_from_xml_name(xml_name)
            py_cls = self.tag_classes.get(xml_name)
            if xml_name in xml_tree.attrib.keys():
                setattr(
                    self,
                    py_name,
                    py_cls(xml_tree.attrib.get(xml_name)),
                )

        # Convert properties to XML elements.
        elems = [e for e in self._elements_required]
        elems.extend([e for e in self._elements_optional])
        for xml_name in elems:
            py_name = self.prop_name_from_xml_name(xml_name)
            py_cls = self.tag_classes.get(xml_name)
            if xml_name == "pcdata":
                if xml_tree.text:
                    setattr(self, py_name, py_cls(xml_tree.text))
                continue
            elif xml_name == "tail":
                if xml_tree.tail:
                    setattr(self, py_name, py_cls(xml_tree.tail))
                continue

            # Handle child elements.
            for c in xml_tree.getchildren():
                if c.tag == xml_name:
                    if py_name.endswith("_items"):  # list-like obj/elem
                        if not getattr(self, py_name):
                            # Instantiate list-like object.
                            setattr(self, py_name, list())
                        getattr(self, py_name).append(
                            py_cls(xml_tree=c, parent_item=self)
                        )
                    else:  # single element
                        setattr(self, py_name, py_cls(xml_tree=c, parent_item=self))

    def _to_xml_tree(self, tag=None):
        # TODO: Why isn't self.XML_TAG sufficient in every case here?
        if tag:
            xml_tag = tag
        else:
            xml_tag = self.XML_TAG
        xml_tree = etree.Element(xml_tag)

        # Convert properties to XML attributes.
        attribs = [a for a in self._attributes_required]
        attribs.extend([a for a in self._attributes_optional])
        for xml_name in attribs:
            # Get attribute's value from attribute's XML name, which might be
            # different from the Python name.
            val = getattr(self, self.prop_name_from_xml_name(xml_name))
            if val is not None:
                xml_tree.set(xml_name, str(val))

        # Convert properties to XML elements.
        elems = [e for e in self._elements_required]
        elems.extend([e for e in self._elements_optional])
        for xml_name in elems:
            py_name = self.prop_name_from_xml_name(xml_name)
            val = getattr(self, py_name)
            if not val:
                continue
            if hasattr(val, "append"):  # list-like child element
                for o in getattr(self, py_name):
                    xml_tree.append(o._to_xml_tree(tag=xml_name))
            elif py_name == "pcdata":  # special text element
                xml_tree.text = val
            elif py_name == "tail":  # special tail element
                xml_tree.tail = val
            else:  # single child element
                o = getattr(self, py_name)
                xml_tree.append(o._to_xml_tree(tag=xml_name))
        return xml_tree

    def _to_xml(self, xml_tree=None):
        if xml_tree is None:
            xml_tree = self._to_xml_tree()
        return etree_to_xmlstring(xml_tree)

    def _update_attribs_and_elems(self):
        for prop_type, prop_data in self._properties.items():
            for importance, values in prop_data.items():
                getattr(self, f"_{prop_type}_{importance}").update(values)


class Span(LIFTUtilsBase):
    """A Unicode string marked with language and formatting information."""

    XML_TAG = "span"

    def __init__(
        self,
        text: str = None,
        tail: str = None,
        lang: str = None,
        href: str = None,
        span_class: str = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._attributes_required = set()
        self._attributes_optional = set(("class", "href", "lang"))
        self._elements_required = set(("pcdata",))
        self._elements_optional = set(("span", "tail"))
        self.tag_classes.update(
            {
                "lang": Lang,
                "href": URL,
                "class": str,
                "pcdata": PCData,
                "span": Span,
            }
        )

        # attributes
        self.lang: Optional[Lang] = None
        self.href: Optional[URL] = None
        self.class_: Optional[str] = None
        # elements
        self.pcdata: PCData = None
        self.tail: Optional[PCData] = None
        self.span_items: Optional[List[Span]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)
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
            raise RequiredValueError(("text",))

    def __str__(self):
        s = self.pcdata
        if self.span_items:
            for item in self.span_items:
                s += item.pcdata
                if item.tail:
                    s += item.tail
        if self.tail:
            s += self.tail


class Trait(LIFTUtilsBase):
    """An important mechanism for giving type information to an object.
    It can also be used for adding binary constraints.
    """

    XML_TAG = "trait"

    def __init__(
        self,
        name: str = None,
        value: str = None,
        trait_id: str = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("name", "value"))
        self._attributes_optional = set(("id",))
        self._elements_required = set()
        self._elements_optional = set(("annotation",))
        self.tag_classes.update(
            {
                "name": Key,
                "value": Key,
                "id": Key,
                "annotation": Annotation,
            }
        )

        # attributes
        self.name: Key = None
        self.value: Key = None
        self.id: Optional[Key] = None
        # elements
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)
        elif name is not None and value is not None:
            self.name = Key(name)
            self.value = Key(value)
            if trait_id is not None:
                self.id = Key(trait_id)
        else:
            raise RequiredValueError(("name", "value"))

    def __str__(self):
        return f"{self.name}: {self.value}"


class Flag(Trait):
    """An important mechanism for giving type information to an object.
    It can also be use for adding binary constraints.

    .. note:: Used by LIFT v0.13 (FieldWorks). Mentioned in specification but
        not defined; assumed to be equivalent to ``Trait``.
    """

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)


class Text(LIFTUtilsBase):
    """Contains textual data mixed with ``span`` elements only."""

    XML_TAG = "text"

    def __init__(
        self,
        text: str = None,
        xml_tree: Optional[etree._Element] = None,
        subinit=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._attributes_required = set()
        self._attributes_optional = set()
        self._elements_required = set(("pcdata",))
        self._elements_optional = set(("span",))
        self.tag_classes.update(
            {
                "pcdata": PCData,
                "span": Span,
            }
        )

        # elements
        self.pcdata: PCData = None
        self.span_items: Optional[List[Span]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._from_xml_tree(xml_tree)
        elif text is not None:
            self.pcdata = PCData(text)
        else:
            raise RequiredValueError(("text",))

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

    XML_TAG = "form"

    def __init__(
        self,
        lang: Lang = None,
        text: Text = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("lang",))
        self._attributes_optional = set()
        self._elements_required = set(("text",))
        self._elements_optional = set(("annotation",))
        self.tag_classes.update(
            {
                "lang": Lang,
                "text": Text,
                "annotation": Annotation,
            }
        )

        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._from_xml_tree(xml_tree)
        elif lang is not None and text is not None:
            self.lang = Lang(lang)
            self.text = Text(text=text)
        else:
            raise RequiredValueError(("lang", "text"))

    def __str__(self):
        return str(self.text)


class URLRef(LIFTUtilsBase):
    """This is a URL with a caption."""

    XML_TAG = "urlref"

    def __init__(
        self,
        href: str = None,
        label: dict = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("href",))
        self._attributes_optional = set()
        self._elements_required = set()
        self._elements_optional = set(("label",))
        self.tag_classes.update(
            {
                "href": URL,
                "label": Multitext,
            }
        )

        # attributes
        self.href: URL = None
        # elements
        # NOTE: `label` elements are not explicitly defined as possibly having
        # multple values here, but they are for LiftRanges and RangeElements.
        self.label: Optional[Multitext] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)
        elif href is not None:
            self.href = URL(href)
            if label is not None:
                self.set_label(label)
        else:
            raise RequiredValueError(("href",))

    def set_label(self, label_dict):
        if not isinstance(label_dict, dict):
            raise RequiredValueError(("dict of {{lang: text}} pairs",))
        self.label = Multitext(label_dict)

    def __str__(self):
        return str(self.href)


class Multitext(Text):
    """Allows for different representations of the same information.
    It can be in a given language, or in multiple languages.
    """

    # Multitext is only used as a super class for other classes, so it
    # doesn't have it's own XML tag.
    XML_TAG = None

    def __init__(
        self,
        form_dict: dict = None,
        # trait_dict: dict = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(
            xml_tree=False,
            **kwargs,
        )
        self._attributes_required = set()
        self._attributes_optional = set()
        self._elements_required = set()
        self._elements_optional = set(("form", "pcdata", "span", "trait"))
        self.tag_classes.update(
            {
                "form": Form,
                "trait": Trait,
            }
        )

        # elements
        self.form_items: Optional[List[Form]] = None
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._from_xml_tree(xml_tree)
        elif form_dict is not None:
            self.set_form_items(form_dict)

    def __str__(self):
        s = "multitext"
        if self.form_items:
            # self.form_items.sort()
            s = f"{self.form_items[0].text} ({self.form_items[0].lang})"
            ct = len(self.form_items)
            if ct > 1:
                s = f"{s} ({ct} forms)"
        return s

    def get_form_by_lang(self, lang):
        """Return first form item with matching ``lang`` attribute.

        :var str lang: Language code; e.g. "en".
        """
        for f in self.form_items:
            if f.lang == lang:
                return f

    def set_form_items(self, form_dict):
        self.form_items = []
        for lg, tx in form_dict.items():
            self.form_items.append(Form(lang=lg, text=tx))


class Gloss(Form):
    """A representation of a sense's gloss.
    It's given in a particular language and script as specified by the ``lang``
    attribute.
    """

    XML_TAG = "gloss"

    def __init__(
        self,
        lang: str = None,
        text: str = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(xml_tree=False, **kwargs)
        self._attributes_required = set(("lang",))
        self._attributes_optional = set()
        self._elements_required = set(("text",))
        self._elements_optional = set(("annotation", "trait"))
        self.tag_classes.update(
            {
                "trait": Trait,
            }
        )

        # elements
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)
        elif lang is not None and text is not None:
            self.lang = Lang(lang)
            self.text = Text(text=text)
        else:
            raise RequiredValueError(("lang", "text"))

    def __str__(self):
        return f"{self.text} ({self.lang})"

    def set_trait_items(self, trait_dict):
        self.trait_items = []
        for name, data in trait_dict.items():
            value = data.get("value")
            trait_id = data.get("trait_id")
            self.trait_items.append(Trait(name=name, value=value, trait_id=trait_id))


class Annotation(Multitext):
    """Provides a mechanism for adding meta-information to almost any element."""

    XML_TAG = "annotation"

    def __init__(
        self,
        name: str = None,
        value: str = None,
        who: str = None,
        when: str = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("name", "value"))
        self._attributes_optional = set(("when", "who"))
        self._elements_required = set()
        self._elements_optional = set(("form", "pcdata", "span", "trait"))
        self.tag_classes.update(
            {
                "name": Key,
                "value": Key,
                "who": Key,
                "when": DateTime,
            }
        )

        # attributes
        self.name: Key = None
        self.value: Key = None
        self.who: Optional[Key] = None
        self.when: Optional[DateTime] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)
        elif name is not None and value is not None:
            self.name = Key(name)
            self.value = Key(value)
            if who is not None:
                self.who = Key(who)
            if when is not None:
                self.when = DateTime(when)
        else:
            raise RequiredValueError(("name", "value"))


class Field(Multitext):
    """A generalised element to allow an application to store information.
    It's for information in a LIFT file that isn't explicitly described in the
    LIFT standard.
    """

    XML_TAG = "field"

    def __init__(
        self,
        field_type: str = None,
        name: str = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._attributes_required = set(("name",))
        if config.LIFT_VERSION == config.LIFT_VERSION_FIELDWORKS:
            self._attributes_required = set(("type",))
        self._attributes_optional = set(("dateCreated", "dateModified"))
        self._elements_required = set()
        self._elements_optional = set(("annotation", "form", "pcdata", "span", "trait"))
        self.tag_classes.update(
            {
                "type": Key,
                "name": Key,
                "dateCreated": DateTime,
                "dateModified": DateTime,
                "annotation": Annotation,
                "trait": Trait,
            }
        )

        # attributes
        if config.LIFT_VERSION == "0.13":
            self.type: Key = None
        else:
            self.name: Key = None
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        if config.LIFT_VERSION == "0.13":
            # self.trait_items: Optional[List[Flag]] = None
            self.trait_items: Optional[List[Trait]] = None
            # NOTE: I think there must be a typo in the docs. I think the
            # 'form_items' class should be "Form" rather than "Span", and "Form"
            # is already accounted for in the subclassing of 'Multitext'.
            # self.form_items: Optional[List[Span]] = None
        else:
            self.trait_items: Optional[List[Trait]] = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

        missing_required_attrib = None
        if config.LIFT_VERSION == "0.13":
            if field_type is not None:
                self.type = Key(field_type)
            elif xml_tree is None:
                missing_required_attrib = "field_type"
        else:
            if name is not None:
                self.name = Key(name)
            elif xml_tree is None:
                missing_required_attrib = "name"

        if missing_required_attrib:
            raise RequiredValueError((missing_required_attrib,))


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

    # Extensible is only used as a super class for other classes, so it
    # doesn't need its own XML tag.
    XML_TAG = None

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        self._attributes_required = set()
        self._attributes_optional = set(("dateCreated", "dateModified"))
        self._elements_required = set()
        self._elements_optional = set(("annotation", "field", "trait"))
        self.tag_classes.update(
            {
                "dateCreated": DateTime,
                "dateModified": DateTime,
                "field": Field,
                "trait": Trait,
                "annotation": Annotation,
            }
        )

        # attributes
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.field_items: Optional[List[Field]] = None
        if config.LIFT_VERSION == "0.13":
            # TODO: Find definition of "Flag" in v0.13?
            # self.trait_items: Optional[List[Flag]] = None
            self.trait_items: Optional[List[Trait]] = None
        else:
            self.trait_items: Optional[List[Trait]] = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

    def add_annotation(self, name=None, value=None, who=None, when=None):
        return self._add_list_item(
            "annotation_items",
            Annotation,
            name=name,
            value=value,
            who=who,
            when=when,
        )

    def add_field(self, name=None):
        if config.LIFT_VERSION == "0.13":
            kwargs = {"field_type": name}
        else:
            kwargs = {"name": name}
        return self._add_list_item("field_items", Field, **kwargs)

    def add_trait(self, name=None, value=None, trait_id=None):
        return self._add_list_item(
            "trait_items",
            Trait,
            name=name,
            value=value,
            trait_id=trait_id,
        )

    def set_date_created(self):
        self.date_created = DateTime()

    def set_date_modified(self):
        self.date_modified = DateTime()
