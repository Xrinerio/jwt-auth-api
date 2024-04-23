from flask import Flask

from config import Config
from .bcrypt import bcrypt
from .database import db
from .api import api
from .views.index import index_bp




def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(index_bp)

    bcrypt.init_app(app)
    api.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
