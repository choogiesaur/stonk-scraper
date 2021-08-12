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
        'layout.html',
        title="Stonk Scraper",
        description="Live scraper for Elon's twitter feed."
    )

