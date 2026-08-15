from ca import *
class Article(Interface):
    id = None
    user = None             # Ref.
    title = None
    content = None
    date = None
    is_legal = None
    deleted = None