"""Define runtime global variables."""

LIFT_VERSION_FIELDWORKS = '0.13'  # used by FLEx 9.1
LIFT_VERSION_LATEST = '0.15'
LIFT_VERSION_DEFAULT = LIFT_VERSION_FIELDWORKS
LIFT_VERSION = None

XML_NAMES = {
    # object attribute keys (L) and corresponding LIFT XML tags (R)
    'abbrevs': 'abbrev',
    'annotations': 'annotation',
    'class_': 'class',
    'date_created': 'dateCreated',
    'date_deleted': 'dateDeleted',
    'date_modified': 'dateModified',
    'descriptions': 'description',
    'entries': 'entry',
    'etymologies': 'etymology',
    'examples': 'example',
    'field_definitions': 'field',
    'fields': 'field',
    'forms': 'form',
    'glosses': 'gloss',
    'grammatical_info': 'grammatical-info',
    'illustrations': 'illustration',
    'labels': 'label',
    'lexical_unit': 'lexical-unit',
    'medias': 'media',
    'notes': 'note',
    'option_range': 'option-range',
    'pcdata': 'text',
    'pronunciations': 'pronunciation',
    'range_elements': 'range-element',
    'relations': 'relation',
    'reversals': 'reversal',
    'senses': 'sense',
    'spans': 'span',
    'subsenses': 'subsense',
    'traits': 'trait',
    'translations': 'translation',
    'usages': 'usage',
    'variants': 'variant',
    'writing_system': 'writing-system',
}
