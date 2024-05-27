import unittest
from lxml import etree

from . import DATA_PATH

from lift_utils import lexicon
from lift_utils.utils import xmlfile_to_etree

LIFT_GOOD = DATA_PATH / "Pumi_2019" / "Pumi_2019.lift"
LIFT_VERSION = '0.13'
LEXICON = lexicon.Lexicon()
LEXICON.parse_lift(LIFT_GOOD)


class TestParse(unittest.TestCase):
    def setUp(self):
        self.lexicon = LEXICON

    def test_lexicon_header_field_items(self):
        self.assertTrue(len(self.lexicon.header.fields.field_items) == 11)

    def test_lexicon_header_ranges(self):
        self.assertTrue(len(self.lexicon.header.ranges.range_items) == 19)

    def test_lexicon_entry_items(self):
        self.assertTrue(len(self.lexicon.entry_items) == 2304)


class TestReadWrite(unittest.TestCase):
    # NOTE: I haven't yet found a reliable way to compare XML file data. Using
    # "canonicalize" and "tostring" both result in XML strings whose child
    # element orders depend on the tree order rather than some kind of sorted
    # order useful for comparison. And since the element order of the input
    # file is unpredictable, there's no way to guarantee that the output file
    # will produce the same order, even if contents are identical.
    def test_read_write_file(self):
        infile = LIFT_GOOD
        outfile = DATA_PATH / "Pumi_out.lift"
        LEXICON.to_lift(outfile)
        xml_in = etree.tostring(
            xmlfile_to_etree(infile),
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()
        xml_out = etree.tostring(
            xmlfile_to_etree(outfile),
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()

        ranges_xml_in = etree.tostring(
            xmlfile_to_etree(infile.with_suffix('.lift-ranges')),
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()
        ranges_xml_out = etree.tostring(
            xmlfile_to_etree(outfile.with_suffix('.lift-ranges')),
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()
        # xml_in = etree.canonicalize(
        #     xmlfile_to_etree(infile),
        #     strip_text=True
        # )
        # xml_out = etree.canonicalize(
        #     xmlfile_to_etree(outfile),
        #     strip_text=True
        # )
        # self.maxDiff = None
        # NOTE: In lieu of being able to compare xml content, just using a file
        # size comparison for the time being. This works okay as long as there
        # aren't too many comments in the infile, since comments aren't kept.
        # This tests that the outfile's size is within 7% of the infile's.
        delta = 0.05
        # print(len(xml_out)/len(xml_in))
        # print(len(ranges_xml_out)/len(ranges_xml_in))
        self.assertAlmostEqual(
            1,
            len(xml_out)/len(xml_in),
            delta=delta
        )
        self.assertAlmostEqual(
            1,
            len(ranges_xml_out)/len(ranges_xml_in),
            delta=delta
        )
