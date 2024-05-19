import unittest
from lxml import etree

from . import DATA_PATH
from .utils import test_attribs
from .utils import test_elems

from lift_utils import base
from lift_utils import config

ENTRY_LIFT_GOOD = str(DATA_PATH / "entry_good_v0.15.lift")


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        self.obj = base.Annotation(self.xml_tree)

    def test_annotation_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_annotation_elems(self):
        pass  # no elements


class TestExtensible(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.obj = base.Extensible(etree.parse(ENTRY_LIFT_GOOD).getroot())

    def test_extensible_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_extensible_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestField(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//field')
        self.obj = base.Field(self.xml_tree)

    def test_field_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_field_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestForm(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        self.obj = base.Form(self.xml_tree)

    def test_form_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_form_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestGloss(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//gloss')
        self.obj = base.Gloss(self.xml_tree)

    def test_gloss_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestMultitext(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        self.obj = base.Multitext(self.xml_tree)

    def test_multitext_attribs(self):
        pass  # no attribs

    def test_multitext_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        if config.LIFT_VERSION != config.LIFT_VERSION_FIELDWORKS:
            optional.remove('text')  # remove deprecated element
        test_elems(self, self.obj, optional)


class TestSpan(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//span')
        self.obj = base.Span(self.xml_tree)

    def test_span_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_span_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        optional.remove('spans')  # hard to test optional span-in-span element
        test_elems(self, self.obj, optional)


class TestText(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        self.obj = None
        for c in self.xml_tree.getchildren():
            if c.tag == 'text':
                self.obj = base.Text(c)
                break
        if not self.obj:
            raise AssertionError

    def test_text_attribs(self):
        pass  # no attribs

    def test_text_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        optional.remove('spans')  # already tested in test_span_elems
        test_elems(self, self.obj, optional)


class TestTrait(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('trait')
        self.obj = base.Trait(self.xml_tree)

    def test_trait_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_trait_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestURLRef(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = config.LIFT_VERSION_LATEST
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//urlref')  # noqa: E501
        self.obj = base.URLRef(self.xml_tree)

    def test_urlref_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_urlref_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)
