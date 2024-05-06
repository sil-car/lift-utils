from typing import List
from typing import Optional

from datatypes import DateTime
from datatypes import Key
from datatypes import Lang
from datatypes import URL


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
