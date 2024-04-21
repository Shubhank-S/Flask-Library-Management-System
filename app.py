import os
from flask import Flask,render_template, request, redirect, url_for,flash
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db.database import db,initialize_database
from models.UserModel import User
from models.BookModel import Book


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
    return "This is home page"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True,port=PORT)