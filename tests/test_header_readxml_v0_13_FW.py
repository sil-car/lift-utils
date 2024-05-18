import unittest
from lxml import etree

from . import DATA_PATH
from .utils import test_attribs
from .utils import test_elems

from lift_utils import config
from lift_utils import header

HEADER_LIFT_GOOD = str(DATA_PATH / "header_good_v0.13_FW.lift")


class TestFields(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//fields')  # noqa: E501
        self.obj = header.Fields(self.xml_tree)

    def test_fields_attribs(self):
        pass  # no attributes to test

    def test_fields_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestHeader(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//header')  # noqa: E501
        self.obj = header.Header(self.xml_tree)

    def test_header_attribs(self):
        pass  # no attributes to test

    def test_header_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)


class TestRange(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = '0.13'
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//range')  # noqa: E501
        self.obj = header.Range(self.xml_tree)

    def test_range_attribs(self):
        required = [p.name for p in self.obj.props.attributes if p.required]
        test_attribs(self, self.obj, required)
        optional = [p.name for p in self.obj.props.attributes if not p.required]  # noqa: E501
        test_attribs(self, self.obj, optional)

    def test_range_elems(self):
        required = [p.name for p in self.obj.props.elements if p.required]
        test_elems(self, self.obj, required)
        optional = [p.name for p in self.obj.props.elements if not p.required]
        test_elems(self, self.obj, optional)
