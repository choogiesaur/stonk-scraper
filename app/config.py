from os import environ, path
from flask import Flask

basedir = path.abspath(path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = environ.get['DATABASE_URL']
    SQLALCHEMY_ECHO = False