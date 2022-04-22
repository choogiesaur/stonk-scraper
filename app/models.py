import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Stonks(db.Model):
    __tablename__ = 'stonks'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(50), index=True, unique=True, nullable=False)
    stonk = db.Column(db.String(200), index=False, unique=True, nullable=False)

    def __init__(self, stonk, ticker):
        self.ticker = ticker
        self.stonk = stonk

    def __repr__(self):
        return '<Ticker {}, Stonk {}>'.format(self.ticker, self.stonk)

class Results(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key = True)
    tweet = db.Column(db.String(140), index=True, unique=True, nullable=False)
    sentiment = db.Column(db.String(30), index=True, unique=True, nullable=False)

    def __init__(self, tweet, sentiment):
        self.tweet = tweet
        self.sentiment = sentiment

    def __repr__(self):
        return '<Tweet {}, Sentiment {}>'.format(self.tweet, self.sentiment)