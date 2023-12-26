from ManageFlightApp.models import Customer


def get_user_by_id(user_id):
    return Customer.query.get(user_id)
