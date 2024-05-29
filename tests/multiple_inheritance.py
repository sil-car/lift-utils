"""
I need to clarify how to properly handle multiple inheritance so that the
final object includes the properties and elements of each super class.
e.g.:
class Class1:
    def __init__(self):
        self.a = 1

class Class2:
    def __init__(self):
        self.b = 2

class Class3(Class2, Class1):
    def __init__(self):
        self.c = 3

obj = Class3()

obj.a = 1
obj.b = 2
obj.c = 3
"""


class Base:
    def __init__(self, x=None):
        self.x = x


class Class1(Base):
    def __init__(self, a=0, x=None):
        super().__init__(x)
        self.a = a


class Class2(Base):
    def __init__(self, b=0, x=None):
        super().__init__(x)
        self.b = b


class Class3(Class1, Class2):
    def __init__(self, c=3, x='x'):
        Class1.__init__(self, a=1, x=x)
        Class2.__init__(self, b=2, x=x)
        self.c = c
