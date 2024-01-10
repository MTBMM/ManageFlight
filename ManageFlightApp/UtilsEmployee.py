from ManageFlightApp.models import *


def get_list_flight():

    departure_airport_alias = aliased(Airport)
    arrival_airport_alias = aliased(Airport)
    list_flight = db.session.query(
        Flight,
        Route,
        departure_airport_alias,
        arrival_airport_alias,

    ).join(Route, Flight.route_id == Route.id).join(
        departure_airport_alias, Route.departure_id == departure_airport_alias.id
    ).join(
        arrival_airport_alias, Route.arrival_id == arrival_airport_alias.id
    ).all()
    return list_flight


def get_class():
    return db.session.query(TicketClass)


def get_detail_flight(flight_id):
    departure_airport_alias = aliased(Airport)
    arrival_airport_alias = aliased(Airport)
    list_flight = db.session.query(
        Flight,
        Route,
        departure_airport_alias,
        arrival_airport_alias,

    ).join(Route, Flight.route_id == Route.id).join(
        departure_airport_alias, Route.departure_id == departure_airport_alias.id
    ).join(
        arrival_airport_alias, Route.arrival_id == arrival_airport_alias.id
    ).filter(Flight.id.__eq__(flight_id)).first()
    return list_flight


def get_stops():
    return db.session.query(Stop).filter(Flight.id.__eq__(Stop.flight_id)).all()


def get_airport_id(name):
    return db.session.query(Airport.id).filter(Airport.name.__eq__(name)).first()


def get_route(de_name, ar_name):
    de_id = get_airport_id(de_name)
    ar_id = get_airport_id(ar_name)
    return db.session.query(Route.id).filter(Route.departure_id.__eq__(de_id[0]),
                                             Route.arrival_id.__eq__(ar_id[0])).first()


def update_flight(departure, arrival, time_de, time_arr, rate1,  rate2, airport1, time_delay1):
    de = db.session.query(Airport.id).filter(Airport.name.__eq__(departure)).first()
    arr = db.session.query(Airport.id).filter(Airport.name.__eq__(arrival)).first()
    route_id = get_route(departure, arrival)
    flight1 = Flight(route_id= route_id[0], departure_time=time_de, arrival_time=time_arr,
                     quantity_class_1=rate1, quantity_class_2=rate1, number_of_airport=2)

    db.session.add_all([stop1, stop2])
    db.session.commit()
#
# r_id =
# a1_id = get_airport_id("Đà Nẵng")
# a2_id = get_airport_id("Hải Phòng")
#
# print(r_id[0])
#
# flight1 = Flight(route_id=r_id[0], departure_time="2023-12-31 20:00:00",arrival_time="2023-12-31 23:55:00",
#                  quantity_class_1=21, quantity_class_2=13, number_of_airport=2)
#
# stop1 = Stop(route_id=r_id[0], airport_id=a1_id[0], arrival_time="2023-12-31 22:00:00", flight=flight1,
#              order=1, time_delay_max=30, time_delay_min=20)
# stop2 = Stop(route_id=r_id[0], airport_id=a2_id[0], arrival_time="2023-12-31 22:00:00", flight=flight1,
#              order=1, time_delay_max=30, time_delay_min=20)
#
