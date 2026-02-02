"""Define runtime global variables."""

from lxml import etree

LIB_VERSION = "0.4"
LIFT_VERSION_FIELDWORKS = "0.13"  # used by FLEx 9.1
LIFT_VERSION_LATEST = "0.15"
LIFT_VERSION_DEFAULT = LIFT_VERSION_FIELDWORKS
LIFT_VERSION = None

XML_PARSER = etree.XMLParser(remove_blank_text=True)
