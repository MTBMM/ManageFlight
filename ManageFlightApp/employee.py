from flask import render_template, request
from ManageFlightApp import UtilsEmployee, utils


def index_employee():

    return render_template("employee/index.html", list_flight=UtilsEmployee.get_list_flight(),
                           airport=utils.get_all_airport_names(), ticket_class=UtilsEmployee.get_class())


def create_schedule():

    if request.method == "POST":
        departure = request.form["from"]
        arrival = request.form["to"]
        time_de = request.form["date_departure"]
        time_arr = request.form["date_arrival"]
        rate1 = request.form["rate1"]
        rate2 = request.form["rate2"]
        airport1 = request.form["airport1"]
        time_delay1 = request.form["time_delay1"]
    return render_template("employee/schedule.html", airport=utils.get_all_airport_names())



