from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class RoleRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alliance = db.Column(db.String(50), nullable=False)
    player = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    coordinates = db.Column(db.String(100))
    request_time = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    assign_time = db.Column(db.DateTime)
    status = db.Column(db.String(10), nullable=False, default='waiting')


from werkzeug.security import generate_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
