"""Read a LIFT file into memory."""

from lxml import etree
from pathlib import Path
from typing import Union

from .lexicon import LIFT
from .base import LIFTUtilsBase
from .utils import xml_to_etree


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
        return self.read() if self.path else ''

    def _read_to_etree(self) -> etree:
        """Read a LIFT file data into memory."""
        # Remove existing line breaks to allow pretty_print to work properly.
        return xml_to_etree(self.path)

    def to_lift(self) -> LIFT:
        """Return a LIFT object."""
        return LIFT(self.path, self.xml_tree)
