from typing import List
from typing import Optional

from .datatypes import PCData
from .datatypes import DateTime
from .datatypes import Key
from .datatypes import Lang
from .datatypes import URL


class Span:
    _attrib_req = []
    _attrib_opt = ['lang', 'href', 'class']
    _elem_req = ['pcdata']
    _elem_opt = ['spans']

    def __init__(self, xml_data=None):
        # attributes
        self.lang: Optional[Lang] = None
        self.href: Optional[URL] = None
        self.style_class: Optional[str] = None
        # elements
        self.pcdata = None
        self.spans: Optional[List[str]] = None  # Type should be 'Span'

        if xml_data is not None:
            self.update_from_xml(xml_data)

    def update_from_xml(self, xml_data):
        for k, v in xml_data.attrib.items():
            if k == 'lang':
                self.lang = Lang(k)
            elif k == 'href':
                self.href = URL(v)
            elif k == 'class':
                self.style_class = v

        if xml_data.text is not None:
            self.pcdata = PCData(xml_data.text)

        for c in xml_data.getchildren():
            if c.tag == 'span':
                s = Span(c)
                if not self.spans:
                    self.spans = [s]
                else:
                    self.spans.append(s)


class Text:
    _attrib_req = []
    _attrib_opt = []
    _elem_req = ['pcdata']
    _elem_opt = ['spans']

    def __init__(self, text=None):
        self.pcdata: str = None
        if text is not None:
            self.pcdata = PCData(text)
        self.spans: Optional[List[Span]] = None

    def __str__(self):
        return self.pcdata


class Trait:
    _attrib_req = ['name', 'value']
    _attrib_opt = ['id']
    _elem_req = []
    _elem_opt = ['annotations']

    def __init__(self, xml_tree=None):
        # attributes
        self.name: Key = None
        self.value: Key = None
        self.id: Optional[Key] = None
        # elements
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for k, v in xml_tree.attrib.items():
            if k == 'name':
                self.name = Key(v)
            elif k == 'value':
                self.value = Key(v)
            elif k == 'id':
                self.id = Key(v)

        for c in xml_tree.getchildren():
            if c.tag == 'annotation':
                a = Annotation(c)
                if not self.annotations:
                    self.annotations = [a]
                else:
                    self.annotations.append(a)


class Form:
    _attrib_req = ['lang']
    _attrib_opt = []
    _elem_req = ['text']
    _elem_opt = ['annotations']

    def __init__(self, xml_tree=None):
        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotations: Optional[List] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for k, v in xml_tree.attrib.items():
            if k == 'lang':
                self.lang = Lang(v)

        for c in xml_tree.getchildren():
            if c.tag == 'text':
                self.text = Text(c.text)
            elif c.tag == 'annotation':
                a = Annotation(c)
                if not self.annotations:
                    self.annotations = [a]
                else:
                    self.annotations.append(a)

    def update_other_from_self(self, other):
        other.lang = self.lang
        other.text = self.text
        other.annotations = self.annotations


class Multitext:
    _attrib_req = []
    _attrib_opt = []
    _elem_req = []
    _elem_opt = ['forms', 'text']

    def __init__(self, xml_tree=None):
        super().__init__()  # needed because listed 1st in multiple interitance
        # elements
        self.forms = None
        self.text = None  # deprecated

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def __str__(self):
        if self.forms:
            self.forms.sort()
            s = f"{self.forms[0].lang}: {self.forms[0].text}"
            ct = len(self.forms)
            if ct > 1:
                s = f"{s} ({ct} forms)"
            return s

    def update_from_xml(self, xml_tree):
        for c in xml_tree.getchildren():
            if c.tag == 'form':
                form = Form()
                form.update_from_xml(c)
                if not self.forms:
                    self.forms = [form]
                else:
                    self.forms.append(form)

    def update_other_from_self(self, other):
        other.forms = self.forms
        other.text = self.text


class Gloss(Form):
    _attrib_req = []
    _attrib_opt = []
    _elem_req = []
    _elem_opt = ['traits']

    def __init__(self, xml_tree=None):
        super().__init__()
        # elements
        self.traits: Optional[List[Trait]] = None

    def update_from_xml(self, xml_tree):
        form = Form(xml_tree)
        form.update_other_from_self(self)
        del form

        for c in xml_tree.getchildren():
            if c.tag == 'trait':
                t = Trait(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)


class URLRef:
    _attrib_req = ['href']
    _attrib_opt = []
    _elem_req = []
    _elem_opt = ['label']

    def __init__(self, xml_tree=None):
        # attributes
        self.href: URL = None
        # elements
        self.label: Optional[Multitext] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for k, v in xml_tree.attrib.items():
            if k == 'href':
                self.href = URL(v)

        for c in xml_tree.getchildren():
            if c.tag == 'label':
                self.label = Multitext(c)


class Annotation(Multitext):
    _attrib_req = ['name', 'value']
    _attrib_opt = ['who', 'when']
    _elem_req = []
    _elem_opt = []

    def __init__(self, xml_tree=None):
        super().__init__()
        self.name: Key = None
        self.value: Key = None
        self.who: Optional[Key] = None
        self.when: Optional[DateTime] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        mul = Multitext(xml_tree)
        mul.update_other_from_self(self)
        del mul

        for k, v in xml_tree.attrib.items():
            if k == 'name':
                self.name = Key(v)
            elif k == 'value':
                self.value = Key(v)
            elif k == 'who':
                self.who = Key(v)
            elif k == 'when':
                self.when = DateTime(v)


class Field(Multitext):
    _attrib_req = ['name']
    _attrib_opt = ['date_created', 'date_modified']
    _elem_req = []
    _elem_opt = ['traits', 'annotations']

    def __init__(self, xml_tree=None):
        super().__init__()
        # attributes
        self.name: str = None
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.traits: Optional[List[Trait]] = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        mul = Multitext(xml_tree)
        mul.update_other_from_self(self)
        del mul

        for k, v in xml_tree.attrib.items():
            if k == 'name':
                self.name = v
            elif k == 'dateCreated':
                self.date_created = DateTime(v)
            elif k == 'dateModified':
                self.date_modified = DateTime(v)

        for c in xml_tree.getchildren():
            if c.tag == 'trait':
                t = Trait(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)
            elif c.tag == 'annotation':
                a = Annotation(c)
                if not self.annotations:
                    self.annotations = [a]
                else:
                    self.annotations.append(a)


class Extensible:
    _attrib_req = []
    _attrib_opt = ['date_created', 'date_modified']
    _elem_req = []
    _elem_opt = ['fields', 'traits', 'annotations']

    def __init__(self, xml_tree=None):
        # attributes
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.fields: Optional[List[Field]] = None
        self.traits: Optional[List[Trait]] = None
        self.annotations: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        for k, v in xml_tree.attrib.items():
            if k == 'dateCreated':
                self.date_created = v
            elif k == 'dateModified':
                self.date_modified = v

        for c in xml_tree.getchildren():
            if c.tag == 'field':
                f = Field(c)
                if not self.fields:
                    self.fields = [f]
                else:
                    self.fields.append(f)
            elif c.tag == 'trait':
                t = Trait(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)
            elif c.tag == 'annotation':
                a = Annotation(c)
                if not self.annotations:
                    self.annotations = [a]
                else:
                    self.annotations.append(a)

    def update_other_from_self(self, other):
        other.date_created = self.date_created
        other.date_modified = self.date_modified
        other.fields = self.fields
        other.traits = self.traits
        other.annotations = self.annotations
