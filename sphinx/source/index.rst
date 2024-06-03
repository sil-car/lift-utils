.. LIFT Utils documentation master file, created by
   sphinx-quickstart on Fri May 10 17:10:02 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LIFT Utils documentation
========================

**LIFT Utils** is a Python library for manipulating linguistic lexicon data in
the XML-based `LIFT format <https://github.com/sillsdev/lift-standard>`_.

Get basic lexicon details:

>>> from lift_utils import Lexicon
>>> lex = Lexicon("sango.lift")
>>> print(len(lex.entry_items))
3507

Get details about entries and their senses:

>>> print(lex.entry_items[0])
kêtê ngû sô asua pë…    pool                            Nom
>>> print(lex.entry_items[0].sense_items[0])
pool            Nom             None
>>> lex.show()  # list all lexicon entries, sorted by lexical-unit
# ...
zo wa (sg)              who?                            zo wa_be18403e-c45d-4fb9-9d5a-35d26bf0b883
zôâ (sg)                island                          zôâ_d10bd14f-eed6-42c9-bbfb-e0f22c5acd8f
zonga (sg)              insult                          zonga_0c9f35f3-3a3f-4660-aa2b-55a701cf2c68
zonyön (sg)             onion                           zonyön_8fbfa01d-c5e8-4a4f-b848-013f601de4d4
zöröndö (sg)            help, rescue                    zöröndö_5d26b3de-26cb-42d2-86ee-33e018ec88c7
zovokö (sg)             African                         zovokö_3e959588-8541-411d-aba5-4a00d39d66ba
zovukö (sg)             African                         zovukö_cc8ad26d-3d79-4249-9c80-1af9fd2185c6
zozo (sg)               palm rat                        zozo_72b4fcfe-3112-4f92-aee7-248d708b6bd4
zû (sg)                 descend                         zû_ed13b0f7-24b4-4233-a6ae-a1e6f0060416
zû na sêse (sg)         land, alight                    zû na sêse_8e32a3f1-1db7-4fdc-a0f1-5c5ccb7c7ca8
zûâ (sg)                island                          zûâ_115eccf6-19af-439f-b134-07ae1b11b51f
zûku (sg)               spill, turn (a container) upside down   zûku_51a7b1be-cb53-40c7-8b0e-fde1ab9cc3f0
zûku li (sg)            hang one's head, bow            zûku li_1a258482-1d61-44f4-b7a9-24f4bad575cc
zûsuka (sg)             until                           zûsuka_8c5e481c-8811-482e-bff0-126282c829ab
zûu (sg)                go down                         zûu_137d7f37-ceff-464a-9d7f-00febbcfd439
>>> item = lex.get_item_by_id('zo wa_be18403e-c45d-4fb9-9d5a-35d26bf0b883')
>>> type(item)
<class 'lift_utils.lexicon.Entry'>
>>> item.__dict__
{'xml_tree': <Element entry at 0x7f382bcb6940>, 'xml_tag': 'entry', 'props': <lift_utils.datatypes.Props object at 0x7f3822b7dc40>, 'date_created': '2017-02-25T11:03:30Z', 'date_modified': '2022-05-07T14:15:56Z', 'field_items': None, 'trait_items': [<lift_utils.base.Trait object at 0x7f3822b8bd00>], 'annotation_items': None, 'id': 'zo wa_be18403e-c45d-4fb9-9d5a-35d26bf0b883', 'guid': 'be18403e-c45d-4fb9-9d5a-35d26bf0b883', 'order': None, 'date_deleted': None, 'lexical_unit': <lift_utils.base.Multitext object at 0x7f3822b8bf10>, 'citation': None, 'pronunciation_items': None, 'variant_items': None, 'sense_items': [<lift_utils.lexicon.Sense object at 0x7f3822b8e160>], 'note_items': None, 'relation_items': [<lift_utils.lexicon.Relation object at 0x7f3822b8eb20>], 'etymology_items': None}

Search the lexicon:

>>> lex.find('house')  # returns first item whose glosses contain the search term
<lift_utils.lexicon.Sense object at 0x7f3da9c919d0>
>>> len(lex.find_all('house'))  # find_all returns a list of all matching items
13
>>> len(lex.find_all('Nom', field='grammatical-info'))  # search other fields as well
2381

Add an annotation to an item:

>>> print(item.annotation_items)
None
>>> from lift_utils import base
>>> from lift_utils.datatypes import Lang
>>> item.annotation_items = [base.Annotation()]
>>> item.annotation_items[0].form_items = [base.Form(lang=Lang('en'), text=base.Text('This is a sample annotation'))]
>>> lex.to_lift("outfile.lift")  # save to file; verify that annotation has been added


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
     - add helper methods to facilitate lexicon manipulation

Indexes
=======

* :ref:`modindex`
* :ref:`genindex`
