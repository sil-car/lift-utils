# flake8: noqa

import unittest
from lxml import etree

from .utils import compare_xml_trees

from lift_utils import base
from lift_utils import config
from lift_utils import datatypes
from lift_utils import header
from lift_utils import utils

LIFT_VERSION = '0.13'


class TestFieldDefn(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = header.FieldDefn(tag=base.Key('field-tag'))
        obj.form_items = [base.Form()]

        xml = f"""
        <field tag="field-tag">
            <form/>
        </field>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestFieldDefns(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = header.FieldDefns()
        obj.field_items = [
            header.FieldDefn(),
        ]

        xml = f"""
        <fields>
            <field/>
        </fields>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestHeader(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = header.Header()
        obj.ranges = header.Ranges()
        obj.ranges.range_items = [
            header.Range(),
            header.Range(),
        ]
        for r in obj.ranges.range_items:
            r.href = base.URL('///fake/path')
        obj.ranges.range_items[0].id = base.Key('range-1')
        obj.ranges.range_items[1].id = base.Key('range-2')
        obj.fields = header.FieldDefns()
        obj.fields.field_items = [
            header.FieldDefn(),
            header.FieldDefn(),
        ]
        obj.xml_tree = obj._to_xml_tree()

        xml = f"""
        <header>
            <ranges>
                <range id="range-1" href="///fake/path"/>
                <range id="range-2" href="///fake/path"/>
            </ranges>
            <fields>
                <field/>
                <field/>
            </fields>
        </header>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # compare_xml_trees(obj.xml_tree, xml_tree)
        self.assertEqual(
            etree.tostring(obj.xml_tree, pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestRange(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = header.Range()
        obj.id = base.Key('range-id')
        obj.href = base.URL('///fake/path')
        obj.range_elements = [header.RangeElement()]
        obj.xml_tree = obj._to_xml_tree()

        xml = f"""
        <range id="range-id" href="///fake/path"/>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        ranges_xml = f"""
        <range id="range-id">
            <range-element/>
        </range>
        """
        ranges_xml_tree = utils.xmlstring_to_etree(ranges_xml)
        # compare_xml_trees(obj.xml_tree, xml_tree)
        self.assertEqual(
            etree.tostring(obj.xml_tree, pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )
        # compare_xml_trees(obj.ranges_xml_tree, ranges_xml_tree)
        self.assertEqual(
            etree.tostring(obj.ranges_xml_tree, pretty_print=True),
            etree.tostring(ranges_xml_tree, pretty_print=True)
        )


class TestRangeElement(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = header.RangeElement(elem_id='range-element-id')
        obj.label_items = [base.Multitext()]

        xml = f"""
        <range-element id="range-element-id">
            <label/>
        </range-element>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(obj._to_xml_tree(), pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )


class TestRanges(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.obj = header.Ranges()
        self.obj.range_items = [
            header.Range(),
        ]
        self.obj.xml_tree = self.obj._to_xml_tree()

    def test_xml(self):
        xml = f"""
        <ranges>
            <range/>
        </ranges>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # compare_xml_trees(self.obj.xml_tree, xml_tree)
        self.assertEqual(
            etree.tostring(self.obj.xml_tree, pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )

    def test_ranges_xml(self):
        xml = f"""
        <lift-ranges>
            <range/>
        </lift-ranges>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            etree.tostring(self.obj.ranges_xml_tree, pretty_print=True),
            etree.tostring(xml_tree, pretty_print=True)
        )
