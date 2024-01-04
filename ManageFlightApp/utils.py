from ManageFlightApp.models import *
import hashlib
from sqlalchemy import func, extract


def get_user_by_id(user_id):
    return Customer.query.get(user_id)


def check_admin(username, password, role=UserRoleEnum.ADMIN):
    password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    return db.session.query(Employee).filter(Employee.username.__eq__(username.strip()),
                                             Employee.password.__eq__(password),
                                             Employee.user_role.__eq__(role)).first()


def flight_states():
    k = db.session.query(Route.name, func.count(Flight.id)).join(Flight, Route.id == Flight.route_id).group_by(
        Route.name).all()
    # import pdb
    # pdb.set_trace()
    return k


def revenue_states():
    return (db.session.query(Route.name, extract('month', Receipt.created_date), func.sum(Receipt.unit_price))
            .join(Flight, Route.id == Flight.route_id)
            .join(Receipt, Flight.id == Receipt.flight_id)
            .group_by(Route.name, extract('month', Receipt.created_date)).all())


def percent_states():
    total_revenue = db.session.query(func.sum(Receipt.unit_price)).scalar()
    k = 100 / total_revenue
    return db.session.query(Route.name, func.sum(Receipt.unit_price) * k).join(Flight,
                                                                               Route.id == Flight.route_id).join(
        Receipt, Flight.id == Receipt.flight_id).group_by(Route.name).all()


def General_States(m):
    total_revenue = db.session.query(func.sum(Receipt.unit_price)).scalar()
    k = 100 / total_revenue
    return (db.session.query(Route.name, func.sum(Receipt.unit_price), func.count(Flight.id),
                             func.sum(Receipt.unit_price) * k)
            .join(Flight, Route.id == Flight.route_id)
            .join(Receipt, Flight.id == Receipt.flight_id).filter(extract('month', Receipt.created_date) == m)
            .group_by(Route.name, extract('month', Receipt.created_date)).all())


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Customer(username=username.strip(),
                 password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return Customer.query.filter(Customer.username.__eq__(username.strip()),
                                 Customer.password.__eq__(password)).first()


def get_all_airport_names():
    return db.session.query(Airport.id, Airport.name).all()


def get_route():
    return (db.session.query(Route.name, Airport.location, Flight.id).join(Airport, Airport.id == Route.departure_id)
            .join(Flight, Flight.id == Route.id)
            )


def get_airport_id(f):
    return db.session.query(Airport.id).filter(Airport.name.__eq__(f))


def get_flight(start_location, end_location, departure):
    de_id = get_airport_id(start_location)
    ar_id = get_airport_id(end_location)
    return (db.session.query(Flight, TicketPrice.price, Flight.departure_time, Flight.arrival_time)
            .join(Route, Flight.route_id == Route.id)
            .join(Airport, Airport.id == Route.departure_id).join(TicketPrice, Flight.id == TicketPrice.flight_id)
            .join(TicketClass, TicketPrice.ticket_class_id == TicketClass.id)
            .filter(Route.departure_id.__eq__(de_id), Route.arrival_id.__eq__(ar_id),
                    Flight.departure_time.__eq__(departure))
            )
