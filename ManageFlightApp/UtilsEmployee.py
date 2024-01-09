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


def update_flight(departure, arrival, time_de, time_arr, rate1,  rate2, airport1, time_delay1):
    de = db.session.query(Airport.id).filter(Airport.name.__eq__(departure)).first()
    arr = db.session.query(Airport.id).filter(Airport.name.__eq__(arrival)).first()
    route = Route(departure_id=de,  arrival_id=arr)
    flight = Flight(departure_time=time_de, arrival_time=time_arr)


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
