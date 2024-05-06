# Datatypes

class PCData(str):
    pass


class DateTime(str):
    # format (str): YYYY-MM-DDTHH:MM:SSZZZZZZ
    # ZZZZZZ: +/-, H, H, :, M, M (offset from GMT)
    pass


class Key(str):
    pass


class Lang(str):
    # format (str): ISO[-SCRIPT[-x-PRIVATE]]
    pass


class RefId(str):
    # format (HEX GUID): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    pass


class URL(str):
    pass
