import unittest

from lxml import etree

from lift_utils import config, header

from . import DATA_PATH
from .utils import test_class_properties

HEADER_LIFT_GOOD = str(DATA_PATH / "header_good_v0.13_FW.lift")
LIFT_VERSION = "0.13"


class TestFieldDefn(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//field")  # noqa: E501
        self.obj = header.FieldDefn(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.FieldDefn, config.LIFT_VERSION)  # noqa: E501

    def test_properties(self):
        test_class_properties(self)


class TestFieldDefns(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//fields")  # noqa: E501
        self.obj = header.FieldDefns(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.FieldDefns, config.LIFT_VERSION)  # noqa: E501

    def test_properties(self):
        test_class_properties(self)

    def test_items(self):
        self.assertTrue(len(self.obj.field_items) > 1)


class TestHeader(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//header")  # noqa: E501
        self.obj = header.Header(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.Header, config.LIFT_VERSION)

    def test_properties(self):
        test_class_properties(self)


class TestRange(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//range")  # noqa: E501
        self.obj = header.Range13(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.Range13, config.LIFT_VERSION)

    def test_properties(self):
        test_class_properties(self)


class TestRanges(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//ranges")  # noqa: E501
        self.obj = header.Ranges(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.Ranges, config.LIFT_VERSION)

    def test_properties(self):
        test_class_properties(self)

    def test_items(self):
        self.assertTrue(len(self.obj.range_items) > 1)


class TestRangeElement(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//range-element")  # noqa: E501
        self.obj = header.RangeElement13(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.RangeElement13, config.LIFT_VERSION)  # noqa: E501

    def test_properties(self):
        test_class_properties(self)
