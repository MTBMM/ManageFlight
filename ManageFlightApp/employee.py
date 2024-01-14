from flask import render_template,\
    request, session, jsonify, url_for, redirect
from ManageFlightApp import UtilsEmployee, utils, app, keys
from twilio.rest import Client


def index_employee():

    return render_template("employee/index.html")


def submit_airplane():
    messg = ""
    if request.method == "POST":

        airports = {}
        for i in range(1, session["airplane"]["quantity_airport"] + 1):
            id = str(i)
            airport = request.form["airport" + str(i)]
            time_delay_min = request.form["time_delay_min" + str(i)]
            time_delay_max = request.form["time_delay_max" + str(i)]
            arr_date = request.form["arr_date" + str(i)]
            airports[id] = {
                "airport": airport,
                "time_delay_min": time_delay_min,
                "time_delay_max": time_delay_max,
                "arr_date":  arr_date
            }

        try:

            UtilsEmployee.update_flight(airports=airports,  airplane=session["airplane"])
            messg = "thành công"

        except:
            messg = "Không thành công"

    return render_template("employee/info_airplane.html", messg=messg, quantity=session["airplane"]["quantity_airport"])




def create_schedule():
    err_msg = ""
    if request.method == "POST":
        departure = request.form["from"]
        arrival = request.form["to"]
        time_de = request.form["date_departure"]
        time_arr = request.form["date_arrival"]
        rate1 = request.form["rate1"]
        rate2 = request.form["rate2"]
        quantity_airport = request.form["quantity_airport"]
        session["airplane"] = {
            "departure": departure,
            "arrival": arrival,
            "time_de": time_de,
            "time_arr":  time_arr,
            "rate1": int(rate1),
            "rate2": int(rate2),
            "quantity_airport":  int(quantity_airport)
        }
        # import pdb
        # pdb.set_trace()
        return redirect(url_for('submit_airplane'))

    return render_template("employee/schedule.html",
                           airport=utils.get_all_airport_names())


def employee_buy_ticket():

    flights = UtilsEmployee.get_list_flight()
    return render_template("employee/BuyTicket.html", flights=flights)


def list_buy_ticket():
    list_book_ticket = UtilsEmployee.customer_booked_ticket()

    return render_template("employee/ListBookTicket.html", list_book_ticket=list_book_ticket)


def load_detail_flight():

    # import pdb
    # pdb.set_trace()

    return render_template("employee/list-schedule.html", list_flight=UtilsEmployee.get_list_flight(),
                           airport=utils.get_all_airport_names(),
                           ticket_class=UtilsEmployee.get_class())


@app.context_processor
def common_reponse():
    return {
        'airport': utils.get_all_airport_names()

    }


def flight_detail():
    flight_id = request.args.get("flight_id")
    list_flight = UtilsEmployee.get_detail_flight(flight_id=flight_id)
    # # if flight_id:
    flight_detail = UtilsEmployee.get_detail_flight(flight_id=int(flight_id))
    return render_template("employee/flight-detail.html", flight_detail=flight_detail,
                           stops=UtilsEmployee.get_stops())


def user_information():
    flight_id = request.args.get("f")
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
        "id_class": list_flight.TicketPrice.ticket_class.id
    }
    session["info"] = info

    return render_template("employee/UserInformation.html")


def enter_info():

    if request.method == "POST":
        name = request.form["fullname"]
        birthdate = request.form["birthdate"]
        phone = request.form["phone"]
        identify = request.form["identify"]
        info_user = {
            "name": name,
            "birthdate": birthdate,
            "phone": phone,
            "identify": identify,
            "departure": session["info"]["departure"],
            "arrival": session["info"]["arrival"],
            "price": session["info"]["price"],
            "departure_time": session["info"]["departure_time"],
            "arrival_time": session["info"]["arrival_time"],
            "class": session["info"]["class"],
            "flight_id": session["info"]["flight_id"],
            "id_class": session["info"]["id_class"]
        }
        session["info"] = info_user

    return render_template("employee/payment.html")


def payment():


     try:
            UtilsEmployee.save_ticket(session.get("info"))
            # client = Client(keys.account_sid, keys.auth_token)
            # client.messages.create(
            #     body="this is a sample message",
            #     from_=keys.twilio_number,
            #      to=keys.my_number)

            del session["info"]

            return jsonify({"code": 200})

     except Exception as ex:
             return jsonify({"code": 400})


def delete_flight(flight_id):
    UtilsEmployee.delete_flight(flight_id=flight_id)


