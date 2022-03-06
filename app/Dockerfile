FROM python:3.7.6

EXPOSE 8080

ADD . /app
WORKDIR /app

COPY requirements.txt /app
COPY ./lib /app
ENV variables.env /stonk-scraper
RUN pip install -r requirements.txt --upgrade pip

COPY . /app

CMD flask run --host 0.0.0.0