import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from db.database import db,initialize_database
from models.UserModel import User


app = Flask(__name__)

# Configure dotenv

load_dotenv()

# Flask App initalize with SQLALCHEMY

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Initialize the database with the Flask app

initialize_database(app)

# Initialize user login management
# Initialize Flask-Login

login_manager = LoginManager()
login_manager.init_app(app)

# User loader function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# PORT

PORT = os.getenv('PORT')

@app.route("/")
def homePage():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True,port=PORT)