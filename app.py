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

# Routes

@app.route('/')
@login_required
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    user = current_user
    # Deleting user from database
    db.session.delete(user)
    db.session.commit()

    logout_user()
    flash('Logged out and account deleted successfully.')
    return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_book.html', book=book)

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True,port=PORT)