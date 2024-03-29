import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from routes import app
from __init__ import db

app.config.from_pyfile('config.py')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

def get(model):
    data = model.query.all()
    return data

if __name__ == '__main__':
    manager.run()