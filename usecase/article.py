from ca import *
from entity.entity import Entity
from datetime import datetime
class Article(Entity.Article):
    container:Entity.Container = None
    def create(self,title,user,content):
        self.title = title
        self.content = content
        self.container.register(self)
        self.user = Entity.Reference(Entity.User,"id",user.id)
        self.date = datetime.now()
    def confirm(self,result:bool):
        self.is_legal = result