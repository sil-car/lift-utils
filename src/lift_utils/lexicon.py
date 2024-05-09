import logging
from typing import List
from typing import Optional

from . import utils
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
    props = {
        'attributes': {
            'required': [],
            'optional': ['type'],
        },
        'elements': {
            'required': [],
            'optional': [],
        },
    }

    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.type: Optional[Key] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        return super().__str__()

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
    props = {
        'attributes': {
            'required': [],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': ['media'],
        },
    }

    def __init__(self, xml_tree=None):
        super().__init__()
        # elements
        self.medias: Optional[List[URLRef]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        return super().__str__()

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
    props = {
        'attributes': {
            'required': ['type', 'source'],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': ['glosses', 'form'],
        },
    }

    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.type: Key = None
        self.source: str = None
        # elements
        self.glosses: Optional[List[Gloss]] = None
        self.form: Optional[Form] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.type} ({self.source})"

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
    props = {
        'attributes': {
            'required': ['value'],
            'optional': [],
        },
        'elements': {
            'required': [],
            'optional': ['trait'],
        },
    }

    def __init__(self, xml_tree=None):
        # attributes
        self.value: Key = None
        # elements
        self.traits: Optional[List[Trait]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        return self.value

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
    props = {
        'attributes': {
            'required': [],
            'optional': ['type'],
        },
        'elements': {
            'required': [],
            'optional': ['main', 'grammatical_info'],
        },
    }

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
    props = {
        'attributes': {
            'required': [],
            'optional': ['type'],
        },
        'elements': {
            'required': [],
            'optional': [],
        },
    }

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
    props = {
        'attributes': {
            'required': [],
            'optional': ['source'],
        },
        'elements': {
            'required': [],
            'optional': ['translation', 'note'],
        },
    }

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
    props = {
        'attributes': {
            'required': ['type', 'ref'],
            'optional': ['order', 'usage'],
        },
        'elements': {
            'required': [],
            'optional': [],
        },
    }

    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.type: Key = None
        self.ref: RefId = None
        self.order: Optional[int] = None
        self.usage: Optional[Multitext] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        return f"{self.type}: {self.ref}"

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
    props = {
        'attributes': {
            'required': [],
            'optional': ['ref'],
        },
        'elements': {
            'required': [],
            'optional': ['pronunciations', 'relations'],
        },
    }

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
    props = {
        'attributes': {
            'required': [],
            'optional': ['id', 'order'],
        },
        'elements': {
            'required': [],
            'optional': [
                'grammatical_info',
                'glosses',
                'definition',
                'relations',
                'notes',
                'examples',
                'reversals',
                'illustrations',
                'subsenses',
            ],
        },
    }

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
        s = 'sense'
        if self.glosses:
            s = '; '.join([str(g) for g in self.glosses])
        elif self.id:
            s = self.id
        return s

    def show(self):
        print(self.__str__())

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
    props = {
        'attributes': {
            'required': [],
            'optional': ['id', 'guid', 'order', 'date_deleted'],
        },
        'elements': {
            'required': [],
            'optional': [
                'lexical_unit',
                'citation',
                'pronunciations',
                'variants',
                'senses',
                'notes',
                'relations',
                'etymologies'
            ],
        },
    }

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
        return self.get_summary_line()

    def get_senses_ct(self):
        ct = 0
        if self.senses:
            ct = len(self.senses)
        return ct

    def get_summary_line(self, lang='en'):
        lu = utils.ellipsize(str(self.lexical_unit), 20)
        gl = self.get_gloss(lang=lang)
        gi = self.get_grammatical_info()
        return f"{lu:20}\t{gl:30}\t{gi}"

    def get_grammatical_info(self, sense_idx=0):
        grammatical_info = ''
        if self.senses:
            grammatical_info = str(self.senses[sense_idx].grammatical_info)
        return grammatical_info

    def get_gloss(self, sense_idx=0, lang='en'):
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


class LIFT:
    props = {
        'attributes': {
            'required': ['version'],
            'optional': ['producer'],
        },
        'elements': {
            'required': [],
            'optional': ['header', 'entry'],
        },
    }

    def __init__(self, xml_tree=None):
        # attributes
        self.version: str = None
        self.producer: Optional[str] = None
        # elements
        self.header: Optional[Header] = None
        self.entries: Optional[List[Entry]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        s = f"LIFT lexicon v{self.version}"
        if self.producer:
            s += f"; produced by {self.producer}"
        return s

    def as_xml(self):
        logging.warning(f"{__class__}: \"as_xml\" not yet implemented.")

    def show(self):
        text = "No entries."
        if self.entries:
            summary_lines = [e.get_summary_line('en') for e in self.entries]
            slist = utils.unicode_sort(summary_lines)
            nl = '\n'
            text = nl.join(slist)
        print(text)

    def update_from_xml(self, xml_tree):
        for k, v in xml_tree.attrib.items():
            if k == 'version':
                self.version = v
            elif k == 'producer':
                self.producer = v

        for elem in xml_tree.getchildren():
            if elem.tag == 'header':
                # TODO: Add Header
                logging.warning(f"{__class__}: Unhandled XML tag: {elem.tag}")
                self.header = Header(elem)
            elif elem.tag == 'entry':
                entry = Entry(elem)
                if not self.entries:
                    self.entries = [entry]
                else:
                    self.entries.append(entry)
            else:
                logging.warning(f"{__class__}: Unhandled XML tag: {elem.tag}")
