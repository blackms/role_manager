from flask import Flask
from flask_session import Session
from flask_migrate import Migrate
from config import Config
from models import db
from routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    init_routes(app)

    return app
