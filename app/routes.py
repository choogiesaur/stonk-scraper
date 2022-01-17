from flask import render_template, Flask
from flask import current_app as app

app = Flask(__name__)

@app.route('/')
def home():
    """Landing page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'},
        {'name': 'Info', 'url': 'info.html'}
    ]
    return render_template(
        'index.html',
        title="Stonk Scraper",
        description="Welcome to the Stonk Scraper! This is a natural language processing web app that performs named entity recognition and sentiment analysis for Elon Musk's twitter feed!"
    )

@app.route('/live', methods=['GET', 'POST', 'PUT'])
def live():
    """Live page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'},
        {'name': 'Info', 'url': 'info.html'}
    ]
    return render_template(
        'live.html',
        title="Stonk Scraper",
        description="Live scraper for Elon's twitter feed. Click the buttons below for named entity recognition and sentiment analysis on live tweets."
    )


@app.route('/demo', methods=['GET', 'POST', 'PUT'])
def demo():
    """Demo page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'},
        {'name': 'Info', 'url': 'info.html'}
    ]
    return render_template(
        'demo.html',
        title="Stonk Scraper",
        description="Demo scraper for Elon's twitter feed. Click the buttons below for named entity recognition and sentiment analysis on sample data."
    )

@app.route('/info', methods=['GET', 'POST', 'PUT'])
def info():
    """Info page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'},
        {'name': 'Info', 'url': 'info.html'}
    ]
    return render_template(
        'info.html',
        title="Stonk Scraper",
        description="Demo scraper for Elon's twitter feed."
    )