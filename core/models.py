from core import db
from datetime import datetime

class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(50000), nullable=False)
    short_id = db.Column(db.String(1000), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    usermail = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(100), nullable=False)