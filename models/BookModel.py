from flask_sqlalchemy import SQLAlchemy

# Import the database object from your database module
from db.database import db

# Define book models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)


