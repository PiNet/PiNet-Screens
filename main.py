import flask_login
from flask import Flask, render_template
from secrets.config import secret_key
import models
from routes import routes


app = Flask(__name__)
app.secret_key = secret_key


login_manager = flask_login.LoginManager()

login_manager.init_app(app)
app.login_manager = login_manager

app.register_blueprint(routes)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/test/<data>")
def para_test(data):
    return "The data sent was {}".format(data)


if __name__ == '__main__':
    app.run()
