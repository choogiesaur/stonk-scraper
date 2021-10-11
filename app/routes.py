from flask import current_app as app
from flask import render_template

@app.route('/')
def home():
    """Landing page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'}
    ]
    return render_template(
        'index.html',
        title="Stonk Scraper",
        description="A natural language processing web app that evaluates sentiment of Elon's twitter feed to determine if stonk will go up or down."
    )

@app.route('/live', methods=['GET', 'POST', 'PUT'])
def live():
    """Live page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'}
    ]
    return render_template(
        'live.html',
        title="Stonk Scraper",
        description="Live scraper for Elon's twitter feed."
    )

@app.route('/demo', method=['GET', 'POST', 'PUT'])
def demo():
    """Demo page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'}
    ]
    return render_template(
        'demo.html',
        title="Stonk Scraper",
        description="Demo scraper for Elon's twitter feed."
    )

