from flask import Response, render_template, Flask, request
from flask import current_app as app
from models import Stonks, db
import json
from __init__ import create_app

app = create_app()

@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'index.html',
        title="Stonk Scraper",
        description="Welcome to the Stonk Scraper! This is a natural language processing web app that performs named entity recognition and sentiment analysis for Elon Musk's twitter feed!"
    )

@app.route('/live', methods=['GET', 'POST', 'PUT'])
def live():
    """Live page."""
    return render_template(
        'live.html',
        title="Stonk Scraper",
        description="Live scraper for Elon's twitter feed. Click the buttons below for named entity recognition and sentiment analysis on live tweets."
    )


@app.route('/demo', methods=['GET', 'POST', 'PUT'])
def demo():
    """Demo page."""
    return render_template(
        'demo.html',
        title="Stonk Scraper",
        description="Demo scraper for Elon's twitter feed. Click the buttons below for named entity recognition and sentiment analysis on sample data."
    )

@app.route('/info', methods=['GET', 'POST', 'PUT'])
def info():
    """Info page."""
    return render_template(
        'info.html',
        title="Stonk Scraper",
        description="Demo scraper for Elon's twitter feed."
    )

@app.route('/fetch-stonks', methods=['GET'])
def fetch():
    stonks = Stonks.query.all()
    results = [
        {
            "id": stonk.id,
            "ticker": stonk.ticker,
            "stonk": stonk.stonk
        } for stonk in stonks]
    json_dumps = json.dumps(results)
    resp = Response(json_dumps, status=200, mimetype='application/json')
    return resp

@app.route('/add-stonks', methods=['POST'])
def add():
    data = request.get_json()
    stonk = data['stonk']
    ticker = data['ticker']
    
    new_stonk = Stonks(stonk=stonk, ticker=ticker)
    db.session.add(new_stonk)
    db.session.commit()
    return json.dumps("Successfully added"), 200