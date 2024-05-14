import unittest
from lxml import etree

from . import DATA_PATH

from lift_utils import base
from lift_utils import config

config.LIFT_VERSION = config.LIFT_VERSION_FIELDWORKS
ENTRY_LIFT_GOOD = str(DATA_PATH / "entry_good_FW.lift")


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        self.cls = base.Annotation
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        self.obj = self.cls(self.xml_tree)
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_annotation_attribs(self):
        required = self.props.get('attributes').get('required')
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')
        test_attribs(self, self.obj, optional)

    def test_annotation_elems(self):
        pass  # no elements


class TestExtensible(unittest.TestCase):
    def setUp(self):
        self.cls = base.Extensible
        self.obj = self.cls(etree.parse(ENTRY_LIFT_GOOD).getroot())
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_extensible(self):
        required = self.props.get('attributes').get('required')
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')
        test_attribs(self, self.obj, optional)


class TestField(unittest.TestCase):
    def setUp(self):
        self.cls = base.Field
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//field')
        self.obj = self.cls(self.xml_tree)
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_field_attribs(self):
        required = self.props.get('attributes').get('required')
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')
        test_attribs(self, self.obj, optional)

    def test_field_elems(self):
        required = self.props.get('elements').get('required')
        test_elems(self, self.obj, required)
        optional = self.props.get('elements').get('optional')
        test_elems(self, self.obj, optional)


class TestForm(unittest.TestCase):
    def setUp(self):
        self.cls = base.Form
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        self.obj = self.cls(self.xml_tree)
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_form_attribs(self):
        required = self.props.get('attributes').get('required')
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')
        test_attribs(self, self.obj, optional)

    def test_form_elems(self):
        required = self.props.get('elements').get('required')
        test_elems(self, self.obj, required)
        optional = self.props.get('elements').get('optional')
        test_elems(self, self.obj, optional)


class TestGloss(unittest.TestCase):
    def setUp(self):
        self.cls = base.Gloss
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//gloss')
        self.obj = self.cls(self.xml_tree)
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_gloss_attribs(self):
        required = self.props.get('attributes').get('required')
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')
        test_attribs(self, self.obj, optional)


class TestMultitext(unittest.TestCase):
    def setUp(self):
        self.cls = base.Multitext
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        self.obj = self.cls(self.xml_tree)
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_multitext_attribs(self):
        required = self.props.get('attributes').get('required')
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')
        test_attribs(self, self.obj, optional)


class TestSpan(unittest.TestCase):
    def setUp(self):
        self.cls = base.Span
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//span')
        self.obj = self.cls(self.xml_tree)
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_span_attribs(self):
        required = self.props.get('attributes').get('required')
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')
        test_attribs(self, self.obj, optional)

    def test_span_elems(self):
        required = self.props.get('elements').get('required')
        test_elems(self, self.obj, required)
        optional = self.props.get('elements').get('optional')
        optional.remove('spans')  # hard to test optional span-in-span element
        test_elems(self, self.obj, optional)


class TestText(unittest.TestCase):
    def setUp(self):
        self.cls = base.Text
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        self.props = self.cls._props.get(config.LIFT_VERSION)
        self.obj = None
        for c in self.xml_tree.getchildren():
            if c.tag == 'text':
                self.obj = base.Text(c)
                break
        if not self.obj:
            raise AssertionError

    def test_text_attribs(self):
        required = self.props.get('attributes').get('required')
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')
        test_attribs(self, self.obj, optional)

    def test_text_elems(self):
        required = self.props.get('elements').get('required')
        test_elems(self, self.obj, required)
        optional = self.props.get('elements').get('optional')
        optional.remove('spans')  # already tested in test_span_elems
        test_elems(self, self.obj, optional)


class TestTrait(unittest.TestCase):
    def setUp(self):
        self.cls = base.Trait
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('trait')
        self.obj = self.cls(self.xml_tree)
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_trait_attribs(self):
        required = self.props.get('attributes').get('required')  # noqa: E501
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')  # noqa: E501
        test_attribs(self, self.obj, optional)


class TestURLRef(unittest.TestCase):
    def setUp(self):
        self.cls = base.URLRef
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//urlref')  # noqa: E501
        self.obj = self.cls(self.xml_tree)
        self.props = self.cls._props.get(config.LIFT_VERSION)

    def test_urlref_attribs(self):
        required = self.props.get('attributes').get('required')  # noqa: E501
        test_attribs(self, self.obj, required)
        optional = self.props.get('attributes').get('optional')  # noqa: E501
        test_attribs(self, self.obj, optional)


def test_attribs(test_cls, obj, attribs):
    for a in attribs:
        try:
            test_cls.assertIsNotNone(obj.__dict__.get(a))
        except AssertionError as e:
            raise Exception(f"\"{a}\" {str(e)}")


def test_elems(test_cls, obj, elems):
    for elem in elems:
        try:
            test_cls.assertIsNotNone(obj.__dict__.get(elem))
        except AssertionError as e:
            raise Exception(f"\"{elem}\" {str(e)}")
