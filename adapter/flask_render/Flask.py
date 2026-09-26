from ca import *
from flask import *
from werkzeug.security import generate_password_hash,check_password_hash
from adapter.settings import GENERAL
from usecase.usecase import UseCase
from adapter.flask_render.DTOs import *
from adapter.lib import *
from datetime import datetime
from pathlib import Path
from mutagen import MutagenError
from mutagen.flac import FLAC
from htmlmin import minify
from markdown import markdown
def after_request(response):
    if response.content_type and 'text/html' in response.content_type:
        html_content = response.get_data(as_text=True)
        minified = minify(html_content,remove_empty_space=True,remove_comments=True,convert_charrefs=False)
        response.set_data(minified)
    return response
class FlaskDisplay(UseCase.Display):
    app = None
    def __init__(self):
        self.app = Flask(GENERAL.APP_NAME)
        self.app.after_request(after_request)
        self.app.add_url_rule("/","index",self.index,methods=["GET","POST"])
        self.app.add_url_rule("/login","login",self.login,methods=["GET","POST"])
        self.app.add_url_rule("/login/",None,self.login,methods=["GET","POST"])
        self.app.add_url_rule("/useram","useram",self.useram,methods=["GET"])
        self.app.add_url_rule("/useram/",None,self.useram,methods=["GET"])
        self.app.add_url_rule("/signup","signup",self.signup,methods=["GET","POST"])
        self.app.add_url_rule("/signup/",None,self.signup,methods=["GET","POST"])
        self.app.add_url_rule("/logout","logout",self.logout,methods=["GET"])
        self.app.add_url_rule("/logout/",None,self.logout,methods=["GET"])
        self.app.add_url_rule("/dtexp","dtexp",self.dtexp,methods=["GET","POST"])
        self.app.add_url_rule("/dtexp/",None,self.dtexp,methods=["GET","POST"])
        self.app.add_url_rule("/exp","exp",self.exp,methods=["GET"])
        self.app.add_url_rule("/exp/",None,self.exp,methods=["GET"])
        self.app.add_url_rule("/post","post",self.post,methods=["GET","POST"])
        self.app.add_url_rule("/post/",None,self.post,methods=["GET","POST"])
    def set_dist(self,dist):
        self.dist = dist
        admin = AdminBlueprint(dist)
        self.app.register_blueprint(admin.app)
    def index(self):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if not user:
            return redirect("/login/")
        if request.method == "POST":
            if not lin(["password","csrftoken"],request.form):
                abort(400)
            if not chkcsrftoken(request.form.get("csrftoken")):
                abort(403)
            if not check_password_hash(user.ident,request.form.get("password")):
                flash("Please check your password.")
                return redirect("/")
            if lin(["new","confirm"],request.form) and request.form.get("new"):
                if request.form.get("new") != request.form.get("confirm"):
                    flash("Please check your new password.")
                    return redirect("/")
                user.ident = generate_password_hash(request.form.get("new"))
                self.dist.update([user])
                flash("Password changed successfully.")
            if lin(["avatar"],request.files):
                avatar = request.files.get("avatar")
                avatar.save("static/avatar/" + str(user.id))
                flash("Avatar uploaded successfully")
            return redirect("/")
        return render_template("index.html",user=user,csrftoken=getcsrftoken())
    def login(self):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if user:
            flash("Please logout first.")
            return redirect("/")
        if request.method == "POST":
            if not lin(["username","password","csrftoken"],request.form):
                abort(400)
            if not chkcsrftoken(request.form.get("csrftoken")):
                abort(403)
            user = self.dist.get([UseCase.Entity.Reference("user","username",request.form.get("username"))])[0]
            if user and check_password_hash(user.ident,request.form.get("password")):
                if user.is_legal:
                    user.logined = True
                    session["user"] = user.id
                    return redirect("/")
                else:
                    flash("User has no permission to visit the website yet.")
                    return redirect("/login/")
            else:
                flash("Please check username and password.")
                return redirect("/login/")
        return render_template("log.html",csrftoken=getcsrftoken())
    def useram(self):
        return render_template("useram.html")
    def signup(self):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if user:
            flash("Please logout first.")
            return redirect("/")
        if request.method == "POST":
            if not lin(["username","password","confirm","reason","csrftoken"],request.form):
                abort(400)
            if not chkcsrftoken(request.form.get("csrftoken")):
                abort(403)
            if len(request.form.get("username")) < 3 or len(request.form.get("username")) > 64:
                flash("Please confirm your username.")
                return redirect("/signup/")
            if request.form.get("password") != request.form.get("confirm") or len(request.form.get("password")) < 8:
                flash("Please confirm your password.")
                return redirect("/signup/")
            user = self.dist.get([UseCase.Entity.Reference("user","username",request.form.get("username"))])[0]
            if user and not user.deleted:
                flash("Username already in use.")
                return redirect("/signup/")
            if not user:
                user = UseCase.User()
                user.username = request.form.get("username")
            user.ident = generate_password_hash(request.form.get("password"))
            user.deleted = False
            user.last_login = datetime.now()
            user.is_admin = False
            user.is_legal = None
            self.dist.update([user])
            flash("The form has been submitted successfully.Please try to login a few days later.")
            return redirect("/login/")
        return render_template("signup.html",csrftoken=getcsrftoken())
    def logout(self):
        session.pop("user")
        return redirect("/login/")
    def dtexp(self):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if not user:
            return redirect("/login/")
        try:
            id = int(request.args.get("id"))
        except ValueError:
            abort(400)
        article = self.dist.get([UseCase.Entity.Reference("article","id",id)])[0]
        if not article or article.deleted:
            abort(404)
        if not article.is_legal:
            abort(403)
        if request.method == "POST":
            if not lin(["text","csrftoken"],request.form):
                abort(400)
            if not request.form.get("text"):
                abort(400)
            if not chkcsrftoken(request.form.get("csrftoken")):
                abort(403)
            comment = UseCase.Comment()
            comment.container = self.dist.containter
            comment.create(user,article,request.form.get("text"))
            flash("Comment submitted successfully.It will be displayed after check.")
            return redirect("/dtexp/?id=" + str(id))
        else:
            auser = self.dist.get([article.user])[0]
            det = ArticleDTO()
            det.extract(article,auser)
            dbcomments = [comment for comment in self.dist.search("comment",dest_type="article",dest_id=id,deleted=False,is_legal=True)]
            comments = []
            for dbcomment in dbcomments:
                dbcomment_user = self.dist.get([dbcomment.user])[0]
                comment = CommentDTO()
                comment.extract(dbcomment,dbcomment_user)
                comments.append(comment)
            return render_template("dtexp.html",detail=det,comments=comments,csrftoken=getcsrftoken())
    def exp(self):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if not user:
            return redirect("/login/")
        try:
            headless = int(request.args.get("headless",0))
            lo_id = int(request.args.get("lo_id",2147483647))
        except ValueError:
            abort(400)
        articles = self.dist.search("article",is_legal=True,deleted=False,ieq=[("id","le",lo_id)],order_by=["date"],desc=["date"],limit=10)
        dtos = []
        lo_id = 2147493647
        for article in articles:
            lo_id = min(lo_id,article.id)
            auser = self.dist.get([article.user])[0]
            dto = ArticleDTO()
            dto.extract(article,auser)
            dto.score(self.dist.score(article,user.thumb()))
            dtos.append(dto)
        if lo_id == 2147493647:
            lo_id = -1
        return render_template("exp.html",articles=dtos,headless=headless,lo_id=lo_id)
    def post(self):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if not user:
            return redirect("/login/")
        if request.method == "POST":
            if not lin(["category","type","csrftoken"],request.form):
                abort(400)
            if not chkcsrftoken(request.form.get("csrftoken")):
                abort(403)
            media_type = request.form.get("type")
            if media_type not in ["text","image","video","audio"]:
                abort(400)
            if request.form.get("type") == "text":
                if not request.form.get("content"):
                    abort(400)
                content = markdown(request.form.get("content"))
            else:
                media_file = request.files.get(media_type)
                if not media_file or not media_file.filename:
                    abort(400)
                filename = randfilename()
                media_file.save(filename)
                if media_type == "image":
                    content = f"""<img src="/{filename}"/>"""
                elif media_type == "video":
                    content = f"""<video controls preload src="/{filename}"></video>"""
                else:                           # audio
                    content = f"""<audio controls preload src="/{filename}"></audio>"""
                    cover = ""
                    music_title = Path(media_file.filename).stem
                    music_artist = ""
                    music_album = ""
                    if Path(media_file.filename).suffix.lower() == ".flac":
                        try:
                            flac = FLAC(filename)
                        except MutagenError:
                            Path(filename).unlink(missing_ok=True)
                            abort(400, description="Could not read metadata from the uploaded FLAC file.")
                        music_title = (flac.get("title") or [music_title])[0]
                        music_artist = (flac.get("artist") or [""])[0]
                        music_album = (flac.get("album") or [""])[0]
                        if flac.pictures:
                            picture = flac.pictures[0]
                            suffix = {
                                "image/jpeg": ".jpg",
                                "image/png": ".png",
                                "image/gif": ".gif",
                                "image/webp": ".webp"
                            }.get(picture.mime.lower())
                            if suffix:
                                cover_path = randfilename() + suffix
                                Path(cover_path).write_bytes(picture.data)
                                cover = "/" + cover_path
            article = UseCase.Article()
            dic = {"ai":True if request.form.get("ai") else False,
                    "description":request.form.get("description-" + request.form.get("type"),""),
                    "type":request.form.get("type"),
                    "category":request.form.get("category").capitalize()}
            if request.form.get("type") == "audio":
                dic.update({
                    "music_title":music_title,
                    "music_artist":music_artist,
                    "music_album":music_album,
                    "cover":cover
                })
            article.content = json.dumps(dic) + "\n" + content
            article.date = datetime.now()
            article.user = UseCase.Entity.Reference("user","id",user.id)
            article.deleted = 0
            article.title = "Untitled"
            self.dist.create([article])
            return redirect("/exp/")
        return render_template("post.html",csrftoken=getcsrftoken())
    def run(self):
        self.app.run(GENERAL.APP_HOST,GENERAL.APP_PORT,GENERAL.APP_DEBUG)
class AdminBlueprint(UseCase.Display):
    app = None
    def __init__(self,dist):
        self.app = Blueprint("admin","admin",url_prefix="/admin/")
        self.app.add_url_rule("/","index",self.index,methods=["GET"])
        self.app.add_url_rule("/review/<type>","review",self.review,methods=["GET","POST"])
        self.app.add_url_rule("/review/<type>/",None,self.review,methods=["GET","POST"])
        self.app.add_url_rule("/modify","modify",self.modify,methods=["GET"])
        self.app.add_url_rule("/modify/",None,self.modify,methods=["GET"])
        self.dist = dist
    def index(self):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if not user:
            return redirect("/login/")
        if not user.is_admin:
            abort(403)
        return render_template("admin/index.html",user=user,version=GENERAL.APP_VERSION)
    def review(self,type):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if not user:
            return redirect("/login/")
        if not user.is_admin:
            abort(403)
        if not type in ["user","article","comment"]:
            abort(400)
        if request.method == "POST":
            if not lin(["id","action","csrftoken"],request.form):
                abort(400)
            if not chkcsrftoken(request.form.get("csrftoken")):
                abort(403)
            try:
                id = int(request.form.get("id"))
            except ValueError:
                abort(400)
            object = self.dist.get([UseCase.Entity.Reference(type,"id",id)])[0]
            if not object:
                abort(404)
            if request.form.get("action") == "confirm":
                object.is_legal = True
            elif request.form.get("action") == "forbid":
                object.is_legal = False
            else:
                object.is_legal = None
            self.dist.update([object])
        object = list(self.dist.search(type,deleted=False,is_legal=None,limit=1))
        if not object:
            flash("Thank you, " + user.username + ". No more " + type + " data to review now.")
            return redirect("/admin/")
        object = object[0]
        if type == "user":
            data = object.thumbnail
        elif type == "article":
            dto = ArticleDTO()
            dto.extract(object,None)
            data = "Body:\n" + dto.body + "\n\n\nDescription:\n" + dto.description
        elif type == "comment":
            data = object.content
        links = externallinks(data)
        return render_template("admin/review.html",user=user,data=data,id=object.id,csrftoken=getcsrftoken(),links=links,version=GENERAL.APP_VERSION)
    def modify(self):
        user = self.dist.get([UseCase.Entity.Reference("user","id",int(session.get("user",-1)))])[0]
        if not user:
            return redirect("/login/")
        if not user.is_admin:
            abort(403)
        return render_template("admin/modify.html",user=user,version=GENERAL.APP_VERSION)
    def run(self):
        raise RuntimeError("You can't run a blueprint.")