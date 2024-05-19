from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RoleRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alliance = db.Column(db.String(50), nullable=False)
    player = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    coordinates = db.Column(db.String(100))
    request_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    assign_time = db.Column(db.DateTime)
    status = db.Column(db.String(10), nullable=False, default='waiting')
