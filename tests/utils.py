from lxml import etree


def test_attribs(test_cls, obj, attribs):
    for attrib in attribs:
        try:
            test_cls.assertIsNotNone(obj.__dict__.get(attrib))
        except AssertionError as e:
            raise Exception(f'"{attrib}" {str(e)}')


def test_elems(test_cls, obj, elems):
    for elem in elems:
        try:
            test_cls.assertIsNotNone(obj.__dict__.get(elem))
        except AssertionError as e:
            raise Exception(f'"{elem}" {str(e)}')


def test_properties(test_cls, props, optional=None):
    for prop in props:
        # Convert from XML name to Python name.
        prop = test_cls.obj.prop_name_from_xml_name(prop)
        try:
            if not optional:
                test_cls.assertIsNotNone(getattr(test_cls.obj, prop))
            else:
                test_cls.assertTrue(hasattr(test_cls.obj, prop))
        except AssertionError as e:
            raise Exception(f'"{prop}" {str(e)}')


def test_class_properties(test_cls):
    for group in (
        test_cls.obj._attributes_required,
        test_cls.obj._elements_required,
    ):
        test_properties(test_cls, group, optional=False)
    for group in (
        test_cls.obj._attributes_optional,
        test_cls.obj._elements_optional,
    ):
        test_properties(test_cls, group, optional=True)


def compare_xml_trees(tree1, tree2):
    print()
    print(etree.tostring(tree1, pretty_print=True).decode())
    print(etree.tostring(tree2, pretty_print=True).decode())


def get_props(props, prop_type="attributes", optional=False):
    if optional:
        return [k for k, v in props.get(prop_type).items() if not v[-1]]
    else:
        return [k for k, v in props.get(prop_type).items() if v[-1]]
