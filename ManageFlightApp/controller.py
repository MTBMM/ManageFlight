from ManageFlightApp import app, login, utils
from flask import render_template
from ManageFlightApp.admin import *


@app.route("/")
def index():
    return render_template("index.html")


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


@app.route("/login")
def login():
    return render_template("LoginForm.html")


if __name__ == '__main__':
    app.run(debug=True)
