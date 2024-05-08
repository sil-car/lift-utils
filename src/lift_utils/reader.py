from lxml import etree
from pathlib import Path

from .lexicon import LIFTLexicon


class LIFTFile:
    def __init__(self, path=None):
        self.path = Path(path) if path else None
        self.header_file = None
        self.xml_tree = self.get_xml_tree() if self.path else None
        self.LIFT = None

    def __str__(self):
        return self.path.stem if self.path else 'no file'

    def get_xml_tree(self):
        # Don't auto-parse XML in order to conserve memory?
        # Remove existing line breaks to allow pretty_print to work properly.
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.parse(str(self.path), parser)

    def show_xml_tree(self):
        print(
            etree.tostring(
                self.get_xml_tree(),
                encoding='UTF-8',
                pretty_print=True,
                xml_declaration=True
            ).decode().rstrip()
        )

    def xml_to_lexicon(self):
        lexicon = LIFTLexicon()
        lexicon.update_from_xml(self.get_xml_tree().getroot())
        return lexicon

    def lexicon_to_xml(self):
        pass
