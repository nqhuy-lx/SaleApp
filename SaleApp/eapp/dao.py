from eapp.model import Category, Product


def load_categories():
    return Category.query.all()

def load_product(cate_id=None, kw=None, page=1):
    query = Product.query
    if kw:
        query = query.filter(Product.name.contains(kw))
    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))
    return query.all()