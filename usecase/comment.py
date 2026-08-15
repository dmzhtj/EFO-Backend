from ca import *
from entity.entity import Entity
from datetime import datetime
class Comment(Entity.Comment):
    container:Entity.Container = None
    def create(self,user,dest,content):
        self.user = Entity.Reference("user","id",user.id)
        if isinstance(dest,Entity.Article):
            self.dest = Entity.Reference("article","id",dest.id)
        elif isinstance(dest,Entity.Comment):
            self.dest = Entity.Reference("comment","id",dest.id)
        else:
            self.dest = Entity.Reference(None,None,None)        # Orphan node.This is dead code.
        self.content = content
        self.deleted = False
        self.date = datetime.now()
        self.container.register(self)
    def confirm(self,result:bool):
        self.is_legal = result