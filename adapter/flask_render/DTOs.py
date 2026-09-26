from ca import *
from json import loads
from random import choice
from bs4 import BeautifulSoup
class UserDTO(DataStructure):
    username = None
    id = None
    is_admin = None
    last_login = None
    is_legal = None
    deleted = None
    def __init__(self,user):
        if user:
            self.id = user.id
            self.username = user.username
            self.is_admin = user.is_admin
            self.last_login = user.last_login
            self.is_legal = user.is_legal
            self.deleted = user.deleted
class ArticleDTO(DataStructure):
    id = None
    title = None
    body = None
    description = None
    ai = None
    category = None
    music_title = None
    music_artist = None
    music_album = None
    cover = None
    date = None
    user = None
    type = None                             # Just for exp page.
    span = ""                               # Just for exp page.
    passed = False                          # Just for exp page.
    def extract(self,article,user):
        self.id = article.id
        self.date = article.date
        self.title = article.title
        lines = article.content.split("\n")
        dic = loads(lines[0].strip())
        self.body = "\n".join(lines[1:])
        self.description = dic.get("description","")
        self.ai = dic.get("ai",True)
        self.category = dic.get("category","Unknown")
        self.type = dic.get("type","text")
        self.music_title = dic.get("music_title","")
        self.music_artist = dic.get("music_artist","")
        self.music_album = dic.get("music_album","")
        self.cover = dic.get("cover","")
        self.user = UserDTO(user)
    def score(self,score):
        if score >= 0.5:
            self.span = "span-2x2"
        elif score >= 0:
            self.span = choice(["span-2w","span-2h"])
        elif score >= -0.5:
            self.span = ""
        else:
            self.passed = choice([True,False])
    def imgsrc(self):
        return BeautifulSoup(self.body, "html.parser").img.attrs["src"]
    def text(self):
        return BeautifulSoup(self.body, "html.parser").getText()
class CommentDTO(DataStructure):
    id = None
    user = None
    content = None
    date = None
    def extract(self,comment,user):
        self.date = comment.date
        self.content = comment.content
        self.user = UserDTO(user)