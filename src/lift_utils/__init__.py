"""Manipulate LIFT files and data"""

from .config import LIB_VERSION
from .lexicon import Entry, Lexicon, Sense

__all__ = [
    Entry,
    Lexicon,
    Sense,
]

__version__ = LIB_VERSION
