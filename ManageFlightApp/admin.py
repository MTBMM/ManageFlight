from ManageFlightApp.models import *
from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, Admin
from ManageFlightApp import admin, db


class AuthenticatedView(ModelView):
    column_display_pk = True
    create_modal = True

    # def is_accessible(self):
    #     return not current_user.is_authenticated and current_user.user_role.__eq__(UserRoleEnum.ADMIN)


class FlightView(AuthenticatedView):
    column_filters = ["departure_time", "arrival_time"]


class CustomerView(AuthenticatedView):
    column_filters = ["username"]


class SeatView(AuthenticatedView):
    column_filters = ["number_seat"]
    column_list = ["number_seat", "status", "plane_id", "kind_id"]


class TicketClassView(AuthenticatedView):
    column_filters = ["name"]


class TicketView(AuthenticatedView):
    column_filters = ["customer_id"]


class PlaneView(AuthenticatedView):
    column_filters = ["name"]


class ReceiptView(AuthenticatedView):
    column_searchable_list = ["created_date", "id"]


class ReceiptDetailView(AuthenticatedView):
    column_searchable_list = ["id"]


class SchedulesView(AuthenticatedView):
    column_searchable_list = ["date_department"]


class RouteView(AuthenticatedView):
    column_filters = ["arrival", "departure"]


class AirportView(AuthenticatedView):
    column_filters = ["location"]


class TicketPriceView(AuthenticatedView):
    column_filters = ["id"]


class StopView(AuthenticatedView):
    column_filters = ["id"]


class AirlineView(AuthenticatedView):
    column_filters = ["id"]


class KindView(AuthenticatedView):
    column_filters = ["id"]

class EmployeeView(AuthenticatedView):
    column_filters = ["id"]


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/index.html')


admin.add_view(CustomerView(Customer, db.session, category="Person"))
admin.add_view(EmployeeView(Employee, db.session, category="Person"))
admin.add_view(SeatView(Seat, db.session, category="Manage Ticket"))
admin.add_view(TicketView(Ticket, db.session, category="Manage Ticket"))
admin.add_view(TicketPriceView(TicketPrice, db.session, category="Manage Ticket"))
admin.add_view(TicketClassView(TicketClass, db.session, category="Manage Ticket"))
admin.add_view(ReceiptView(Receipt, db.session, category="Bill"))
admin.add_view(ReceiptDetailView(ReceiptDetail, db.session, category="Bill"))
admin.add_view(SchedulesView(Schedules, db.session, category="Manage chedules"))
admin.add_view(StopView(Stop, db.session,  category="Manage chedules"))
admin.add_view(RouteView(Route, db.session))
admin.add_view(FlightView(Flight, db.session))
admin.add_view(AirportView(Airport, db.session))
admin.add_view(AirlineView(Airline, db.session))
admin.add_view(KindView(Kind, db.session))


