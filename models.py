from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RoleRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alliance = db.Column(db.String(50))
    player = db.Column(db.String(50))
    role = db.Column(db.String(50))
    coordinates = db.Column(db.String(50), nullable=True)
    request_time = db.Column(db.DateTime, default=datetime.utcnow)
    assign_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<RoleRequest {self.player} - {self.role}>'
