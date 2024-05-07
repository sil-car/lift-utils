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
    def __init__(self):
        super().__init__()
        # attributes
        self.n_type: Optional[Key] = None


class Phonetic(Multitext, Extensible):
    def __init__(self):
        super().__init__()
        # elements
        self.medias: Optional[List[URLRef]] = None


class Etymology(Extensible):
    def __init__(self):
        super().__init__()
        # attributes
        self.type: Key = ''
        self.source: str = ''
        # elements
        self.glosses: Optional[List[Gloss]] = None
        self.form: Optional[Form] = None


class GrammaticalInfo:
    def __init__(self):
        # attributes
        self.value: Key = ''
        # elements
        self.traits: Optional[List[Trait]] = None


class Reversal(Multitext):
    def __init__(self):
        super().__init__()
        # attributes
        self.r_type: Optional[Key] = None
        # elements
        self.main: Optional[str] = None  # Type should be 'Reversal'
        self.grammatical_info: Optional[GrammaticalInfo] = None


class Translation(Multitext):
    def __init__(self):
        super().__init__()
        # attributes
        self.t_type: Optional[Key] = None


class Example(Multitext, Extensible):
    def __init__(self):
        super().__init__()
        # attributes
        self.source: Optional[Key] = None
        # elements
        self.translations: Optional[List[Translation]] = None
        self.notes: Optional[List[Note]] = None


class Relation(Extensible):
    def __init__(self):
        super().__init__()
        # attributes
        self.type: Key = ''
        self.ref: RefId = ''
        self.order: Optional[int] = None
        self.usage: Optional[Multitext] = None


class Variant(Multitext, Extensible):
    def __init__(self):
        super().__init__()
        # attributes
        self.ref: Optional[RefId] = None
        # elements
        self.pronunciations: Optional[List[Phonetic]] = None
        self.relations: Optional[List[Relation]] = None


class Sense(Extensible):
    def __init__(self):
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


class Entry(Extensible):
    def __init__(self):
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


class LIFT:
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
