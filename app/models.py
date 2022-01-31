import flask_sqlalchemy
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
# app.config.from_pyfile('config.py')

db = flask_sqlalchemy.SQLAlchemy()

class Stonks(db.Model):
    __tablename__ = 'stonk'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(50), index=True, unique=True, nullable=False)
    stonk = db.Column(db.String(200), index=False, unique=True, nullable=False)

    def __init__(self, stonk, ticker):
        self.ticker = ticker
        self.stonk = stonk

    def __repr__(self):
        return '<Ticker {}>'.format(self.ticker)