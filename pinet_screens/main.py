import flask_login
from flask import Flask, render_template, redirect, url_for
from secrets.config import secret_key
from routes import routes
import database as database
import util as util
import getpass


app = Flask(__name__)
app.secret_key = secret_key


login_manager = flask_login.LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'routes.login'
login_manager.login_message_category = "danger"
app.login_manager = login_manager

app.register_blueprint(routes)


@login_manager.user_loader
def load_user(id):
    return database.get_login_user_from_id(id)

@app.route("/")
def home():
    if flask_login.user_logged_in:
        return redirect(url_for("routes.clients_home"))
    else:
        return redirect(url_for("routes.login"))


def validate_startup(override_first_time_check=False):
    users = database.get_all_users()

    if users and not override_first_time_check:
        return
    if not users:
        print("No users found on the system. This is likely the first time the application has been started.")
    print("Enter new user details below.")

    username = input("Input username: ")
    password = getpass.getpass("Input password: ")
    util.create_user(username, password)


if __name__ == '__main__':
    validate_startup()
    app.run()
