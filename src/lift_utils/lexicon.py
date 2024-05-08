import logging
from typing import List
from typing import Optional

from .base import Extensible
from .base import Form
from .base import Gloss
from .base import Multitext
from .base import Trait
from .base import URLRef
from .datatypes import DateTime
from .datatypes import Key
from .datatypes import RefId
from .header import Header


class Note(Multitext, Extensible):
    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
        del ext

        mul = Multitext(xml_tree)
        mul.update_other_from_self(self)
        del mul

        for k, v in xml_tree.attrib.items():
            if k == 'type':
                self.type = Key(v)


class Phonetic(Multitext, Extensible):
    def __init__(self, xml_tree=None):
        super().__init__()
        # elements
        self.medias: Optional[List[URLRef]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
        del ext

        mul = Multitext(xml_tree)
        mul.update_other_from_self(self)
        del mul

        for c in xml_tree.getchildren():
            if c.tag == 'media':
                r = URLRef()
                r.update_from_xml(c)
                if not self.medias:
                    self.medias = [r]
                else:
                    self.medias.append(r)


class Etymology(Extensible):
    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.type: Key = ''
        self.source: str = ''
        # elements
        self.glosses: Optional[List[Gloss]] = None
        self.form: Optional[Form] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
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


class GrammaticalInfo:
    def __init__(self, xml_tree=None):
        # attributes
        self.value: Key = ''
        # elements
        self.traits: Optional[List[Trait]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for k, v in xml_tree.attrib.items():
            if k == 'value':
                self.value = Key(v)

        for c in xml_tree.getchildren():
            if c.tag == 'trait':
                t = Trait()
                t.update_from_xml(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)


class Reversal(Multitext):
    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.type: Optional[Key] = None
        # elements
        self.main: Optional[str] = None  # Type should be 'Reversal'
        self.grammatical_info: Optional[GrammaticalInfo] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        mul = Multitext(xml_tree)
        mul.update_other_from_self(self)
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
    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        mul = Multitext(xml_tree)
        mul.update_other_from_self(self)
        del mul

        for k, v in xml_tree.attrib.items():
            if k == 'type':
                self.type = Key(v)


class Example(Multitext, Extensible):
    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.source: Optional[Key] = None
        # elements
        self.translations: Optional[List[Translation]] = None
        self.notes: Optional[List[Note]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
        del ext

        mul = Multitext(xml_tree)
        mul.update_other_from_self(self)
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
                n = Note(c)
                if not self.notes:
                    self.notes = [n]
                else:
                    self.notes.append(n)


class Relation(Extensible):
    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.type: Key = None
        self.ref: RefId = None
        self.order: Optional[int] = None
        self.usage: Optional[Multitext] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
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
    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.ref: Optional[RefId] = None
        # elements
        self.pronunciations: Optional[List[Phonetic]] = None
        self.relations: Optional[List[Relation]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        return self.ref if self.ref else 'variant'

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
        del ext

        mul = Multitext(xml_tree)
        mul.update_other_from_self(self)
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
    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.id: Optional[RefId] = None
        self.order: Optional[int] = None
        # elements
        self.grammatical_info: Optional[GrammaticalInfo] = None
        self.glosses: Optional[List[Gloss]] = None
        self.definition: Optional[Multitext] = None
        self.relations: Optional[List[Relation]] = None
        self.notes: Optional[List[Note]] = None
        self.examples: Optional[List[Example]] = None
        self.reversals: Optional[List[Reversal]] = None
        self.illustrations: Optional[List[URLRef]] = None
        self.subsenses: Optional[List] = None  # Type should be 'Sense'

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        return self.id if self.id else 'sense'

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
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
    def __init__(self, xml_tree=None):
        super().__init__()
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
            self.update_from_xml(xml_tree)

    def __str__(self):
        return self.id if self.id else 'entry'

    def get_senses_ct(self):
        ct = 0
        if self.senses:
            ct = len(self.senses)
        return ct

    def update_from_xml(self, xml_tree):
        ext = Extensible(xml_tree)
        ext.update_other_from_self(self)
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


class LIFTLexicon:
    def __init__(
        self,
        producer: Optional[str] = None,
        header: Optional[Header] = None,
        entries: Optional[List[Entry]] = None,
        version: int = None
    ):
        # attributes
        self.version = version
        self.producer = producer
        # elements
        self.header = header
        self.entries = entries

    def __str__(self):
        return 'LIFT-lexicon'

    def update_from_xml(self, xml_tree):
        for elem in xml_tree.getchildren():
            if elem.tag == 'header':
                # TODO: Add Header
                logging.warning(f"{__class__}: Unhandled XML tag: {elem.tag}")
            elif elem.tag == 'entry':
                entry = Entry(elem)
                if not self.entries:
                    self.entries = [entry]
                else:
                    self.entries.append(entry)
            else:
                logging.warning(f"Unhandled tag while parsing root children: {elem.tag}")  # noqa: E501
