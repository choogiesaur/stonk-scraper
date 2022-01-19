from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        # Import the routes
        from . import routes
        # Create sql tables for data models
        db.create_all()

        return app