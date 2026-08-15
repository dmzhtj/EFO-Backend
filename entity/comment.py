from ca import *
class Comment(Interface):
    id = None
    user = None                 # Ref
    content = None
    dest = None                 # Ref.
    is_legal = None
    deleted = None
    date = None