from ca import *
from entity.entity import Entity as _Entity
from usecase.article import Article as _Article
from usecase.comment import Comment as _Comment
from usecase.display import Display as _Display
from usecase.distribute import Distribute as _Distribute
from usecase.lib import modify as _modify
from usecase.operations import Add as _Add,Set as _Set,Apply as _Apply,Option as _Option
from usecase.user import User as _User
class UseCase(Layer):
    Entity = _Entity
    Article = _Article
    Comment = _Comment
    Display = _Display
    Distribute = _Distribute
    modify = _modify
    User = _User
    class Options:
        Add = _Add
        Set = _Set
        Apply = _Apply
        Option = _Option