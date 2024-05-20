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
                obj.__dict__[p.name] = p.prop_type(obj.xml_tree.attrib.get(key))  # noqa: E501

    if obj.props.elements:
        for p in obj.props.elements:
            if p.name == 'pcdata' and obj.xml_tree.text:
                obj.__dict__[p.name] = obj.xml_tree.text
            for c in obj.xml_tree.getchildren():
                tag = config.XML_NAMES.get(p.name, p.name)
                if p.name in ['fields', 'ranges'] and p.item_type is None:
                    # These elements are plural but have explicit tags.
                    tag = p.name
                if tag == c.tag:
                    if hasattr(p.prop_type, 'append'):  # list-like object
                        if not obj.__dict__.get(p.name):
                            # Instantiate object.
                            obj.__dict__[p.name] = p.prop_type()
                        obj.__dict__[p.name].append(p.item_type(c))
                    else:  # single element
                        obj.__dict__[p.name] = p.prop_type(c)


def get_xml_parser():
    return etree.XMLParser(remove_blank_text=True)


def unicode_sort(in_list):
    def fmt(string):
        return unidecode.unidecode(string.lower())
    return sorted(in_list, key=fmt)


def xml_to_etree(filepath):
    return etree.parse(str(filepath), get_xml_parser()).getroot()
