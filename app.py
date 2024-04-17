from flask import Flask

app = Flask(__name__)

@app.route("/")
def startapp():
    return "Flask is Running"


if __name__ == "__main__":
    app.run(debug=True)