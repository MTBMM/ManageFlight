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
    return (db.session.query(Route.name, extract('month', Receipt.created_date), func.sum(Receipt.unit_price)).join(Flight, Route.id == Flight.route_id)
            .join(Receipt, Flight.id == Receipt.flight_id)
            .group_by(Route.name, extract('month', Receipt.created_date)).all())
