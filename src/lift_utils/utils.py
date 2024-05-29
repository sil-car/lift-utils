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


def search_entry(
    entry,
    text,
    field,
    target_groups,
    header_fields,
    get_all
):
    items = []
    if 'senses' in target_groups:
        if not entry.sense_items:
            if not get_all:
                return
            else:
                return items
        for sense in entry.sense_items:
            result = search_sense(
                sense,
                text,
                field,
                target_groups,
                header_fields,
                get_all
            )
            if result is not None:
                if not get_all:
                    return result
                else:
                    items.extend(result)

            if not sense.subsense_items:
                continue
            for subsense in sense.subsense_items:
                result = search_sense(
                    subsense,
                    text,
                    field,
                    target_groups,
                    header_fields,
                    get_all
                )
                if result is not None:
                    if not get_all:
                        return result
                    else:
                        items.extend(result)

    if 'entries' in target_groups:
        if field == 'lexical-unit':
            if not entry.lexical_unit or not entry.lexical_unit.form_items:  # noqa: E501
                if not get_all:
                    return
                else:
                    return items
            for form in entry.lexical_unit.form_items:
                if text in str(form.text):
                    if not get_all:
                        return entry
                    else:
                        items.append(entry)
        elif field == 'variant':
            if not entry.variant_items:
                if not get_all:
                    return
                else:
                    return items
            for variant in entry.variant_items:
                if not variant.form_items:
                    continue
                for form in variant.form_items:
                    if text in str(form.text):
                        if not get_all:
                            return entry
                        else:
                            items.append(entry)
        elif field in header_fields:
            if not entry.field_items:
                if not get_all:
                    return
                else:
                    return items
            for field_item in entry.field_items:
                if field_item.type == field and field_item.form_items:  # noqa: E501
                    for form in field_item.form_items:
                        if text in str(form.text):
                            if not get_all:
                                return entry
                            else:
                                items.append(entry)
    if get_all:
        return items


def search_sense(
    sense,
    text,
    field,
    target_groups,
    header_fields,
    get_all
):
    items = []
    if field == 'gloss':
        if not sense.gloss_items:
            if not get_all:
                return
            else:
                return items
        for gloss in sense.gloss_items:
            if text in str(gloss.text):
                if not get_all:
                    return sense
                else:
                    items.append(sense)
    elif field == 'definition':
        if not sense.definition or not sense.definition.form_items:  # noqa: E501
            if not get_all:
                return
            else:
                return items
        for form in sense.definition.form_items:
            if text in str(form.text):
                if not get_all:
                    return sense
                else:
                    items.append(sense)
    elif field == 'grammatical-info':
        if not sense.grammatical_info:
            if not get_all:
                return
            else:
                return items
        if text in str(sense.grammatical_info):
            if not get_all:
                return sense
            else:
                items.append(sense)
    elif field in header_fields:
        if not sense.field_items:
            if not get_all:
                return
            else:
                return items
        for field_item in sense.field_items:
            if field_item.type == field and field_item.form_items:  # noqa: E501
                for form in field_item.form_items:
                    if text in str(form.text):
                        if not get_all:
                            return sense
                        else:
                            items.append(sense)
    if get_all:
        return items
