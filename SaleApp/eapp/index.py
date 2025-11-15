from flask import render_template, request, redirect
from flask_login import login_user
from eapp import admin
from eapp import app, dao, login

@app.route('/')
def index():
    categories = dao.load_categories()

    products = dao.load_product(cate_id=request.args.get('category_id'),
                                kw=request.args.get('kw'),
                                page=request.args.get('page'))
    return render_template('index.html',
                           msg='Welcome to my web',
                           categories=categories,
                           products=products)

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)

if __name__ == '__main__':
    app.run(debug=True)
