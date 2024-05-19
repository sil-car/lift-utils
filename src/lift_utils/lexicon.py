"""Manipulate lexicon entries and their dependent elements."""

import logging
from lxml import etree
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union
from urllib.parse import unquote
from urllib.parse import urlparse

from . import config
from . import utils
from .base import Extensible
from .base import Form
from .base import Gloss
from .base import LIFTUtilsBase
from .base import Multitext
from .base import Span
from .base import Trait
from .base import URLRef
from .datatypes import DateTime
from .datatypes import Key
from .datatypes import RefId
from .datatypes import Prop
from .datatypes import Props
from .datatypes import URL
from .header import Header
from .header import Range
from .utils import xml_to_etree


class Note(Multitext, Extensible):
    """For storing descriptive information of many kinds.
    It can include comments, bibliographic information and domain specific
    notes.

    :ivar Optional[Key] type: Gives the type of note by reference to a
        ``range-element`` in the ``note-type`` range.
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
            Prop('type'),
        ]
        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return super().__str__()

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        mul = Multitext(xml_tree)
        mul._update_other_from_self(self)
        del mul

        for k, v in xml_tree.attrib.items():
            if k == 'type':
                self.type = Key(v)


class Phonetic(Multitext, Extensible):
    """This represents a single pronunciation in phonetic form.

    :ivar Optional[List[URLRef]] medias: Stores an audio representation of the
        text.
    :ivar Optional[List[Span]] forms: `Used by LIFT v0.13 (FieldWorks).` Stores
        the phonetic representation using whichever writing system: IPA,
        Americanist, etc.
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
            Prop('medias'),
        ]
        # elements
        self.medias: Optional[List[URLRef]] = None
        if config.LIFT_VERSION == '0.13':
            self.forms: Optional[List[Span]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return super().__str__()

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        mul = Multitext(xml_tree)
        mul._update_other_from_self(self)
        del mul

        for c in xml_tree.getchildren():
            if c.tag == 'media':
                r = URLRef()
                r._update_from_xml(c)
                if not self.medias:
                    self.medias = [r]
                else:
                    self.medias.append(r)
            if c.tag == 'form':
                if config.LIFT_VERSION == '0.13':
                    f = Form(c)
                    if not self.forms:
                        self.forms = [f]
                    else:
                        self.forms.append(f)


class Etymology(Extensible):
    """For describing lexical relations with a word not in the lexicon.

    :ivar Key type: Gives the etymological relationship between this sense and
        some other word in another language.
    :ivar str source: Gives the language for the source language of the
        etymological relation.
    :ivar Optional[List[Gloss]] glosses: Gives glosses of the word that the
        etymological relationship is with.
    :ivar Optional[Form] form: Holds the form of the etymological reference.
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
            Prop('type', required=True),
            Prop('source', required=True),
        ]
        self.props.elements = [
            Prop('glosses'),
            Prop('form'),
        ]
        # attributes
        self.type: Key = None
        self.source: str = None
        # elements
        self.glosses: Optional[List[Gloss]] = None
        self.form: Optional[Form] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.type} ({self.source})"

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        for k, v in xml_tree.attrib.items():
            if k == 'type':
                self.type = Key(v)
            elif k == 'source':
                self.source = v

        for c in xml_tree.getchildren():
            if c.tag == 'gloss':
                g = Gloss(c)
                if not self.glosses:
                    self.glosses = [g]
                else:
                    self.glosses.append(g)
            if c.tag == 'form':
                self.form = Form(c)


class GrammaticalInfo(LIFTUtilsBase):
    """A reference to a ``range-element`` in the ``grammatical-info`` range.

    :ivar Key value: The part of speech tag into the ``grammatical-info``
        range.
    :ivar Optional[List[Trait]] traits: Allows the grammatical information for
        a given sense to have more information than just the part of speech
        given by the ``value`` attribute.
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
            Prop('value', required=True),
        ]
        self.props.elements = [
            Prop('traits'),
        ]
        # attributes
        self.value: Key = None
        # elements
        self.traits: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        traits = ''
        if self.traits:
            traits = f": {'; '.join([t for t in self.traits])}"
        return f"{self.value}{traits}"

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        for k, v in xml_tree.attrib.items():
            if k == 'value':
                self.value = Key(v)

        for c in xml_tree.getchildren():
            if c.tag == 'trait':
                t = Trait()
                t._update_from_xml(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)


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
            Prop('type'),
        ]
        self.props.elements = [
            Prop('main'),
            Prop('grammatical_info'),
        ]
        # attributes
        self.type: Optional[Key] = None
        # elements
        self.main: Optional[str] = None  # Type should be 'Reversal'
        self.grammatical_info: Optional[GrammaticalInfo] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        mul = Multitext(xml_tree)
        mul._update_other_from_self(self)
        del mul

        for k, v in xml_tree.attrib.items():
            if k == 'type':
                self.type = Key(v)

        for c in xml_tree.getchildren():
            if c.tag == 'main':
                self.main = v
            elif c.tag == 'grammatical-info':
                self.grammatical_info = GrammaticalInfo(c)


class Translation(Multitext):
    """A ``Multitext`` with an optional translation ``type`` attribute.

    :ivar Optional[Key] type: Gives the type of the translation.
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
            Prop('type'),
        ]
        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        mul = Multitext(xml_tree)
        mul._update_other_from_self(self)
        del mul

        for k, v in xml_tree.attrib.items():
            if k == 'type':
                self.type = Key(v)


class Example(Multitext, Extensible):
    """Gives an example sentence or phrase.
    It is given in the language and glosses of that example in other languages.

    :ivar Optional[Key] source: Reference by which another application may
        refer to this example or is a reference into another database of texts,
        for example.
    :ivar Optional[List[Translation]] translations: Gives translations of the
        example into different languages.
    :ivar Optional[List[Note]] notes: Holds notes on this example.
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
            Prop('source'),
        ]
        self.props.elements = [
            Prop('translations'),
            Prop('notes'),
        ]
        # attributes
        self.source: Optional[Key] = None
        # elements
        self.translations: Optional[List[Translation]] = None
        if config.LIFT_VERSION in ['0.15']:
            self.notes: Optional[List[Note]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        mul = Multitext(xml_tree)
        mul._update_other_from_self(self)
        del mul

        for c in xml_tree.getchildren():
            if c.tag == 'source':
                self.source = Key(c.text)
            elif c.tag == 'translation':
                t = Translation(c)
                if not self.translations:
                    self.translations = [t]
                else:
                    self.translations.append(t)
            elif c.tag == 'note':
                if config.LIFT_VERSION in ['0.15']:
                    n = Note(c)
                    if not self.notes:
                        self.notes = [n]
                    else:
                        self.notes.append(n)


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
            Prop('type', required=True),
            Prop('ref', required=True),
            Prop('order'),
            Prop('usage'),
        ]
        # attributes
        self.type: Key = None
        self.ref: RefId = None
        self.order: Optional[int] = None
        self.usage: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.type}: {self.ref}"

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        for k, v in xml_tree.attrib.items():
            if k == 'type':
                self.type = Key(v)
            elif k == 'ref':
                self.ref = RefId(v)
            elif k == 'order':
                self.order = int(v)
            elif k == 'usage':
                # TODO: How can an attrib value be a Multitext?
                self.usage = v


class Variant(Multitext, Extensible):
    """``variant`` elements are used for all sorts of variation.

    :ivar Optional[RefId] ref: Gives the variation as a reference to another
        ``entry`` or ``sense`` rather than specifying the ``form`` (that is,
        the ``Multitext`` value of the variant).
    :ivar Optional[List[Phonetic]] pronunciations: Holds the phonetic variant
        whether it is that this is a variation in phonetics only or that the
        phonetic variation arises because of an orthographic or phonemic
        variation.
    :ivar Optional[List[Relation]]relations: Some variants have a lexical
        relationship with other senses or entries in the lexicon.
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
            Prop('ref'),
        ]
        self.props.elements = [
            Prop('pronunciations'),
            Prop('relations'),
        ]
        # attributes
        self.ref: Optional[RefId] = None
        # elements
        self.pronunciations: Optional[List[Phonetic]] = None
        self.relations: Optional[List[Relation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return self.ref if self.ref else 'variant'

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        mul = Multitext(xml_tree)
        mul._update_other_from_self(self)
        del mul

        for k, v in xml_tree.attrib.items():
            if k == 'ref':
                self.ref = RefId(v)

        for c in xml_tree.getchildren():
            if c.tag == 'pronunciation':
                p = Phonetic(c)
                if not self.pronunciations:
                    self.pronunciations = [p]
                else:
                    self.pronunciations.append(p)
            elif c.tag == 'relation':
                r = Relation(c)
                if not self.relations:
                    self.relations = [r]
                else:
                    self.relations.append(r)


class Sense(Extensible):
    """An ``entry`` is made up of a number of ``sense`` elements.

    :ivar Optional[RefId] id: This gives an identifier for this ``Sense`` so
        that things can refer to it.
    :ivar Optional[int] order: A number that is used to give the relative
        order of senses within an entry.
    :ivar Optional[GrammaticalInfo] grammatical_info: Grammatical information.
    :ivar Optional[List[Form]] glosses: `Used by LIFT v0.13 (FieldWorks).` Each
        ``gloss`` is a single string in a single language and writing system.
    :ivar Optional[List[Gloss]] glosses: Each ``gloss`` is a single string in a
        single language and writing system.
    :ivar Optional[Multitext] definition: Gives the definition in multiple
        languages or writing systems.
    :ivar Optional[List[Relation]] relations: While a lexical relation isn't
        strictly owned by a sense it is a good place to hold it.
    :ivar Optional[List[Note]] notes: There are lots of different types of
        notes.
    :ivar Optional[List[Example]] examples: Examples may be used for different
        target audiences.
    :ivar Optional[List[Reversal]] reversals: There may be different reversal
        indexes.
    :ivar Optional[List[URLRef]] illustrations: The picture doesn't have to be
        static.
    :ivar Optional[List] subsenses: Senses can form a hierarchy.
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
            Prop('id'),
            Prop('order'),
        ]
        self.props.elements = [
            Prop('grammatical_info'),
            Prop('glosses'),
            Prop('definition'),
            Prop('relations'),
            Prop('notes'),
            Prop('examples'),
            Prop('reversals'),
            Prop('illustrations'),
            Prop('subsenses'),
        ]
        # attributes
        self.id: Optional[RefId] = None
        self.order: Optional[int] = None
        # elements
        self.grammatical_info: Optional[GrammaticalInfo] = None
        if config.LIFT_VERSION == '0.13':
            self.glosses: Optional[List[Form]] = None
        else:
            self.glosses: Optional[List[Gloss]] = None
        self.definition: Optional[Multitext] = None
        self.relations: Optional[List[Relation]] = None
        self.notes: Optional[List[Note]] = None
        self.examples: Optional[List[Example]] = None
        self.reversals: Optional[List[Reversal]] = None
        self.illustrations: Optional[List[URLRef]] = None
        self.subsenses: Optional[List] = None  # Type should be 'Sense'

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return self.get_summary_line()

    def get_summary_line(self, lang='en'):
        """Return a one-line summary of the entry's data for a given language.
        Defaults to English.
        """
        gl = utils.ellipsize(str(self.get_gloss(lang=lang)), 10)
        gi = utils.ellipsize(self.get_grammatical_info(), 10)
        de = str(self.definition)
        return f"{gl:10}\t{gi:10}\t{de}"

    def get_gloss(self, lang='en'):
        """Get gloss details for a given language.
        Defaults to English.
        """
        gloss = ''
        if self.glosses:
            # Choose 1st gloss if preferred language not found.
            gloss = str(self.glosses[0])
            for g in self.glosses:
                if g.lang == lang:
                    # Choose preferred language gloss.
                    gloss = str(g)
        return gloss

    def get_grammatical_info(self):
        """Get basic grammatical info.
        """
        grammatical_info = ''
        if self.grammatical_info:
            grammatical_info = str(self.grammatical_info)
        return grammatical_info

    def show(self):
        """Print an overview of the ``sense`` in the terminal window."""
        print(self.__str__())

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        for k, v in xml_tree.attrib.items():
            if k == 'id':
                self.id = v
            elif k == 'order':
                self.order = v

        for c in xml_tree.getchildren():
            if c.tag == 'grammatical-info':
                self.grammatical_info = GrammaticalInfo(c)
            elif c.tag == 'gloss':
                if config.LIFT_VERSION == '0.13':
                    g = Form(c)
                else:
                    g = Gloss(c)
                if not self.glosses:
                    self.glosses = [g]
                else:
                    self.glosses.append(g)
            elif c.tag == 'definition':
                m = Multitext(c)
                self.definition = m
            elif c.tag == 'relation':
                r = Relation(c)
                if not self.relations:
                    self.relations = [r]
                else:
                    self.relations.append(r)
            elif c.tag == 'note':
                n = Note(c)
                if not self.notes:
                    self.notes = [n]
                else:
                    self.notes.append(n)
            elif c.tag == 'example':
                e = Example(c)
                if not self.examples:
                    self.examples = [e]
                else:
                    self.examples.append(e)
            elif c.tag == 'reversal':
                r = Reversal(c)
                if not self.reversals:
                    self.reversals = [r]
                else:
                    self.reversals.append(r)
            elif c.tag == 'illustration':
                r = URLRef(c)
                if not self.illustrations:
                    self.illustrations = [r]
                else:
                    self.illustrations.append(r)
            elif c.tag == 'subsense':
                s = Sense(c)
                if not self.subsenses:
                    self.subsenses = [s]
                else:
                    self.subsenses.append(s)


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
    :ivar Optional[List[Phonetic]] pronunciations: There can be multiple
        phonetic forms of an entry.
    :ivar Optional[List[Variant]] variants: Any constrained variants or free
        orthographic variants.
    :ivar Optional[List[Sense]] senses: This is where the definition goes.
    :ivar Optional[List[Note]] notes: The more notes you keep the better.
    :ivar Optional[List[Relation]] relations: Gives a lexical relationship
        between this entry and another ``entry`` or ``sense``.
    :ivar Optional[List[Etymology]] etymologies: Differs from a lexical
        relation in that it has no referent in the lexicon.
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
            Prop('id'),
            Prop('guid'),
            Prop('order'),
            Prop('date_deleted'),
        ]
        self.props.elements = [
            Prop('lexical_unit'),
            Prop('citation'),
            Prop('pronunciations'),
            Prop('variants'),
            Prop('senses'),
            Prop('notes'),
            Prop('relations'),
            Prop('etymologies'),
        ]
        # attributes
        self.id: Optional[RefId] = None
        self.guid: Optional[str] = None  # deprecated
        self.order: Optional[int] = None
        self.date_deleted: Optional[DateTime] = None
        # elements
        self.lexical_unit: Optional[Multitext] = None
        self.citation: Optional[Multitext] = None
        self.pronunciations: Optional[List[Phonetic]] = None
        self.variants: Optional[List[Variant]] = None
        self.senses: Optional[List[Sense]] = None
        self.notes: Optional[List[Note]] = None
        self.relations: Optional[List[Relation]] = None
        self.etymologies: Optional[List[Etymology]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return self.get_summary_line()

    def get_summary_line(self, lang='en'):
        """Return a one-line summary of the entry's data for a given language.
        Defaults to English.
        """
        lu = utils.ellipsize(str(self.lexical_unit), 20)
        gl = self.get_gloss(lang=lang)
        gi = self.get_grammatical_info()
        return f"{lu:20}\t{gl:30}\t{gi}"

    def get_grammatical_info(self, sense_idx=0):
        """Get basic grammatical info for a given sense index [default=0].
        """
        grammatical_info = ''
        if self.senses:
            grammatical_info = self.senses[sense_idx].get_grammatical_info()
        return grammatical_info

    def get_gloss(self, sense_idx=0, lang='en'):
        """Get gloss details for a given sense index and language.
        Defaults to index 0 and English.
        """
        gloss = ''
        if self.senses and self.senses[sense_idx].glosses:
            # Choose 1st gloss if preferred language not found.
            gloss = str(self.senses[sense_idx].glosses[0])
            for g in self.senses[sense_idx].glosses:
                if g.lang == lang:
                    # Choose preferred language gloss.
                    gloss = str(g)
        return gloss

    def show(self):
        """Print an overview of the ``entry`` in the terminal window."""
        # Add header.
        text = ['\nEntry\n============']
        # Add overview line.
        if self.lexical_unit:
            text.append(f"{self.lexical_unit}; {self.get_grammatical_info()}; {self.get_gloss()}")  # noqa: E501
        # Add traits.
        if self.traits:
            text.append('; '.join([str(t) for t in self.traits]))
        # Add senses.
        if self.senses:
            text.append('\n'.join([f"sense: {str(s)}" for s in self.senses]))
        # Add variants.
        if self.variants:
            text.append('; '.join(str(v) for v in self.variants))
        # Add notes.
        if self.notes:
            text.append('; '.join(str(n) for n in self.notes))
        # Add etymologies.
        if self.etymologies:
            text.append('; '.join(str(e) for e in self.etymologies))
        print('\n'.join(text))

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        ext = Extensible(xml_tree)
        ext._update_other_from_self(self)
        del ext

        for k, v in xml_tree.attrib.items():
            if k == 'id':
                self.id = v
            elif k == 'guid':
                self.guid = v
            elif k == 'order':
                self.order = v
            elif k == 'dateDeleted':
                self.date_deleted = v

        for c in xml_tree.getchildren():
            if c.tag == 'lexical-unit':
                self.lexical_unit = Multitext(c)
            elif c.tag == 'citation':
                self.citation = Multitext(c)
            elif c.tag == 'pronunciation':
                p = Phonetic(c)
                if not self.pronunciations:
                    self.pronunciations = [p]
                else:
                    self.pronunciations.append(p)
            elif c.tag == 'variant':
                v = Variant(c)
                if not self.variants:
                    self.variants = [v]
                else:
                    self.variants.append(v)
            elif c.tag == 'sense':
                s = Sense(c)
                if not self.senses:
                    self.senses = [s]
                else:
                    self.senses.append(s)
            elif c.tag == 'note':
                n = Note(c)
                if not self.notes:
                    self.notes = [n]
                else:
                    self.notes.append(n)
            elif c.tag == 'relation':
                r = Relation(c)
                if not self.relations:
                    self.relations = [r]
                else:
                    self.relations.append(r)
            elif c.tag == 'etymology':
                e = Etymology(c)
                if not self.etymologies:
                    self.etymologies = [e]
                else:
                    self.etymologies.append(e)


class Lexicon(LIFTUtilsBase):
    """This is the main class of the lexicon.
    It contains the header and all the entries in the database.

    :ivar str version: Specifies the lift language version number.
    :ivar Optional[str] producer: Identifies the particular producer of this
        lift file.
    :ivar Optional[Header] header: Contains the header information for the
        database.
    :ivar Optional[List[Entry]] entries: Each of the entries in the lexicon.
    """

    def __init__(
        self,
        path: Optional[Union[Path, str]] = None,
        xml_tree: Optional[etree.ElementTree] = None
    ):
        super().__init__()
        if xml_tree is not None:
            super()._update_from_xml(xml_tree)
        # properties
        self.props = Props(lift_version=config.LIFT_VERSION)
        self.props.attributes = [
            Prop('version', required=True),
            Prop('producer'),
        ]
        self.props.elements = [
            Prop('header'),
            Prop('entries'),
        ]
        self.path = Path(path)
        # attributes
        self.version: str = None
        self.producer: Optional[str] = None
        # elements
        self.header: Optional[Header] = None
        self.entries: Optional[List[Entry]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        s = f"LIFT lexicon v{self.version}"
        if self.producer:
            s += f"; produced by {self.producer}"
        return s

    def show(self):
        """Print an overview of the ``lexicon`` in the terminal window."""
        text = "No entries."
        if self.entries:
            summary_lines = [e.get_summary_line('en') for e in self.entries]
            slist = utils.unicode_sort(summary_lines)
            nl = '\n'
            text = nl.join(slist)
        print(text)

    def get_item_by_id(self, refid) -> Union[Entry, Sense, None]:
        """Return an entry or sense by its ``RefId``."""

        if not self.entries:
            return

        for entry in self.entries:
            if entry.id == refid:
                return entry
            if entry.senses:
                for sense in entry.senses:
                    if sense.id == refid:
                        return sense

    def _update_from_xml(self, xml_tree):
        self.xml_tree = xml_tree

        for k, v in xml_tree.attrib.items():
            if k == 'version':
                self.version = v
                config.LIFT_VERSION = self.version  # allow global access
            elif k == 'producer':
                self.producer = v

        for c in xml_tree.getchildren():
            if c.tag == 'header':
                # Get initial header info from LIFT file.
                self.header = Header(c)
                # Update header range data from external file(s).
                ext_hrefs = set()
                for r in self.header.ranges[:]:
                    if r.href:
                        ext_hrefs.add(r.href)
                for p in ext_hrefs:
                    self._update_header_from_href(p)
            elif c.tag == 'entry':
                entry = Entry(c)
                if not self.entries:
                    self.entries = [entry]
                else:
                    self.entries.append(entry)
            else:
                logging.warning(f"{__class__}: Unhandled XML tag: {c.tag}")

    def _update_header_from_href(self, href: URL):
        filepath = unquote(urlparse(href).path)
        try:
            xml_tree = xml_to_etree(filepath)
        except OSError:
            # Probably absolute URI from a different device.
            # Try same file name, but in same dir as current LIFT file.
            relpath = self.path.parent / Path(filepath).name
            xml_tree = xml_to_etree(relpath)

        for _range in xml_tree.getchildren():
            for i, r in enumerate(self.header.ranges[:]):
                if _range.attrib.get('id') == r.id:
                    # print(f'matched {r.id}')
                    href = r.href
                    self.header.ranges[i] = Range(_range)
                    self.header.ranges[i].href = href  # add href back in
