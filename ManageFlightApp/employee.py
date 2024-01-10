from flask import render_template, request
from ManageFlightApp import UtilsEmployee, utils, app


def index_employee():

    return render_template("employee/index.html")


def create_schedule():
    err_msg = ""
    if request.method == "POST":
        departure = request.form["from"]
        arrival = request.form["to"]
        time_de = request.form["date_departure"]
        time_arr = request.form["date_arrival"]
        rate1 = request.form["rate1"]
        rate2 = request.form["rate2"]
        airport1 = request.form["airport1"]
        time_delay_min = request.form["time_delay_min"]
        time_delay_max = request.form["time_delay_max"]
        arr_date = request.form["arr_date"]

        quantity_airport = request.form["quantity_airport"]
        # import pdb
        # pdb.set_trace()
        try:
            UtilsEmployee.update_flight(departure=departure, arrival=arrival, time_de=time_de,
                            time_arr=time_arr,
                            rate1=rate1, rate2=rate2,
                            airport1=airport1, time_delay_min=time_delay_min,
                            time_delay_max=time_delay_max, arr_date=arr_date,
                                       quantity_airport=quantity_airport
                                       )
            err_msg = "Success!!"

        except:
            err_msg = ""

    return render_template("employee/schedule.html",
                           airport=utils.get_all_airport_names(), err_msg=err_msg)


def employee_buy_ticket():

    flights = UtilsEmployee.get_list_flight()
    return render_template("employee/BuyTicket.html", flights=flights)


def list_buy_ticket():
    return render_template("employee/ListBookTicket.html")


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

    # # if flight_id:
    flight_detail = UtilsEmployee.get_detail_flight(flight_id=int(flight_id))
    return render_template("employee/flight-detail.html", flight_detail=flight_detail,
                           stops=UtilsEmployee.get_stops())
