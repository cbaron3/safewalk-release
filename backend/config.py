"""
    file:
    purpose:
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

class Config(object):
    DEBUG = False

    TESTING = False

    CSRF_ENABLED = True

    SECRET_KEY = os.environ.get('FLASK_APP_SECRET_KEY') or 'you-will-never-guess'

    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_APP_DB_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('FLASK_APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('FLASK_APP_MAIL_PASSWORD')