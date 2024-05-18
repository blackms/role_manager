from flask import Flask
from flask_session import Session
from config import Config
from models import db
from routes import init_routes

app = Flask(__name__)
app.config.from_object(Config)
Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
