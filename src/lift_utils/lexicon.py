"""Manipulate lexicon entries and their dependent elements."""

from pathlib import Path
from typing import List, Optional, Union
from urllib.parse import unquote, urlparse

from lxml import etree

from . import config, utils
from .base import (
    Extensible,
    Form,
    Gloss,
    LIFTUtilsBase,
    Multitext,
    Trait,
    URLRef,
)
from .datatypes import URL, DateTime, Key, RefId
from .errors import InvalidExtensionError
from .header import Header, Range, Range13
from .utils import (
    get_writing_systems_from_entry,
    search_entry,
    xmlfile_to_etree,
)


class Note(Multitext, Extensible):
    """For storing descriptive information of many kinds.
    It can include comments, bibliographic information and domain specific
    notes.

    :ivar Optional[Key] type: Gives the type of note by reference to a
        ``range-element`` in the ``note-type`` range.
    """

    XML_TAG = "note"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        # TODO: Can we just use super().__init__() here and elsewhere?
        Extensible.__init__(self, **kwargs)
        Multitext.__init__(self, **kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(),
                "optional": set(("type",)),
            },
            "elements": {
                "required": set(),
                "optional": set(),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "type": Key,
            }
        )

        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

    def __str__(self):
        return super().__str__()


class Phonetic(Multitext, Extensible):
    """This represents a single pronunciation in phonetic form.

    :ivar Optional[List[URLRef]] media_items: Stores an audio representation of
        the text.
    :ivar Optional[List[Span]] form_items: `Used by LIFT v0.13 (FieldWorks).`
        Stores the phonetic representation using whichever writing system: IPA,
        Americanist, etc.
    """

    XML_TAG = "pronunciation"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        Extensible.__init__(self, **kwargs)
        Multitext.__init__(self, **kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(),
                "optional": set(),
            },
            "elements": {
                "required": set(),
                "optional": set(("media",)),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "media": URLRef,
            }
        )

        # elements
        self.media_items: Optional[List[URLRef]] = None
        # NOTE: See note in base.Field definition re: superseded 'form_items'.
        # if config.LIFT_VERSION == '0.13':
        #     self.form_items: Optional[List[Span]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

    def __str__(self):
        return str(super())

    # NOTE: See note in base.Field definition re: superseded 'form_items'.
    # def add_form(
    #     self,
    #     text=None,
    #     tail=None,
    #     lang=None,
    #     href=None,
    #     span_class=None,
    # ):
    #     if config.LIFT_VERSION != '0.13':
    #         raise UnsupportedActionException(config.LIFT_VERSION)
    #     self._add_list_item(
    #         'form_items',
    #         Span,
    #         text=text,
    #         tail=tail,
    #         lang=lang,
    #         href=href,
    #         span_class=span_class,
    #     )

    # NOTE: See note in base.Field definition re: superseded 'form_items'.
    def add_form(self, lang, text):
        self._add_list_item(
            "form_items",
            Multitext,
            {lang: text},
        )

    def add_media(self, href=None, label=None):
        self._add_list_item("media_items", URLRef, href=href, label=label)


class Etymology(Extensible):
    """For describing lexical relations with a word not in the lexicon.

    :ivar Key type: Gives the etymological relationship between this sense and
        some other word in another language.
    :ivar str source: Gives the language for the source language of the
        etymological relation.
    :ivar Optional[List[Gloss]] gloss_items: Gives glosses of the word that the
        etymological relationship is with.
    :ivar Optional[Form] form: Holds the form of the etymological reference.
    """

    XML_TAG = "etymology"

    def __init__(
        self,
        etym_type: Key = None,
        source: str = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(("source", "type")),
                "optional": set(),
            },
            "elements": {
                "required": set(),
                "optional": set(("form", "gloss")),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "type": Key,
                "source": str,
                "form": Form,
                "gloss": Gloss,
            }
        )

        # attributes
        self.type = etym_type
        self.source = source
        # elements
        self.gloss_items: Optional[List[Gloss]] = None
        self.form: Optional[Form] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

    def __str__(self):
        return f"{self.type} ({self.source})"

    def add_gloss(self, lang, text):
        self._add_list_item("gloss_items", Gloss, lang=lang, text=text)

    def set_form(self):
        pass


class GrammaticalInfo(LIFTUtilsBase):
    """A reference to a ``range-element`` in the ``grammatical-info`` range.

    :ivar Key value: The part of speech tag into the ``grammatical-info``
        range.
    :ivar Optional[List[Trait]] trait_items: Allows the grammatical information
        for a given sense to have more information than just the part of speech
        given by the ``value`` attribute.
    """

    XML_TAG = "grammatical-info"

    def __init__(
        self, value: Key = None, xml_tree: Optional[etree._Element] = None, **kwargs
    ):
        super().__init__(**kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(("value",)),
                "optional": set(),
            },
            "elements": {
                "required": set(),
                "optional": set(("trait",)),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "value": Key,
                "trait": Trait,
            }
        )

        # attributes
        self.value = None
        # elements
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)
        elif value is not None:
            self.value = Key(value)

    def __str__(self):
        traits = ""
        if self.trait_items:
            traits = f": {'; '.join([str(t) for t in self.trait_items])}"
        return f"{self.value}{traits}"


class Reversal(Multitext):
    """Enables a wider use of a dictionary.

    :ivar Optional[Key] type: Gives the type of the reversal as a
        ``range-element`` in the ``reversal-type`` range.
    :ivar Optional[Reversal] main: This gives the parent reversal in a
        hierarchical set of reversals.
    :ivar Optional[GrammaticalInfo] grammatical_info: This allows a reversal
        relation to specify what the grammatical information is in the reversal
        language.
    """

    XML_TAG = "reversal"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(),
                "optional": set(("type",)),
            },
            "elements": {
                "required": set(),
                "optional": set(("grammatical-info", "main")),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "type": Key,
                "grammatical-info": GrammaticalInfo,
                "main": Reversal,
            }
        )

        # attributes
        self.type: Optional[Key] = None
        # elements
        self.main: Optional[Reversal] = None
        self.grammatical_info: Optional[GrammaticalInfo] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class Translation(Multitext):
    """A ``Multitext`` with an optional translation ``type`` attribute.

    :ivar Optional[Key] type: Gives the type of the translation.
    """

    XML_TAG = "translation"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(),
                "optional": set(("type",)),
            },
            "elements": {
                "required": set(),
                "optional": set(),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "type": Key,
            }
        )

        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class Example(Multitext, Extensible):
    """Gives an example sentence or phrase.
    It is given in the language and glosses of that example in other languages.

    :ivar Optional[Key] source: Reference by which another application may
        refer to this example or is a reference into another database of texts,
        for example.
    :ivar Optional[List[Translation]] translation_items: Gives translations of
        the example into different languages.
    :ivar Optional[List[Note]] note_items: Holds notes on this example.
    """

    XML_TAG = "example"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        # TODO: Consider replacing these two __inits__ with super().__init__.
        Extensible.__init__(self, **kwargs)
        Multitext.__init__(self, **kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(),
                "optional": set(("source",)),
            },
            "elements": {
                "required": set(),
                "optional": set(("translation", "note")),
            },
        }
        if config.LIFT_VERSION == "0.13":
            self._properties.get("elements")["optional"] = set(("translation",))
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "source": Key,
                "translation": Translation,
                "note": Note,
            }
        )

        # attributes
        self.source: Optional[Key] = None
        # elements
        self.translation_items: Optional[List[Translation]] = None
        if config.LIFT_VERSION == "0.13":
            if hasattr(self, "note_items"):
                del self.note_items
        else:
            self.note_items: Optional[List[Note]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)


class Relation(Extensible):
    """This element is used for lexical relations.

    :ivar Key type: Is the type of the particular lexical relation.
    :ivar RefId ref: This is the other end of the relation, either a ``sense``
        or an ``entry``.
    :ivar Optional[int] order: Gives the relative ordering of relations of a
        given type when a multiple relation is being described.
    :ivar Optional[Multitext] usage: Gives information on usage in one or more
        languages or writing systems.
    """

    XML_TAG = "relation"

    def __init__(
        self,
        rel_type: Key = None,
        ref: RefId = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(("type", "ref")),
                "optional": set(("order",)),
            },
            "elements": {
                "required": set(),
                "optional": set(("usage",)),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "type": Key,
                "ref": RefId,
                "order": int,
                "usage": Multitext,
            }
        )

        # attributes
        self.type = rel_type
        self.ref = ref
        self.order: Optional[int] = None
        # elements
        self.usage_items: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

    def __str__(self):
        return f"{self.type}: {self.ref}"


class Variant(Multitext, Extensible):
    """``Variant`` elements are used for all sorts of variation.

    :ivar Optional[RefId] ref: Gives the variation as a reference to another
        ``entry`` or ``sense`` rather than specifying the ``form`` (that is,
        the ``Multitext`` value of the variant).
    :ivar Optional[List[Phonetic]] pronunciation_items: Holds the phonetic
        variant whether it is that this is a variation in phonetics only or
        that the phonetic variation arises because of an orthographic or
        phonemic variation.
    :ivar Optional[List[Relation]] relation_items: Some variants have a lexical
        relationship with other senses or entries in the lexicon.
    """

    XML_TAG = "variant"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        Extensible.__init__(self, **kwargs)
        Multitext.__init__(self, **kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(),
                "optional": set(("ref",)),
            },
            "elements": {
                "required": set(),
                "optional": set(("pronunciation", "relation")),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "ref": RefId,
                "pronunciation": Phonetic,
                "relation": Relation,
            }
        )

        # attributes
        self.ref: Optional[RefId] = None
        # elements
        self.pronunciation_items: Optional[List[Phonetic]] = None
        self.relation_items: Optional[List[Relation]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)

    def __str__(self):
        return self.ref if self.ref else "variant"


class Sense(Extensible):
    """An ``entry`` is made up of a number of ``sense`` elements.

    :ivar Optional[RefId] id: This gives an identifier for this ``Sense`` so
        that things can refer to it.
    :ivar Optional[int] order: A number that is used to give the relative
        order of senses within an entry.
    :ivar Optional[GrammaticalInfo] grammatical_info: Grammatical information.
    :ivar Optional[List[Union[Gloss, Form]]] gloss_items: Each ``gloss`` is a
        single string in a single language and writing system. ``Form`` is used
        by LIFT v0.13 (FieldWorks), while ``Gloss`` is used in later versions.
    :ivar Optional[Multitext] definition: Gives the definition in multiple
        languages or writing systems.
    :ivar Optional[List[Relation]] relation_items: While a lexical relation
        isn't strictly owned by a sense it is a good place to hold it.
    :ivar Optional[List[Note]] note_items: There are lots of different types of
        notes.
    :ivar Optional[List[Example]] example_items: Examples may be used for
        different target audiences.
    :ivar Optional[List[Reversal]] reversal_items: There may be different
        reversal indexes.
    :ivar Optional[List[URLRef]] illustration_items: The picture doesn't have
        to be static.
    :ivar Optional[List[Sense]] subsense_items: Senses can form a hierarchy.
    """

    XML_TAG = "sense"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(),
                "optional": set(("id", "order")),
            },
            "elements": {
                "required": set(),
                "optional": set(
                    (
                        "definition",
                        "example",
                        "gloss",
                        "grammatical-info",
                        "illustration",
                        "note",
                        "relation",
                        "reversal",
                        "subsense",
                    )
                ),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "id": RefId,
                "order": int,
                "definition": Multitext,
                "example": Example,
                "gloss": Gloss,
                "grammatical-info": GrammaticalInfo,
                "illustration": URLRef,
                "note": Note,
                "relation": Relation,
                "reversal": Reversal,
                "subsense": Sense,
            }
        )

        # attributes
        self.id: Optional[RefId] = None
        self.order: Optional[int] = None
        # elements
        self.definition: Optional[Multitext] = None
        self.example_items: Optional[List[Example]] = None
        if config.LIFT_VERSION == "0.13":
            self.tag_classes["gloss"] = Form
            self.gloss_items: Optional[List[Form]] = None
        else:
            self.gloss_items: Optional[List[Gloss]] = None
        self.grammatical_info: Optional[GrammaticalInfo] = None
        self.illustration_items: Optional[List[URLRef]] = None
        self.note_items: Optional[List[Note]] = None
        self.relation_items: Optional[List[Relation]] = None
        self.reversal_items: Optional[List[Reversal]] = None
        self.subsense_items: Optional[List[Sense]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)
        else:
            self.set_date_created()

    def __str__(self):
        return self._summary_line()

    def add_example(self) -> Example:
        """Add an empty ``Example`` item to the sense.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("example_items", Example)

    def add_gloss(self, lang, text) -> Gloss:
        """Add a ``Gloss`` item to the sense.
        Returns the new object.

        :var str lang: The gloss's language.
        :var str text: The actual gloss text.
        """
        self.set_date_modified()
        return self._add_list_item("gloss_items", Gloss, lang=lang, text=text)

    def add_illustration(self, href=None) -> URLRef:
        """Add a ``URLRef`` illustration item to the sense.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("illustration_items", URLRef, href=href)

    def add_note(self) -> Note:
        """Add an empty ``Note`` item to the sense.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("note_items", Note)

    def add_relation(self) -> Relation:
        """Add an empty ``Relation`` item to the sense.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("relation_items", Relation)

    def add_reversal(self) -> Reversal:
        """Add an empty ``Reversal`` item to the sense.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("reversal_items", Reversal)

    def add_subsense(self):
        """Add an empty ``Subense`` item to the sense.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("subsense_items", Sense)

    def get_id(self) -> RefId:
        """Return the object's ``id`` attribute."""
        return self.id

    def get_gloss(self, lang="en") -> str:
        """Get the gloss for a given language.
        Defaults to English; falls back otherwise to the first gloss.
        """
        gloss = ""
        if self.gloss_items:
            # Choose 1st gloss if preferred language not found.
            gloss = str(self.gloss_items[0])
            for g in self.gloss_items:
                if g.lang == lang:
                    # Choose preferred language gloss.
                    gloss = str(g)
        return gloss

    def get_grammatical_info(self) -> GrammaticalInfo:
        """Return the grammatical-info part of speech value."""
        grammatical_info = ""
        if self.grammatical_info:
            grammatical_info = str(self.grammatical_info)
        return grammatical_info

    def set_definition(self, forms_dict=None):
        """Set the sense's definition.

        :var Optional[dict] forms_dict: ``dict`` keys are language codes,
            values are the text for each definition.
        """
        self.set_date_modified()
        self.definition = Multitext(forms_dict)

    def set_grammatical_info(self, value: str):
        """Set the sense's ``GrammaticalInfo``.

        :var str value: The part of speech tag in the ``grammatical-info``
            range.
        """
        self.set_date_modified()
        self.grammatical_info = GrammaticalInfo(value=value)

    def _summary_line(self, lang="en"):
        """Return a one-line summary of the entry's data for a given language.
        Defaults to English.
        """
        gl = utils.ellipsize(str(self.get_gloss(lang=lang)), 20)
        gi = utils.ellipsize(self.get_grammatical_info(), 10)
        return f"{gl:20}\t{gi:10}\t{self.id}"


class Entry(Extensible):
    """This is the core of a lexicon. A lexicon is made up of a set of entries.

    :ivar Optional[RefId] id: This gives a unique identifier to this ``entry``.
    :ivar Optional[str] guid: `Deprecated.` This gives a unique identifier to
        this entry in the form of a “universally unique identifier” (RFC 4122).
    :ivar Optional[int] order: This is the homograph number.
    :ivar Optional[DateTime] date_deleted: If this attribute exists then it
        indicates that the particular ``entry`` has been deleted.
    :ivar Optional[Multitext] lexical_unit: The lexical form is the primary
        lexical form as is found as the primary lexical form in the source data
        models for this standard.
    :ivar Optional[Multitext] citation: This is the form that is to be printed
        in the dictionary.
    :ivar Optional[List[Phonetic]] pronunciation_items: There can be multiple
        phonetic forms of an entry.
    :ivar Optional[List[Variant]] variant_items: Any constrained variants or
        free orthographic variants.
    :ivar Optional[List[Sense]] sense_items: This is where the definition goes.
    :ivar Optional[List[Note]] note_items: The more notes you keep the better.
    :ivar Optional[List[Relation]] relation_items: Gives a lexical relationship
        between this entry and another ``entry`` or ``sense``.
    :ivar Optional[List[Etymology]] etymology_items: Differs from a lexical
        relation in that it has no referent in the lexicon.
    """

    XML_TAG = "entry"

    def __init__(self, xml_tree: Optional[etree._Element] = None, **kwargs):
        super().__init__(**kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(),
                "optional": set(
                    (
                        "guid",
                        "id",
                        "dateDeleted",
                        "order",
                    )
                ),
            },
            "elements": {
                "required": set(),
                "optional": set(
                    (
                        "citation",
                        "etymology",
                        "lexical-unit",
                        "note",
                        "pronunciation",
                        "relation",
                        "sense",
                        "variant",
                    )
                ),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "guid": str,
                "id": RefId,
                "dateDeleted": DateTime,
                "order": int,
                "citation": Multitext,
                "etymology": Etymology,
                "lexical-unit": Multitext,
                "note": Note,
                "pronunciation": Phonetic,
                "relation": Relation,
                "sense": Sense,
                "variant": Variant,
            }
        )

        # attributes
        self.id: Optional[RefId] = None
        self.guid: Optional[str] = None  # deprecated
        self.date_deleted: Optional[DateTime] = None
        self.order: Optional[int] = None
        # elements
        self.citation: Optional[Multitext] = None
        self.etymology_items: Optional[List[Etymology]] = None
        self.lexical_unit: Optional[Multitext] = None
        self.note_items: Optional[List[Note]] = None
        self.pronunciation_items: Optional[List[Phonetic]] = None
        self.relation_items: Optional[List[Relation]] = None
        self.sense_items: Optional[List[Sense]] = None
        self.variant_items: Optional[List[Variant]] = None

        if xml_tree is not None:
            self._from_xml_tree(xml_tree)
        else:
            self.set_date_created()

    def __str__(self):
        return self._summary_line()

    def add_etymology(self) -> Etymology:
        """Add an empty ``Etymology`` item to the entry.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("etymology_items", Etymology)

    def add_note(self) -> Note:
        """Add an empty ``Note`` item to the entry.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("note_items", Note)

    def add_pronunciation(self) -> Phonetic:
        """Add an empty ``Phonetic`` item to the entry.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("pronunciation_items", Phonetic)

    def add_relation(self) -> Relation:
        """Add an empty ``Relation`` item to the entry.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("relation_items", Relation)

    def add_sense(self) -> Sense:
        """Add an empty ``Sense`` item to the entry.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        sense = self._add_list_item("sense_items", Sense)
        sense.date_created = DateTime()
        new_id = RefId()
        # NOTE: When creating an entry from a lexicon we can check all existing
        # IDs to make sure the generated one is unique. But when creating a
        # sense from an entry we don't have the ability to access the lexicon
        # directly. Will just assume for now that the generated ID is unique.
        sense.id = new_id
        return sense

    def add_variant(self) -> Variant:
        """Add an empty ``Variant`` item to the entry.
        Returns the new object, which can then be used to add data to it.
        """
        self.set_date_modified()
        return self._add_list_item("variant_items", Variant)

    def get_id(self) -> RefId:
        """Return the object's unique identifier"""
        return self.id

    def set_citation(self, forms_dict=None):
        """Set the entry's ``Citation``.

        :var Optional[dict] forms_dict: ``dict`` keys are language codes,
            values are the text descriptions of the ``Citation``.
        """
        self.set_date_modified()
        self.citation = Multitext(forms_dict)

    def set_lexical_unit(self, forms_dict=None):
        """Set the entry's ``LexicalUnit``.

        :var Optional[dict] forms_dict: ``dict`` keys are lanuage codes,
            values are text descriptions of the ``LexicalUnit``.
        """
        self.set_date_modified()
        self.lexical_unit = Multitext(forms_dict)

    def _summary_line(self, lang="en"):
        """Return a one-line summary of the entry's data for a given language.
        Defaults to English.
        """
        lu = utils.ellipsize(str(self.lexical_unit), 20)
        # gl = self.get_gloss(lang=lang)
        # return f"{lu:20}\t{gl:30}\t{self.id}"
        return f"{lu:20}\t{self.id}"


class Lexicon(LIFTUtilsBase):
    """This is the main class of the lexicon.
    It contains the header and all the entries in the database.

    :ivar str version: Specifies the lift language version number.
    :ivar Optional[str] producer: Identifies the particular producer of this
        lift file.
    :ivar Optional[Header] header: Contains the header information for the
        database.
    :ivar Optional[List[Entry]] entry_items: Each of the entries in the
        lexicon.
    :ivar Optional[Path] path: File path to a LIFT file to import.
    """

    XML_TAG = "lift"

    def __init__(
        self,
        path: Optional[Union[Path, str]] = None,
        version: str = None,
        xml_tree: Optional[etree._Element] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # Define new properties.
        self._properties = {
            "attributes": {
                "required": set(("version",)),
                "optional": set(("producer",)),
            },
            "elements": {
                "required": set(),
                "optional": set(("entry", "header")),
            },
        }
        self._update_attribs_and_elems()
        self.tag_classes.update(
            {
                "version": str,
                "producer": str,
                "entry": Entry,
                "header": Header,
            }
        )

        self.lift_xml_tree = None
        self.ranges_xml_tree = None
        self.analysis_writing_systems = None
        self.vernacular_writing_systems = None
        # attributes
        self.version = version
        # Make version accessible globally.
        config.LIFT_VERSION = self.version
        self.producer: str = f"LIFT-Utils {config.LIB_VERSION}"
        # elements
        self.header: Optional[Header] = None
        self.entry_items: Optional[List[Entry]] = None
        if path:
            self.path = Path(path).expanduser()
            if self.path.suffix == ".lift":
                self._from_lift(self.path)
            else:
                raise InvalidExtensionError(self.path.name)
        elif xml_tree is not None:
            self._from_xml_tree(xml_tree)
            self._find_writing_systems()

    def __str__(self):
        return f"LIFT lexicon v{self.version}; produced by {self.producer}"

    def add_entry(self) -> Entry:
        """Add an empty ``Entry`` to the lexicon.
        Returns the ``Entry`` object, which can then be used to add data to it.
        """
        entry = self._add_list_item("entry_items", Entry)
        entry.date_created = DateTime()
        new_id = RefId()
        while self.get_item_by_id(new_id):  # make sure it's unique
            new_id = RefId()
        entry.id = new_id
        return entry

    def find(
        self, text: str, field: str = "gloss", match_type: str = "contains"
    ) -> Union[Entry, Sense, None]:
        """Return the first matching ``Entry`` or ``Sense`` item.
        The field searched can be the entry's "lexical-unit" or "variant"
        field, the sense's "gloss" [default], "definition", or
        "grammatical-info" field, as well as any fields defined in the LIFT
        file's header.

        :var str text: The search term.
        :var str field: The field to be searched [default is "gloss"].
        :var str match_type: The kind comparison between the search term and
            the field's data. Possible values are "contains" [default],
            "exact", or "regex".
        """
        return self._find(text, field=field, match_type=match_type)

    def find_all(
        self, text: str = "", field: str = "gloss", match_type: str = "contains"
    ) -> List[Union[Entry, Sense]]:
        """Return all matching ``Entry`` or ``Sense`` items.
        The field searched can be the entry's "lexical-unit" or "variant"
        field, the sense's "gloss" [default], "definition", or
        "grammatical-info" field, as well as any fields defined in the LIFT
        file's header.

        :var str text: The search term.
        :var str field: The field to be searched [default is "gloss"].
        :var str match_type: The kind comparison between the search term and
            the field's data. Possible values are "contains" [default],
            "exact", or "regex".
        """
        return self._find(text, field=field, match_type=match_type, get_all=True)

    def get_item_by_id(self, refid: str) -> Union[Entry, Sense, None]:
        """Return an entry or sense by its ``id`` attribute.

        :var str refid: The ``id`` attribute of the entry or sense.
        """
        return self._item_from_id(refid, item_type="self")

    def get_item_parent_by_id(self, refid: str) -> Union[Entry, Sense, None]:
        """Return an sense's parent item by the sense's ``id`` attribute.

        :var str refid: The ``id`` attribute of the entry or sense.
        """
        return self._item_from_id(refid, item_type="parent")

    def get_range_elements(self, range_name):
        """Returns a generator object that lists all the names defined in the
        header for the given ``range``.

        :var str range_name: The name of the header range.
        """
        for r in self.header.ranges.range_items:
            if r.id == range_name:
                for e in r.range_element_items:
                    yield e.id

    def get_ranges(self):
        """Returns a generator object that lists all the range names defined in
        the header.
        """
        for r in self.header.ranges.range_items:
            yield r.id

    def show(self):
        """Print an overview of the ``Lexicon`` in the terminal window."""
        text = None
        if self.entry_items:
            summary_lines = [e._summary_line("en") for e in self.entry_items]  # noqa: E501
            slist = utils.unicode_sort(summary_lines)
            text = "\n".join(slist)
        print(text)

    def to_lift(self, file_path: str):
        """Save the ``Lexicon`` as a LIFT file.
        The LIFT-RANGES file will be automatically created in the same folder
        as the LIFT file.

        :var str file_path: Full or relative path to new LIFT file.
        """
        outfile = (
            Path(file_path).expanduser().with_suffix(".lift")
        )  # ensure suffix  # noqa: E501
        ranges_file = outfile.with_suffix(".lift-ranges")

        # Write LIFT file.
        lift_tree = self._to_xml_tree()
        for _range in lift_tree.find(".//ranges").getchildren():
            for _range_element in _range:
                _range.remove(_range_element)
            for attrib in _range.attrib.keys():
                if attrib not in ["id", "href"]:
                    del _range.attrib[attrib]
        outfile.write_text(self._to_xml(lift_tree))

        # Write LIFT-RANGES file.
        lift_ranges = self.header.ranges._to_xml_tree()
        lift_ranges.tag = "lift-ranges"
        for _range in list(lift_ranges):
            del _range.attrib["href"]
        ranges_file.write_text(self._to_xml(lift_ranges))

    def _find(self, text, field="gloss", match_type="contains", get_all=False):
        items = []
        target_groups = ["entries", "senses"]
        entry_only_fields = ["lexical-unit", "variant"]
        sense_only_fields = ["gloss", "definition", "grammatical-info"]
        header_fields = [f.tag for f in self.header.fields.field_items]
        if field in entry_only_fields:
            target_groups.remove("senses")
        elif field in sense_only_fields:
            target_groups.remove("entries")

        for entry in self.entry_items:
            result = search_entry(
                entry, text, field, target_groups, header_fields, match_type, get_all
            )
            if result is not None:
                if not get_all:
                    return result
                else:
                    items.extend(result)
        if get_all:
            return items

    def _find_writing_systems(self):
        """Infer the lexicon's writing systems (vernacular and analysis)."""
        if self.vernacular_writing_systems is None:
            self.vernacular_writing_systems = []
        if self.analysis_writing_systems is None:
            self.analysis_writing_systems = []

        for e in self.entry_items:
            writing_systems = get_writing_systems_from_entry(e)
            for lang in writing_systems.get("vernacular"):
                if lang not in self.vernacular_writing_systems:
                    self.vernacular_writing_systems.append(lang)
            for lang in writing_systems.get("analysis"):
                if lang not in self.analysis_writing_systems:
                    self.analysis_writing_systems.append(lang)

    def _from_lift(self, infile):
        infile = Path(infile)
        if not infile.is_file():
            raise FileNotFoundError
        self._from_xml_tree(xmlfile_to_etree(infile))
        self._find_writing_systems()

    def _item_from_id(self, refid, item_type="self"):
        if not self.entry_items:
            return
        for entry in self.entry_items:
            if entry.id == refid:
                if item_type == "self":
                    return entry
                elif item_type == "parent":
                    return None
            if entry.sense_items:
                for sense in entry.sense_items:
                    if sense.id == refid:
                        if item_type == "self":
                            return sense
                        elif item_type == "parent":
                            return entry
                    if sense.subsense_items:
                        for subsense in sense.subsense_items:
                            if subsense.id == refid:
                                if item_type == "self":
                                    return subsense
                                elif item_type == "parent":
                                    return sense

    def _from_xml_tree(self, xml_tree):
        self.version = xml_tree.attrib.get("version")
        # Allow global access to version number.
        config.LIFT_VERSION = self.version
        # Update object attributes.
        LIFTUtilsBase.etree_to_obj_attributes(xml_tree, self)
        # Update header range data from external file(s).
        ext_hrefs = set()
        for r in self.header.ranges.range_items:
            if r.href:
                ext_hrefs.add(r.href)
        for p in ext_hrefs:
            self._update_header_from_href(p)
        # Update ranges xml_trees.
        self.header.ranges._to_xml_tree()

    def _update_header_from_href(self, href: URL):
        filepath = unquote(urlparse(href).path)
        try:
            xml_tree = xmlfile_to_etree(filepath)
        except OSError:
            # Probably absolute URI from a different device.
            # Try same file name, but in same dir as current LIFT file.
            relpath = self.path.parent / Path(filepath).name
            xml_tree = xmlfile_to_etree(relpath)

        # Update model data.
        for _range in xml_tree.getchildren():
            for i, r in enumerate(self.header.ranges.range_items[:]):
                if _range.attrib.get("id") == r.id:
                    if self.version == "0.13":
                        self.header.ranges.range_items[i] = Range13(xml_tree=_range)  # noqa: E501
                    else:
                        self.header.ranges.range_items[i] = Range(xml_tree=_range)  # noqa: E501
                    self.header.ranges.range_items[i].href = r.href  # add href
                    break
