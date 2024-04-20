from flask import Flask
from dotenv import load_dotenv
from db.database import db,initialize_database
import os

app = Flask(__name__)

# Configure dotenv

load_dotenv()

# Flask App initalize with SQLALCHEMY

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Initialize the database with the Flask app

initialize_database(app)

# PORT

PORT = os.getenv('PORT')

@app.route("/")
def homePage():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True,port=PORT)