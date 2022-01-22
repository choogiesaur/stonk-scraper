from . import db

class Stonks(db.Model):
    """Data model for stonks and their ticker symbols."""

    __tablename__ = 'stonks-and-ticker-symbols'
    
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