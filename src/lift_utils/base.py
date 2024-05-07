from typing import List
from typing import Optional

from .datatypes import DateTime
from .datatypes import Key
from .datatypes import Lang
from .datatypes import URL


class Span:
    def __init__(self):
        # attributes
        self.lang: Optional[Lang] = None
        self.href: Optional[URL] = None
        self.style_class: Optional[str] = None
        # elements
        self.pcdata = ''
        self.spans: Optional[List[str]] = None  # Type should be 'Span'


class Text:
    def __init__(self):
        self.pcdata: str = ''
        self.spans: Optional[List[Span]] = None


class Trait:
    def __init__(self):
        self.name: Key = ''
        self.value: Key = ''
        self.trait_id: Optional[Key] = None


class Form:
    def __init__(self):
        # attributes
        self.lang: Lang = ''
        # elements
        self.text: Text = ''
        self.annotations: Optional[List] = None


class Multitext:
    def __init__(self):
        self.forms: Optional[List] = None
        self.text: Optional[str] = None  # deprecated


class Gloss(Form):
    def __init__(self):
        super().__init__()
        # elements
        self.traits: Optional[List[Trait]] = None


class URLRef:
    def __init__(self):
        # attributes
        self.href: URL = ''
        # elements
        self.label: Optional[Multitext] = None


class Annotation(Multitext):
    def __init__(self):
        super().__init__()
        self.name: Key = ''
        self.value: Key = ''
        self.who: Optional[Key] = None
        self.when: Optional[DateTime] = None


class Field(Multitext):
    def __init__(self):
        super().__init__()
        # attributes
        self.name: str = ''
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.traits: Optional[List[Trait]] = None
        self.annotations: Optional[List[Annotation]] = None


class Extensible:
    def __init__(self):
        # annotations
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.fields: Optional[List[Field]] = None
        self.traits: Optional[List[Trait]] = None
        self.annotations: Optional[List[Annotation]] = None
