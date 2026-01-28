import unittest

from lxml import etree

from lift_utils import base, config

from . import DATA_PATH
from .utils import test_class_properties, test_properties

ENTRY_LIFT_GOOD = str(DATA_PATH / "entry_good_v0.15.lift")
LIFT_VERSION = config.LIFT_VERSION_LATEST


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find(".//annotation")  # noqa: E501
        self.obj = base.Annotation(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)


class TestExtensible(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.obj = base.Extensible(etree.parse(ENTRY_LIFT_GOOD).getroot())

    def test_properties(self):
        test_class_properties(self)


class TestField(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find(".//field")
        self.obj = base.Field(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)


class TestForm(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find(".//form")
        self.obj = base.Form(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)


class TestGloss(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find(".//gloss")
        self.obj = base.Gloss(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)


class TestMultitext(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find(".//annotation")  # noqa: E501
        self.obj = base.Multitext(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)


class TestSpan(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find(".//span")
        self.obj = base.Span(xml_tree=self.xml_tree)

    def test_properties(self):
        for group in (
            self.obj._attributes_required,
            self.obj._elements_required,
        ):
            test_properties(self, group, optional=False)
        elements_optional = self.obj._elements_optional.copy()
        elements_optional.discard("span")  # hard to test optional nested element
        for group in (
            self.obj._attributes_optional,
            elements_optional,
        ):
            test_properties(self, group, optional=True)


class TestText(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find(".//form")
        self.obj = None
        for c in self.xml_tree.getchildren():
            if c.tag == "text":
                self.obj = base.Text(c)
                break
        if not self.obj:
            raise AssertionError

    def test_properties(self):
        for group in (
            self.obj._attributes_required,
            self.obj._elements_required,
        ):
            test_properties(self, group, optional=False)
        elements_optional = self.obj._elements_optional.copy()
        elements_optional.discard("span")  # already tested in TestSpan
        for group in (
            self.obj._attributes_optional,
            elements_optional,
        ):
            test_properties(self, group, optional=True)


class TestTrait(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find("trait")
        self.obj = base.Trait(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)


class TestURLRef(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find(".//urlref")  # noqa: E501
        self.obj = base.URLRef(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)
