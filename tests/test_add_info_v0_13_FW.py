import unittest
from pathlib import Path

from lift_utils import lexicon
from lift_utils import Lexicon
from lift_utils import base
from lift_utils import datatypes
from lift_utils import errors

DATA_DIR = Path(__file__).parent / 'data'
LEXICON = Lexicon(DATA_DIR / "sango" / "sango.lift")


class TestAddExtensibleItems(unittest.TestCase):
    def setUp(self):
        self.lexicon = LEXICON
        self.entry = self.lexicon.entry_items[0]

    def test_add_annotation(self):
        self.assertRaises(
            errors.RequiredValueException,
            self.entry.add_annotation,
            name='name'
            )
        self.entry.add_annotation(name="test", value="test value")
        self.assertIsInstance(self.entry.annotation_items[0], base.Annotation)
        self.assertEqual(len(self.entry.annotation_items), 1)

    def test_add_field(self):
        self.assertRaises(
            errors.RequiredValueException,
            self.entry.add_field
        )
        self.entry.add_field(name="Test Field")
        self.assertIsInstance(self.entry.field_items[0], base.Field)
        self.assertEqual(self.entry.field_items[0].type, 'Test Field')

    def test_add_trait(self):
        self.assertRaises(
            errors.RequiredValueException,
            self.entry.add_trait
        )
        idx = 0
        if self.entry.trait_items:
            idx = len(self.entry.trait_items)
        self.entry.add_trait(name="trait-name", value="trait-value")
        self.assertIsInstance(self.entry.trait_items[idx], base.Trait)
        self.assertEqual(self.entry.trait_items[idx].name, 'trait-name')
        self.assertEqual(self.entry.trait_items[idx].value, 'trait-value')


class TestCreateBaseItems(unittest.TestCase):
    def test_create_annotation_missing_info(self):
        self.assertRaises(errors.RequiredValueException, base.Annotation)
        self.assertRaises(
            errors.RequiredValueException,
            base.Annotation,
            name='test'
        )

    def test_create_annotation_optional(self):
        self.anno = base.Annotation(
            name='optional-name',
            value='optional-value',
            who='optional-person',
            when='optional-timestamp'
        )
        self.assertIsInstance(self.anno.who, datatypes.Key)
        self.assertIsInstance(self.anno.when, datatypes.DateTime)
        self.assertEqual(self.anno.who, 'optional-person')
        self.assertEqual(self.anno.when, 'optional-timestamp')

    def test_create_annotation_required(self):
        self.anno = base.Annotation(name='test', value="value")
        self.assertIsInstance(self.anno.name, datatypes.Key)
        self.assertIsInstance(self.anno.value, datatypes.Key)
        self.assertEqual(self.anno.name, 'test')
        self.assertEqual(self.anno.value, 'value')

    def test_create_annotation(self):
        self.assertRaises(errors.RequiredValueException, base.Annotation)
        self.assertRaises(
            errors.RequiredValueException,
            base.Annotation,
            name='test'
        )
        self.anno = base.Annotation(
            name='name',
            value='value',
            who='optional-person',
            when='optional-timestamp'
        )
        self.assertIsInstance(self.anno.name, datatypes.Key)
        self.assertIsInstance(self.anno.value, datatypes.Key)
        self.assertIsInstance(self.anno.who, datatypes.Key)
        self.assertIsInstance(self.anno.when, datatypes.DateTime)
        self.assertEqual(self.anno.name, 'name')
        self.assertEqual(self.anno.value, 'value')
        self.assertEqual(self.anno.who, 'optional-person')
        self.assertEqual(self.anno.when, 'optional-timestamp')

    def test_create_field(self):
        self.assertRaises(errors.RequiredValueException, base.Field)
        self.field = base.Field(
            field_type="test-field"
        )
        self.assertIsInstance(self.field.type, datatypes.Key)
        self.assertEqual(self.field.type, "test-field")

    def test_create_form(self):
        self.assertRaises(errors.RequiredValueException, base.Form)
        self.form = base.Form(
            lang="en",
            text="text"
        )
        self.assertIsInstance(self.form.lang, datatypes.Lang)
        self.assertIsInstance(self.form.text, base.Text)
        self.assertEqual(self.form.lang, "en")
        self.assertEqual(str(self.form.text), "text")

    def test_create_span(self):
        self.assertRaises(errors.RequiredValueException, base.Span)
        self.span = base.Span(
            text="this text",
            lang="en",
            href="https://example.com",
            span_class="bold",
            tail="tail text"
        )
        self.assertIsInstance(self.span.pcdata, datatypes.PCData)
        self.assertIsInstance(self.span.tail, datatypes.PCData)
        self.assertIsInstance(self.span.lang, datatypes.Lang)
        self.assertIsInstance(self.span.href, datatypes.URL)
        self.assertIsInstance(self.span.class_, str)
        self.assertEqual(self.span.pcdata, "this text")
        self.assertEqual(self.span.tail, "tail text")
        self.assertEqual(self.span.lang, "en")
        self.assertEqual(self.span.href, "https://example.com")
        self.assertEqual(self.span.class_, "bold")

    def test_create_text(self):
        self.assertRaises(errors.RequiredValueException, base.Text)
        self.text = base.Text(
            text="text"
        )
        self.assertIsInstance(self.text.pcdata, datatypes.PCData)
        self.assertEqual(self.text.pcdata, "text")

    def test_create_trait(self):
        self.assertRaises(errors.RequiredValueException, base.Trait)
        self.trait = base.Trait(
            name="name",
            value="value",
            trait_id="trait-id"
        )
        self.assertIsInstance(self.trait.name, datatypes.Key)
        self.assertIsInstance(self.trait.value, datatypes.Key)
        self.assertIsInstance(self.trait.id, datatypes.Key)
        self.assertEqual(self.trait.name, "name")
        self.assertEqual(self.trait.value, "value")
        self.assertEqual(self.trait.id, "trait-id")

    def test_create_urlref(self):
        self.assertRaises(errors.RequiredValueException, base.URLRef)
        self.url = base.URLRef(
            href="https://www.example.com"
        )
        self.assertIsInstance(self.url.href, datatypes.URL)
        self.assertEqual(self.url.href, "https://www.example.com")


class TestModifyLexiconItems(unittest.TestCase):
    def setUp(self):
        self.lexicon = LEXICON

    def test_entry_add_etymology(self):
        entry = self.lexicon.entry_items[0]
        idx = entry.add_etymology()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(entry.etymology_items[idx], lexicon.Etymology)

    def test_entry_add_note(self):
        entry = self.lexicon.entry_items[0]
        idx = entry.add_note()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(entry.note_items[idx], lexicon.Note)

    def test_entry_add_pronunciation(self):
        entry = self.lexicon.entry_items[0]
        idx = entry.add_pronunciation()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(entry.pronunciation_items[idx], lexicon.Phonetic)

    def test_entry_add_relation(self):
        entry = self.lexicon.entry_items[0]
        idx = entry.add_relation()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(entry.relation_items[idx], lexicon.Relation)

    def test_entry_add_sense(self):
        entry = self.lexicon.entry_items[0]
        idx = entry.add_sense()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(entry.sense_items[idx], lexicon.Sense)

    def test_entry_add_variant(self):
        entry = self.lexicon.entry_items[0]
        idx = entry.add_variant()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(entry.variant_items[idx], lexicon.Variant)

    def test_entry_set_lexical_unit(self):
        entry = self.lexicon.entry_items[0]
        entry.set_lexical_unit({'en': 'english text', 'sg': 'atëne ti sängö'})
        self.assertEqual(len(entry.lexical_unit.form_items), 2)

    def test_entry_set_pronunciation_item(self):
        entry_id = "rô_ff402c0b-4eb5-4df1-bd29-a1900aaf7567"
        entry = self.lexicon.get_item_by_id(entry_id)
        labels = {
            "en": "pronunciation recording",
            "fr": "enregistrement de prononciation",
        }
        entry.pronunciation_items[0].add_media(
            href="file:///home/user/pronunciation.wav",
            label=labels
        )
        media_item = entry.pronunciation_items[0].media_items[0]
        self.assertEqual(
            media_item.href,
            "file:///home/user/pronunciation.wav"
        )
        self.assertEqual(len(media_item.label.form_items), 2)
        for f in media_item.label.form_items:
            self.assertIn(f.lang, labels.keys())
            self.assertIn(str(f.text), labels.values())

    def test_etymology_add_gloss_item(self):
        entry_id = "yongo_eafee046-6df9-4162-8c38-a2536713b69f"
        entry = self.lexicon.get_item_by_id(entry_id)
        entry.etymology_items[0].add_gloss("en", "English gloss")
        idx = len(entry.etymology_items[0].gloss_items) - 1
        gloss_item = entry.etymology_items[0].gloss_items[idx]
        self.assertEqual(gloss_item.lang, 'en')
        self.assertEqual(str(gloss_item.text), 'English gloss')

    def test_lexicon_add_entry_item(self):
        len_before = len(self.lexicon.entry_items)
        self.lexicon.add_entry()
        len_after = len(self.lexicon.entry_items)
        idx = len_after - 1

        self.assertEqual(len_after - 1, len_before)
        self.assertIsNotNone(self.lexicon.entry_items[idx].id)
        self.assertIsNotNone(self.lexicon.entry_items[idx].date_created)