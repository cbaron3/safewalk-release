"""
    file:
    purpose:
"""

from config import Config
from flask import Flask
from app import create_app

application = create_app(Config)

if __name__ == "__main__":
    # PROCFILE -> web: gunicorn --bind :8000 --workers 3 --threads 2 project.wsgi:application
    # Good for testing, use https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/ for production
    application.run()