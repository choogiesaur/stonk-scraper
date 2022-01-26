from __init__ import db
from sqlalchemy.dialects.postgresql import JSON

class Stonks(db.Model):
    __tablename__ = 'stonk'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    stonk = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    ticker = db.Column(
        db.String(20),
        index=True,
        unique=True,
        nullable=False
    )

    def __init__(self, stonk, ticker):
        self.stonk = stonk
        self.ticker = ticker

    def __repr__(self):
        return '<id {}>'.format(self.id)