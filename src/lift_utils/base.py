from typing import List
from typing import Optional

from .datatypes import PCData
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
    def __init__(self, text):
        self.pcdata: str = None
        if text:
            self.pcdata = PCData(text)
        self.spans: Optional[List[Span]] = None

    def __str__(self):
        return self.pcdata


class Trait:
    def __init__(self):
        self.name: Key = ''
        self.value: Key = ''
        self.id: Optional[Key] = None

    def update_from_xml(self, xml_tree):
        name = xml_tree.attrib.get('name')
        if name:
            self.name = name
        value = xml_tree.attrib.get('value')
        if value:
            self.value = value
        trait_id = xml_tree.attrib.get('trait-id')
        if trait_id:
            self.id = trait_id


class Form:
    def __init__(self, xml_tree=None):
        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotations: Optional[List] = None

        if xml_tree is not None:
            self.update_from_xml(xml_tree)

    def update_from_xml(self, xml_tree):
        lg = xml_tree.attrib.get('lang')
        if lg:
            self.lang = Lang(lg)
        for c in xml_tree:
            if c.tag == 'text':
                self.text = Text(c.text)

    def update_other_from_self(self, other):
        other.lang = self.lang
        other.text = self.text
        other.annotations = self.annotations


class Multitext:
    def __init__(self, xml_tree=None):
        super().__init__()  # needed because listed 1st in multiple interitance
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
                f = Field()
                f.update_from_xml(c)
                if not self.fields:
                    self.fields = [f]
                else:
                    self.fields.append(f)
            elif c.tag == 'trait':
                t = Trait()
                t.update_from_xml(c)
                if not self.traits:
                    self.traits = [t]
                else:
                    self.traits.append(t)
            elif c.tag == 'annotation':
                a = Annotation()
                a.update_from_xml(c)
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
