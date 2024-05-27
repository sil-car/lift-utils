.. LIFT Utils documentation master file, created by
   sphinx-quickstart on Fri May 10 17:10:02 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LIFT Utils documentation
========================

**LIFT Utils** is a Python library for manipulating linguistic lexicon files in
the XML-based `LIFT format <https://github.com/sillsdev/lift-standard>`_.

>>> from lift_utils import lexicon
>>> lex = lexicon.Lexicon("sango.lift")
>>> print(len(lex.entry_items))
3507
>>> print(lex.entry_items[0])
kêtê ngû sô asua pë…    pool                            Nom
>>> print(lex.entry_items[0].sense_items[0])
pool            Nom             None
>>> for k, v in lex.entry_items[0].__dict__.items():
...     print(f"{k}: {v}")
... 
xml_tree: <Element entry at 0x7f4c7f33fa00>
xml_tag: entry
props: <lift_utils.datatypes.Props object at 0x7f4c7f335190>
date_created: 2019-03-05T12:19:45Z
date_modified: 2022-05-04T11:17:08Z
field_items: None
trait_items: [<lift_utils.base.Trait object at 0x7f4c7f348d90>]
annotation_items: None
id: kêtê ngû sô asua pëpe_000d9e27-d103-4601-a4b1-6c3ee5ef4c01
guid: 000d9e27-d103-4601-a4b1-6c3ee5ef4c01
order: None
date_deleted: None
lexical_unit: kêtê ngû sô asua pëpe (sg)
citation: None
pronunciation_items: None
variant_items: None
sense_items: [<lift_utils.lexicon.Sense object at 0x7f4c7f31f1f0>, <lift_utils.lexicon.Sense object at 0x7f4c7f31fbb0>]
note_items: None
relation_items: [<lift_utils.lexicon.Relation object at 0x7f4c7f3293a0>, <lift_utils.lexicon.Relation object at 0x7f4c7f331250>, <lift_utils.lexicon.Relation object at 0x7f4c7f331a90>]
etymology_items: None

.. toctree::
   :maxdepth: 4

Roadmap
=======

.. list-table::
   :widths: 8 32
   :header-rows: 1

   * - Release
     - Feature
   * - v0.1
     - read support for LIFT files
   * - v0.2
     - write support for LIFT files
   * - v0.3
     - add helper methods (get, set, add, list, etc.)

Indexes
=======

* :ref:`modindex`
* :ref:`genindex`
