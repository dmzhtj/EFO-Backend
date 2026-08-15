from uuid import uuid4
from re import findall
from flask import session
def fill_fields(ori,dest,fields:list[str]):
    for field in fields:
        setattr(dest,field,getattr(ori,field))
def lin(ls1:list,ls2:list):
    for i in ls1:
        if not i in ls2:
            return False
    return True
def chkcsrftoken(token:str):
    return token == session.get("csrf_token")
def getcsrftoken():
    token = str(uuid4())
    session["csrf_token"] = token
    return token
def randfilename():
    return "static/uploads/" + uuid4().hex
def externallinks(text):
    return findall(r'https?://[^\s<>"\'()]+',text)