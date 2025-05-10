from datetime import datetime
from app.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    nickname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, nickname, password):
        self.username = username
        self.nickname = nickname
        self.password = password
        self.score = 0
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'score': self.score,
            'created_at': self.created_at.isoformat()  # Convert datetime to ISO format
        }