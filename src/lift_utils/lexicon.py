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
from .header import Header
from .header import Range
from .utils import xmlfile_to_etree
from .utils import etree_to_obj_attributes


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
        Extensible.__init__(self, xml_tree=xml_tree)
        Multitext.__init__(self, xml_tree=xml_tree)
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
        Extensible.__init__(self, xml_tree=xml_tree)
        Multitext.__init__(self, xml_tree=xml_tree)
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
        return super().__str__()


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
        super().__init__(xml_tree=xml_tree)
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
        value: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
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
        self.value = value
        # elements
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        traits = ''
        if self.trait_items:
            traits = f": {'; '.join([t for t in self.trait_items])}"
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
        super().__init__(xml_tree=xml_tree)
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
        super().__init__(xml_tree=xml_tree)
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
        Extensible.__init__(self, xml_tree=xml_tree)
        Multitext.__init__(self, xml_tree=xml_tree)
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
        super().__init__(xml_tree=xml_tree)
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
    """``variant`` elements are used for all sorts of variation.

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
        Extensible.__init__(self, xml_tree=xml_tree)
        Multitext.__init__(self, xml_tree=xml_tree)
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
    :ivar Optional[List[Form]] gloss_items: `Used by LIFT v0.13 (FieldWorks).`
        Each ``gloss`` is a single string in a single language and writing
        system.
    :ivar Optional[List[Gloss]] gloss_items: Each ``gloss`` is a single string
        in a single language and writing system.
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
    :ivar Optional[List] subsense_items: Senses can form a hierarchy.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
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
        self.subsense_items: Optional[List] = None

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
        if self.gloss_items:
            # Choose 1st gloss if preferred language not found.
            gloss = str(self.gloss_items[0])
            for g in self.gloss_items:
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
        super().__init__(xml_tree=xml_tree)
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
        if self.sense_items:
            grammatical_info = self.sense_items[sense_idx].get_grammatical_info()  # noqa: E501
        return grammatical_info

    def get_gloss(self, sense_idx=0, lang='en'):
        """Get gloss details for a given sense index and language.
        Defaults to index 0 and English.
        """
        gloss = ''
        if self.sense_items and self.sense_items[sense_idx].gloss_items:
            # Choose 1st gloss if preferred language not found.
            gloss = str(self.sense_items[sense_idx].gloss_items[0])
            for g in self.sense_items[sense_idx].gloss_items:
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


class Lexicon(LIFTUtilsBase):

    _producer = f"LIFT-Utils {config.LIB_VERSION}"

    """This is the main class of the lexicon.
    It contains the header and all the entries in the database.

    :ivar str version: Specifies the lift language version number.
    :ivar Optional[str] producer: Identifies the particular producer of this
        lift file.
    :ivar Optional[Header] header: Contains the header information for the
        database.
    :ivar Optional[List[Entry]] entry_items: Each of the entries in the
        lexicon.
    """

    def __init__(
        self,
        path: Optional[Union[Path, str]] = None,
        version: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=xml_tree)
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
        # attributes
        self.version = version
        self.producer: Optional[str] = None
        # elements
        self.header: Optional[Header] = None
        self.entry_items: Optional[List[Entry]] = None
        if path:
            self.path = Path(path)
            if self.path.suffix == '.lift':
                self.parse_lift(self.path)
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

    def parse_lift(self, infile):
        infile = Path(infile)
        if not infile.is_file():
            print(f"Error: Invalid file path: {infile}")
            exit(1)
        xml_tree = xmlfile_to_etree(infile)
        self._update_from_xml(xml_tree)

    def to_lift(self, outfile):
        self.producer = Lexicon._producer
        Path(outfile).write_text(self.to_xml())

    def show(self):
        """Print an overview of the ``lexicon`` in the terminal window."""
        text = "No entries."
        if self.entry_items:
            summary_lines = [e.get_summary_line('en') for e in self.entry_items]  # noqa: E501
            slist = utils.unicode_sort(summary_lines)
            nl = '\n'
            text = nl.join(slist)
        print(text)

    def get_item_by_id(self, refid) -> Union[Entry, Sense, None]:
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

    def _update_header_from_href(self, href: URL):
        filepath = unquote(urlparse(href).path)
        try:
            xml_tree = xmlfile_to_etree(filepath)
        except OSError:
            # Probably absolute URI from a different device.
            # Try same file name, but in same dir as current LIFT file.
            relpath = self.path.parent / Path(filepath).name
            xml_tree = xmlfile_to_etree(relpath)

        for _range in xml_tree.getchildren():
            for i, r in enumerate(self.header.ranges.range_items[:]):
                if _range.attrib.get('id') == r.id:
                    href = r.href
                    self.header.ranges.range_items[i] = Range(xml_tree=_range)
                    self.header.ranges.range_items[i].href = href  # add href
                    break
