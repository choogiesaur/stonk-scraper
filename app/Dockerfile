FROM python:3.7.6

EXPOSE 5000

ADD . /app
WORKDIR /app

COPY requirements.txt /app
COPY ./lib /app
ENV variables.env /stonk-scraper
RUN pip install -r requirements.txt --upgrade pip

COPY . /app

CMD python stonk-scraper.py