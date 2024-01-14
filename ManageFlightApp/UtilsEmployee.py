from ManageFlightApp.models import *


def get_list_flight():

    departure_airport_alias = aliased(Airport)
    arrival_airport_alias = aliased(Airport)
    list_flight = db.session.query(
        Flight,
        Route,
        departure_airport_alias,
        arrival_airport_alias,
        TicketPrice
    ).join(Route, Flight.route_id == Route.id).join(
        departure_airport_alias, Route.departure_id == departure_airport_alias.id
    ).join(
        arrival_airport_alias, Route.arrival_id == arrival_airport_alias.id
    ).join(TicketPrice, TicketPrice.flight_id == Flight.id).all()
    return list_flight

def get_list_ticket():
        pass

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
    de_id = get_airport_id(name=de_name)
    ar_id = get_airport_id(name=ar_name)
    return db.session.query(Route.id).filter(Route.departure_id.__eq__(de_id[0]),
                                             Route.arrival_id.__eq__(ar_id[0])).first()


def update_flight(departure, arrival, time_de, time_arr, rate1,  rate2, airport1, arr_date,
                  time_delay_max, time_delay_min, quantity_airport):

    a2_id = get_airport_id(airport1)
    route_id = get_route(de_name=departure, ar_name=arrival)

    flight1 = Flight(route_id=route_id[0], departure_time=time_de, arrival_time=time_arr,
                     quantity_class_1=rate1, quantity_class_2=rate2, number_of_airport=quantity_airport)
    # import pdb
    # pdb.set_trace()
    stop1 = Stop(route_id=route_id[0], airport_id=a2_id[0], arrival_time=arr_date, flight=flight1,
                  time_delay_max=time_delay_max, time_delay_min=time_delay_min)
    db.session.add(stop1)
    db.session.commit()


