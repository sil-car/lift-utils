"""Various utility functions."""
import regex
import unidecode
from datetime import datetime
from datetime import timezone
from lxml import etree

from . import config


def ellipsize(string, length):
    if len(string) > length:
        i = length - 1
        string = f"{string[:i]}…"
    return string


def etree_to_obj_attributes(xml_tree, obj):
    if obj.props.attributes:
        for p in obj.props.attributes:
            key = config.XML_NAMES.get(p.name, p.name)
            if key in xml_tree.attrib.keys():
                obj.__dict__[p.name] = p.prop_type(xml_tree.attrib.get(key))

    if obj.props.elements:
        for p in obj.props.elements:
            tag = config.XML_NAMES.get(p.name, p.name)
            if xml_tree.text and p.name == 'pcdata':
                obj.__dict__[p.name] = p.prop_type(xml_tree.text)
                continue
            elif xml_tree.tail and p.name == 'tail':
                obj.__dict__[p.name] = p.prop_type(xml_tree.tail)
                continue
            for c in xml_tree.getchildren():
                if c.tag == tag:
                    if hasattr(p.prop_type, 'append'):  # list-like obj/elem
                        if not obj.__dict__.get(p.name):
                            # Instantiate list-like object.
                            obj.__dict__[p.name] = p.prop_type()
                        obj.__dict__[p.name].append(p.item_type(xml_tree=c))
                    else:  # single element
                        obj.__dict__[p.name] = p.prop_type(xml_tree=c)


def obj_attributes_to_etree(obj, root_tag):
    xml_tree = etree.Element(root_tag)

    if obj.props.attributes:
        for attrib in obj.props.attributes:
            attr = attrib.name
            val = obj.__dict__.get(attr)
            if val is not None:
                xml_tree.set(config.XML_NAMES.get(attr, attr), str(val))

    if obj.props.elements:
        for elem in obj.props.elements:
            attr = elem.name
            val = obj.__dict__.get(attr)
            if not val:
                continue
            name = config.XML_NAMES.get(attr, attr)
            if hasattr(val, 'append'):  # list-like element
                for o in obj.__dict__.get(attr):
                    xml_tree.append(obj_attributes_to_etree(o, name))
            elif attr == 'pcdata':
                xml_tree.text = val
            elif attr == 'tail':
                xml_tree.tail = val
            else:  # single element
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
    match_type,
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
                match_type,
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
                    match_type,
                    get_all
                )
                if result is not None:
                    if not get_all:
                        return result
                    else:
                        items.extend(result)

    if 'entries' in target_groups:
        if field == 'lexical-unit':
            if not entry.lexical_unit or not entry.lexical_unit.form_items:
                if not get_all:
                    return
                else:
                    return items
            if form_items_has_match(
                entry.lexical_unit.form_items,
                text,
                match_type
            ):
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
                if form_items_has_match(variant.form_items, text, match_type):
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
                if field_item.type == field and field_item.form_items:
                    if form_items_has_match(
                        field_item.form_items,
                        text,
                        match_type
                    ):
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
    match_type,
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
        if form_items_has_match(sense.definition.form_items, text, match_type):
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
            if field_item.type == field and field_item.form_items:
                if form_items_has_match(
                    field_item.form_items,
                    text,
                    match_type
                ):
                    if not get_all:
                        return sense
                    else:
                        items.append(sense)
    if get_all:
        return items


def form_items_has_match(form_items, text, match_type):
    for form in form_items:
        if match_type == 'contains':
            if text in str(form.text):
                return True
        elif match_type == 'exact':
            if text == str(form.text):
                return True
        elif match_type == 'regex':
            if regex.match(text, form.text):
                return True


def get_current_timestamp():
    return datetime.strftime(datetime.now(timezone.utc), '%Y-%m-%dT%H:%M:%SZ')


def get_writing_systems_from_entry(entry) -> dict:
    ws = {'vernacular': [], 'analysis': []}
    ws['analysis'].extend(get_ws_from_field_items(entry.field_items))
    if entry.etymology_items:
        for y in entry.etymology_items:
            ws['analysis'].extend(get_ws_from_field_items(y.field_items))
    if entry.lexical_unit and entry.lexical_unit.form_items:
        for f in entry.lexical_unit.form_items:
            ws['vernacular'].append(f.lang)
    if entry.note_items:
        for n in entry.note_items:
            ws['analysis'].extend(get_ws_from_field_items(n.field_items))
    if entry.pronunciation_items:
        for p in entry.pronunciation_items:
            if p.form_items:
                for f in p.form_items:
                    ws['vernacular'].append(f.lang)
            ws['analysis'].extend(get_ws_from_field_items(p.field_items))
    if entry.variant_items:
        for v in entry.variant_items:
            ws['analysis'].extend(get_ws_from_field_items(v.field_items))
    if entry.sense_items:
        for s in entry.sense_items:
            ws['analysis'].extend(get_ws_from_sense(s))

    # Remove repeated elements.
    ws['vernacular'] = list(set(ws.get('vernacular')))
    ws['analysis'] = list(set(ws.get('analysis')))
    return ws


def get_ws_from_sense(sense) -> list:
    analysis_ws = []
    analysis_ws.extend(get_ws_from_field_items(sense.field_items))
    if sense.example_items:
        for e in sense.example_items:
            analysis_ws.extend(get_ws_from_field_items(e.field_items))
    if sense.note_items:
        for n in sense.note_items:
            analysis_ws.extend(get_ws_from_field_items(n.field_items))
    if sense.relation_items:
        for r in sense.relation_items:
            analysis_ws.extend(get_ws_from_field_items(r.field_items))
    return list(set(analysis_ws))


def get_ws_from_field_items(field_items):
    writing_systems = []
    if field_items is not None:
        for field in field_items:
            if field.form_items:
                for m in field.form_items:
                    writing_systems.append(m.lang)
    return writing_systems
