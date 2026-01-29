import unittest

from lxml import etree

from lift_utils import config, header

from . import DATA_PATH
from .utils import test_class_properties, test_properties

HEADER_LIFT_GOOD = str(DATA_PATH / "header_good_v0.15.lift")
LIFT_VERSION = config.LIFT_VERSION_LATEST
config.LIFT_VERSION = None


class TestFieldDefinition(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//field")  # noqa: E501
        self.obj = header.FieldDefinition(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestFields(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//fields")  # noqa: E501
        self.obj = header.Fields(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def test_items(self):
        self.assertTrue(len(self.obj.field_items) > 1)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestHeader(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//header")  # noqa: E501
        self.obj = header.Header(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestRanges(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//ranges")  # noqa: E501
        self.obj = header.Ranges(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def test_items(self):
        self.assertTrue(len(self.obj.range_items) > 1)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestRange(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//range")  # noqa: E501
        self.obj = header.Range(xml_tree=self.xml_tree)

    def test_properties(self):
        for group in (
            self.obj._attributes_required,
            self.obj._elements_required,
        ):
            test_properties(self, group, optional=False)
        elem_optional = self.obj._elements_optional.copy()
        elem_optional.discard("annotation")
        elem_optional.discard("field")
        elem_optional.discard("trait")
        for group in (
            self.obj._attributes_optional,
            elem_optional,
        ):
            test_properties(self, group, optional=True)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestRangeElement(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find(".//range-element")  # noqa: E501
        self.obj = header.RangeElement(xml_tree=self.xml_tree)

    def test_properties(self):
        for group in (
            self.obj._attributes_required,
            self.obj._elements_required,
        ):
            test_properties(self, group, optional=False)
        elem_optional = self.obj._elements_optional.copy()
        elem_optional.discard("annotation")
        elem_optional.discard("field")
        elem_optional.discard("trait")
        for group in (
            self.obj._attributes_optional,
            elem_optional,
        ):
            test_properties(self, group, optional=True)

    def tearDown(self):
        config.LIFT_VERSION = None
