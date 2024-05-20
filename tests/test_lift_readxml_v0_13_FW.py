import unittest
# from lxml import etree

from . import DATA_PATH

from lift_utils import lift

LIFT_GOOD = str(DATA_PATH / "Pumi_2019" / "Pumi_2019.lift")
LIFT_VERSION = '0.13'


class TestLIFTFile(unittest.TestCase):
    def setUp(self):
        self.lift_file = lift.LIFTFile(LIFT_GOOD)
        self.lexicon = self.lift_file.to_lexicon()

    # def test_lexicon_header_ranges(self):
    #     print(len(self.lexicon.header.ranges))
