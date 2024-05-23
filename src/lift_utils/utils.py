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
            if p.name == 'pcdata' and obj.xml_tree.text:
                obj.__dict__[p.name] = p.prop_type(obj.xml_tree.text)
                continue
            elif p.name == 'tail' and obj.xml_tree.tail:
                obj.__dict__[p.name] = p.prop_type(obj.xml_tree.tail)
                continue

            for c in obj.xml_tree.getchildren():
                tag = config.XML_NAMES.get(p.name, p.name)
                if p.name in ['fields', 'ranges'] and p.item_type is None:
                    # These elements are plural but have explicit tags.
                    tag = p.name
                if tag == c.tag:
                    if hasattr(p.prop_type, 'append'):  # list-like object
                        if obj.__dict__.get(p.name) is None:
                            # Instantiate list-like object.
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
            attr = attrib.name
            val = obj.__dict__.get(attr)
            name = config.XML_NAMES.get(attr, attr)
            if val:
                xml_tree.set(name, val)

    if obj.props.elements:
        for elem in obj.props.elements:
            attr = elem.name
            name = config.XML_NAMES.get(attr, attr)
            val = obj.__dict__.get(attr)
            if hasattr(val, 'append'):  # list-like element
                for o in obj.__dict__.get(attr):
                    # TODO: Rather than create an empty subelement, this should
                    # recursively call itself, which means it should also take
                    # a parent node as input rather than a tag name.
                    # etree.SubElement(xml_tree, x)
                    xml_tree.append(obj_attributes_to_etree(o, name))
            elif val and attr == 'pcdata':
                xml_tree.text = val
            elif val and attr == 'tail':
                xml_tree.tail = val
            elif val:  # single element
                # etree.SubElement(xml_tree, x)
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


def get_dict_key_from_value(dictionary, value, idx=0):
    keys = []
    for k, v in dictionary.items():
        if v == value:
            keys.append(k)
    if keys:
        return keys[idx]
    else:
        return None
