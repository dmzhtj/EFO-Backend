from ca import *
from entity.article import Article as _Article
from entity.container import Container as _Container
from entity.user import User as _User
from entity.lib import Reference as _Reference
from entity.comment import Comment as _Comment
class Entity(Layer):
    Article = _Article
    Container = _Container
    User = _User
    Reference = _Reference
    Comment = _Comment