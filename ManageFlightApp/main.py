from flask import render_template
from ManageFlightApp import app, controllers, utils, login, employee

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

app.add_url_rule('/flight_detail', 'flight_detail', employee.flight_detail,
                 methods=['get'])


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


@app.route("/info")
def info():
    return render_template('user/ticket-info.html')


@app.route("/confirm")
def confirm():
    return render_template('user/confirm.html')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from ManageFlightApp.admin import *

    app.run(debug=True)
