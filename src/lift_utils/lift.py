"""Read a LIFT file into memory."""

from lxml import etree
from pathlib import Path
from typing import Union

from .lexicon import Lexicon
from .base import LIFTUtilsBase
from .utils import xmlfile_to_etree


class LIFTFile(LIFTUtilsBase):
    """Return ``LIFTFile`` object that can be read into memory.

    :ivar Path path: The LIFT file object.
    :ivar int size: Size in bytes of the LIFT file.
    """

    def __init__(self, path: Union[Path, str] = None):
        self.path = Path(path) if path else None
        self.size: int = self.path.stat().st_size if self.path else None
        if self.path and self.path.is_file():
            self.xml_tree = self._read_to_etree()

    def __str__(self):
        return self.path.read_text() if self.path else ''

    def _read_to_etree(self) -> etree:
        # Remove existing line breaks to allow pretty_print to work properly.
        return xmlfile_to_etree(self.path)

    def to_lexicon(self) -> Lexicon:
        """Parse LIFT data to a Lexicon object."""
        return Lexicon(self.path, self.xml_tree)
