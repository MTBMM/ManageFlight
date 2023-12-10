from ManageFlightApp import app, login, utils
from flask import render_template


@app.route("/")
def index():
    return render_template("index.html")


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)

