from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    #Database
    user = environ.get('user')
    password = environ.get('password')
    servername = environ.get('servername')
    database = environ.get('database')
    # General
    TESTING = environ.get('TESTING')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY') or 'super-secret-secret-key'
    # Database
    SQLALCHEMY_DATABASE_URI = f'mssql+pymssql://{user}:{password}@{servername}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False