from ca import *
from entity.entity import Entity
from usecase.lib import modify
class User(Entity.User):
    container:Entity.Container = None
    ident = None
    def create(self,username,identification,login):
        self.username = username
        self.ident = identification
        self.login = login
        self.container.register(self)
    def confirm(self,result:bool):
        self.is_legal = result
    def modify(self,collections,operation):
        if not self.is_admin or not self.is_legal:
            return
        modify(collections,operation,self.container)
    def thumb(self,thumb=None):
        if hasattr(self.container,"thumb"):
            return self.container.thumb(self.id,thumb)
        return None