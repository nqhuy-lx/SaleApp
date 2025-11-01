from flask import render_template, request

from eapp import app, dao

@app.route('/')
def index():
    categories = dao.load_categories()

    products = dao.load_product(cate_id=request.args.get('category_id'), kw=request.args.get('kw'), page=request.args.get('page'))
    return render_template('index.html', msg='Welcome to my web', categories=categories, products=products)


if __name__ == '__main__':
    app.run(debug=True)
