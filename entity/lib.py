from ca import *
class Reference(DataStructure):
    type = None
    by = None
    data = None
    def __init__(self,type,by,data):
        self.type = type
        self.by = by
        self.data = data