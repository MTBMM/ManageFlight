from ManageFlightApp.models import *
import hashlib


def get_user_by_id(user_id):
    return Customer.query.get(user_id)


def check_admin(username, password, role=UserRoleEnum.ADMIN):
    password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    return db.session.query(Employee).filter(Employee.username.__eq__(username.strip()),
                                         Employee.password.__eq__(password), Employee.user_role.__eq__(role)).first()
