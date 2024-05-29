from lxml import etree


def test_attribs(test_cls, obj, attribs):
    for a in attribs:
        try:
            test_cls.assertIsNotNone(obj.__dict__.get(a))
        except AssertionError as e:
            raise Exception(f"\"{a}\" {str(e)}")


def test_elems(test_cls, obj, elems):
    for elem in elems:
        try:
            test_cls.assertIsNotNone(obj.__dict__.get(elem))
        except AssertionError as e:
            raise Exception(f"\"{elem}\" {str(e)}")


def compare_xml_trees(tree1, tree2):
    print()
    print(etree.tostring(tree1, pretty_print=True).decode())
    print(etree.tostring(tree2, pretty_print=True).decode())
