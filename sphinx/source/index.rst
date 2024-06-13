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
>>> sg_lex = Lexicon("~/lift/sango LIFT export/sango LIFT export.lift")
>>> print(len(sg_lex.entry_items))
3479

Get details about entries and their senses:

>>> print(sg_lex.entry_items[0])
kêtê ngû sô asua pë…	kêtê ngû sô asua pëpe_000d9e27-d103-4601-a4b1-6c3ee5ef4c01
>>> print(sg_lex.entry_items[0].sense_items[0])
pool                	Noun      	27bb9896-e413-4c14-8cdc-cbe26ecbc148
>>> sg_lex.show()  # list all lexicon entries, sorted by lexical-unit
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
>>> item = sg_lex.get_item_by_id('zo wa_be18403e-c45d-4fb9-9d5a-35d26bf0b883')
>>> type(item)
<class 'lift_utils.lexicon.Entry'>
>>> item.show()
_xml_tag: entry
date_created: 2017-02-25T11:03:30Z
date_modified: 2022-05-07T14:15:56Z
field_items: None
trait_items: [<lift_utils.base.Trait object at 0x7fd777f4cbb0>]
annotation_items: None
id: zo wa_be18403e-c45d-4fb9-9d5a-35d26bf0b883
guid: be18403e-c45d-4fb9-9d5a-35d26bf0b883
order: None
date_deleted: None
lexical_unit: zo wa (sg)
citation: None
pronunciation_items: None
variant_items: None
sense_items: [<lift_utils.lexicon.Sense object at 0x7fd777f48fd0>]
note_items: None
relation_items: [<lift_utils.lexicon.Relation object at 0x7fd777f4c130>]
etymology_items: None

Search the lexicon:

>>> sg_lex.find('house')  # 'find' returns first item whose glosses contain the search term
<lift_utils.lexicon.Sense object at 0x7f3689d9e5b0>
>>> len(sg_lex.find_all('house'))  # 'find_all' returns a list of all matching items
13
>>> len(sg_lex.find_all('Noun', field='grammatical-info'))  # search other fields as well
2357

Compare data across multiple lexicons:

>>> import multiprocessing as mp
>>> from tabulate import tabulate  # pip install tabulate
>>> cawls = [f"{n:04d}" for n in range(1, 1701)]  # CAWL numbers, 0001 to 1700
>>> def lus_from_lift(lift, cawls):  # prepare multiprocess function
...     lex = Lexicon(lift)
...     lexical_units = []
...     for cawl in cawls:
...         lexical_unit = None
...         item = lex.find(cawl, field='CAWL', match_type='exact')
...         if item and item.id:
...             parent = lex.get_item_parent_by_id(item.id)
...             if parent:
...                 lexical_unit = parent.lexical_unit
...         lexical_units.append(lexical_unit)
...     return lexical_units
...
>>> lifts = [
...     '~/lift/Bhogoto FLEx LIFT export/Bhogoto FLEx LIFT export.lift',
...     '~/lift/Gbagiri FLEx LIFT export/FLEx LIFT export.lift',
...     '~/lift/Gbanu FLEx LIFT export/FLEx LIFT export.lift',
... ]
>>> with mp.Pool(3) as p:  # use multiprocessing to handle 3 files at once
...     lus_by_lex = p.starmap(lus_from_lift, ((lift, cawls) for lift in lifts))
...
>>> table = zip(cawls, *lus_by_lex)  # convert "columns" to "rows" for table
>>> print(tabulate(table))  # shows 4 columns: CAWL#, Bhogoto, Gbagiri, Gbanu
----  -----------------------------------------  ---------------  ---------------------------
0001  tɛɛ (bdt-CF)                                                tɛ (gbv)
0002  ndara (bdt-CF) (3 forms)                   ndara (gbv)      ndara te wire (gbv)
0003  zu (bdt-CF) (3 forms)                      zu (gbv)         zu (gbv)
0004  baŋge (bdt-CF)                                              ngɔri (gbv)
0005  dɔɔti ri (bdt-CF)                          ri (gbv)         ri (gbv)
# ...
1696  demɔ (bdt-CF) (3 forms)
1697  mɔ nɛ de nɛ (bdt-CF)                                        dɛ ɗãa tom (gbv)
1698  eyɛ (bdt-CF)
1699  ɛ̧ɛ (bdt-CF)
1700  hoo hoo (bdt-CF)
----  -----------------------------------------  ---------------  ---------------------------


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
