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
        if hasattr(obj, 'pcdata'):
            obj.pcdata = xml_tree.text
        else:
            obj.text = xml_tree.text
    if xml_tree.tail:
        obj.tail = xml_tree.tail

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


def obj_attributes_to_etree(obj, root_tag):
    if not isinstance(root_tag, etree._Element):
        xml_tree = etree.Element(root_tag)
    else:
        xml_tree = root_tag

    if obj.props.attributes:
        for attrib in obj.props.attributes:
            a = attrib.name
            x = config.XML_NAMES.get(a, a)
            xml_tree.set(x, obj.__dict__.get(a))

    if obj.props.elements:
        for elem in obj.props.elements:
            e = elem.name
            x = config.XML_NAMES.get(e, e)
            if hasattr(obj.__dict__.get(e), 'append'):
                for i in obj.__dict__.get(e):
                    # TODO: Rather than create an empty subelement, this should
                    # recursively call itself, which means it should also take
                    # a parent node as input rather than a tag name.
                    etree.SubElement(xml_tree, x)
            # elif hasattr(obj.__dict__.get(e), 'xml_tree'):
            #     e._build_xml_tree()
            elif e == 'pcdata':
                xml_tree.text = obj.__dict__.get(e)
            elif e == 'tail':
                xml_tree.tail = obj.__dict__.get(e)
            elif obj.__dict__.get(e):
                etree.SubElement(xml_tree, x)
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


def get_dict_key_from_value(dictionary, value, idx=0):
    keys = []
    for k, v in dictionary.items():
        if v == value:
            keys.append(k)
    if keys:
        return keys[idx]
    else:
        return None
