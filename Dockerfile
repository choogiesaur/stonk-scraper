FROM python:3.7.6
ADD . /stonk-scraper
WORKDIR /stonk-scraper
RUN pip install -r requirements.txt
