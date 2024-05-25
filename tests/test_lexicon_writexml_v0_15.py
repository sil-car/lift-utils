# flake8: noqa

import unittest
from lxml import etree

from .utils import compare_xml_trees

from lift_utils import base
from lift_utils import config
from lift_utils import datatypes
from lift_utils import lexicon
from lift_utils import utils

LIFT_VERSION = '0.13'


class TestEntry(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Entry()
        obj.id = lexicon.RefId('unique-entry-and-sense-id')
        obj.lexical_unit = lexicon.Multitext()
        obj.sense_items = [lexicon.Sense()]

        xml = f"""
        <entry id="unique-entry-and-sense-id">
            <lexical-unit/>
            <sense/>
        </entry>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestEtymology(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Etymology(
            etym_type=datatypes.Key("Etype"),
            source="Esource"
        )
        obj.gloss_items = [
            base.Gloss(),
            base.Gloss(),
        ]
        obj.form = base.Form()

        xml = f"""
        <etymology type="Etype" source="Esource">
            <gloss/>
            <gloss/>
            <form/>
        </etymology>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestExample(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Example()
        obj.source = base.Key('example source')
        obj.translation_items = [
            lexicon.Translation()
        ]

        xml = f"""
        <example source="example source">
            <translation/>
        </example>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestExtensible(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Etymology()
        obj.type = datatypes.Key("Etype")
        obj.source = "Esource"
        obj.gloss_items = [
            base.Gloss(),
            base.Gloss(),
        ]
        obj.form = base.Form()
        obj.date_created = datatypes.DateTime("0000-00-00")
        obj.date_modified = datatypes.DateTime("0000-00-00")
        obj.field_items = [
            base.Field(),
            base.Field(),
        ]
        obj.trait_items = [
            base.Trait(),
            base.Trait(),
        ]
        obj.annotation_items = [
            base.Annotation(),
            base.Annotation(),
        ]

        xml = f"""
        <etymology dateCreated="{obj.date_created}" dateModified="{obj.date_modified}" type="Etype" source="Esource">
            <field/>
            <field/>
            <trait/>
            <trait/>
            <annotation/>
            <annotation/>
            <gloss/>
            <gloss/>
            <form/>
        </etymology>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestGrammaticalInfo(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.GrammaticalInfo(value=datatypes.Key("g-i-value"))
        obj.trait_items = [
            base.Trait(),
        ]

        xml = f"""
        <grammatical-info value="g-i-value">
            <trait/>
        </grammatical-info>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestLexicon(unittest.TestCase):
    def test_xml(self):
        # config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Lexicon(version='0.13')
        obj.producer = f"LIFTUtils {config.LIB_VERSION}"
        obj.entry_items = [
            lexicon.Entry(),
        ]

        xml = f"""
        <lift version="0.13" producer="LIFTUtils {config.LIB_VERSION}">
            <entry/>
        </lift>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestNote(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Note()
        obj.type = datatypes.Key("note-type")
        obj.form_items = [
            base.Form(
                lang=datatypes.Lang("en"),
                text=base.Text("This is a note")
            )
        ]

        xml = f"""
        <note type="note-type">
            <form lang="en">
                <text>This is a note</text>
            </form>
        </note>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # compare_xml_trees(obj._to_xml_tree(), xml_tree)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestPhonetic(unittest.TestCase):
    def test_xml(self):
        href1 = 'https://example.com'
        href2 = 'file:///home/user/audio.wav'
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Phonetic()
        obj.media_items = [
            base.URLRef(href1),
            base.URLRef(href2),
        ]
        obj.form_items = [
            base.Span(),
            base.Span(),
        ]

        xml = f"""
        <pronunciation>
            <form/>
            <form/>
            <media href="{href1}"/>
            <media href="{href2}"/>
        </pronunciation>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # compare_xml_trees(obj._to_xml_tree(), xml_tree)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestRelation(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Relation(
            rel_type=base.Key("rel-type"),
            ref=lexicon.RefId("ref-id")
        )
        obj.usage_items = [
            base.Multitext()
        ]

        xml = f"""
        <relation type="rel-type" ref="ref-id">
            <usage/>
        </relation>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestReversal(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Reversal()
        obj.main = lexicon.Reversal()
        obj.grammatical_info = lexicon.GrammaticalInfo(value="g-i-value")

        xml = f"""
        <reversal>
            <main/>
            <grammatical-info value="g-i-value"/>
        </reversal>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestSense(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Sense()
        obj.grammatical_info = lexicon.GrammaticalInfo()
        obj.definition = lexicon.Multitext()
        obj.subsense_items = [lexicon.Sense()]

        xml = f"""
        <sense>
            <grammatical-info/>
            <definition/>
            <subsense/>
        </sense>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestTranslation(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Translation()
        obj.type = base.Key('literal')
        obj.form_items = [
            base.Form()
        ]

        xml = f"""
        <translation type="literal">
            <form/>
        </translation>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestVariant(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Variant()
        obj.pronunciation_items = [lexicon.Phonetic()]
        obj.relation_items = [lexicon.Relation()]

        xml = f"""
        <variant>
            <pronunciation/>
            <relation/>
        </variant>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )
