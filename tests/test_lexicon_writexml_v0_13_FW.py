# flake8: noqa: E501

import unittest
from lxml import etree

from lift_utils import config
from lift_utils import datatypes
from lift_utils import lexicon
from lift_utils import utils

LIFT_VERSION = '0.13'


@unittest.skip('method not ready')
class TestExtensible(unittest.TestCase):
    def test_xml(self):
        obj = lexicon.Etymology()
        obj.type = datatypes.Key("Etype")
        obj.source = "Esource"
        obj.form = base.Form()
        obj.glosses = [
            base.Gloss(),
            base.Gloss(),
        ]
        obj.date_created = datatypes.DateTime("0000-00-00")
        obj.date_modified = datatypes.DateTime("0000-00-00")
        obj.fields = [
            base.Field(),
            base.Field(),
            base.Trait(),
            base.Trait(),
            base.Annotation(),
            base.Annotation(),
        ]

        xml = f"""
        <etymology type="Etype" source="Esource" dateCreated="{obj.date_created}" dateModified="{obj.date_modified}">
            <form/>
            <gloss/>
            <gloss/>
            <field/>
            <field/>
            <trait/>
            <trait/>
            <annotation/>
            <annotation/>
        </etymology>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )
