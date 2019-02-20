#! /study/Projects/flask/Projects/flaskblog/venv/bin/ python
# encoding:utf-8
# create console commands here

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User
import os

app = create_app(os.environ.get('FLASK_CONFIG') or 'production_config')
manager = Manager(app)
migrate = Migrate(app, db)


def create_context():
    return dict(app=app, db=db, User=User)


manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=create_context))


if __name__ == '__main__':
    manager.run()
