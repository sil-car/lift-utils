import unittest
# from lxml import etree

from . import DATA_PATH

from lift_utils import lift

LIFT_GOOD = str(DATA_PATH / "Pumi_2019" / "Pumi_2019.lift")
LIFT_VERSION = '0.13'
LEXICON = lift.LIFTFile(LIFT_GOOD).to_lexicon()


class TestLIFTFile(unittest.TestCase):
    def setUp(self):
        self.lexicon = LEXICON

    def test_lexicon_header_fields(self):
        self.assertTrue(len(self.lexicon.header.fields.fields) == 11)

    def test_lexicon_header_ranges(self):
        self.assertTrue(len(self.lexicon.header.ranges.ranges) == 19)

    def test_lexicon_entries(self):
        self.assertTrue(len(self.lexicon.entries) == 2304)
