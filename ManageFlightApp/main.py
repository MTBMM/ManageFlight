from flask import render_template, session
from ManageFlightApp import app, controllers, utils, login, employee
# from flask_session import Session
from ManageFlightApp import app, controllers, utils, login, employee, decorator

app.add_url_rule("/", 'index', controllers.index, methods=['get', 'post'])
app.add_url_rule("/register", 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/login', 'login', controllers.login, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/sign_admin', 'sign_admin', controllers.sign_admin, methods=['post'])
app.add_url_rule('/list-flight', 'list-flight', controllers.list_flight_booking, methods=['get', 'post'])
app.add_url_rule('/load_pos', 'load_pos', controllers.load_pos, methods=['get'])
app.add_url_rule('/ticket', 'ticket', controllers.ticket, methods=['get'])
app.add_url_rule('/employee', 'index_employee', employee.index_employee, methods=['get'])
app.add_url_rule('/create_schedule', 'create_schedule', employee.create_schedule, methods=['get', 'post'])
app.add_url_rule('/list_buy_ticket', 'list_buy_ticket', employee.list_buy_ticket, methods=['get'])
app.add_url_rule('/employee_buy_ticket', 'employee_buy_ticket', employee.employee_buy_ticket, methods=['get'])
app.add_url_rule('/load_detail_flight', 'load_detail_flight', employee.load_detail_flight,
                 methods=['get'])
app.add_url_rule('/confirm', 'enter_customer_info', controllers.enter_customer_info, methods=['get', 'post'])
app.add_url_rule('/api/info', 'enter_flight_detail', controllers.enter_flight_detail, methods=['get', 'post'])

app.add_url_rule('/flight_detail', 'flight_detail', employee.flight_detail,
                 methods=['get'])

app.add_url_rule("/UserInformation", 'user_information', employee.user_information,
                 methods=['get'])


app.add_url_rule("/payment", 'payment', employee.payment,
                 methods=['get', 'post'])
app.add_url_rule("/api/pay", 'payment', employee.payment,
                 methods=['post'])

app.add_url_rule("/enter_info", "enter_info", employee.enter_info, methods=["get", "post"])
app.add_url_rule("/submit_airplane", "submit_airplane", employee.submit_airplane, methods=["get", "post"])
# app.add_url_rule("/delete_flight/<int:flight_id>", "delete_flight", employee.delete_flight, methods=["get"])
app.add_url_rule("/export_ticket", "export_ticket", employee.export_ticket, methods=["get"])


# app.add_url_rule('/ticket', 'ticket', controllers.ticket, methods=['get'])

@app.route("/user")
def user():
    return render_template('user/index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route("/account")
def account():
    return render_template('user/account.html')

#
# app.config['SECRET_KEY'] = '123'
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)


# @app.route("/info")
# def info():
#     return render_template('user/ticket-info.html')




@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from ManageFlightApp.admin import *

    app.run(debug=True)
