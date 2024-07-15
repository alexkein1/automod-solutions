from flask import Flask, render_template, send_from_directory, abort

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/auth')
def authorize():
    return render_template('authorize.html')


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5795)
