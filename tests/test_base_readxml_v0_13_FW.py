import unittest
from lxml import etree

from . import DATA_PATH
from .utils import test_attribs
from .utils import test_elems

from lift_utils import base
from lift_utils import config

ENTRY_LIFT_GOOD = str(DATA_PATH / "entry_good_v0.13_FW.lift")


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        self.obj = base.Annotation(xml_tree=self.xml_tree)

    def test_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        pass  # no elements


class TestExtensible(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.obj = base.Extensible(etree.parse(ENTRY_LIFT_GOOD).getroot())

    def test_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestField(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//field')
        self.obj = base.Field(xml_tree=self.xml_tree)

    def test_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        optional.remove('span_items')
        test_elems(self, self.obj, optional)


class TestForm(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        self.obj = base.Form(xml_tree=self.xml_tree)

    def test_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestGloss(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//gloss')
        self.obj = base.Gloss(xml_tree=self.xml_tree)

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestMultitextText(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().findall('.//annotation')[1]  # noqa: E501
        self.obj = base.Multitext(xml_tree=self.xml_tree)

    def test_attribs(self):
        pass  # no attribs

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        optional.remove('form_items')
        optional.remove('trait_items')
        test_elems(self, self.obj, optional)


class TestMultitextForm(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        self.obj = base.Multitext(xml_tree=self.xml_tree)

    def test_attribs(self):
        pass  # no attribs

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        required.remove('pcdata')
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        optional.remove('span_items')
        test_elems(self, self.obj, optional)


class TestSpan(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//span')
        self.obj = base.Span(xml_tree=self.xml_tree)

    def test_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        optional.remove('span_items')  # hard to test optional nested element
        test_elems(self, self.obj, optional)


class TestText(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//text')
        self.obj = base.Text(xml_tree=self.xml_tree)

    def test_attribs(self):
        pass  # no attribs

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestTrait(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('trait')
        self.obj = base.Trait(xml_tree=self.xml_tree)

    def test_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestURLRef(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//urlref')  # noqa: E501
        self.obj = base.URLRef(xml_tree=self.xml_tree)

    def test_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)
