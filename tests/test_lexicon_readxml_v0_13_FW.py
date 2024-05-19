import unittest
from lxml import etree

from . import DATA_PATH
from .utils import test_attribs
from .utils import test_elems

from lift_utils import lexicon

LIFT_GOOD = str(DATA_PATH / "lexicon_good_v0.13_FW.lift")
# LIFT_VERSION = '0.13'


class TestLexicon(unittest.TestCase):
    def setUp(self):
        self.xml_tree = etree.parse(LIFT_GOOD).getroot()
        self.obj = lexicon.Lexicon(LIFT_GOOD, self.xml_tree)

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


class TestEntry(unittest.TestCase):
    def setUp(self):
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//entry')
        self.obj = lexicon.Entry(self.xml_tree)

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


class TestSense(unittest.TestCase):
    def setUp(self):
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//sense')
        self.obj = lexicon.Sense(self.xml_tree)

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


class TestVariant(unittest.TestCase):
    def setUp(self):
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//variant')
        self.obj = lexicon.Variant(self.xml_tree)

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


class TestRelation(unittest.TestCase):
    def setUp(self):
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//relation')
        self.obj = lexicon.Relation(self.xml_tree)

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
