import unittest
from lxml import etree

from . import DATA_PATH

from lift_utils import base
from lift_utils import config

config.LIFT_VERSION = config.LIFT_VERSION_FIELDWORKS
ENTRY_LIFT_GOOD = str(DATA_PATH / "entry_good_FW.lift")


class TestAnnotation(unittest.TestCase):
    def test_annotation_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')
        ann = base.Annotation(xml_tree)
        for a in base.Annotation._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(ann.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")


class TestExtensible(unittest.TestCase):
    def test_extensible_good(self):
        ext = base.Extensible(etree.parse(ENTRY_LIFT_GOOD).getroot())
        for a in base.Extensible._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(ext.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")


class TestField(unittest.TestCase):
    def test_field_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//field')
        field = base.Field(xml_tree)
        for a in base.Field._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(field.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")


class TestForm(unittest.TestCase):
    def test_form_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        form = base.Form(xml_tree)
        for a in base.Form._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(form.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")

        for elem in base.Form._props.get(config.LIFT_VERSION).get('elements').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(form.__dict__.get(elem))
            except AssertionError as e:
                raise Exception(f"\"{elem}\" {str(e)}")


class TestGloss(unittest.TestCase):
    def test_gloss_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//gloss')
        glo = base.Gloss(xml_tree)
        for a in base.Gloss._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(glo.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")


class TestMultitext(unittest.TestCase):
    def test_multitext_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        mul = base.Multitext(xml_tree)
        for a in base.Multitext._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(mul.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")


class TestSpan(unittest.TestCase):
    def test_span_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//span')
        sp = base.Span(xml_tree)
        for a in base.Span._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(sp.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")

        for elem in base.Span._props.get(config.LIFT_VERSION).get('elements').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(sp.__dict__.get(elem))
            except AssertionError as e:
                raise Exception(f"\"{elem}\" {str(e)}")


class TestText(unittest.TestCase):
    def test_text_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        text = None
        for c in xml_tree.getchildren():
            if c.tag == 'text':
                text = base.Text(c)
                break
        if not text:
            raise AssertionError

        for a in base.Text._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(text.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")

        for elem in base.Text._props.get(config.LIFT_VERSION).get('elements').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(text.__dict__.get(elem))
            except AssertionError as e:
                raise Exception(f"\"{elem}\" {str(e)}")


class TestTrait(unittest.TestCase):
    def test_trait_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('trait')
        trait = base.Trait(xml_tree)
        for a in base.Trait._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(trait.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")


class TestURLRef(unittest.TestCase):
    def test_urlref_good(self):
        xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//urlref')
        ref = base.URLRef(xml_tree)
        for a in base.URLRef._props.get(config.LIFT_VERSION).get('attributes').get('required'):  # noqa: E501
            try:
                self.assertIsNotNone(ref.__dict__.get(a))
            except AssertionError as e:
                raise Exception(f"\"{a}\" {str(e)}")
