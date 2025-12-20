import hashlib
import cloudinary.uploader
from sqlalchemy.exc import IntegrityError

from eapp import app, db
from eapp.models import Category, Product, User, Receipt, ReceiptDetails
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime

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

def add_receipt(cart):
    if cart:
        r=Receipt(user=current_user)
        db.session.add(r)
        for c in cart.values():
            d=ReceiptDetails(quantity=c['quantity'], price=c['price'], receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()

def stats_revenue_by_product(kw=None):
    query = (db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity*ReceiptDetails.price))
                                .join(ReceiptDetails, ReceiptDetails.product_id==Product.id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.group_by(Product.id).all()

def stats_revenue_by_time(time='month', year=datetime.now().year):
    return ((db.session.query(func.extract(time, Receipt.created_date), func.sum(ReceiptDetails.quantity*ReceiptDetails.price))
                                .join(ReceiptDetails, ReceiptDetails.receipt_id==Receipt.id))
                                .filter(func.extract("year", Receipt.created_date)==year).group_by(func.extract(time, Receipt.created_date)).all())

if __name__ =='__main__':
    with app.app_context():
        print(stats_revenue_by_product('plus'))