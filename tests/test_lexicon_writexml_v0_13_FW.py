# flake8: noqa

import unittest
from lxml import etree

from lift_utils import base
from lift_utils import config
from lift_utils import datatypes
from lift_utils import lexicon
from lift_utils import utils

LIFT_VERSION = '0.13'


@unittest.skip('not ready')
class TestEtymology(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Etymology()
        obj.type = datatypes.Key("Etype")
        obj.source = "Esource"
        obj.glosses = [
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


@unittest.skip('not ready')
class TestExtensible(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Etymology()
        obj.type = datatypes.Key("Etype")
        obj.source = "Esource"
        obj.glosses = [
            base.Gloss(),
            base.Gloss(),
        ]
        obj.form = base.Form()
        obj.date_created = datatypes.DateTime("0000-00-00")
        obj.date_modified = datatypes.DateTime("0000-00-00")
        obj.fields = [
            base.Field(),
            base.Field(),
        ]
        obj.traits = [
            base.Trait(),
            base.Trait(),
        ]
        obj.annotations = [
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
        # print(etree.tostring(obj._to_xml_tree(), pretty_print=True).decode())
        # print(etree.tostring(xml_tree, pretty_print=True).decode())
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


@unittest.skip('not ready')
class TestNote(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Note()
        obj.type = datatypes.Key("note-type")
        for p in obj.props.attributes:
            print(p.name)

        xml = f"""
        <note type="note-type"/>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


@unittest.skip('not ready')
class TestPhonetic(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = lexicon.Phonetic()
        obj.medias = [
            base.URLRef(),
            base.URLRef(),
        ]
        obj.forms = [
            base.Span(),
            base.Span(),
        ]

        xml = f"""
        <phonetic>
            <media/>
            <media/>
            <form/>
            <form/>
        </phonetic>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # print(etree.tostring(obj._to_xml_tree(), pretty_print=True))
        # print(etree.tostring(xml_tree, pretty_print=True))
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )
