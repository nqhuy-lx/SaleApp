from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user, login_required
from eapp import app, dao, login, utils
from eapp.dao import add_user


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

@app.route('/register', methods=['post'])
def register_process():
    data = request.form
    password = data.get('password')
    confirm = data.get('confirm')
    if password != confirm:
        err_mgs = "Please check your confirm password!"
        return render_template('register.html', err_mgs=err_mgs)

    try:
        add_user(name=data.get('name'), username=data.get('username'), password=password, avatar=request.files.get('avatar'))
        return redirect('/login')
    except Exception as ex:
        return render_template('register.html', err_msg=str(ex))


@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    next = request.args.get('next')
    return redirect(next if next else '/')


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)

@app.route('/api/carts', methods=['post'])
def add_to_cart():
    # print(request.json)
    cart = session.get('cart')
    if not cart:
        cart = {}
    id = str(request.json.get('id'))
    name = request.json.get('name')
    price = request.json.get('price')
    if id in cart:
        cart[id]["quantity"] +=1
    else:
        name = request.json.get('name')
        price = request.json.get('price')
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }
    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))

@app.route('/cart')
def cart_view():
    return render_template('cart.html')

@app.context_processor
def common_responses():
    return {
        'categories': dao.load_categories(),
        'cart_stats': utils.stats_cart(session.get('cart'))
    }

@app.route('/api/pay', methods=['POST'])
@login_required
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except Exception as ex:
        return jsonify({'status': 500, 'err_msg': str(ex)})
    else:
        del session['cart']
        return jsonify({'status': 201})

@app.route('/api/carts/<id>', methods=['put'])
def update_to_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        cart[id]["quantity"] = int(request.json.get("quantity"))

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/carts/<id>', methods=['delete'])
def delete_to_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        del cart[id]

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))

if __name__ == '__main__':
    app.run(debug=True)
