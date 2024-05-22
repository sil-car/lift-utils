# flake8: noqa: E501

import unittest
from lxml import etree

from lift_utils import base
from lift_utils import config
from lift_utils import datatypes
from lift_utils import utils

from lift_utils.lexicon import Etymology

LIFT_VERSION = '0.13'


class TestAnnotation(unittest.TestCase):
    def test_xml(self):
        obj = base.Annotation()
        obj.name = datatypes.Key("annotation-name")
        obj.value = datatypes.Key("annotation-value")
        obj.who = datatypes.Key("Annotation Who")
        obj.when = datatypes.DateTime("0000-00-00")

        xml = f"""
        <annotation name="{obj.name}" value="{obj.value}" who="{obj.who}" when="{obj.when}"/>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


# class TestExtensible(unittest.TestCase):
#     def test_xml(self):
#         obj = Etymology()
#         obj.type = datatypes.Key("Etype")
#         obj.source = "Esource"
#         obj.form = base.Form()
#         obj.glosses = [
#             base.Gloss(),
#             base.Gloss(),
#         ]
#         obj.date_created = datatypes.DateTime("0000-00-00")
#         obj.date_modified = datatypes.DateTime("0000-00-00")
#         obj.fields = [
#             base.Field(),
#             base.Field(),
#             base.Trait(),
#             base.Trait(),
#             base.Annotation(),
#             base.Annotation(),
#         ]

#         xml = f"""
#         <etymology type="Etype" source="Esource" dateCreated="{obj.date_created}" dateModified="{obj.date_modified}">
#             <form/>
#             <gloss/>
#             <gloss/>
#             <field/>
#             <field/>
#             <trait/>
#             <trait/>
#             <annotation/>
#             <annotation/>
#         </etymology>
#         """
#         xml_tree = utils.xmlstring_to_etree(xml)
#         self.assertEqual(
#             etree.tostring(obj._to_xml_tree(), pretty_print=True),
#             etree.tostring(xml_tree, pretty_print=True)
#         )


class TestField(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = base.Field()
        obj.date_created = datatypes.DateTime("0000-00-00")
        obj.date_modified = datatypes.DateTime("0000-00-00")
        obj.prop_type = datatypes.Key("field-type")
        obj.annotations = [
            base.Annotation(),
            base.Annotation(),
        ]
        obj.traits = [
            base.Flag(),
            base.Flag(),
        ]
        obj.forms = [
            base.Form(),
            base.Form(),
        ]

        xml = f"""
        <field dateCreated="{obj.date_created}" dateModified="{obj.date_modified}" type="{obj.prop_type}">
            <annotation/>
            <annotation/>
            <trait/>
            <trait/>
            <form/>
            <form/>
        </field>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # print(etree.tostring(obj._to_xml_tree(), pretty_print=True))
        # print(etree.tostring(xml_tree, pretty_print=True))
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestForm(unittest.TestCase):
    def test_xml(self):
        obj = base.Form()
        obj.lang = datatypes.Lang('en')
        obj.text = base.Text()
        obj.annotations = [
            base.Annotation(),
            base.Annotation(),
        ]

        xml = f"""
        <form lang="{obj.lang}">
            <text/>
            <annotation/>
            <annotation/>
        </form>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestGloss(unittest.TestCase):
    def test_xml(self):
        obj = base.Gloss()
        obj.traits = [
            base.Trait(),
            base.Trait(),
        ]

        xml = f"""
        <gloss>
            <trait/>
            <trait/>
        </gloss>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # print(etree.tostring(obj._to_xml_tree(), pretty_print=True))
        # print(etree.tostring(xml_tree, pretty_print=True))
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestMultitext(unittest.TestCase):
    def test_xml(self):
        obj = base.Multitext()
        obj.forms = [
            base.Form(),
            base.Form(),
        ]
        obj.traits = [
            base.Trait(),
            base.Trait(),
        ]

        xml = f"""
        <multitext>
            <form/>
            <form/>
            <trait/>
            <trait/>
        </multitext>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # print(etree.tostring(obj._to_xml_tree(), pretty_print=True))
        # print(etree.tostring(xml_tree, pretty_print=True))
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestSpan(unittest.TestCase):
    def test_xml(self):
        obj = base.Span()
        obj.lang = datatypes.Lang('en')
        obj.href = datatypes.URL("https://example.com")
        obj.class_ = "TestClass"
        obj.pcdata = datatypes.PCData("test text")
        obj.tail = datatypes.PCData(" a tail.")

        xml = f"""
        <xml>
        <span lang="{obj.lang}" href="{obj.href}" class="{obj.class_}">{obj.pcdata}</span>{obj.tail}</xml>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        xml_tree = xml_tree.getchildren()[0]
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestText(unittest.TestCase):
    def test_xml(self):
        obj = base.Text()
        obj.pcdata = datatypes.PCData('Test text')
        obj.spans = [
            base.Span(),
            base.Span(),
        ]

        xml = f"""
        <text>{obj.pcdata}<span/><span/></text>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestTrait(unittest.TestCase):
    def test_xml(self):
        obj = base.Trait()
        obj.name = datatypes.Key('TraitName')
        obj.value = datatypes.Key('TraitValue')
        obj.id = datatypes.Key('TraitID')
        obj.annotations = [
            base.Annotation(),
            base.Annotation(),
        ]

        xml = f"""
        <trait name="{obj.name}" value="{obj.value}" id="{obj.id}">
            <annotation/>
            <annotation/>
        </trait>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestURLRef(unittest.TestCase):
    def test_xml(self):
        obj = base.URLRef()
        obj.href = datatypes.URL("https://example.com")
        obj.label = base.Multitext()

        xml = f"""
        <urlref href="{obj.href}">
            <label/>
        </urlref>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )
