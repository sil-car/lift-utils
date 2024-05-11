"""Read a LIFT file into memory."""

import sys
from lxml import etree
from pathlib import Path
from typing import Union

from . import lexicon


class LIFTFile:
    """Return ``LIFTFile`` object that can be read into memory.

    :ivar Path path: The LIFT file object.
    :ivar int size: Size in bytes of the LIFT file.
    """

    _parser = etree.XMLParser(remove_blank_text=True)

    def __init__(self, path: Union[Path, str] = None):
        self.path = Path(path) if path else None
        self.size: int = self.path.stat().st_size if self.path else None

    def __str__(self):
        return self.read() if self.path else ''

    def _read_to_etree(self) -> etree:
        """Read a LIFT file data into memory."""
        # Remove existing line breaks to allow pretty_print to work properly.
        return etree.parse(str(self.path), LIFTFile._parser).getroot()

    def lift(self) -> lexicon.LIFT:
        """Return a LIFT object."""
        return lexicon.LIFT(self._read_to_etree())

    def show(self):
        """Print the LIFT file's content to stdout."""
        try:
            print(
                etree.tostring(
                    self._read_to_etree(),
                    encoding='UTF-8',
                    pretty_print=True,
                    xml_declaration=True
                ).decode().rstrip(),
                flush=True
            )
        except BrokenPipeError:
            sys.stdout = None
