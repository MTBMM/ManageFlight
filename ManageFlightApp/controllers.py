from functools import wraps

import cloudinary
from functools import wraps
from flask import render_template, url_for, request, redirect, session, Flask, jsonify
from cloudinary import uploader
from flask_login import login_user, logout_user, current_user
from ManageFlightApp.models import UserRoleEnum
from ManageFlightApp import app, utils, UtilsEmployee, login


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login_user", next=request.url))
        return f(*args, **kwargs)

    return check


@login.user_loader
def user_loader(user_id):
    return utils.get_user_by_id(user_id=user_id)


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
    stops = UtilsEmployee.get_stops()
    # if flights
    # price_eco = flights
    return render_template('user/list-flight.html', airport=airport, flights=flights,
                           start=location_from, end=location_to, stops=stops)


@login_required
def load_pos():
    flight_id = request.args.get('flight_id')
    class_id = request.args.get('class_id')
    list_flight = UtilsEmployee.get_detail_flight(flight_id=int(flight_id))
    list_airport = UtilsEmployee.get_airport()
    for airport in list_airport:
        if airport.id == list_flight.Route.departure_id:
            departure = airport.name
        if airport.id == list_flight.Route.arrival_id:
            arrival = airport.name

    info = {
        "flight_id": list_flight.Flight.id,
        "departure": departure,
        "arrival": arrival,
        "price": list_flight.TicketPrice.price,
        "departure_time": list_flight.Flight.departure_time,
        "arrival_time": list_flight.Flight.arrival_time,
        "class": list_flight.TicketPrice.ticket_class.name,
        "id_class": list_flight.TicketPrice.ticket_class.id,
        "plane": list_flight[5]
    }
    session["info"] = info
    # import pdb
    # pdb.set_trace()
    seats = utils.get_seat(flight_id)
    seat_first = utils.get_seat_first(flight_id)
    seat_first = int(seat_first[0])
    class_id = int(class_id)
    return render_template('user/position.html', seats=seats, seat_first=seat_first, class_id=class_id)


def api_info():
    data = request.json
    id_value = data.get('id')
    name_value = data.get('name')
    status_value = data.get('status')
    response_data = {
        'id_seat': id_value,
        'name': name_value,
        'status': status_value,
        "departure": session["info"]["departure"],
        "arrival": session["info"]["arrival"],
        "price": session["info"]["price"],
        "departure_time": session["info"]["departure_time"],
        "arrival_time": session["info"]["arrival_time"],
        "class": session["info"]["class"],
        "flight_id": session["info"]["flight_id"],
        "id_class": session["info"]["id_class"],
        "plane": session["info"]["plane"]
    }
    session['info'] = response_data
    # import pdb
    # pdb.set_trace()
    return jsonify(response_data)


def enter_flight_detail():
    response_data = {
        'id_seat': session["info"]["id_seat"],
        'name_seat': session["info"]["name"],
        'status': session["info"]["status"],
        "departure": session["info"]["departure"],
        "arrival": session["info"]["arrival"],
        "price": session["info"]["price"],
        "departure_time": session["info"]["departure_time"],
        "arrival_time": session["info"]["arrival_time"],
        "class": session["info"]["class"],
        "flight_id": session["info"]["flight_id"],
        "id_class": session["info"]["id_class"],
        "plane": session["info"]["plane"]
    }
    session['info'] = response_data
    return render_template('user/ticket-info.html')


def enter_customer_info():
    if request.method == "POST":
        name = request.form["fullname"]
        birthdate = request.form["dob"]
        phone = request.form["phone"]
        identify = request.form["id"]
        gender = request.form["gender"]
        info_user = {
            "name": name,
            "birthdate": birthdate,
            "phone": phone,
            "identify": identify,
            "gender": gender,
            "departure": session["info"]["departure"],
            "arrival": session["info"]["arrival"],
            "price": session["info"]["price"],
            "departure_time": session["info"]["departure_time"],
            "arrival_time": session["info"]["arrival_time"],
            "class": session["info"]["class"],
            "flight_id": session["info"]["flight_id"],
            "id_class": session["info"]["id_class"],
            "plane": session["info"]["plane"],
            'id_seat': session["info"]["id_seat"],
            'name_seat': session["info"]["name_seat"],
            'status': session["info"]["status"]
        }
        session['info'] = info_user
        # import pdb
        # pdb.set_trace()
        return render_template('user/confirm.html')


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
    customer_info = session.get('info', {})
    return render_template("user/ticket.html", customer_info=customer_info)


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


def payment_cus():
    try:
        utils.save_ticket(session.get("info"))
        import pdb
        pdb.set_trace()
        # client = Client(keys.account_sid, keys.auth_token)
        # client.messages.create(
        #     body="this is a sample message",
        #     from_=keys.twilio_number,
        #      to=keys.my_number)
        #
        # del session["info"]

        return jsonify({"code": 200})

    except Exception as ex:
        return jsonify({"code": 400})


if __name__ == '__main__':
    app.run(debug=True)
