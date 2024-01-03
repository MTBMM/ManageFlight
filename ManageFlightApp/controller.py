from ManageFlightApp import app, login, utils
from flask import render_template, redirect, request
from ManageFlightApp.admin import *
from flask_login import login_user as flask_login_user, logout_user, current_user
from ManageFlightApp.models import *


@app.route("/")
def index():
    return render_template("Manage.html")


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


@app.route("/login")
def login():
    return render_template("LoginForm.html")


@app.route("/sign_admin", methods=["post"])
def sign_admin():
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method.__eq__("POST"):

        user = utils.check_admin(username=username, password=password, role=UserRoleEnum.ADMIN)
        if user:
            flask_login_user(user=user)

    return redirect("/admin")


if __name__ == '__main__':
    app.run(debug=True)
