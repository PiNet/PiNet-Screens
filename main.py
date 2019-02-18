from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/test/<data>")
def para_test(data):
    return "The data sent was {}".format(data)

if __name__ == '__main__':
    app.run()