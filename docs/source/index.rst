.. LIFT Utils documentation master file, created by
   sphinx-quickstart on Fri May 10 17:10:02 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LIFT Utils documentation
========================

**LIFT Utils** is a Python library for manipulating linguistic files in the
XML-based `LIFT <https://github.com/sillsdev/lift-standard>`_ format.

>>> from lift_utils import lift
>>> lex = lift.LIFTFile("sango.lift").lift()
>>> print(len(lex.entries))
3507
>>> print(lex.entries[0])
kêtê ngû sô asua pë…    pool                            Nom
>>> print(lex.entries[0].senses[0])
pool            Nom             None

.. toctree::
   :maxdepth: 3

Indexes
=======

* :ref:`modindex`
* :ref:`genindex`
