from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from eapp.models import Category, Product, UserRole
from flask import redirect
from eapp import db, app

class AdminView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ProductView(AdminView):
    column_list = ["id", "name", "price", "category_id"]
    column_searchable_list = ["name"]
    column_filters = ["name"]
    can_export = True
    column_editable_list = ["name"]
    page_size = 10

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin = Admin(app=app, name="e-Commerce's Admin")

admin.add_view(AdminView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name="Log out"))
