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
