from flask import Flask
from dotenv import load_dotenv
from db.database import db ,init_app
import os

app = Flask(__name__)

# Configure dotenv

load_dotenv()

# Flask App initalize with SQLALCHEMY

init_app(app)

# PORT

PORT = os.getenv('PORT')

@app.route("/")
def startapp():
    return "Flask is Running"


if __name__ == "__main__":
    app.run(debug=True,port=PORT)