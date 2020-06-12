"""
    file: migrate.py
    purpose: Handle database migrations
"""

from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import db
from safewalk import create_app

app = create_app('config.Config')
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # python migrate.py db init
    # python migrate.py db migrate
    # python migrate.py db upgrade
    manager.run()