from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, LoginManager
import cloudinary
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = "uocgitaobotdangcapmotchut"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4' % quote('root')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
cloudinary.config(cloud_name='uploadstatic',
                    api_key='192984554588374',
                    api_secret='pJB25mr86dVIemjALn2TgJXcj0M')