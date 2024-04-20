from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a database object
db = SQLAlchemy()

# Function to initialize the database
def initialize_database(app):
    # Load the database URI from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    # Bind the database to the Flask app
    db.init_app(app)

    # Create all tables in the database
    with app.app_context():
        db.create_all()
