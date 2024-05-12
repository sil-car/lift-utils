"""Various utility functions."""

import unidecode
from lxml import etree


def ellipsize(string, length):
    if len(string) > length:
        i = length - 1
        string = f"{string[:i]}…"
    return string


def get_xml_parser():
    return etree.XMLParser(remove_blank_text=True)


def unicode_sort(in_list):
    def fmt(string):
        return unidecode.unidecode(string.lower())
    return sorted(in_list, key=fmt)


def xml_to_etree(filepath):
    return etree.parse(str(filepath), get_xml_parser()).getroot()
