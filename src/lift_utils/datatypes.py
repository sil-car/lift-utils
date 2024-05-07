# Datatypes

class PCData(str):
    def __init__(self):
        super().__init__()


class DateTime(str):
    # format (str): YYYY-MM-DDTHH:MM:SSZZZZZZ
    # ZZZZZZ: +/-, H, H, :, M, M (offset from GMT)
    def __init__(self):
        super().__init__()


class Key(str):
    def __init__(self):
        super().__init__()


class Lang(str):
    # format (str): ISO[-SCRIPT[-x-PRIVATE]]
    def __init__(self):
        super().__init__()


class RefId(str):
    # format (HEX GUID): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    def __init__(self):
        super().__init__()


class URL(str):
    def __init__(self):
        super().__init__()
