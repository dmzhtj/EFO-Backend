from ca import *
from entity.entity import Entity
from usecase.lib import modify
from usecase.operations import Set
class Distribute(Interface):
    containter:Entity.Container = None
    def get(self,refs):
        return [self.containter.get_element_by_ref(ref) for ref in refs]
    def update(self,objs):
        for obj in objs:
            self.containter.register(obj)
    def create(self,objs):
        for obj in objs:
            self.containter.register(obj)
    def delete(self,refs):
        modify(refs,Set("deleted",True),self.containter)
    def modify(self,refs,operation):
        modify(refs,operation,self.containter)
    def search(self,type,**fields):
        return self.containter.search(type,**fields)
    def score(self,article,thumbnail):...