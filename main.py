from adapter.flask_render.Flask import FlaskDisplay
from adapter.flask_render.RDB import RDB,db,ensure_registration_reason_column
from adapter.randdis import RandDistribute
disp = FlaskDisplay()
disp.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
disp.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
disp.app.secret_key = open("secret.key","r").read().strip()
rdb = RDB(disp.app)
with disp.app.app_context():
    db.create_all()
    ensure_registration_reason_column()
dist = RandDistribute()
dist.containter = rdb
disp.set_dist(dist)
disp.run()