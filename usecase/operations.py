from ca import *
class Option(DataStructure):
    data = None
    field = None
    def __init__(self,field:str,data=None):
        self.field = field
        self.data = data
class Add(Option):...
class Set(Option):...
class Apply(Option):...