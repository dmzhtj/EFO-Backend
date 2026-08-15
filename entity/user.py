from ca import *
class User(Interface):
    id = None
    username = None
    logined = None
    is_admin = None
    last_login = None
    is_legal = None
    deleted = None
    def login() -> None:...