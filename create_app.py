import logging
from flask import Flask
from flask_session import Session
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app)
    db.init_app(app)

    migrate = Migrate(app, db)

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    init_routes(app)

    return app
