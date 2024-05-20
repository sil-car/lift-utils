import unittest
from lxml import etree

from . import DATA_PATH
from .utils import test_attribs
from .utils import test_elems

from lift_utils import config
from lift_utils import header

HEADER_LIFT_GOOD = str(DATA_PATH / "header_good_v0.13_FW.lift")
LIFT_VERSION = '0.13'


class TestFieldDefn(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//field')  # noqa: E501
        self.obj = header.FieldDefn(self.xml_tree)

    def test_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)


class TestFieldDefns(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//fields')  # noqa: E501
        self.obj = header.FieldDefns(self.xml_tree)

    def test_attribs(self):
        pass  # no attributes to test

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)

    def test_items(self):
        self.assertTrue(len(self.obj.fields) > 1)


class TestHeader(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//header')  # noqa: E501
        self.obj = header.Header(self.xml_tree)

    def test_attribs(self):
        pass  # no attributes to test

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestRanges(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//ranges')  # noqa: E501
        self.obj = header.Ranges(self.xml_tree)

    def test_attribs(self):
        pass  # no attributes

    def test_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)

    def test_items(self):
        self.assertTrue(len(self.obj.ranges) > 1)


class TestRange(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//range')  # noqa: E501
        self.obj = header.Range(self.xml_tree)

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


class TestRangeElement(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//range-element')  # noqa: E501
        self.obj = header.RangeElement(self.xml_tree)

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
