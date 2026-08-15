from ca import *
from usecase.usecase import UseCase
from adapter.lib import fill_fields
from adapter.settings import DATA

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Unicode(64),nullable=False,unique=True,index=True)
    ident = db.Column(db.String(128),nullable=False)
    is_admin = db.Column(db.Boolean,nullable=False,default=False)
    is_legal = db.Column(db.Boolean,nullable=True)
    deleted = db.Column(db.Boolean,nullable=False,default=False)
    last_login = db.Column(db.DateTime,nullable=False,default=datetime.now)
    thumbnail = db.Column(db.String(DATA.THUMB_SIZE),nullable=True)
class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer,db.ForeignKey('user.id'))
    title = db.Column(db.Unicode(64),nullable=False)
    content = db.Column(db.Unicode(65536),nullable=True)
    date = db.Column(db.DateTime,nullable=False,index=True,default=datetime.now)
    is_legal = db.Column(db.Boolean,nullable=True)
    deleted = db.Column(db.Boolean,nullable=False,default=False)
class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer,db.ForeignKey('user.id'))
    content = db.Column(db.Unicode(128),nullable=False)
    dest_type = db.Column(db.String(16),nullable=False)
    dest_id = db.Column(db.Integer,nullable=False)
    is_legal = db.Column(db.Boolean,nullable=True)
    deleted = db.Column(db.Boolean,nullable=False,default=False)
    date = db.Column(db.DateTime,nullable=False,index=True,default=datetime.now)

class RDB(UseCase.Entity.Container):
    def __init__(self,app):
        self.app = app
        db.init_app(app)
    def qrf(self,type):
        if type == "user":
            queryclass = User
            resclass = UseCase.User
            fields = ["deleted","id","ident","is_admin","is_legal","last_login","username"]
        elif type == "article":
            queryclass = Article
            resclass = UseCase.Article
            fields = ["content","date","deleted","id","is_legal","title"]
        elif type == "comment":
            queryclass = Comment
            resclass = UseCase.Comment
            fields = ["content","date","deleted","id","is_legal"]
        return queryclass,resclass,fields
    def mapdata(self,type,data,resclass,fields):
        result = resclass()
        result.container = self
        fill_fields(data,result,fields)
        if type == "user":
            data:User
            result.logined = None                   ####### Unknown currently #######
        elif type == "article":
            data:Article
            result.user = UseCase.Entity.Reference("user","id",data.user)
        elif type == "comment":
            data:Comment
            result.dest = UseCase.Entity.Reference(data.dest_type,"id",data.dest_id)
            result.user = UseCase.Entity.Reference("user","id",data.user)
        return result
    def fmapdata(self,type,data,base,fields):
        fill_fields(data,base,fields)
        if type == "user":
            pass                                    ####### Useless #######
        elif type == "article":
            base.user = self.get_element_by_ref(data.user).id
        elif type == "comment":
            base.user = self.get_element_by_ref(data.user).id
            base.dest_type = data.dest.type
            base.dest_id = self.get_element_by_ref(data.dest).id
    def get_element_by_ref(self,ref:UseCase.Entity.Reference):
        with self.app.app_context():
            queryclass,resclass,fields = self.qrf(ref.type)
            if ref.by == "id":
                data = queryclass.query.get(ref.data)
                if not data:
                    return None
            else:
                query = queryclass.query.filter(getattr(queryclass,ref.by)==ref.data)
                if query.count() != 1:
                    # raise ValueError("Element not found or not unique.")
                    return None
                data = query.first()
            result = self.mapdata(ref.type,data,resclass,fields)
        return result
    def search(self,type:str,**fields):
        with self.app.app_context():
            queryclass,resclass,fields_ = self.qrf(type)
            query = queryclass.query
            for field in fields:
                if not field in ["limit","order_by","desc","ieq"]:
                    query = query.filter(getattr(queryclass,field)==fields[field])
            if "ieq" in fields:
                for field,sign,data in fields["ieq"]:
                    if sign == "le":
                        query = query.filter(getattr(queryclass,field)<=data)
                    elif sign == "lt":
                        query = query.filter(getattr(queryclass,field)<data)
                    elif sign == "ge":
                        query = query.filter(getattr(queryclass,field)>=data)
                    elif sign == "gt":
                        query = query.filter(getattr(queryclass,field)>data)
            if "order_by" in fields:
                fields["order_by"].reverse()
                for field in fields["order_by"]:
                    base = getattr(queryclass,field)
                    if "desc" in fields and field in fields["desc"]:
                        order = base.desc()
                    query = query.order_by(order)
            if "limit" in fields:
                query = query.limit(fields["limit"])
            return map(lambda x:self.mapdata(type,x,resclass,fields_),query.all())
    def register(self,object):
        if isinstance(object,UseCase.User):
            type = "user"
        elif isinstance(object,UseCase.Article):
            type = "article"
        elif isinstance(object,UseCase.Comment):
            type = "comment"
        queryclass,resclass,fields = self.qrf(type)
        if object.id:
            dbobj = queryclass.query.get(object.id)
            if not dbobj:
                raise ValueError("Do not specify an id for a transient object.")
        else:
            dbobj = queryclass()
        self.fmapdata(type,object,dbobj,fields)
        db.session.add(dbobj)
        db.session.commit()
        object.id = dbobj.id
    def thumb(self,userid:int,thumbnail=None):
        user = User.query.get(userid)
        if thumbnail:
            user.thumbnail = thumbnail
            db.session.add(user)
            db.session.commit()
        return user.thumbnail