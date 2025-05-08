import os

class Config:
    SECRET_KEY = os.urandom(24)  # Secret key for sessions/cookies
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
