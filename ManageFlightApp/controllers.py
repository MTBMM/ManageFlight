import cloudinary
from flask import render_template, url_for, request, redirect
from cloudinary import uploader
from flask_login import login_user, logout_user, login_required
from ManageFlightApp.models import UserRoleEnum
from ManageFlightApp import app, utils


def index():
    airport = utils.get_all_airport_names()
    return render_template('home/index.html', airport=airport)


def list_flight_booking():
    airport = utils.get_all_airport_names()

    location_from = request.form['from']
    location_to = request.form['to']
    departure = request.form["departure"]
    # import pdb
    # pdb.set_trace()

    flights = utils.get_flight_details(start_location=location_from, end_location=location_to, departure=departure)

    return render_template('home/list-flight.html', airport=airport, flights=flights,
                               start=location_from, end=location_to)


def load_pos():
    # pos_type = dao.load_type_of_position()
    return render_template('user/position.html')


def register():
    err_msg = ''

    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            try:

                utils.register(username=request.form['username'],
                               password=password, avatar=avatar)
                print('thành cong')

                return redirect('/login')
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'
    return render_template('home/register.html', err_msg=err_msg)


def ticket():
    return render_template("ticket.html")


def login():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.auth_user(username=username, password=password)
        if user:
            # ghi nhận user đã đăng nhập ; current_user toàn cục
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_mgs = "Lỗi sai username hoặc password!!"
    return render_template('home/login.html', err_mgs=err_mgs)


@login_required
def logout_my_user():
    logout_user()
    return redirect('/')


def sign_admin():
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method.__eq__("POST"):

        user = utils.check_admin(username=username, password=password, role=UserRoleEnum.ADMIN)
        if user:
            login_user(user=user)

    return redirect("/admin")


if __name__ == '__main__':
    app.run(debug=True)
