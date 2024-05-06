from typing import List
from typing import Optional


# Datatypes

class PCData(str):
    pass


class DateTime(str):
    # format (str): YYYY-MM-DDTHH:MM:SSZZZZZZ
    # ZZZZZZ: +/-, H, H, :, M, M (offset from GMT)
    pass


class Key(str):
    pass


class Lang(str):
    # format (str): ISO[-SCRIPT[-x-PRIVATE]]
    pass


class RefId(str):
    # format (HEX GUID): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    pass


class URL(str):
    pass


# Base elements

class Span:
    # attributes
    lang: Optional[Lang] = None
    href: Optional[URL] = None
    style_class: Optional[str] = None
    # elements
    pcdata = ''
    spans: Optional[List[str]] = None  # Type should be 'Span', but not allowed


class Text:
    pcdata: str = ''
    spans: Optional[List[Span]] = None


class Trait:
    name: Key = ''
    value: Key = ''
    trait_id: Optional[Key] = None


class Form:
    # attributes
    lang: Lang = ''
    # elements
    text: Text = ''
    annotations: Optional[List] = None


class Multitext:
    forms: Optional[List] = None
    text: Optional[str] = None  # deprecated


class Gloss(Form):
    # elements
    traits: Optional[List[Trait]] = None


class URLRef:
    # attributes
    href: URL = ''
    # elements
    label: Optional[Multitext] = None


class Annotation(Multitext):
    name: Key = ''
    value: Key = ''
    who: Optional[Key] = None
    when: Optional[DateTime] = None


class Field(Multitext):
    # attributes
    name: str = ''
    date_created: Optional[DateTime] = None
    date_modified: Optional[DateTime] = None
    # elements
    traits: Optional[List[Trait]] = None
    annotations: Optional[List[Annotation]] = None


class Extensible:
    # annotations
    date_created: Optional[DateTime] = None
    date_modified: Optional[DateTime] = None
    # elements
    fields: Optional[List[Field]] = None
    traits: Optional[List[Trait]] = None
    annotations: Optional[List[Annotation]] = None


# Header elements

class FieldDefinitions:
    # attributes
    name: Key = ''
    fd_class: Optional[str] = None
    fd_type: Optional[str] = None
    option_range: Optional[Key] = None
    writing_system: Optional[str] = None
    # elements
    label: Optional[Multitext] = None
    description: Optional[Multitext] = None


class Range:
    pass


class Ranges(list):
    pass


class Fields(list):
    pass


class Header:
    # elements
    description: Optional[Multitext] = None
    ranges: Optional[Ranges] = None
    fields: Optional[Fields] = None


# Core model elements

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
