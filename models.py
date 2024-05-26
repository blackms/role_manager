from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Enum

db = SQLAlchemy()

class RoleRequest(db.Model):
    __tablename__ = 'role_requests'
    id = Column(Integer, primary_key=True)
    alliance = Column(String(50), nullable=False)
    player = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    coordinates = Column(String(50), nullable=True)
    request_time = Column(DateTime, default=datetime.utcnow)
    assign_time = Column(DateTime, nullable=True)
    status = Column(Enum('waiting', 'assigned', 'finished', name='status'), default='waiting')