from flask import Flask
from .main_routes import main_routes
from .role_routes import role_routes
from .dashboard_routes import dashboard_routes

def init_routes(app: Flask):
    app.register_blueprint(main_routes)
    app.register_blueprint(role_routes)
    app.register_blueprint(dashboard_routes)
