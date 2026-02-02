"""Various utility functions."""

import re
from datetime import datetime, timezone

import unidecode
from lxml import etree

from . import config


def ellipsize(string, length):
    if len(string) > length:
        i = length - 1
        string = f"{string[:i]}…"
    return string


def etree_to_obj_attributes(xml_tree, obj, props):
    # Convert XML attributes to python properties.
    attribs = [a for a in obj._attributes_required]
    attribs.extend([a for a in obj._attributes_optional])
    for xml_name in attribs:
        py_name = obj.prop_name_from_xml_name(xml_name)
        if xml_name in xml_tree.attrib.keys():
            setattr(
                obj,
                py_name,
                obj.tag_classes.get(xml_name)(xml_tree.attrib.get(xml_name)),
            )

    # Convert properties to XML elements.
    elems = [e for e in obj._elements_required]
    elems.extend([e for e in obj._elements_optional])
    for xml_name in elems:
        py_name = obj.prop_name_from_xml_name(xml_name)
        py_cls = obj.tag_classes.get(xml_name)
        if xml_name == "pcdata":
            if xml_tree.text:
                setattr(obj, py_name, py_cls(xml_tree.text))
            continue
        elif xml_name == "tail":
            if xml_tree.tail:
                setattr(obj, py_name, py_cls(xml_tree.tail))
            continue

        if xml_name in config.MULTIPLE_ITEM_TAGS:
            multiple = True
        else:
            multiple = False

        for c in xml_tree.getchildren():
            if c.tag == xml_name:
                if py_name.endswith("_items"):  # list-like obj/elem
                    if not getattr(obj, py_name):
                        # Instantiate list-like object.
                        setattr(obj, py_name, list())
                    getattr(obj, py_name).append(py_cls(xml_tree=c, parent=obj))
                else:  # single element
                    setattr(obj, py_name, py_cls(xml_tree=c, parent=obj))
                if not multiple:
                    break


def unicode_sort(in_list):
    def fmt(string):
        return unidecode.unidecode(string.lower())

    return sorted(in_list, key=fmt)


def sort_xml(xml_tree):
    sort_xml_attributes(xml_tree)
    sort_xml_elements(xml_tree)


def sort_xml_attributes(xml_tree):
    for el in xml_tree.iter():
        attrib = el.attrib
        if len(attrib) > 1:
            attributes = sorted(attrib.items())
            attrib.clear()
            attrib.update(attributes)


def get_sort_value(xml_elem):
    tag = xml_elem.tag
    if isinstance(tag, str):
        return tag
    else:
        # Some tags are Comment objects and can't be sorted as strings.
        return "0"


def sort_xml_elements(xml_tree):
    for el in xml_tree.iter():
        if len(el.getchildren()) > 1:
            sorted_children = sorted(el, key=get_sort_value)
            el[:] = sorted_children


def xmlfile_to_etree(filepath):
    xml_tree = etree.parse(str(filepath), config.XML_PARSER).getroot()
    # Sort attributes & elements alphabetically for deterministic behavior.
    sort_xml(xml_tree)
    return xml_tree


def xmlstring_to_etree(xmlstring):
    xml_tree = etree.fromstring(xmlstring, config.XML_PARSER)
    # Sort attributes & elements alphabetically for deterministic behavior.
    sort_xml(xml_tree)
    return xml_tree


def etree_to_xmlstring(xml_tree):
    # Sort attributes alphabetically for deterministic behavior.
    sort_xml(xml_tree)
    return (
        etree.tostring(
            xml_tree, encoding="UTF-8", pretty_print=True, xml_declaration=True
        )
        .decode()
        .rstrip()
    )


def search_entry(entry, text, field, target_groups, header_fields, match_type, get_all):
    items = []
    if "senses" in target_groups:
        if not entry.sense_items:
            if not get_all:
                return
            else:
                return items
        for sense in entry.sense_items:
            result = search_sense(
                sense, text, field, target_groups, header_fields, match_type, get_all
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
                    get_all,
                )
                if result is not None:
                    if not get_all:
                        return result
                    else:
                        items.extend(result)

    if "entries" in target_groups:
        if field == "lexical-unit":
            if not entry.lexical_unit or not entry.lexical_unit.form_items:
                if not get_all:
                    return
                else:
                    return items
            if form_items_has_match(entry.lexical_unit.form_items, text, match_type):
                if not get_all:
                    return entry
                else:
                    items.append(entry)
        elif field == "variant":
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
                    if form_items_has_match(field_item.form_items, text, match_type):
                        if not get_all:
                            return entry
                        else:
                            items.append(entry)
    if get_all:
        return items


def search_sense(sense, text, field, target_groups, header_fields, match_type, get_all):
    items = []
    if field == "gloss":
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
    elif field == "definition":
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
    elif field == "grammatical-info":
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
                if form_items_has_match(field_item.form_items, text, match_type):
                    if not get_all:
                        return sense
                    else:
                        items.append(sense)
    if get_all:
        return items


def form_items_has_match(form_items, text, match_type):
    for form in form_items:
        if form.__class__.__name__ == "Span":
            value = ""
            if form.pcdata:
                value += str(form.pcdata)
            if form.tail:
                value += str(form.tail)
        else:
            value = str(form.text)
        if match_type == "contains":
            if text in value:
                return True
        elif match_type == "exact":
            if text == value:
                return True
        elif match_type == "regex":
            if re.match(text, value):
                return True


def get_current_timestamp():
    return datetime.strftime(datetime.now(timezone.utc), "%Y-%m-%dT%H:%M:%SZ")


def get_writing_systems_from_entry(entry) -> dict:
    ws = {"vernacular": [], "analysis": []}
    ws["analysis"].extend(get_ws_from_field_items(entry.field_items))
    if entry.etymology_items:
        for y in entry.etymology_items:
            ws["analysis"].extend(get_ws_from_field_items(y.field_items))
    if entry.lexical_unit and entry.lexical_unit.form_items:
        for f in entry.lexical_unit.form_items:
            ws["vernacular"].append(f.lang)
    if entry.note_items:
        for n in entry.note_items:
            ws["analysis"].extend(get_ws_from_field_items(n.field_items))
    if entry.pronunciation_items:
        for p in entry.pronunciation_items:
            if p.form_items:
                for f in p.form_items:
                    ws["vernacular"].append(f.lang)
            ws["analysis"].extend(get_ws_from_field_items(p.field_items))
    if entry.variant_items:
        for v in entry.variant_items:
            ws["analysis"].extend(get_ws_from_field_items(v.field_items))
    if entry.sense_items:
        for s in entry.sense_items:
            ws["analysis"].extend(get_ws_from_sense(s))

    # Remove repeated elements.
    ws["vernacular"] = list(set(ws.get("vernacular")))
    ws["analysis"] = list(set(ws.get("analysis")))
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
