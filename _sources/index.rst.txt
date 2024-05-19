.. LIFT Utils documentation master file, created by
   sphinx-quickstart on Fri May 10 17:10:02 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LIFT Utils documentation
========================

**LIFT Utils** is a Python library for manipulating linguistic files in the
XML-based `LIFT <https://github.com/sillsdev/lift-standard>`_ format.

>>> from lift_utils import lift
>>> lex = lift.LIFTFile("sango.lift").to_lexicon()
>>> print(len(lex.entries))
3507
>>> print(lex.entries[0])
kêtê ngû sô asua pë…    pool                            Nom
>>> print(lex.entries[0].senses[0])
pool            Nom             None
>>> for k, v in lex.entries[0].__dict__.items():
...     print(f"{k}: {v}")
... 
xml_tree: <Element entry at 0x7f8fd404d580>
date_created: 2019-03-05T12:19:45Z
date_modified: 2022-05-04T11:17:08Z
fields: None
traits: [<lift_utils.base.Trait object at 0x7f8fd3098940>]
annotations: None
id: kêtê ngû sô asua pëpe_000d9e27-d103-4601-a4b1-6c3ee5ef4c01
guid: 000d9e27-d103-4601-a4b1-6c3ee5ef4c01
order: None
date_deleted: None
lexical_unit: kêtê ngû sô asua pëpe (sg)
citation: None
pronunciations: None
variants: None
senses: [<lift_utils.lexicon.Sense object at 0x7f8fd3098ac0>, <lift_utils.lexicon.Sense object at 0x7f8fd3098af0>]
notes: None
relations: [<lift_utils.lexicon.Relation object at 0x7f8fd3098400>, <lift_utils.lexicon.Relation object at 0x7f8fd3098a00>, <lift_utils.lexicon.Relation object at 0x7f8fd3098a90>]
etymologies: None

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
