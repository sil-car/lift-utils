# flake8: noqa: E501

import unittest

from lift_utils import base, config, datatypes, utils

LIFT_VERSION = "0.13"


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION

    def test_xml(self):
        name = "annotation-name"
        value = "annotation-value"
        who = "Annotation Who"
        when = "0000-00-00"
        obj = base.Annotation(name=name, value=value, who=who, when=when)

        xml = f"""
        <annotation name="{name}" value="{value}" who="{who}" when="{when}"/>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree),
        )

    def tearDown(self):
        config.LIFT_VERSION = None


class TestField(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION

    def test_xml(self):
        obj = base.Field(field_type="field-type")
        obj.date_created = datatypes.DateTime("0000-00-00")
        obj.date_modified = datatypes.DateTime("0000-00-00")
        obj.annotation_items = [
            base.Annotation(
                name="",
                value="",
            ),
            base.Annotation(
                name="",
                value="",
            ),
        ]
        obj.trait_items = [
            base.Trait(name="", value=""),
            base.Trait(name="", value=""),
        ]
        obj.form_items = [
            base.Form(lang="", text=""),
            base.Form(lang="", text=""),
        ]

        xml = f"""
        <field dateCreated="{obj.date_created}" dateModified="{obj.date_modified}" type="{obj.type}">
            <annotation name="" value=""/>
            <annotation name="" value=""/>
            <form lang="">
                <text/>
            </form>
            <form lang="">
                <text/>
            </form>
            <trait name="" value=""/>
            <trait name="" value=""/>
        </field>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree),
        )

    def tearDown(self):
        config.LIFT_VERSION = None


class TestForm(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION

    def test_xml(self):
        obj = base.Form(lang="en", text="")
        obj.annotation_items = [
            base.Annotation(
                name="",
                value="",
            ),
            base.Annotation(
                name="",
                value="",
            ),
        ]

        xml = """
        <form lang="en">
            <annotation name="" value=""/>
            <annotation name="" value=""/>
            <text/>
        </form>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree),
        )

    def tearDown(self):
        config.LIFT_VERSION = None


class TestGloss(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION

    def test_xml(self):
        obj = base.Gloss(lang="", text="")
        obj.trait_items = [
            base.Trait(name="", value=""),
            base.Trait(name="", value=""),
        ]

        xml = """
        <gloss lang="">
            <text/>
            <trait name="" value=""/>
            <trait name="" value=""/>
        </gloss>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree),
        )

    def tearDown(self):
        config.LIFT_VERSION = None


class TestSpan(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION

    def test_xml(self):
        text = "test text"
        obj = base.Span(text=text)
        obj.lang = datatypes.Lang("en")
        obj.href = datatypes.URL("https://example.com")
        obj.class_ = "TestClass"
        obj.tail = datatypes.PCData(" a tail.")

        xml = f"""
        <xml>
        <span class="{obj.class_}" href="{obj.href}" lang="{obj.lang}" >{text}</span>{obj.tail}</xml>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        xml_tree = xml_tree.getchildren()[0]
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree),
        )

    def tearDown(self):
        config.LIFT_VERSION = None


class TestText(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION

    def test_xml(self):
        obj = base.Text("Test text")
        obj.span_items = [
            base.Span(text=""),
            base.Span(text=""),
        ]

        xml = """
        <text>Test text<span/><span/></text>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree),
        )

    def tearDown(self):
        config.LIFT_VERSION = None


class TestTrait(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION

    def test_xml(self):
        obj = base.Trait(name="TraitName", value="TraitValue")
        obj.id = datatypes.Key("TraitID")
        obj.annotation_items = [
            base.Annotation(name="", value=""),
            base.Annotation(name="", value=""),
        ]

        xml = f"""
        <trait name="TraitName" value="TraitValue" id="{obj.id}">
            <annotation name="" value=""/>
            <annotation name="" value=""/>
        </trait>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree),
        )

    def tearDown(self):
        config.LIFT_VERSION = None


class TestURLRef(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION

    def test_xml(self):
        obj = base.URLRef(href="https://example.com")
        obj.label = base.Multitext()

        xml = """
        <urlref href="https://example.com">
            <label/>
        </urlref>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree),
        )

    def tearDown(self):
        config.LIFT_VERSION = None
