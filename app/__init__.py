from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        # Import the routes
        from . import routes
        # Cre ate sql tables for data models
        db.create_all()

        return app