from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RoleRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alliance = db.Column(db.String(50))
    player = db.Column(db.String(50))
    role = db.Column(db.String(50))
    coordinates = db.Column(db.String(100))
    request_time = db.Column(db.DateTime, default=datetime.utcnow)
    assign_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, alliance, player, role, coordinates=None, request_time=None, assign_time=None):
        self.alliance = alliance
        self.player = player
        self.role = role
        self.coordinates = coordinates
        self.request_time = request_time if request_time else datetime.utcnow()
        self.assign_time = assign_time
