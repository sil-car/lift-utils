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

    if obj.props.attributes:
        for p in obj.props.attributes:
            key = config.XML_NAMES.get(p.name, p.name)
            if key in obj.xml_tree.attrib.keys():
                obj.__dict__[p.name] = p.prop_type(obj.xml_tree.attrib.get(key))  # noqa: E501

    if obj.props.elements:
        for p in obj.props.elements:
            tag = config.XML_NAMES.get(p.name, p.name)
            if obj.xml_tree.text and p.name == 'pcdata':
                obj.__dict__[p.name] = p.prop_type(obj.xml_tree.text)
                continue
            elif obj.xml_tree.tail and p.name == 'tail':
                obj.__dict__[p.name] = p.prop_type(obj.xml_tree.tail)
                continue
            for c in obj.xml_tree.getchildren():
                if c.tag == tag:
                    if hasattr(p.prop_type, 'append'):  # list-like obj/elem
                        c_obj = p.item_type(xml_tree=c)
                        if obj.__dict__.get(p.name) is None:
                            # Instantiate list-like object.
                            obj.__dict__[p.name] = p.prop_type()
                        obj.__dict__[p.name].append(c_obj)
                    else:  # single element
                        obj.__dict__[p.name] = p.prop_type(xml_tree=c)


def obj_attributes_to_etree(obj, root_tag):
    xml_tree = etree.Element(root_tag)

    if obj.props.attributes:
        for attrib in obj.props.attributes:
            attr = attrib.name
            val = obj.__dict__.get(attr)
            name = config.XML_NAMES.get(attr, attr)
            if val is not None:
                xml_tree.set(name, str(val))

    if obj.props.elements:
        for elem in obj.props.elements:
            attr = elem.name
            name = config.XML_NAMES.get(attr, attr)
            val = obj.__dict__.get(attr)
            if hasattr(val, 'append'):  # list-like element
                for o in obj.__dict__.get(attr):
                    xml_tree.append(obj_attributes_to_etree(o, name))
            elif val and attr == 'pcdata':
                xml_tree.text = val
            elif val and attr == 'tail':
                xml_tree.tail = val
            elif val:  # single element
                xml_tree.append(
                    obj_attributes_to_etree(obj.__dict__.get(attr), name)
                )
    return xml_tree


def get_xml_parser():
    return etree.XMLParser(remove_blank_text=True)


def unicode_sort(in_list):
    def fmt(string):
        return unidecode.unidecode(string.lower())
    return sorted(in_list, key=fmt)


def xmlfile_to_etree(filepath):
    return etree.parse(str(filepath), get_xml_parser()).getroot()


def xmlstring_to_etree(xmlstring):
    return etree.fromstring(xmlstring, get_xml_parser())


def etree_to_xmlstring(xml_tree):
    return etree.tostring(
        xml_tree,
        encoding='UTF-8',
        pretty_print=True,
        xml_declaration=True
    ).decode().rstrip()
