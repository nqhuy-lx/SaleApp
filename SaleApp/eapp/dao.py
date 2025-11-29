import hashlib
import cloudinary.uploader
from sqlalchemy.exc import IntegrityError

from eapp import app, db
from eapp.models import Category, Product, User


def load_categories():
    return Category.query.all()

def load_product(cate_id=None, kw=None, page=1):
    query = Product.query
    if kw:
        query = query.filter(Product.name.contains(kw))
    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))
    return query.all()

def get_user_by_id(id):
    return User.query.get(id)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username==username, User.password==password).first()

def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name.strip(), username=username.strip(), password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get("secure_url")
    db.session().add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise  Exception("Username already exists!")