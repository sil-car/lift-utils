from typing import List
from typing import Optional

from base import Extensible
from base import Form
from base import Gloss
from base import Multitext
from base import Trait
from base import URLRef
from datatypes import DateTime
from datatypes import Key
from datatypes import RefId
from header import Header


class Note(Multitext, Extensible):
    # attributes
    n_type: Optional[Key] = None


class Phonetic(Multitext, Extensible):
    # elements
    medias: Optional[List[URLRef]] = None


class Etymology(Extensible):
    # attributes
    e_type: Key = ''
    source: str = ''
    # elements
    glosses: Optional[List[Gloss]] = None
    form: Optional[Form] = None


class GrammaticalInfo:
    # attributes
    value: Key = ''
    # elements
    traits: Optional[List[Trait]] = None


class Reversal(Multitext):
    # attributes
    r_type: Optional[Key] = None
    # elements
    main: Optional[str] = None  # Type should be 'Reversal' but not allowed
    grammatical_info: Optional[GrammaticalInfo] = None


class Translation(Multitext):
    # attributes
    t_type: Optional[Key] = None


class Example(Multitext, Extensible):
    # attributes
    source: Optional[Key] = None
    # elements
    translations: Optional[List[Translation]] = None
    notes: Optional[List[Note]] = None


class Relation(Extensible):
    # attributes
    r_type: Key = ''
    ref: RefId = ''
    order: Optional[int] = None
    usage: Optional[Multitext] = None


class Variant(Multitext, Extensible):
    # attributes
    ref: Optional[RefId] = None
    # elements
    pronunciations: Optional[List[Phonetic]] = None
    relations: Optional[List[Relation]] = None


class Sense(Extensible):
    # attributes
    s_id: Optional[RefId] = None
    order: Optional[int] = None
    # elements
    grammatical_info: Optional[GrammaticalInfo] = None
    glosses: Optional[List[Gloss]] = None
    definition: Optional[Multitext] = None
    relations: Optional[List[Relation]] = None
    notes: Optional[List[Note]] = None
    examples: Optional[List[Example]] = None
    reversals: Optional[List[Reversal]] = None
    illustrations: Optional[List[URLRef]] = None
    subsenses: Optional[List] = None  # Type should be 'Sense' but not allowed


class Entry(Extensible):
    # attributes
    e_id: Optional[RefId] = None
    guid: Optional[str] = None  # deprecated
    order: Optional[int] = None
    date_deleted: Optional[DateTime] = None
    # elements
    lexical_unit: Optional[Multitext] = None
    citation: Optional[Multitext] = None
    pronunciations: Optional[List[Phonetic]] = None
    variants: Optional[List[Variant]] = None
    senses: Optional[List[Sense]] = None
    notes: Optional[List[Note]] = None
    relations: Optional[List[Relation]] = None
    etymologies: Optional[List[Etymology]] = None


class LIFt:
    # attributes
    version: int = 0
    producer: Optional[str] = None
    # elements
    header: Optional[Header] = None
    entries: Optional[List[Entry]] = None
