from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import cloudinary
app = Flask(__name__)
app.secret_key = "bbbbbb"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:24042003@localhost/saledb1?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
app.config["page_size"] = 3
cloudinary.config(
    cloud_name="dsuunnyft",
    api_key="647967525442925",
    api_secret="DyORc5iac39ghbqY6wKHYvBtSac"
)
login = LoginManager(app=app)
