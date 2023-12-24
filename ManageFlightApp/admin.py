from ManageFlightApp.models import *
from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, Admin

#
# class AuthenticatedView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.ADMIN)


class FlightView(ModelView):
    column_display_pk = True
    column_filters = ["departure_time"]
    column_list = ['departure_time', 'arrival_time']


class CustomerView(ModelView):
    column_display_pk = True


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name="QUẢN TRỊ HÀNG HÀNG KHÔNG", template_mode="bootstrap4", index_view=MyAdminIndexView())
admin.add_view(FlightView(Flight, db.session))
admin.add_view(CustomerView(Customer, db.session))
