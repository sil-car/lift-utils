"""Manipulate lexicon entries and their dependent elements."""

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
from .datatypes import URL
from .errors import UnsupportedActionException
from .header import Header
from .header import Range
from .utils import xmlfile_to_etree
from .utils import etree_to_obj_attributes
from .utils import search_entry


class Note(Multitext, Extensible):
    """For storing descriptive information of many kinds.
    It can include comments, bibliographic information and domain specific
    notes.

    :ivar Optional[Key] type: Gives the type of note by reference to a
        ``range-element`` in the ``note-type`` range.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        Extensible.__init__(self)
        Multitext.__init__(self)
        # properties
        self.props.add_to('attributes', Prop('type', prop_type=Key))
        self.xml_tag = 'note'
        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

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

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        Extensible.__init__(self)
        Multitext.__init__(self)
        # properties
        self.props.add_to(
            'elements',
            Prop('media_items', prop_type=list, item_type=URLRef)
        )
        if config.LIFT_VERSION == '0.13':
            self.props.add_to(
                'elements',
                Prop('form_items', prop_type=list, item_type=Span)
            )
        self.xml_tag = 'pronunciation'
        # elements
        self.media_items: Optional[List[URLRef]] = None
        if config.LIFT_VERSION == '0.13':
            self.form_items: Optional[List[Span]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return str(super())

    def add_form(
        self,
        text=None,
        tail=None,
        lang=None,
        href=None,
        span_class=None,
    ):
        if config.LIFT_VERSION != '0.13':
            raise UnsupportedActionException(config.LIFT_VERSION)
        self._add_list_item(
            'form_items',
            Span,
            text=text,
            tail=tail,
            lang=lang,
            href=href,
            span_class=span_class,
        )

    def add_media(self, href=None, label=None):
        self._add_list_item('media_items', URLRef, href=href, label=label)


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

    def __init__(
        self,
        etym_type: Key = None,
        source: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        attribs = [
            Prop('type', required=True, prop_type=Key),
            Prop('source', required=True, prop_type=str),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('gloss_items', prop_type=list, item_type=Gloss),
            Prop('form', prop_type=Form),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'etymology'
        # attributes
        self.type = etym_type
        self.source = source
        # elements
        self.gloss_items: Optional[List[Gloss]] = None
        self.form: Optional[Form] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.type} ({self.source})"

    def add_gloss(self, lang, text):
        self._add_list_item('gloss_items', Gloss, lang=lang, text=text)

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

    def __init__(
        self,
        value: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        self.props.add_to(
            'attributes',
            Prop('value', required=True, prop_type=Key)
        )
        self.props.add_to(
            'elements',
            Prop('trait_items', prop_type=list, item_type=Trait)
        )
        self.xml_tag = 'grammatical-info'
        # attributes
        self.value = None
        # elements
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif value is not None:
            self.value = Key(value)

    def __str__(self):
        traits = ''
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

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        self.props.add_to(
            'attributes',
            Prop('type', prop_type=Key)
        )
        elems = [
            Prop('main', prop_type=Reversal),
            Prop('grammatical_info', prop_type=GrammaticalInfo),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'reversal'
        # attributes
        self.type: Optional[Key] = None
        # elements
        self.main: Optional[Reversal] = None
        self.grammatical_info: Optional[GrammaticalInfo] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


class Translation(Multitext):
    """A ``Multitext`` with an optional translation ``type`` attribute.

    :ivar Optional[Key] type: Gives the type of the translation.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        self.props.add_to(
            'attributes',
            Prop('type', prop_type=Key)
        )
        self.xml_tag = 'translation'
        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


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

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        Extensible.__init__(self)
        Multitext.__init__(self)
        # properties
        self.props.add_to(
            'attributes',
            Prop('source', prop_type=Key)
        )
        self.props.add_to(
            'elements',
            Prop('translation_items', prop_type=list, item_type=Translation)
        )
        if config.LIFT_VERSION in ['0.15']:
            self.props.add_to(
                'elements',
                Prop('note_items', prop_type=list, item_type=Note)
            )
        self.xml_tag = 'example'
        # attributes
        self.source: Optional[Key] = None
        # elements
        self.translation_items: Optional[List[Translation]] = None
        if config.LIFT_VERSION in ['0.15']:
            self.note_items: Optional[List[Note]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)


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
        rel_type: Key = None,
        ref: RefId = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        attribs = [
            Prop('type', required=True, prop_type=Key),
            Prop('ref', required=True, prop_type=RefId),
            Prop('order', prop_type=int),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        self.props.add_to(
            'elements',
            Prop('usage_items', prop_type=list, item_type=Multitext)
        )
        self.xml_tag = 'relation'
        # attributes
        self.type = rel_type
        self.ref = ref
        self.order: Optional[int] = None
        # elements
        self.usage_items: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

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

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        Extensible.__init__(self)
        Multitext.__init__(self)
        # properties
        self.props.add_to(
            'attributes',
            Prop('ref', prop_type=RefId)
        )
        elems = [
            Prop('pronunciation_items', prop_type=list, item_type=Phonetic),
            Prop('relation_items', prop_type=list, item_type=Relation),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'variant'
        # attributes
        self.ref: Optional[RefId] = None
        # elements
        self.pronunciation_items: Optional[List[Phonetic]] = None
        self.relation_items: Optional[List[Relation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return self.ref if self.ref else 'variant'


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

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        attribs = [
            Prop('id', prop_type=RefId),
            Prop('order', prop_type=int),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('grammatical_info', prop_type=GrammaticalInfo),
            Prop('definition', prop_type=Multitext),
            Prop('relation_items', prop_type=list, item_type=Relation),
            Prop('note_items', prop_type=list, item_type=Note),
            Prop('example_items', prop_type=list, item_type=Example),
            Prop('reversal_items', prop_type=list, item_type=Reversal),
            Prop('illustration_items', prop_type=list, item_type=URLRef),
            Prop('subsense_items', prop_type=list, item_type=Sense),
        ]
        if config.LIFT_VERSION == '0.13':
            elems.append(Prop('gloss_items', prop_type=list, item_type=Form))
        else:
            elems.append(Prop('gloss_items', prop_type=list, item_type=Gloss))
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'sense'
        # attributes
        self.id: Optional[RefId] = None
        self.order: Optional[int] = None
        # elements
        self.grammatical_info: Optional[GrammaticalInfo] = None
        if config.LIFT_VERSION == '0.13':
            self.gloss_items: Optional[List[Form]] = None
        else:
            self.gloss_items: Optional[List[Gloss]] = None
        self.definition: Optional[Multitext] = None
        self.relation_items: Optional[List[Relation]] = None
        self.note_items: Optional[List[Note]] = None
        self.example_items: Optional[List[Example]] = None
        self.reversal_items: Optional[List[Reversal]] = None
        self.illustration_items: Optional[List[URLRef]] = None
        self.subsense_items: Optional[List[Sense]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return self._summary_line()

    def add_example(self) -> int:
        """Add an empty ``Example`` item to the sense.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('example_items', Example)

    def add_gloss(self, lang, text) -> int:
        """Add a ``Gloss`` item to the sense.
        Returns the index of the new item.

        :var str lang: The gloss's language.
        :var str text: The actual gloss text.
        """
        return self._add_list_item('gloss_items', Gloss, lang=lang, text=text)

    def add_illustration(self, href=None) -> int:
        """Add an ``URLRef`` illustration item to the sense.
        Returns the index of the new item.
        """
        return self._add_list_item('illustration_items', URLRef, href=href)

    def add_note(self) -> int:
        """Add an empty ``Note`` item to the sense.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('note_items', Note)

    def add_relation(self) -> int:
        """Add an empty ``Relation`` item to the sense.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('relation_items', Relation)

    def add_reversal(self) -> int:
        """Add an empty ``Reversal`` item to the sense.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('reversal_items', Reversal)

    def add_subsense(self) -> int:
        """Add an empty ``Subense`` item to the sense.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('subsense_items', Sense)

    def get_id(self) -> RefId:
        """Return the object's unique identifier"""
        return self.id

    def get_gloss(self, lang='en') -> str:
        """Get the gloss for a given language.
        Defaults to English; falls back otherwise to the first gloss.
        """
        gloss = ''
        if self.gloss_items:
            # Choose 1st gloss if preferred language not found.
            gloss = str(self.gloss_items[0])
            for g in self.gloss_items:
                if g.lang == lang:
                    # Choose preferred language gloss.
                    gloss = str(g)
        return gloss

    def get_grammatical_info(self) -> GrammaticalInfo:
        """Return the grammatical-info part of speech value.
        """
        grammatical_info = ''
        if self.grammatical_info:
            grammatical_info = str(self.grammatical_info)
        return grammatical_info

    def set_definition(self, forms_dict=None):
        """Set the sense's definition.

        :var Optional[dict] forms_dict: ``dict`` keys are language codes,
            values are the text for each definition.
        """
        self.definition = Multitext(forms_dict)

    def set_grammatical_info(self, value: str):
        """Set the sense's ``GrammaticalInfo``.

        :var str value: The part of speech tag into the ``grammatical-info``
            range.
        """
        self.grammatical_info = GrammaticalInfo(value=value)

    def _summary_line(self, lang='en'):
        """Return a one-line summary of the entry's data for a given language.
        Defaults to English.
        """
        gl = utils.ellipsize(str(self.get_gloss(lang=lang)), 20)
        gi = utils.ellipsize(self.get_grammatical_info(), 10)
        return f"{gl:20}\t{gi:10}\t{self.id}"

    def show(self):
        """Print an overview of the ``sense`` in the terminal window."""
        print(self)


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

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        attribs = [
            Prop('id', prop_type=RefId),
            Prop('guid', prop_type=str),
            Prop('order', prop_type=str),
            Prop('date_deleted', prop_type=DateTime),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('lexical_unit', prop_type=Multitext),
            Prop('citation', prop_type=Multitext),
            Prop('pronunciation_items', prop_type=list, item_type=Phonetic),
            Prop('variant_items', prop_type=list, item_type=Variant),
            Prop('sense_items', prop_type=list, item_type=Sense),
            Prop('note_items', prop_type=list, item_type=Note),
            Prop('relation_items', prop_type=list, item_type=Relation),
            Prop('etymology_items', prop_type=list, item_type=Etymology),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'entry'
        # attributes
        self.id: Optional[RefId] = None
        self.guid: Optional[str] = None  # deprecated
        self.order: Optional[int] = None
        self.date_deleted: Optional[DateTime] = None
        # elements
        self.lexical_unit: Optional[Multitext] = None
        self.citation: Optional[Multitext] = None
        self.pronunciation_items: Optional[List[Phonetic]] = None
        self.variant_items: Optional[List[Variant]] = None
        self.sense_items: Optional[List[Sense]] = None
        self.note_items: Optional[List[Note]] = None
        self.relation_items: Optional[List[Relation]] = None
        self.etymology_items: Optional[List[Etymology]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return self._summary_line()

    def add_etymology(self) -> int:
        """Add an empty ``Etymology`` item to the entry.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('etymology_items', Etymology)

    def add_note(self) -> int:
        """Add an empty ``Note`` item to the entry.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('note_items', Note)

    def add_pronunciation(self) -> int:
        """Add an empty ``Phonetic`` item to the entry.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('pronunciation_items', Phonetic)

    def add_relation(self) -> int:
        """Add an empty ``Relation`` item to the entry.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('relation_items', Relation)

    def add_sense(self) -> int:
        """Add an empty ``Sense`` item to the entry.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('sense_items', Sense)

    def add_variant(self) -> int:
        """Add an empty ``Variant`` item to the entry.
        Returns the index of the new item. Use this index to add data to it.
        """
        return self._add_list_item('variant_items', Variant)

    def get_id(self) -> RefId:
        """Return the object's unique identifier"""
        return self.id

    def set_citation(self, forms_dict=None):
        """Set the entry's ``Citation``.

        :var Optional[dict] forms_dict: ``dict`` keys are language codes,
            values are the text descriptions of the ``Citation``.
        """
        self.citation = Multitext(forms_dict)

    def set_lexical_unit(self, forms_dict=None):
        """Set the entry's ``LexicalUnit``.

        :var Optional[dict] forms_dict: ``dict`` keys are lanuage codes,
            values are text descriptions of the ``LexicalUnit``.
        """
        self.lexical_unit = Multitext(forms_dict)

    def show(self):
        """Print an overview of the ``entry`` in the terminal window."""
        # Add header.
        text = ['\nEntry\n============']
        # Add overview line.
        if self.lexical_unit:
            text.append(f"{self.lexical_unit}; {self.get_grammatical_info()}; {self.get_gloss()}")  # noqa: E501
        # Add traits.
        if self.trait_items:
            text.append('; '.join([str(t) for t in self.trait_items]))
        # Add senses.
        if self.sense_items:
            text.append('\n'.join([f"sense: {str(s)}" for s in self.sense_items]))  # noqa: E501
        # Add variants.
        if self.variant_items:
            text.append('; '.join(str(v) for v in self.variant_items))
        # Add notes.
        if self.note_items:
            text.append('; '.join(str(n) for n in self.note_items))
        # Add etymologies.
        if self.etymology_items:
            text.append('; '.join(str(e) for e in self.etymology_items))
        print('\n'.join(text))

    def _summary_line(self, lang='en'):
        """Return a one-line summary of the entry's data for a given language.
        Defaults to English.
        """
        lu = utils.ellipsize(str(self.lexical_unit), 20)
        gl = self.get_gloss(lang=lang)
        return f"{lu:20}\t{gl:30}\t{self.id}"


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

    _producer = f"LIFT-Utils {config.LIB_VERSION}"

    def __init__(
        self,
        path: Optional[Union[Path, str]] = None,
        version: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # properties
        attribs = [
            Prop('version', required=True, prop_type=str),
            Prop('producer', prop_type=str),
        ]
        for a in attribs:
            self.props.add_to('attributes', a)
        elems = [
            Prop('header', prop_type=Header),
            Prop('entry_items', prop_type=list, item_type=Entry),
        ]
        for e in elems:
            self.props.add_to('elements', e)
        self.xml_tag = 'lift'
        self.lift_xml_tree = None
        self.ranges_xml_tree = None
        # attributes
        self.version = version
        self.producer: Optional[str] = None
        # elements
        self.header: Optional[Header] = None
        self.entry_items: Optional[List[Entry]] = None
        if path:
            self.path = Path(path)
            if self.path.suffix == '.lift':
                self._from_lift(self.path)
            else:
                print(f"Error: Not a valid LIFT file: {self.path}")
                exit(1)
        elif xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        s = f"LIFT lexicon v{self.version}"
        if self.producer:
            s += f"; produced by {self.producer}"
        return s

    def add_entry(self):
        self._add_list_item('entry_items', Entry)
        self.entry_items[-1].date_created = DateTime()
        new_id = RefId()
        while self.get_item_by_id(new_id):  # make sure it's unique
            new_id = RefId()
        self.entry_items[-1].id = new_id

    def find(
        self,
        text: str,
        field: str = 'gloss'
    ) -> Union[Entry, Sense, None]:
        """Return the first matching ``Entry`` or ``Sense`` item.
        The field searched can be "lexical-unit", "variant", "gloss", or
        "definition", as well as any fields defined in the LIFT file's header.
        """
        return self._find(text, field=field)

    def find_all(
        self,
        text: str,
        field: str = 'gloss'
    ) -> List[Union[Entry, Sense]]:
        """Return all matching ``Entry`` or ``Sense`` items.
        The field searched can be "lexical-unit", "variant", "gloss",
        "definition", or "grammatical-info", as well as any fields defined in
        the LIFT file's header.
        """
        return self._find(text, field=field, get_all=True)

    def get_item_by_id(self, refid: str) -> Union[Entry, Sense, None]:
        """Return an entry or sense by its ``RefId``."""
        if not self.entry_items:
            return
        for entry in self.entry_items:
            if entry.id == refid:
                return entry
            if entry.sense_items:
                for sense in entry.sense_items:
                    if sense.id == refid:
                        return sense
                    if sense.subsense_items:
                        for subsense in sense.subsense_items:
                            if subsense.id == refid:
                                return subsense

    def show(self):
        """Print an overview of the ``Lexicon`` in the terminal window."""
        text = "No entries."
        if self.entry_items:
            summary_lines = [e._summary_line('en') for e in self.entry_items]  # noqa: E501
            slist = utils.unicode_sort(summary_lines)
            nl = '\n'
            text = nl.join(slist)
        print(text)

    def _find(self, text, field='gloss', get_all=False):
        items = []

        target_groups = ['entries', 'senses']
        entry_only_fields = ['lexical-unit', 'variant']
        sense_only_fields = ['gloss', 'definition', 'grammatical-info']
        header_fields = [f.tag for f in self.header.fields.field_items]
        if field in entry_only_fields:
            target_groups.remove('senses')
        elif field in sense_only_fields:
            target_groups.remove('entries')

        for entry in self.entry_items:
            result = search_entry(
                entry,
                text,
                field,
                target_groups,
                header_fields,
                get_all
            )
            if result is not None:
                if not get_all:
                    return result
                else:
                    items.extend(result)
        if get_all:
            return items

    def _from_lift(self, infile):
        infile = Path(infile)
        if not infile.is_file():
            print(f"Error: Invalid file path: {infile}")
            exit(1)
        xml_tree = xmlfile_to_etree(infile)
        self._update_from_xml(xml_tree)

    def to_lift(self, file_path: str):
        """Save the ``Lexicon`` as a LIFT file.
        The LIFT-RANGES file will be automatically created in the same folder
        as the LIFT file.
        """
        outfile = Path(file_path).with_suffix('.lift')  # ensure suffix
        ranges_file = outfile.with_suffix('.lift-ranges')
        self.producer = Lexicon._producer

        # Write LIFT file.
        lift_tree = self._to_xml_tree()
        for _range in lift_tree.find('.//ranges').getchildren():
            for _range_element in _range:
                _range.remove(_range_element)
            for attrib in _range.attrib.keys():
                if attrib not in ['id', 'href']:
                    del _range.attrib[attrib]
        outfile.write_text(self._to_xml(lift_tree))

        # Write LIFT-RANGES file.
        lift_ranges = self.header.ranges._to_xml_tree()
        lift_ranges.tag = 'lift-ranges'
        for _range in list(lift_ranges):
            del _range.attrib['href']
        ranges_file.write_text(self._to_xml(lift_ranges))

    def _update_from_xml(self, xml_tree):
        # Set initial xml_tree.
        self.xml_tree = xml_tree
        self.version = xml_tree.attrib.get('version')
        # Allow global access to version number.
        config.LIFT_VERSION = self.version
        # Update object attributes.
        etree_to_obj_attributes(xml_tree, self)
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
                if _range.attrib.get('id') == r.id:
                    href = r.href
                    self.header.ranges.range_items[i] = Range(xml_tree=_range)
                    self.header.ranges.range_items[i].href = href  # add href
                    break
