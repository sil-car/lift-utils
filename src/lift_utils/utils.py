"""Various utility functions."""

import unidecode
from lxml import etree

from . import config


def ellipsize(string, length):
    if len(string) > length:
        i = length - 1
        string = f"{string[:i]}…"
    return string


def etree_to_obj_attributes(xml_tree, obj):
    obj.xml_tree = xml_tree

    if xml_tree.text:
        obj.text = xml_tree.text

    if obj.props.attributes:
        for p in obj.props.attributes:
            key = config.XML_NAMES.get(p.name)
            if not key:
                key = p.name
            if key in obj.xml_tree.attrib.keys():
                obj.__dict__[p.name] = p.type(obj.xml_tree.attrib.get(key))

    if obj.props.elements:
        for p in obj.props.elements:
            if p.name == 'pcdata' and obj.xml_tree.text:
                obj.__dict__[p.name] = obj.xml_tree.text
            for c in obj.xml_tree.getchildren():
                tag = config.XML_NAMES.get(p.name)
                if not tag:
                    tag = p.name
                if c.tag == 'fields' and tag == 'field':
                    # Tag for Extensible should remain 'fields', but otherwise
                    # it should be 'field' (e.g. for Header)
                    tag = 'fields'
                if tag == c.tag:
                    if hasattr(p.type, 'append') and tag != 'fields':
                        # List-like object; special exception for
                        # header.Header.fields attribute.
                        if not obj.__dict__.get(p.name):
                            obj.__dict__[p.name] = [p.list_type(c)]
                        else:
                            obj.__dict__[p.name].append(p.list_type(c))
                    else:  # single element
                        obj.__dict__[p.name] = p.type(c)


def get_xml_parser():
    return etree.XMLParser(remove_blank_text=True)


def unicode_sort(in_list):
    def fmt(string):
        return unidecode.unidecode(string.lower())
    return sorted(in_list, key=fmt)


def xml_to_etree(filepath):
    return etree.parse(str(filepath), get_xml_parser()).getroot()
