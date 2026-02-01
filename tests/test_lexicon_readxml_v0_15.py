import unittest

from lxml import etree

from lift_utils import config, lexicon

from . import DATA_PATH
from .utils import test_class_properties

LIFT_GOOD = str(DATA_PATH / "lexicon_good_v0.15.lift")
LIFT_VERSION = "0.15"


class TestEntry(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//entry")
        self.obj = lexicon.Entry(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestEtymology(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//etymology")
        self.obj = lexicon.Etymology(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestExample(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//example")
        self.obj = lexicon.Example(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestGrammaticalInfo(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//grammatical-info")  # noqa: E501
        self.obj = lexicon.GrammaticalInfo(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestLexicon(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot()
        self.obj = lexicon.Lexicon(path=LIFT_GOOD, xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestNote(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//note")
        self.obj = lexicon.Note(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestPhonetic(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//pronunciation")  # noqa: E501
        self.obj = lexicon.Phonetic(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestRelation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//relation")
        self.obj = lexicon.Relation(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestReversal(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//reversal")
        self.obj = lexicon.Reversal(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestSense(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//sense")
        self.obj = lexicon.Sense(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestTranslation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//translation")
        self.obj = lexicon.Translation(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None


class TestVariant(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find(".//variant")
        self.obj = lexicon.Variant(xml_tree=self.xml_tree)

    def test_properties(self):
        test_class_properties(self)

    def tearDown(self):
        config.LIFT_VERSION = None
